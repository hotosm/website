# Humanitarian OpenStreetMap Team CMS

This project is a website for the Humanitarian OpenStreetMap Team. It's built using the Wagtail CMS, a powerful and flexible Django content management system.

## Codebase Overview

The codebase is structured as a standard Django project with a `settings` directory containing different settings files for different environments: `base.py` for common settings, `dev.py` for development settings, and `production.py` for production settings. Several Django apps are included for different parts of the website, with the main app being the `home` app, which contains the models, views, and templates for the homepage and other top-level pages.

The project uses Docker for development and production environments, with separate Docker Compose files for each. The `Dockerfile.dev` file is used for the development environment, and the `Dockerfile.prod` file is used for the production environment.

## Setting Up Environment Variables

To set up environment variables for your local development environment, you'll need to create a `.env.dev` file in the root directory of the project. This file will store your environment variables.

You can refer to the `.env.dev.example` file in the root directory of the project as an example of what your `.env.dev` file should look like. Simply copy the contents of `.env.dev.example` into your `.env.dev` file and replace the placeholder values with your actual values.

Remember to keep your `.env.dev` file secure and do not commit it to your version control system. It's already included in the `.gitignore` file to prevent accidental commits.

## Dependency Management

This project uses Pipenv for dependency management. Pipenv is a Python tool that combines the best features of pip (Python's package installer), Pipfile (a manifest file format for Python package requirements), and virtualenv (a tool for creating isolated Python environments).

Dependencies are specified in the `Pipfile`, and the exact versions of the dependencies are locked in the `Pipfile.lock`. To install the dependencies, run `pipenv install`. To add a new dependency, run `pipenv install {dependency}`.

## Using the Makefile

Ensure you have the superuser credentials you want in your .env.dev file prior to running `make build-dev`.
The Makefile provides several commands for building and running the project:

- `make build-dev`: Builds and starts the Docker images for the development environment.
- `make up-dev`: Starts the Docker containers for the development environment.
- `make down-dev`: Stops the Docker containers for the development environment.
- `make build-prod`: Builds the Docker images for the production environment.
- `make up-prod`: Starts the Docker containers for the production environment.
- `make down-prod`: Stops the Docker containers for the production environment.
- `make test`: Runs the tests.
- `make refresh-db`: Deletes all Docker volumes (use with caution).
