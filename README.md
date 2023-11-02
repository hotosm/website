# Humanitarian OpenStreetMap Team CMS

This project is a website for the Humanitarian OpenStreetMap Team. It's built using the Wagtail CMS, a powerful and flexible Django content management system.

## Codebase Overview

The codebase is structured as a standard Django project with a `settings` directory containing different settings files for different environments: `base.py` for common settings, `dev.py` for development settings, and `production.py` for production settings. Several Django apps are included for different parts of the website, with the main app being the `home` app, which contains the models, views, and templates for the homepage and other top-level pages.

The project uses Docker for development and production environments, with separate Docker Compose files for each. The `Dockerfile.dev` file is used for the development environment, and the `Dockerfile.prod` file is used for the production environment.

## Dependency Management

This project uses Pipenv for dependency management. Pipenv is a Python tool that combines the best features of pip (Python's package installer), Pipfile (a manifest file format for Python package requirements), and virtualenv (a tool for creating isolated Python environments).

Dependencies are specified in the `Pipfile`, and the exact versions of the dependencies are locked in the `Pipfile.lock`. To install the dependencies, run `pipenv install`. To add a new dependency, run `pipenv install {dependency}`.

## Using the Makefile

The Makefile provides several commands for building and running the project:

- `make build-dev`: Builds the Docker images for the development environment.
- `make up-dev`: Starts the Docker containers for the development environment.
- `make down-dev`: Stops the Docker containers for the development environment.
- `make build-prod`: Builds the Docker images for the production environment.
- `make up-prod`: Starts the Docker containers for the production environment.
- `make down-prod`: Stops the Docker containers for the production environment.
- `make test`: Runs the tests.
- `make refresh-db`: Deletes all Docker volumes (use with caution).

## Creating a Superuser

To access the Wagtail admin interface at http://localhost:8000/admin/login/, you need to create a superuser. You can do this with the Django `createsuperuser` command.

First, find the ID of the Docker container running the Django application with `docker ps`. Then, run the following command, replacing `container_id` with the actual container ID:

```bash
docker exec -it container_id python manage.py createsuperuser
```

Follow the prompts to create the superuser.
