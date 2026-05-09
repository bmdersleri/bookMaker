# bookMaker — Complete Project Explanation for LLM

This document provides a complete, self-contained explanation of the bookMaker project so that any LLM reading it can understand the project's purpose, architecture, workflow, features, conventions, and current state without reading any other file.

---

## 1. Project Identity

**bookMaker** is an LLM-assisted, author-controlled, quality-gated academic/technical book authoring studio. It automates the production of structured, pedagogically sound textbooks using DeepSeek Chat as the LLM backend.

- **Language:** Python 3.14.x development environment; minimum supported Python 3.12
- **Package name:** `bookmaker`
- **CLI command:** `bookmaker`
- **Package manager:** uv
- **LLM provider:** DeepSeek Chat (single model)
- **Encoding:** UTF-8 everywhere
- **Path handling:** `pathlib.Path`
- **Primary output format:** Turkish academic/technical books

---

## 2. Repository

| Attribute | Value |
|-----------|-------|
| URL | `https://github.com/bmdersleri/bookMaker` |
| Branch | `main` (single branch) |
| Local path | `D:\bookMaker_clean` |
| Git user | Ismail Kirbas |

---

## 3. High-Level Architecture

```
bookMaker/
├── src/bookmaker/               # Main Python package
│   ├── cli.py                   # Typer CLI entry point
│   ├── core/                    # BookConfig, paths, errors
│   │   ├── config.py            # BookConfig — reads book_manifest.yaml
│   │   ├── paths.py             # find_project_root, BookPaths, ChapterPaths
│   │   └── errors.py            # ConfigError
│   ├── generation/              # LLM chapter generation pipeline
│   │   ├── pipeline.py          # ChapterGenerator — 5 strategies
│   │   ├── prompts.py           # System & user prompt builders
│   │   ├── spec.py              # Spec generation + validation
│   │   ├── postprocess.py       # normalize(), build_front_matter(), insert_section()
│   │   └── clean_text.py        # TextCleaner (regex, 0-token)
│   ├── manifest/                # Pydantic data models
│   │   ├── models.py            # BookManifest, PipelineState, ChapterManifest, etc.
│   │   └── manager.py           # ManifestManager — read/write book_manifest.yaml
│   ├── chapter/                 # Chapter parser, validator, scoring
│   │   ├── validator.py         # validate(), validate_book() — profile-aware
│   │   ├── validation_modes.py  # Profile-based test mode constants
│   │   └── parser.py            # Markdown parser
│   ├── code/                     # Profile-aware code adapters
│   │   ├── runner.py             # select_code_adapter() — profile/language dispatch
│   │   ├── extractor.py          # extract_fenced_blocks() — markdown code extraction
│   │   ├── models.py             # CodeBlock, CodeTestResult dataclasses
│   │   ├── report.py             # summarize_test_results() — post-run summary
│   │   └── adapters/
│   │       ├── base.py           # CodeAdapter (ABC) + ReviewOnlyAdapter
│   │       ├── java.py           # JavaCodeAdapter — javac compilation
│   │       ├── flutter.py        # FlutterCodeAdapter — dart analyze (placeholder)
│   │       ├── python.py         # PythonCodeAdapter — py_compile syntax check
│   │       └── react.py          # ReactCodeAdapter — node --check (JS) + review-only skip (TS/JSX)
│   ├── production/              # Export + visual engines
│   │   ├── pandoc.py            # Pandoc DOCX/PDF/EPUB/HTML conversion
│   │   ├── mermaid.py           # Mermaid → PNG (mmdc CLI, legacy)
│   │   ├── readiness.py         # Export preflight checks
│   │   ├── export_report.py     # Export result logging
│   │   ├── mermaid_theme.py     # Profile-based Mermaid themes (5 profiles)
│   │   ├── mermaid_renderer.py  # mmdc PNG renderer with cache
│   │   ├── themes/              # 5 JSON theme files
│   │   ├── screenshot_engine.py # Tagged block screenshot engine
│   │   ├── screenshot_strategies/
│   │   │   ├── base.py          # ScreenshotStrategy (ABC) + ScreenshotConfig
│   │   │   ├── python_plot.py   # matplotlib/plotly → PNG
│   │   │   ├── python_console.py # Terminal output → PNG
│   │   │   └── react_component.py # React/JSX → headless Chromium PNG
│   │   └── pipeline.py          # Full production pipeline
│   ├── studio/                  # FastAPI GUI (localhost:8765)
│   │   ├── app.py               # FastAPI app with all routes
│   │   ├── jobs.py              # Background job queue + worker thread
│   │   ├── services/            # Service layer
│   │   │   ├── book_service.py
│   │   │   ├── chapter_service.py
│   │   │   ├── prompt_service.py
│   │   │   ├── export_service.py
│   │   │   ├── generation_service.py
│   │   │   ├── observer_service.py
│   │   │   ├── pipeline_service.py
│   │   │   ├── quality_service.py
│   │   │   ├── wizard_service.py
│   │   │   ├── build_service.py
│   │   │   ├── assemble_service.py
│   │   │   └── llm_service.py
│   │   ├── templates/
│   │   │   └── index.html       # Single-page GUI template
│   │   └── static/
│   │       ├── app.js            # All client-side logic
│   │       └── styles.css        # All CSS styles
│   └── llm/                      # LLM API client
│       ├── config.py             # LLMConfig (reads llm_config.json)
│       └── openai.py             # OpenAICompatibleClient
├── tests/                        # Test suite (377 tests)
│   ├── unit/
│   │   ├── test_studio_app.py    # API endpoint tests
│   │   └── test_studio_services.py
│   ├── production/
│   │   ├── test_mermaid_renderer.py     # 36 mermaid theme + renderer tests
│   │   └── test_screenshot_engine.py   # 37 screenshot engine tests
│   ├── test_chapter_validation_modes.py
│   ├── test_chapter_validator_profile_modes.py
│   ├── test_e2e_smoke.py         # End-to-end smoke tests
│   ├── test_export_readiness.py
│   └── test_toolchain.py         # Toolchain readiness tests
├── book_projects/                # Book projects (content, not framework)
│   ├── flutter-ile-mobil-uygulama-gelistirme/
│   └── python-programlama-giris/
├── tools/                        # Utility scripts
├── docs/                         # Historical design documents (archive)
├── llm_config.json               # Global LLM API configuration (not in git)
└── pyproject.toml                # Project metadata + dependencies
```

---

## 4. Book Project Structure

Each book is an independent directory under `book_projects/`:

```
<book-alias>/
├── book_manifest.yaml            # SINGLE source of truth for all book config
├── pipeline_state.yaml           # Runtime state, scores, automation flags
├── prompts/
│   ├── default_chapter.md        # Default chapter generation prompt
│   └── default_review.md         # Default review prompt
├── chapters/
│   └── <chapter-alias>/
│       ├── chapter_manifest.yaml # Chapter-level scope/structure/automation
│       ├── prompt.md             # Chapter-specific prompt
│       └── content/
│           ├── draft.md          # Generated draft
│           ├── final.md          # Approved final version
│           └── revisions/        # Revision history
├── exports/                      # Build outputs
│   ├── docx/
│   ├── pdf/
│   └── md/
└── logs/                         # Runtime logs
    ├── production/               # Pipeline step outputs per job
    ├── errors/
    └── reviews/                  # Quality review reports
```

**Key rule:** `book_manifest.yaml` is the SINGLE configuration source. `book_profile.yaml` is kept only as a read-only legacy fallback for older projects and must not be created by new tooling.

---

## 5. The Central Configuration: book_manifest.yaml

### BookManifest Pydantic Model

```python
class BookManifest(BaseModel):
    book: BookInfo                    # title, alias, author, language, version, edition, year
    production: ProductionConfig      # producer_model, observer_model, generation_mode, approval_required
    style: StyleConfig                # target_audience, tone, code_language, framework
    technical_profile: TechnicalProfile | None
    automation: AutomationConfig      # code_meta_required, screenshot_required, qr_policy, github_code_export
    pandoc: PandocConfig | None       # from_format, filter, reference_doc, toc, toc_depth, toc_title
    mermaid: MermaidConfig | None     # theme, scale, width, background, theme_overrides
    outputs: OutputsConfig | None     # docx, pdf, epub, html_site
    chapters: list[BookChapterRef]    # alias, order, chapter_id, title, source, status
```

### BookConfig Compatibility Layer

`BookConfig` (in `core/config.py`) reads `book_manifest.yaml` and converts it to a legacy dict format via `_manifest_to_raw()`. This provides backward compatibility for all existing code that accesses config values through property accessors like `config.title`, `config.author`, `config.chapter_ids`, `config.reference_docx_path`, etc.

### Validation Profiles

The `style.code_language` field determines the validation profile:
- `java` → Java profile (compile, run, run_assert test modes)
- `dart` / `flutter` → Flutter profile (dart_analyze, flutter_test, widget_test, etc.)
- `python` / anything else → Generic profile (review_only, skip, none)

Profile resolution: `resolve_validation_profile_from_manifest(manifest)` checks `style.code_language`, `style.framework`, and `book.alias` to determine the profile.

---

## 6. Chapter Generation Pipeline

The pipeline has 6 stages: **SPEC → VALIDATE → SEED → NORMALIZE → ENRICH → ASSEMBLE**

### Stage 1: SPEC (Specification Plan)
**File:** `generation/spec.py` — `generate_spec()`, `build_spec_prompt()`

LLM is given the chapter title and concepts. It produces a PLAN (no code blocks allowed) covering: concepts, code examples (described, not written), diagram plans, glossary, assessment questions, exercises, common errors, and tables.

**Output:** `logs/production/{job_id}/step0_spec.md` (800-1300 words)
**Prompt saved to:** `logs/production/{job_id}/prompt0_spec.txt`

### Stage 2: VALIDATE (Spec Validation)
**File:** `generation/spec.py` — `validate_spec()`, `build_spec_validation_prompt()`

The spec is re-checked by LLM: are all concepts covered? Is the format correct? Are there missing sections? Result is `PASS` or `REVISION` (pipeline continues either way).

**Output:** `logs/production/{job_id}/step0_validation.md`

### Stage 3: SEED (Draft Generation)
**File:** `generation/spec.py` — `build_seed_from_spec_prompt()`

The longest and most critical stage. LLM generates the actual chapter content following the 6-step pedagogical depth chain:

1. **TANIM** — Define the concept in 1-2 clear sentences
2. **NEDEN VAR?** — What problem does it solve?
3. **NASIL KULLANILIR?** — Working code example with line-by-line explanation
4. **NE ZAMAN TERCİH EDİLİR?** — When to use this vs. alternatives
5. **ALTERNATİFLERİ** — Comparison table with similar concepts
6. **YAYGIN HATALAR** — Common mistakes and solutions

Writing rules: H1=chapter title, H2=main sections, H3=subsections, code in ``` ``` blocks, meaningful variable names, 3+ comment lines per code block, `// Çıktı: ...` notation. Target: 6000-8000 words. Truncation management via `generate_text_with_resume()` (max 5 resumes).

**Output:** `logs/production/{job_id}/step1_seed.md`
**Prompt saved to:** `logs/production/{job_id}/prompt1_seed.txt`

### Stage 4: NORMALIZE (Cleanup + Front Matter + Mermaid)
**File:** `generation/postprocess.py` — `normalize()`, `normalize_with_mermaid()`

`normalize_with_mermaid()` wraps `normalize()` and then processes mermaid blocks to PNG via `MermaidRenderer` (if mmdc is installed). Returns normalized text unchanged if mmdc is not available.

0-token operations: TextCleaner (quotes, whitespace), heading hierarchy fix, YAML front matter insertion, excess whitespace cleanup.

Front matter is built by `build_front_matter()` using config values:
```yaml
---
title: "Chapter Title"
subtitle: "Book Title"
author: "Author Name"
date: "2026"
lang: tr-TR
project-alias: book-alias
chapter-alias: chapter-01
chapter_id: chapter-01
---
```

**Output:** `logs/production/{job_id}/step2_normalized.md`

### Stage 5: ENRICH (Parallel Enrichment)
**File:** `generation/prompts.py` — `build_enrich_*` functions

6 parallel LLM calls (ThreadPoolExecutor, max 4 workers):

| Component | Prompt Builder | Description |
|-----------|---------------|-------------|
| Özet (Summary) | `build_enrich_summary_prompt()` | 3-5 sentences, key takeaways |
| Sözlük (Glossary) | `build_enrich_glossary_prompt()` | Min 10 terms, `**Term** — definition` format |
| Soru (Questions) | `build_enrich_questions_prompt()` | 5-10 T/F + 5-10 fill-in-the-blank |
| Alıştırma (Exercises) | `build_enrich_exercises_prompt()` | 3 programming exercises with difficulty |
| Hata (Errors) | `build_enrich_errors_prompt()` | Common mistakes and misconceptions |
| Köprü (Bridge) | `build_enrich_bridge_prompt()` | Link to next chapter |

**Outputs:** `logs/production/{job_id}/step3_enrich_{summary,glossary,questions,exercises,errors,bridge}.md`

### Stage 6: ASSEMBLE (Assembly + Screenshots)
**File:** `generation/postprocess.py` — `insert_section()`, `process_screenshots()`

Final `normalize()` pass. Screenshot processing runs in `_save_chapter()` via `process_screenshots()` — tagged code blocks (`python plot`, `python console`, `jsx screenshot`) are rendered to PNG via Playwright (if installed).

Enrichment outputs are inserted into the normalized text. Insertion order (at end of chapter): Exercises → Questions → Glossary → Summary → Errors → Bridge. `insert_section()` matches Turkish variations (özet/özet, sözlük/sozluk, alıştırma/alistirma).

Final `normalize()` pass and save to draft.

**Outputs:**
- `logs/production/{job_id}/step4_final.md`
- `chapters/{chapter_id}/content/draft.md`
- `logs/production/{job_id}/metrics.json` — `{chapter, words, time, model}`

### System Prompt (Author Persona)

`build_system_author(code_language)` dynamically generates the system prompt based on the book's code language. All hardcoded "Java" references have been parameterized. The persona is: academic but plain, practice-focused, uses the 6-step chain, uses everyday analogies — a senior technical writer.

---

## 7. Studio GUI

**Framework:** FastAPI + vanilla JavaScript (no frontend framework)
**URL:** `http://localhost:8765`
**Start:** `uv run python -m bookmaker.studio.app`

### 6 Tabs

| Tab | Purpose |
|-----|---------|
| **Bölümler (Chapters)** | Chapter table with sort, filter, pagination, drag-drop reorder, inline title editing (double-click), bulk actions, chapter wizard (+ Bölüm Ekle), view/edit/check/build/generate per chapter |
| **Pipeline** | Manual pipeline trigger (chapter ID, title, concepts), progress bar with live polling, job list table, expandable job detail panel (per-step prompt→output mapping, timing), cancel support |
| **Kalite (Quality)** | Book quality report (score/decision), chapter quality table (sortable), check modal with issues, book statistics (words, code blocks, diagrams, reading time), full-text search |
| **Build/Export** | Export targets summary, code extraction (profile-aware), Mermaid PNG render, book assembly (merged .md), format export (DOCX/PDF/EPUB/HTML), export config (reference DOCX, lua filter, TOC depth), backup/restore |
| **Promptlar (Prompts)** | Prompt editor with scope selector (default chapter, default review, chapter-specific), load/save, dirty-state tracking with unsaved changes warning |
| **Yapılandırma (Config)** | Full `book_manifest.yaml` editor with sub-tabs: Kitap Bilgisi, Üretim, Stil, Otomasyon, Export. All fields editable and saved via `PUT /api/manifest` |

### Key UI Features
- **Inline chapter title editing:** Double-click a title in the chapters table to edit. Enter/blur saves (`PUT /api/chapters/{id}`), Escape cancels.
- **Split-panel markdown editor:** Left side = textarea, right side = live HTML preview. Save writes to `draft.md` or `final.md`.
- **Pipeline job detail:** Click any job row to expand a detail panel showing per-step status, prompt filename, output filename, and elapsed time.
- **Chapter wizard:** 3-step modal for creating new books with LLM-generated chapter plans.
- **Toast notifications:** 3-level (success/error/info) with auto-dismiss.

### Job Queue System

`jobs.py` implements an in-memory job queue with a daemon worker thread:
- Jobs are created via `create_job()` → stored in `_JOBS` dict
- Worker polls every 1 second via `_dequeue()`
- `_execute_job()` → `_run_pipeline()` for generation, `_run_build()` for DOCX
- Progress tracked via `update_job()` (current step, done/total, log)
- Each pipeline step records: `{name, status, started_at, elapsed_s, prompt_file, output_file}`
- Jobs persisted to `logs/studio_jobs/{job_id}.json`

### API Endpoints (59 routes)

Key endpoint groups:
- `/api/projects` — List book projects with `book_manifest.yaml`
- `/api/active-book` — Get/set active book
- `/api/chapters` — CRUD + reorder
- `/api/manifest` — Read/write full `book_manifest.yaml`
- `/api/prompts/default/{type}` — Read/write default prompts
- `/api/prompts/chapter/{id}` — Read/write chapter prompts
- `/api/view/{id}` — Read chapter content; `/api/view/{id}/save` — Save edited content
- `/api/generate/{id}` — Queue pipeline job
- `/api/jobs` — List jobs; `/api/jobs/{id}` — Get job detail; `/api/jobs/{id}/cancel`
- `/api/check/{id}` — Validate chapter
- `/api/quality/report` — Full quality report; `/api/quality/book` — Book-level report
- `/api/stats` — Book statistics
- `/api/search` — Full-text search
- `/api/build/{id}` — Build DOCX for chapter
- `/api/assemble` — Merge all chapters
- `/api/export/readiness` — Export preflight (manifest/chapter/pandoc readiness)
- `/api/export/{fmt}` — Export to format (docx/pdf/epub/html, readiness check zorunlu)
- `/api/extract/code` — Extract code blocks
- `/api/render/mermaid` — Render Mermaid to PNG
- `/api/backup` / `/api/restore` — Backup/restore project
- `/api/index` / `/api/glossary` — Generate index/glossary
- `/api/observer/review/{id}` — Observer LLM review
- `/api/book/create` — Wizard: create new book
- `/api/wizard/plan` — Wizard: LLM chapter plan

---

## 8. Multi-Language Support

All prompt builders are parameterized with `code_language`:

```python
# In spec.py, prompts.py, jobs.py
build_spec_prompt(title, concepts, ..., code_language="python")
build_seed_from_spec_prompt(spec, title, code_language="dart")
build_system_author("java")  # generates Java-specific system prompt
build_system_author("python")  # generates Python-specific system prompt
```

The `code_language` flows through:
1. `book_manifest.yaml` → `style.code_language`
2. `BookManifest.style.code_language` → `BookConfig.primary_code_language`
3. `ChapterGenerator.code_language` → all prompt builders

Supported languages: Java, Python, Dart/Flutter, and generic (any language).

---

## 9. Quality Control

### Chapter Validator (`chapter/validator.py`)

Validates chapter markdown against `chapter_spec.md`:
- **Structural checks:** YAML front matter, heading hierarchy, section presence
- **Code checks:** CODE_META blocks, language/profile compatibility, test mode validation
- **Asset checks:** SCREENSHOT_META, MERMAID_META
- **Scoring:** 0-100 with decision (pass/fail/warn)

Profile-aware validation:
```python
validate(chapter, final_mode=False, profile=None)
# profile="flutter" → only accepts Dart/Flutter test modes
# profile="java" → only accepts Java test modes
# profile=None → legacy fallback (infers from file path)
```

### CLI Commands
```bash
bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme
bookmaker check chapter chapters/giris/content/draft.md
bookmaker check book ... --json --verbose
```

### Code Adapter Architecture (`code/adapters/`)

Profile-aware code adapters provide language-specific code block compilation/verification. The adapter is selected via `select_code_adapter(profile, code_language)` in `code/runner.py` and used by `quality_service.compile_code()`.

| Profile | Adapter | Tools | Status |
|---------|---------|-------|--------|
| Java | `JavaCodeAdapter` | `javac` | Active — full compilation |
| Flutter | `FlutterCodeAdapter` | `dart analyze` | Placeholder — skips safely |
| Python | `PythonCodeAdapter` | `python -m py_compile` | Active — syntax check |
| React | `ReactCodeAdapter` | `node --check` (JS), review-only (TS/JSX) | Active — JS syntax, safe skip for typed/JSX |
| Generic | `ReviewOnlyAdapter` | — | Active — manual review |

Each adapter inherits from `CodeAdapter` (ABC) and implements:
- `extract_blocks(text) → list[str]` — extract fenced code blocks from markdown
- `run_tests(blocks, workdir) → list[dict]` — write to temp files and execute language tool

The dispatch rules in `select_code_adapter()`:
1. `profile="flutter"` or `code_language="dart"` → `FlutterCodeAdapter`
2. `profile="java"` or `code_language="java"` → `JavaCodeAdapter`
3. `profile="python"` or `code_language="python"` → `PythonCodeAdapter`
4. `code_language` in {javascript, js, jsx, tsx, typescript, ts} → `ReactCodeAdapter` (JS blocks → `node --check`, TS/JSX blocks → review_only skip)
5. Otherwise → `ReviewOnlyAdapter`

---

## 10. Production / Export

### Export Service (`studio/services/export_service.py`)

`export_to_format()` accepts optional overrides:
```python
export_to_format(root, "docx",
    reference_doc="build/custom.docx",
    lua_filter="build/custom.lua",
    toc_depth=3)
```

Resolution order: parameter → `book_manifest.yaml` pandoc config → hardcoded defaults.

Before pandoc conversion, export flow runs readiness checks and writes a report to:
- `logs/production/export_<timestamp>.json`

Report contains readiness snapshot, export command/result, and failure reason (if any).

### Pandoc Command Builder (`production/pandoc.py`)
```python
config.pandoc_cmd(input_path, output_path, toc=True)
# → ['pandoc', '-f', 'markdown+...', '-o', 'output.docx', 'input.md',
#    '--reference-doc', 'ref.docx', '--lua-filter', 'styles.lua',
#    '--toc', '--toc-depth', '2']
```

### Mermaid Theme Engine (`production/mermaid_theme.py`, `mermaid_renderer.py`)

Profile-based Mermaid diagram rendering integrated into the NORMALIZE pipeline stage via `normalize_with_mermaid()` (postprocess.py). If `mmdc` is not installed, returns the normalized text unchanged.

**Theme Manager** (`mermaid_theme.py`):
- 5 profile themes: flutter, java, python, react, default
- Each theme is a JSON file under `production/themes/`
- `MermaidTheme.load(name)` loads a theme, falls back to `default.json`
- `MermaidThemeManager.for_profile(profile, overrides)` resolves profile → theme
- `theme.merge(overrides)` applies `themeVariables` from manifest without mutating original
- `theme.config_file()` context manager creates temp JSON for mmdc `--configFile`

**Renderer** (`mermaid_renderer.py`):
- `MermaidRenderer(config)` — main class, checks mmdc availability
- `process_markdown(md_content, assets_dir, chapter_alias)` — finds `mermaid` blocks, renders to PNG, updates markdown references
- `MermaidRenderConfig.from_manifest(dict)` — loads config from book_manifest.yaml
- Idempotent: MD5 hash + theme name = cache key, stored in `.mermaid_cache.json`
- Failed renders keep original block with HTML comment, don't break the pipeline

**Manifest config:**
```yaml
mermaid:
  theme: flutter         # default | flutter | java | python | react
  scale: 2               # 1=normal, 2=retina
  background: white      # white | transparent
  width: 900             # diagram width in px
  theme_overrides:       # optional fine-tuning
    themeVariables:
      fontSize: "16px"
```

### Screenshot Engine (`production/screenshot_engine.py`, `screenshot_strategies/`)

Playwright-based screenshot rendering for tagged code blocks. Runs after ASSEMBLE in `_save_chapter()` via `process_screenshots()` wrapper (postprocess.py). If Playwright is not installed, returns text unchanged.

**Three strategies:**

| Strategy | Fence syntax | What it does |
|----------|-------------|--------------|
| `PythonPlotStrategy` | `python plot` | Replaces `plt.show()`/`fig.show()` with `savefig`/`write_image`, runs via `sys.executable`, returns PNG |
| `PythonConsoleStrategy` | `python console` | Runs code in subprocess, captures stdout/stderr, renders dark/light terminal HTML, screenshots via Playwright |
| `ReactComponentStrategy` | `jsx screenshot` | Injects component into CDN React+Babel HTML template, opens in headless Chromium, waits for render, screenshots `#root` |

**Key design:**
- All Playwright imports are lazy (`try/except ImportError` inside capture methods)
- `_TAGGED_BLOCK_RE` regex only matches blocks with explicit hints (`python plot`, `python console`, `jsx screenshot`) — plain `python` blocks are untouched
- Cache key = MD5(code + hint), stored in `.screenshot_cache.json`
- Failed renders keep original block with `<!-- SCREENSHOT HATASI -->` comment

**SEED prompt instruction:** The SEED prompt template teaches the LLM to use tagged fence syntax:
- `python plot` → matplotlib/plotly/seaborn graphs
- `python console` → terminal output display
- `jsx screenshot` → React component render

**Manifest config:**
```yaml
production:
  screenshots:
    enabled: true
    python_timeout: 15
    react_timeout: 10
    viewport_width: 1280
    viewport_height: 720
    scale: 2
    terminal_theme: dark     # dark | light
```

---

## 11. Key Design Decisions

1. **Single config source:** `book_manifest.yaml` — `book_profile.yaml` legacy fallback only
2. **Single LLM model:** DeepSeek Chat (no dual-model complexity)
3. **Single global LLM config:** `llm_config.json` at repo root (no per-book config)
4. **Manifest-based project discovery:** `find_project_root()` looks for `book_manifest.yaml`
5. **Project isolation:** Each book is an independent directory under `book_projects/`
6. **Alias-only chapter references:** Chapters identified by alias, not numeric IDs
7. **Convention over configuration:** Paths derived from aliases, not stored in YAML
8. **Single branch:** `main` (all feature branches deleted)
9. **Vanilla JS frontend:** No framework dependencies for the Studio GUI
10. **0-token postprocessing:** TextCleaner and normalization use regex, not LLM

---

## 12. Development Commands

```bash
# Setup
uv sync

# Lint
uv run ruff check src/

# Test (377 passed)
uv run pytest tests/ -q --tb=short

# Start Studio GUI
uv run python -m bookmaker.studio.app
# → http://localhost:8765

# Quality check
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json

# Syntax check
python -m py_compile src/bookMaker/generation/prompts.py
```

---

## 13. Key Files Reference

| File | Purpose |
|------|---------|
| `src/bookmaker/manifest/models.py` | All Pydantic models (BookManifest, PipelineState, PandocConfig, etc.) |
| `src/bookmaker/core/config.py` | BookConfig — reads book_manifest.yaml, provides property accessors |
| `src/bookmaker/generation/pipeline.py` | ChapterGenerator — orchestrates the 6-stage pipeline |
| `src/bookmaker/generation/prompts.py` | All prompt builders + `build_system_author()` |
| `src/bookmaker/generation/spec.py` | Spec generation, validation, seed-from-spec |
| `src/bookmaker/generation/postprocess.py` | normalize(), build_front_matter(), insert_section() |
| `src/bookmaker/studio/app.py` | FastAPI app with all 59 routes |
| `src/bookmaker/studio/jobs.py` | Job queue, worker thread, _run_pipeline() |
| `src/bookmaker/studio/services/wizard_service.py` | create_book() — wizard book creation |
| `src/bookmaker/studio/services/export_service.py` | assemble_book(), export_to_format(), render_mermaid() |
| `src/bookmaker/chapter/validator.py` | Chapter validation with profile-aware test mode checking |
| `src/bookmaker/chapter/validation_modes.py` | Profile constants, test mode helpers |
| `src/bookmaker/code/runner.py` | select_code_adapter() — profile/language to adapter dispatch |
| `src/bookmaker/code/adapters/base.py` | CodeAdapter (ABC) + ReviewOnlyAdapter |
| `src/bookmaker/code/adapters/java.py` | JavaCodeAdapter — javac compilation |
| `src/bookmaker/code/adapters/flutter.py` | FlutterCodeAdapter — dart analyze (placeholder) |
| `src/bookmaker/code/adapters/python.py` | PythonCodeAdapter — py_compile syntax check |
| `src/bookmaker/code/adapters/react.py` | ReactCodeAdapter — node --check (JS) + review-only skip (TS/JSX) |
| `src/bookmaker/code/extractor.py` | extract_fenced_blocks() — regex code block extraction |
| `src/bookmaker/code/report.py` | summarize_test_results() — compile/skip/error counts |
| `src/bookmaker/llm/openai.py` | OpenAICompatibleClient with retry + auto-resume |

---

## 14. Current Project State (2026-05-07)

- **Phase:** FAZ 4 + FAZ 5 complete; post-migration cleanup done
- **Tests:** 279 passed, ruff clean
- **Branch:** `main` (single branch, all others deleted)
- **GUI:** 6 tabs functional, inline editing, pipeline detail tracking, export controls
- **Configuration:** `book_manifest.yaml` as single source, `book_profile.yaml` legacy fallback only
- **Multi-language:** Java, Python, Dart/Flutter, generic profiles supported
- **Book projects:** Flutter (16 chapters) and Python (5 chapters) sample projects present
- **Next:** FAZ 7 (multi-book, user roles, reader mode, Docker/PWA)

---

## 15. Conventions

- **Language:** Turkish for docs, prompts, and UI; English for code identifiers
- **Chapter IDs:** `chapter-alias` format (e.g., `giris`, `dart-temelleri`, `bolum-01`)
- **File naming:** Snake case for Python, kebab case for chapter aliases
- **YAML:** `ruamel.yaml` for read/write, Pydantic for validation
- **Logging:** Print statements (no logging module)
- **Error handling:** Graceful degradation — pipeline continues on non-fatal errors
- **Never commit:** `llm_config.json`, `.claude/settings.local.json`, `build/`, `.playwright-mcp/`, generated export files

---

## 16. CI / QA State

The repository includes GitHub Actions CI for linting and testing on every push and PR:

- Ruff lint (`src/` and `tests/`)
- Pytest test suite (304 tests)
- Prompt validation
- Sample Flutter book project quality check
- Python 3.12 / 3.13 matrix

Before any structural change, run:

```powershell
uv run ruff check src/ tests/
uv run pytest tests/ -q --tb=short
```

Release readiness is tracked in `RELEASE_CHECKLIST.md`.

---

## 17. Development Environment and Toolchain

The project supports local development and devcontainer/Codespaces-based
workflows. `.devcontainer/` provides a ready-to-use Dockerfile and
devcontainer.json.

Core tools: Python 3.12+, uv, Pandoc, Node.js, Playwright (headless Chromium).
Optional tools: Java JDK, Dart/Flutter, Mermaid CLI (mmdc).

Check toolchain readiness:

```powershell
bookmaker check toolchain        # human-readable
bookmaker check toolchain --json # JSON output
```

The `src/bookmaker/core/toolchain.py` module provides `check_toolchain()`
which checks availability and version of all dev tools. Critical tools
(python, uv) produce errors if missing; all others produce warnings.
