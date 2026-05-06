---
name: bookmaker-project-manifests
description: BookMaker project-based manifest workflow. Use when working with book_manifest.yaml, chapter_manifest.yaml, pipeline_state.yaml, book_projects/*, `bookmaker init`, `bookmaker check book`, chapter ordering, project paths, or migration from legacy book_profile/book_architecture layouts.
---

# BookMaker Project Manifests

## Canonical Model

Treat `book_manifest.yaml` as the book-level source of truth and `chapter_manifest.yaml` as the chapter-level source of truth. Runtime state belongs in `pipeline_state.yaml`; logs and exports must stay inside the book project.

Default project used by acceptance checks:

```text
book_projects/flutter-ile-mobil-uygulama-gelistirme
```

## Workflow

1. Inspect `src/bookmaker/manifest/models.py`, `src/bookmaker/core/paths.py`, and `src/bookmaker/chapter/book_validator.py` before changing manifest behavior.
2. Preserve compatibility fields in Pydantic models unless the user explicitly requests removal.
3. Derive chapter order from `book_manifest.yaml > chapters`; do not reintroduce fixed Java chapter lists.
4. Keep path conventions in code, not duplicated in YAML.
5. Validate with the Flutter book project after any manifest or check flow change.

## Checks

```powershell
$env:UV_CACHE_DIR='.\\.uv-cache'
uv run pytest tests/cli/test_check_command.py tests/integration/test_init.py -q --tb=short
uv run pytest tests/ -q --tb=short
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
```

## References

- Read `references/project-architecture.md` for the directory contract, manifest fields, and migration rules.
