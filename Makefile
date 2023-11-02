.PHONY: build-dev build-prod test up-dev up-prod down-dev down-prod

build-dev:
	@docker-compose -f docker-compose.dev.yml build
	@docker-compose -f docker-compose.dev.yml up -d

build-prod:
	@docker-compose -f docker-compose.prod.yml build

test:
	@pytest

up-dev:
	@docker-compose -f docker-compose.dev.yml up -d

up-prod:
	@docker-compose -f docker-compose.prod.yml up

down-dev:
	@docker-compose -f docker-compose.dev.yml down

down-prod:
	@docker-compose -f docker-compose.prod.yml down

refresh-db:
	@docker volume rm $(docker volume ls -q)
