dev:
    uv sync

test:
    uv run pytest tests/ -q --tb=short

fast:
    uv run pytest tests/ -q --tb=short -m "not slow"

all:
    uv run pytest tests/

lint:
    uv run ruff check src/ tests/

fmt:
    uv run ruff format src/ tests/

check:
    uv run ruff check src/ tests/
    uv run pytest tests/ -q --tb=short -m "not slow"

ci:
    uv run ruff check src/ tests/ --fix
    uv run pytest tests/ -q --tb=short -m "not slow"
    echo "CI OK"

version:
    uv run python -m bookmaker --version

studio:
    uv run python -c "from bookmaker.studio.app import run_studio; run_studio()"

help:
    uv run python -m bookmaker --help
