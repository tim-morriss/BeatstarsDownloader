.PHONY: lint install-deps black isort flake8 mypy codespell

lint: install-deps black isort flake8 mypy codespell

install-deps:
	@echo "Installing dependencies..."
	poetry install --with dev

black:
	@echo "Running black formatter check..."
	poetry run black --check --diff .

isort:
	@echo "Running isort import sorting check..."
	poetry run isort --check-only --diff .

flake8:
	@echo "Running flake8 linting..."
	poetry run flake8 .


mypy:
	@echo "Running mypy type checking..."
	poetry run mypy .

codespell:
	@echo "Running codespell..."
	poetry run codespell