# CLAUDE.md — bookMaker Agent Instructions

## Project Identity
bookMaker is an LLM-assisted, author-controlled, quality-gated Turkish academic/technical book authoring studio. Primary output: "Java'nın Temelleri" textbook (27 chapters + 4 appendices).

## Repository
- Repo: `https://github.com/bmdersleri/bookMaker`
- Branch: `deepseek` (main branch: `main`)
- Git user: Ismail Kirbas
- Book content lives in `book_projects/java-temelleri/` (separate repo)

## Architecture
```
src/bookmaker/
├── cli.py                    # Typer CLI entry point
├── generation/
│   ├── pipeline.py           # ChapterGenerator — 5 strategies
│   ├── prompts.py            # SYSTEM_AUTHOR + seed/enrich prompts
│   ├── spec.py               # Spec generation + validation
│   ├── postprocess.py        # Normalize, deepen, assemble, insert
│   └── clean_text.py         # TextCleaner (regex, 0 token)
├── chapter/                  # Parser, validator, scoring
├── production/               # Mermaid, Pandoc, QR, pipeline
├── studio/                   # FastAPI GUI (localhost:8765)
└── llm/                      # DeepSeek API client
```

## Core Rules
- Python package: `bookmaker`, CLI command: `bookmaker`
- LLM provider: DeepSeek Chat (single model, `llm_config.json`)
- Never commit: `llm_config.json`, `.claude/settings.local.json`, `.remember/`, `build/`, `debug.log`
- Use venv at `.venv/` (Python 3.14.4, `uv sync` to install)
- Prefer editing existing files; small, reviewable changes
- Turkish academic writing style in docs and prompts
- UTF-8 everywhere, `pathlib.Path`, avoid shell-string composition

## Key Paths
| What | Where |
|------|-------|
| Prompts | `src/bookmaker/generation/prompts.py` |
| Spec prompts | `src/bookmaker/generation/spec.py` |
| Pipeline | `src/bookmaker/generation/pipeline.py` |
| Postprocess | `src/bookmaker/generation/postprocess.py` |
| Validation script | `tools/validate_prompt_changes.py` |
| Pipeline test | `tools/test_pipeline_full.py` |
| Book project | `book_projects/java-temelleri/` |
| Build output | `book_projects/java-temelleri/build/` |

## Environment
- Python 3.14.4 venv at `.venv/`, managed with uv 0.11.9
- `[tool.uv] link-mode = "copy"` configured in pyproject.toml (suppresses hardlink warnings)
- `git config core.autocrlf input` set (LF endings, no CRLF warnings)
- Bash on Windows: `just`, `fd`, `mkdocs` NOT available from bash
- `.claude/settings.local.json` has broad permission patterns (not in git)

## Common Commands
```bash
# Setup
uv sync
cp llm_config.example.json llm_config.json  # edit with real key

# Lint & test (just replacements since just isn't in bash PATH)
uv run ruff check src/           # lint
uv run pytest tests/ -q --tb=short  # test

# Validation
python tools/validate_prompt_changes.py

# Pipeline test (uses API — costly)
python tools/test_pipeline_full.py

# Syntax check
python -m py_compile src/bookmaker/generation/prompts.py

# Git
git push origin deepseek
```

## Current Focus
- Prompt engineering for chapter generation pipeline
- 4-stage pipeline: Spec → Seed → Normalize → Enrich → Assemble
- 6-step pedagogical depth chain: TANIM → NEDEN → NASIL → NE ZAMAN → ALTERNATİF → HATA
- Enrichment: parallel LLM calls for özet/sözlük/soru/alıştırma/hata/köprü
