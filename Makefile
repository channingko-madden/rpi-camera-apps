.PHONY: format, pre_commit, test

SHELL=/bin/bash

format:
	poetry run ruff format .

pre_commit:
	poetry run pre-commit install

test:
	poetry run pytest tests/
