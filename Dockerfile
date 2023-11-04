# This is a coppy of Dockerfile.dev for GH action debugging purposes

# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1\
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install the project requirements.
RUN pipenv install --dev --system --deploy

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Copy the entrypoint script into the Docker image
COPY --chown=wagtail:wagtail entrypoint.dev.sh /app/entrypoint.dev.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.dev.sh

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# # Collect static files.
# RUN python manage.py collectstatic --noinput --clear

# Use the entrypoint script as the Docker entrypoint
ENTRYPOINT ["/app/entrypoint.dev.sh"]
