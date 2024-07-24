.PHONY: install
install: ## Install the poetry environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry run pre-commit install
	@poetry shell

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help



re-build-backend:
	@echo "Rebuilding backend the project..."
	@docker-compose -f ./docker-compose.local.yaml up --build -d backend

re-build-frontend:
	@echo "Rebuilding backend the project..."
	@docker-compose -f ./docker-compose.local.yaml up --build -d frontend

make-migrations:
	@echo "Making migrations..."
	@PATHONPATH=./src poetry run alembic revision -m "Auto create migration" --autogenerate

migrate:
	@echo "Migrating..."
	@PATHONPATH=./src poetry run alembic upgrade head

create-envs-local:
	@echo "Creating .envs.local file..."
	@cat ./.envs.local > .env

delete-db:
	@echo "Flushing database..."
	@docker-compose -f ./docker-compose.local.yaml down db --rmi all
	@rm -Rf ./data/db


delete-migrations:
	@echo "Deleting migrations..."
	@rm -Rf ./backend/migrations/versions/*.py

recreate-db:
	@echo "Recycling database..."
	@make delete-db
	@docker-compose -f ./docker-compose.local.yaml up db -d
	@make delete-migrations
	@echo "Waiting for db to start..."
	@while ! docker-compose -f ./docker-compose.local.yaml exec db pg_isready; do echo "..." \
	&& sleep 2; done;
	@make make-migrations
	@make migrate
