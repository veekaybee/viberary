# This Makefile lints, formats, and tests your Python code.

.PHONY: all lint format test

all: lint format test

lint:
	ruff

format:
	black .

test:
	pytest

embed:
<<<<<<< HEAD
<<<<<<< HEAD
	docker exec -it viberary-flask-1 python /viberary/src/index/index_embeddings.py

=======
	docker exec -it viberary-flask-1 python /app/src/index/index_embeddings.py
>>>>>>> 57fb5c2 (rerank)
=======
	docker exec -it viberary-flask-1 python /viberary/src/index/index_embeddings.py
>>>>>>> e4ee750 (Deduping, reranking, and adding config)

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f -t
