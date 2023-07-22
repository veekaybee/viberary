
.PHONY: all lint format test embed build up down logs

ci: lint format test
intel: build up-intel embed
arm: build up-arm embed

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

up-intel:
	docker compose up -d

up-arm:
	export DOCKER_DEFAULT_PLATFORM=linux/amd64
	docker compose up -d

onnx:
	docker exec -it viberary optimum-cli export onnx --model sentence-transformers/msmarco-distilbert-base-v3 sentence-transformers/msmarco-distilbert-base-v3_onnx/

down:
	docker compose down

logs:
	docker compose logs -f -t
