
.PHONY: all lint format test embed build up down logs

ci: lint format test

lint:
	ruff

format:
	black .

test:
	pytest

embed:
	docker exec -it viberary python /viberary/src/index/index_embeddings.py

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f -t
