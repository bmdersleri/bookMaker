# CLAUDE.md — bookMaker Agent Instructions

## Project Identity
bookMaker is an LLM-assisted, author-controlled, quality-gated Turkish academic/technical book authoring studio. Primary output: "Java'nın Temelleri" textbook (27 chapters + 4 appendices).

## Repository
- Repo: `https://github.com/bmdersleri/bookMaker`
- Branch: `main` (tek branch)
- Git user: Ismail Kirbas
- Book content lives in `book_projects/` (ornek: `flutter-ile-mobil-uygulama-gelistirme/`, `python-programlama-giris/`)

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
├── chapter/                  # Parser, validator, scoring, validation_modes
├── production/               # Mermaid, Pandoc, QR, pipeline
├── manifest/                 # BookManifest, PipelineState, BookChapterRef modelleri
├── studio/                   # FastAPI GUI (localhost:8765)
│   └── services/             # book, chapter, prompt, export, wizard, etc.
├── llm/                      # DeepSeek API client
└── core/                     # BookConfig, paths, errors
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
| BookManifest model | `src/bookmaker/manifest/models.py` |
| BookConfig | `src/bookmaker/core/config.py` |
| Studio GUI | `src/bookmaker/studio/app.py` |
| Pipeline jobs | `src/bookmaker/studio/jobs.py` |
| Book projects | `book_projects/` |
| Flutter kitap | `book_projects/flutter-ile-mobil-uygulama-gelistirme/` |

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
- 6-stage pipeline: SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE
- Multi-language prompt engineering (Java, Python, Dart/Flutter, generic)
- Studio GUI improvements (inline editing, pipeline tracking, export controls)
- book_manifest.yaml as single configuration source (book_profile.yaml eliminated)
- 6-step pedagogical depth chain: TANIM → NEDEN → NASIL → NE ZAMAN → ALTERNATİF → HATA

## Project Skills
See `.claude/skills/` for detailed workflows:
- `pipeline-dev` — edit → validate → test cycle for generation code
- `chapter-debug` — analyze pipeline output for quality issues
- `quick-validate` — pre-commit fast check (<5s, no API)
- Invoke `quick-validate` skill before every commit that touches Python code
