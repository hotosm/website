.PHONY: build-dev build-prod test up-dev up-prod down-dev down-prod

build:
	@docker compose -f docker-compose.dev.yml build
	@docker compose -f docker-compose.dev.yml up -d

build-prod:
	@docker compose -f docker-compose.prod.yml build
	@docker compose -f docker-compose.prod.yml up -d

test:
	@docker compose -f docker-compose.dev.yml run --rm web pytest

cov:
	@docker compose -f docker-compose.dev.yml run --rm web coverage run -m pytest

messages:
	@docker compose -f docker-compose.dev.yml run --rm web python manage.py makemessages -l en
	@docker compose -f docker-compose.dev.yml run --rm web python manage.py makemessages -l fr
	@docker compose -f docker-compose.dev.yml run --rm web python manage.py makemessages -l es
	@docker compose -f docker-compose.dev.yml run --rm web python manage.py compilemessages

up:
	@docker compose -f docker-compose.dev.yml up -d

up-prod:
	@docker compose -f docker-compose.prod.yml up

down:
	@docker compose -f docker-compose.dev.yml down

down-prod:
	@docker compose -f docker-compose.prod.yml down

refresh-db:
	@if [ -n "$(shell docker volume ls -q)" ]; then docker volume rm $(shell docker volume ls -q); fi
