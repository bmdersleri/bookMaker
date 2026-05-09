# CLAUDE.md — bookMaker Agent Instructions

## 1. Project Identity

`bookMaker` is an LLM-assisted, author-controlled, quality-gated academic/technical book authoring studio.

Primary book context:
- Main textbook target: `Java'nın Temelleri`
- Typical outputs: Turkish academic textbook chapters, manifests, validation reports, code samples, diagrams, and export-ready artifacts
- Authoring principle: the human author controls scope, structure, quality gates, and final approval

Repository:
- GitHub: `https://github.com/bmdersleri/bookMaker`
- Default branch: `main`
- Git user: Ismail Kirbas
- Book projects live under: `book_projects/`

Example book project paths:
- `book_projects/flutter-ile-mobil-uygulama-gelistirme/`
- `book_projects/python-programlama-giris/`

---

## 2. Non-Negotiable Rules

Follow these rules in every task:

1. Work in small, reviewable changes.
2. Inspect relevant files before editing.
3. Prefer editing existing files over creating new ones.
4. Do not rewrite unrelated files.
5. Do not commit, push, reset, clean, delete, or rename large folders without explicit user approval.
6. Do not read, print, copy, commit, or expose secrets.
7. Keep Turkish academic tone in documentation, prompts, and book content.
8. Use UTF-8 everywhere.
9. Use `pathlib.Path` in Python code.
10. Avoid fragile shell-string composition; prefer argument lists or Python-native file operations.
11. For Windows commands, prefer PowerShell-compatible syntax.
12. Before any commit proposal touching Python code, run the `quick-validate` workflow or the closest available fast validation commands.

Protected files and directories:
- `llm_config.json`
- `.claude/settings.local.json`
- `.remember/`
- `.env`
- `*.key`
- `*.pem`
- `id_rsa`
- `id_ed25519`
- `credentials.json`
- `tokens.json`
- `build/`
- `debug.log`

Never include secrets or local credentials in diffs, logs, summaries, or generated documentation.

---

## 3. Default Working Method

For each development task:

1. Restate the goal in one short sentence.
2. Identify the smallest relevant file set.
3. Inspect before editing.
4. Propose a concise plan.
5. Make minimal changes.
6. Run the narrowest relevant validation/test command.
7. Summarize:
   - changed files
   - reason for each change
   - validation result
   - remaining risks or next step

When the request is exploratory, analyze first and do not edit until the user approves.

When uncertain, choose the safest minimal change and clearly state the assumption.

---

## 4. Architecture Map

```text
src/bookmaker/
├── cli.py                    # Typer CLI entry point
├── generation/
│   ├── pipeline.py           # ChapterGenerator; generation pipeline strategies
│   ├── prompts.py            # SYSTEM_AUTHOR and seed/enrich prompts
│   ├── spec.py               # Spec generation and validation
│   ├── postprocess.py        # Normalize, deepen, assemble, insert
│   └── clean_text.py         # TextCleaner; regex-based cleanup
├── chapter/                  # Parser, validator, scoring, validation_modes
├── production/               # Mermaid, Pandoc, QR, production pipeline
├── manifest/                 # BookManifest, PipelineState, BookChapterRef models
├── studio/                   # FastAPI GUI; localhost:8765
│   └── services/             # book, chapter, prompt, export, wizard services
├── llm/                      # DeepSeek API client
└── core/                     # BookConfig, paths, errors
```

Important files:
| Purpose | Path |
|---|---|
| Project overview for LLMs | `LLM_EXPLANATION.md` |
| Main generation prompts | `src/bookmaker/generation/prompts.py` |
| Spec prompts and validation | `src/bookmaker/generation/spec.py` |
| Generation pipeline | `src/bookmaker/generation/pipeline.py` |
| Post-processing | `src/bookmaker/generation/postprocess.py` |
| BookManifest model | `src/bookmaker/manifest/models.py` |
| BookConfig | `src/bookmaker/core/config.py` |
| Studio app | `src/bookmaker/studio/app.py` |
| Studio jobs | `src/bookmaker/studio/jobs.py` |
| Book projects | `book_projects/` |

---

## 5. Environment Assumptions

Primary environment:
- Windows
- PowerShell 7 preferred
- Python virtual environment: `.venv/`
- Dependency manager: `uv`
- Package name: `bookmaker`
- CLI command: `bookmaker`
- LLM provider: DeepSeek Chat via `llm_config.json`
- Line endings: LF preferred
- Encoding: UTF-8

Do not assume these tools are available unless verified:
- `just`
- `fd`
- `mkdocs`
- Bash-only utilities

If a command fails because of shell differences, convert it to PowerShell-compatible syntax.

---

## 6. Common Commands

### Setup

```powershell
uv sync
Copy-Item llm_config.example.json llm_config.json
```

After copying `llm_config.json`, the user must add the real API key manually. Do not open or print this file.

### Fast validation

```powershell
uv run ruff check src/
uv run pytest tests/ -q --tb=short
python tools/validate_prompt_changes.py
```

### Targeted checks

```powershell
uv run pytest tests/<test_file>.py -q --tb=short
python -m py_compile src/bookmaker/generation/prompts.py
python -m py_compile src/bookmaker/generation/spec.py
python -m py_compile src/bookmaker/generation/pipeline.py
```

### Book quality check

```powershell
uv run bookmaker check book book_projects/<project-name> --json --verbose
```

### Costly/API-based checks

Run only with explicit user approval:

```powershell
python tools/test_pipeline_full.py
```

### Git safety

Allowed without extra approval:
```powershell
git status --short
git diff --stat
git diff -- <path>
```

Require explicit user approval:
```powershell
git add
git commit
git push
git reset
git clean
git checkout
Remove-Item
Rename-Item
```

Default branch is `main`. Do not use or push to another branch unless the user explicitly requests it.

---

## 7. Current Technical Focus

Current development priorities:
- 6-stage generation pipeline:
  1. SPEC
  2. VALIDATE
  3. SEED
  4. NORMALIZE
  5. ENRICH
  6. ASSEMBLE
- Multi-language prompt engineering:
  - Java
  - Python
  - Dart/Flutter
  - generic technical books
- Studio GUI improvements:
  - inline editing
  - pipeline tracking
  - export controls
  - safer manifest editing
- `book_manifest.yaml` as the single configuration source
- `book_profile.yaml` has been eliminated
- Pedagogical depth chain:
  1. TANIM
  2. NEDEN
  3. NASIL
  4. NE ZAMAN
  5. ALTERNATİF
  6. HATA

---

## 8. Academic Writing Rules

For Turkish academic content:
- Use clear, fluent, formal Turkish.
- Avoid filler and vague claims.
- Prefer structured explanations with examples.
- Use consistent technical terminology.
- Preserve important English technical terms when standard in the field.
- For textbook chapters, maintain pedagogical progression.
- When generating examples, ensure they are testable, realistic, and aligned with the target student level.

For code examples:
- Keep examples minimal but complete.
- Add comments only when they teach something useful.
- Avoid deprecated APIs.
- Prefer reproducible examples.
- If a code block is meant to be tested, ensure the expected output is clear.

---

## 9. Pipeline and Prompt Editing Rules

When editing generation prompts or pipeline code:

1. Read the existing prompt/pipeline logic first.
2. Preserve current public interfaces unless the task explicitly requires an API change.
3. Avoid large prompt rewrites; prefer targeted improvements.
4. Validate prompt syntax after editing.
5. Check for Turkish character corruption.
6. Do not run full API pipeline tests unless explicitly approved.

Minimum validation after prompt edits:

```powershell
python tools/validate_prompt_changes.py
python -m py_compile src/bookmaker/generation/prompts.py
python -m py_compile src/bookmaker/generation/spec.py
```

Minimum validation after Python code edits:

```powershell
uv run ruff check src/
uv run pytest tests/ -q --tb=short
```

---

## 10. Studio GUI Rules

When working under `src/bookmaker/studio/`:

- Preserve existing FastAPI route behavior unless the task requires a route change.
- Keep UI changes small and readable.
- Prefer user-friendly validation and error messages.
- Do not hard-code project-specific paths when a service/helper exists.
- Check relevant service, route, and template/static files together.
- For manifest editing, prioritize error prevention over after-the-fact correction.

---

## 11. Book Project Rules

When working under `book_projects/`:

- Do not alter generated chapter content unless the user asks for content editing.
- Preserve manifest structure.
- Prefer fixing validation configuration or pipeline logic before manually patching generated outputs.
- For chapter quality issues, inspect:
  - `book_manifest.yaml`
  - chapter manifest
  - `content/draft.md`
  - `content/final.md`
  - logs under `logs/reviews/`

For project-based books, expect paths similar to:

```text
book_projects/<project>/
├── book_manifest.yaml
├── chapters/
│   └── <chapter-alias>/
│       ├── chapter_manifest.yaml
│       └── content/
│           ├── draft.md
│           ├── final.md
│           └── revisions/
└── logs/
    └── reviews/
```

---

## 12. Claude Skills

Use workflows under `.claude/skills/` when available:

- `pipeline-dev` — edit → validate → test cycle for generation code
- `chapter-debug` — analyze pipeline output and quality issues
- `quick-validate` — fast pre-commit validation; no API; target <5s

Before any commit proposal touching Python code, invoke or approximate `quick-validate`.

---

## 13. Response Format to User

After completing a task, respond with:

```text
Summary:
- ...

Changed files:
- ...

Validation:
- ...

Notes/Risks:
- ...

Suggested commit message:
...
```

Do not over-explain routine implementation details. Highlight only decisions, risks, and validation results.
