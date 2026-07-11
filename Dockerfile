ARG PYTHON_IMG_TAG=3.11
ARG NODE_IMG_TAG=20.5.1
ARG UV_IMG_TAG=0.9.27

FROM node:${NODE_IMG_TAG}-bookworm-slim AS frontend-base
COPY . ./app
WORKDIR /app/frontend
RUN mkdir -p ./node_modules
RUN npm install
RUN mkdir -p ./dist/css
RUN npm run build

FROM ghcr.io/astral-sh/uv:${UV_IMG_TAG} AS uv

# Define the base stage
FROM docker.io/python:${PYTHON_IMG_TAG}-slim-bookworm AS base
ARG APP_VERSION
ARG COMMIT_REF
ARG PYTHON_IMG_TAG
LABEL org.hotosm.fmtm.app-name="backend" \
      org.hotosm.fmtm.app-version="${APP_VERSION}" \
      org.hotosm.fmtm.git-commit-ref="${COMMIT_REF:-none}" \
      org.hotosm.fmtm.python-img-tag="${PYTHON_IMG_TAG}" \
      org.hotosm.fmtm.maintainer="sysadmin@hotosm.org" \
      org.hotosm.fmtm.api-port="8000"
RUN set -ex \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install \
    -y --no-install-recommends "locales" "ca-certificates" "gettext" "libmagickwand-dev" \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates
# Set locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


# Install runtime Python dependencies with uv sync + cache
FROM base AS build
RUN set -ex \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install \
    -y --no-install-recommends \
        "build-essential" \
        "gcc" \
        "libpq-dev" \
        "libmariadb-dev" \
        "libjpeg62-turbo-dev" \
        "zlib1g-dev" \
        "libwebp-dev" \
        "nodejs" \
        "npm" \
        "libmagickwand-dev" \
    && rm -rf /var/lib/apt/lists/*
COPY --from=uv /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON="python${PYTHON_IMG_TAG}" \
    UV_PROJECT_ENVIRONMENT=/opt/python
COPY pyproject.toml uv.lock /opt/python/
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_CACHE_DIR=/root/.cache/uv uv sync \
        --project /opt/python \
        --frozen \
        --no-editable \
        --no-dev


# Define run stage
FROM base AS runtime
ARG PYTHON_IMG_TAG
ENV PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/opt/python/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHON_LIB="/opt/python/lib/python$PYTHON_IMG_TAG/site-packages" \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
# Install non-dev versions of packages (smaller)
RUN apt-get update && apt-get install -y "curl"
RUN set -ex \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install \
    -y --no-install-recommends \
        "postgresql-client" \
        "libmariadb3" \
        "libjpeg62-turbo" \
        "zlib1g" \
        "libwebp-dev" \
        "nodejs" \
        "npm" \
        "libmagickwand-dev" \
    && rm -rf /var/lib/apt/lists/*
# Copy the entrypoint script into the Docker image
COPY --chown=wagtail:wagtail container-entrypoint.sh /
# Copy Python environment from build stage
COPY --from=build /opt/python /opt/python
# Copy compiled css from frontend stage
COPY --from=frontend-base /app/frontend/dist/css /app/frontend/dist/css
COPY --from=frontend-base /app/frontend/node_modules /app/frontend/node_modules
# Use /app folder as a directory where the source code is stored.
WORKDIR /app
# Copy project
COPY . /app/

# Add non-root user, permissions
RUN useradd -u 1000 -m -c "hotosm account" -d /home/wagtail -s /bin/false wagtail \
    && chown -R wagtail:wagtail /app /home/wagtail \
    && chmod +x /container-entrypoint.sh
# Change to non-root user
USER wagtail
# Add entrypoint for all following stages
ENTRYPOINT ["/container-entrypoint.sh"]


# Install dev dependencies with uv sync + cache
FROM runtime AS dev-deps
USER root
COPY --from=uv /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock /opt/python/
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_CACHE_DIR=/root/.cache/uv uv sync \
        --project /opt/python \
        --frozen \
        --no-editable \
        --group dev
USER wagtail


# Define test (ci) stage
FROM dev-deps AS test
USER root
RUN python -c "import compileall; compileall.compile_path(maxlevels=10, quiet=1)"
CMD ["pytest"]


# Define debug (development) stage
FROM dev-deps AS debug
# Add Healthcheck
HEALTHCHECK --start-period=10s --interval=5s --retries=20 --timeout=5s \
    CMD curl --fail http://localhost:8000 || exit 1
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Define prod stage
FROM runtime AS prod
# Add Healthcheck
HEALTHCHECK --start-period=10s --interval=5s --retries=20 --timeout=5s \
    CMD curl --fail http://localhost:8000/__lbheartbeat__ || exit 1
COPY --chown=wagtail:wagtail gunicorn_config.py ./
# Compile translations and gather static files at build time so they ship in
# the image. Runtime pods do not (and should not) regenerate these.
# CMS content translations are handled separately by wagtail_localize (DB-backed).
RUN DJANGO_SETTINGS_MODULE=hot_osm.settings.production \
    SECRET_KEY=build-only \
    python manage.py compilemessages \
 && DJANGO_SETTINGS_MODULE=hot_osm.settings.production \
    SECRET_KEY=build-only \
    python manage.py collectstatic --noinput
# Pre-compile packages to .pyc (init speed gains)
RUN python -c "import compileall; compileall.compile_path(maxlevels=10, quiet=1)"
CMD ["gunicorn", "-c", "gunicorn_config.py", "hot_osm.wsgi:application"]
