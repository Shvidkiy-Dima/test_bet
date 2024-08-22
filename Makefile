format: ## Format the source code
	$(.PY) ruff check --config pyproject.toml --fix
	$(.PY) ruff format --config pyproject.toml --exclude venv
.PHONY: format

build:
	docker compose -f  docker/docker-compose.yml build

run-local:
	docker compose -f  docker/docker-compose.yml  -p dev up

run-test:
	docker compose -f  docker/docker-compose.test.yml -p test up --abort-on-container-exit --exit-code-from bet_maker

