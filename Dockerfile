ARG PYTHON_IMG_TAG=3.11


# Define the base stage
FROM docker.io/python:${PYTHON_IMG_TAG}-slim-bookworm as base
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
    -y --no-install-recommends "locales" "ca-certificates" \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates
# Set locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


# Extract dependencies using poetry (to requirements.txt)
FROM base as extract-deps
WORKDIR /opt/python
COPY pyproject.toml poetry.lock* /opt/python/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    poetry==1.7.1 poetry-plugin-export==1.6.0
RUN poetry export --without dev --output requirement.txt
RUN poetry export --only dev --output requirement-dev.txt


# Define build stage (install deps)
FROM base as build
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
    && rm -rf /var/lib/apt/lists/*
COPY --from=extract-deps \
    /opt/python/requirements.txt /opt/python/
RUN pip install --user --no-warn-script-location \
    --no-cache-dir -r /opt/python/requirements.txt


# Define run stage
FROM base as runtime
ARG PYTHON_IMG_TAG
ENV PORT=8000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/home/wagtail/.local/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHON_LIB="/home/wagtail/.local/lib/python$PYTHON_IMG_TAG/site-packages" \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
# Install non-dev versions of packages (smaller)
RUN set -ex \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install \
    -y --no-install-recommends \
        "postgresql-client" \
        "libmariadb3" \
        "libjpeg62-turbo" \
        "zlib1g" \
        "libwebp-dev" \
    && rm -rf /var/lib/apt/lists/*
# Copy the entrypoint script into the Docker image
COPY --chown=wagtail:wagtail entrypoint.dev.sh /app/entrypoint.dev.sh
# Copy pip dependencies from build stage
COPY --from=build \
    /root/.local \
    /home/wagtail/.local
# Use /app folder as a directory where the source code is stored.
WORKDIR /app
# Copy project
COPY . /app/
# Add non-root user, permissions
RUN useradd -u 1001 -m -c "hotosm account" -d /home/wagtail -s /bin/false wagtail \
    && chown -R wagtail:wagtail /app /home/wagtail \
    && chmod +x /app/entrypoint.dev.sh
# Change to non-root user
USER wagtail


# Define test (ci) stage
FROM runtime as test
USER root
ARG PYTHON_IMG_TAG
COPY --from=extract-deps \
    /opt/python/requirements-dev.txt /opt/python/
# Copy packages from user to root dirs (run ci as root)
# && install dev dependencies (pytest)
RUN mv /home/appuser/.local/bin/* /usr/local/bin/ \
    && mv /home/appuser/.local/lib/python${PYTHON_IMG_TAG}/site-packages/* \
    /usr/local/lib/python${PYTHON_IMG_TAG}/site-packages/ \
    && pip install --upgrade --no-warn-script-location \
    --no-cache-dir -r \
    /opt/python/requirements-dev.txt \
    && rm -r /opt/python \
    # Pre-compile packages to .pyc (init speed gains)
    && python -c "import compileall; compileall.compile_path(maxlevels=10, quiet=1)"
CMD [ "pytest" ]


# Define debug (development) stage
FROM runtime as debug
# Add Healthcheck
HEALTHCHECK --start-period=10s --interval=5s --retries=20 --timeout=5s \
    CMD curl --fail http://localhost:8000 || exit 1
# Use the entrypoint script as the Docker entrypoint
ENTRYPOINT ["/app/entrypoint.dev.sh"]
CMD ["./wait-for-it.sh", "db:5432", "--", \
    "python", "manage.py", "runserver", "0.0.0.0:8000"]


# Define prod stage
FROM runtime as prod
# Add Healthcheck
HEALTHCHECK --start-period=10s --interval=5s --retries=20 --timeout=5s \
    CMD curl --fail http://localhost:8000 || exit 1
# Pre-compile packages to .pyc (init speed gains)
RUN python -c "import compileall; compileall.compile_path(maxlevels=10, quiet=1)" \
    # Collect static files
    && python manage.py collectstatic --noinput --clear
# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn hot_osm.wsgi:application
