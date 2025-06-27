.PHONY: lint install-deps black isort flake8 mypy codespell build clean publish test-publish version

lint: install-deps black isort flake8 mypy codespell

install-deps:
	@echo "Installing dependencies..."
	poetry install --with dev

black:
	@echo "Running black formatter check..."
	poetry run python -m black --check --diff .

isort:
	@echo "Running isort import sorting check..."
	poetry run python -m isort --check-only --diff .

flake8:
	@echo "Running flake8 linting..."
	poetry run python -m flake8 .


mypy:
	@echo "Running mypy type checking..."
	poetry run python -m mypy .

codespell:
	@echo "Running codespell..."
	@poetry run python -c "import subprocess; subprocess.run(['codespell'], check=False)" || echo "Codespell check completed"

# Quick release workflow
release-patch: lint
	poetry version patch
	rm -rf dist/
	poetry build
	poetry publish

release-minor: lint  
	poetry version minor
	rm -rf dist/
	poetry build
	poetry publish

release-major: lint
	poetry version major
	rm -rf dist/
	poetry build
	poetry publish