# This Makefile lints, formats, and tests your Python code.

.PHONY: all lint format test

all: lint format test

lint:
	ruff

format:
	black .

test:
	pytest
