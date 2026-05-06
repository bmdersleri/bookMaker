# BookMaker Repo Map

## Active Repo

```text
D:\bookMaker_clean
```

Do not develop in `D:\bookMaker_Deepseek` unless the user explicitly asks.

## High-Signal Files

```text
SESSION.md
MIGRATION.md
TODO.md
pyproject.toml
src/bookmaker/commands/
src/bookmaker/chapter/
src/bookmaker/manifest/
src/bookmaker/studio/
tests/
book_projects/flutter-ile-mobil-uygulama-gelistirme/
```

## Common Commands

```powershell
git status --short
git log --oneline -10
git branch -vv
git remote -v

$env:UV_CACHE_DIR='.\\.uv-cache'
uv run ruff check src/ tests/
uv run pytest tests/ -q --tb=short
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
git diff --check
```

## Files To Avoid Committing

```text
phase4_*.ps1
_phase4_*.py
*.stackdump
book_projects/*/logs/**/*.json
.uv-cache/
.pytest_cache/
.ruff_cache/
llm_config.json
```
