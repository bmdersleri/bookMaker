default:
    @just --list

dev:
    uv sync

test:
    uv run pytest tests/ -v

test-cov:
    uv run pytest tests/ --cov=bookmaker --cov-report=term-missing

lint:
    uv run ruff check src/ tests/
    uv run ruff format --check src/ tests/

fmt:
    uv run ruff format src/ tests/
    uv run ruff check --fix src/ tests/

check: lint test

version:
    uv run bookmaker --version
