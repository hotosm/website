.PHONY: build-dev build-prod test up-dev up-prod down-dev down-prod

build-dev:
	@docker compose -f docker-compose.dev.yml build
	@docker compose -f docker-compose.dev.yml up -d

build-prod:
	@docker compose -f docker-compose.prod.yml build
	@docker compose -f docker-compose.prod.yml up -d

test:
	@docker build --target test -t myproject:test -f Dockerfile.dev .
	@docker run --rm myproject:test
	@docker rmi myproject:test

up-dev:
	@docker compose -f docker-compose.dev.yml up -d

up-prod:
	@docker compose -f docker-compose.prod.yml up

down-dev:
	@docker compose -f docker-compose.dev.yml down

down-prod:
	@docker compose -f docker-compose.prod.yml down

refresh-db:
	@if [ -n "$(shell docker volume ls -q)" ]; then docker volume rm $(shell docker volume ls -q); fi
