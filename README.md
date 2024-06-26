# Humanitarian OpenStreetMap Team CMS

This project is a website for the Humanitarian OpenStreetMap Team. It's built using the Wagtail CMS, a powerful and flexible Django content management system.

## Codebase Overview

The codebase is structured as a standard Django project with a `settings` directory containing different settings files for different environments: `base.py` for common settings, `dev.py` for development settings, and `production.py` for production settings. Several Django apps are included for different parts of the website, with the main app being the `home` app, which contains the models, views, and templates for the homepage and other top-level pages.

The project uses Docker for development and production environments, with separate Docker Compose files for each.

This project's frontend leverages TailwindCSS and Alpine.js. The design of the components is inspired by TailwindUI.

TailwindCSS is a utility-first CSS framework that we've used for styling our application. It allows for rapid UI development with its low-level utility classes.

Alpine.js, on the other hand, is a minimal JavaScript framework used for managing component behavior. It operates entirely on the client-side, in the browser. This means that Alpine.js interacts with the HTML after Django has completed its server-side rendering.

Together, TailwindCSS and Alpine.js provide a powerful and efficient combination for building interactive user interfaces.

## Setting Up Environment Variables

To set up environment variables for your local development environment, you'll need to create a `.env' file in the root directory of the project. This file will store your environment variables.

You can refer to the `.env.example` file in the root directory of the project as an example of what your `.env` file should look like. Simply copy the contents of `.env.example` into your `.env.dev` file and replace the placeholder values with your actual values.

Remember to keep your `.env` file secure and do not commit it to your version control system. It's already included in the `.gitignore` file to prevent accidental commits.

## Dependency Management

This project uses Poetry for dependency management. Poetry is a Python tool that helps to handle dependency installation, building packages, and versioning. It simplifies package management and deployment by adding a layer of abstraction over the standard setup tools.

Dependencies are specified in the `pyproject.toml`, and the exact versions of the dependencies are locked in the `poetry.lock`. To install the dependencies, run `poetry install`. To add a new dependency, run `poetry add {dependency}`.

Note that you don't need to run `poetry install`, as Docker handles this when building.

## Using the Makefile

Ensure you have the superuser credentials you want in your .env.dev file prior to running `make build`.
The Makefile provides several commands for building and running the project:

- `make build`: Builds and starts the Docker images for the development environment.
- `make up`: Starts the Docker containers for the development environment.
- `make down`: Stops the Docker containers for the development environment.
- `make build-prod`: Builds the Docker images for the production environment.
- `make up-prod`: Starts the Docker containers for the production environment.
- `make down-prod`: Stops the Docker containers for the production environment.
- `make test`: Runs the tests.
- `make refresh-db`: Deletes all Docker volumes (use with caution).

## Building Tailwind

When you attempt to use a class that isn't currently used anywhere in the project, the live reload will not rebuild the CSS, and thus, these classes won't work until you rebuild the CSS:

1. Open Docker Desktop
2. In the Containers tab, click on the `web-1` container (within the `website` container)
3. Move to the `Exec` tab within this container
4. Move into the `frontend` folder with `cd frontend`
5. Run `npm run build` to rebuild the CSS

You'll need to do this every time you use a currently unused class.

## Wagtail Migrations

Wagtail migrations should be handled within the Docker container. The process for doing this is largely the same as building Tailwind:

1. Open Docker Desktop
2. In the Containers tab, click on the `web-1` container (within the `website` container)
3. Move to the `Exec` tab within this container
4. Run `python manage.py makemigrations` and then `python manage.py migrate` (if successful)
