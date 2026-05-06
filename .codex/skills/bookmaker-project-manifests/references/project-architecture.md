# Project Architecture Reference

## Directory Contract

```text
book_projects/<book-alias>/
├── book_manifest.yaml
├── pipeline_state.yaml
├── prompts/
│   ├── default_chapter.md
│   └── default_review.md
├── chapters/
│   └── <chapter-alias>/
│       ├── chapter_manifest.yaml
│       ├── prompt.md
│       └── content/
│           ├── draft.md
│           ├── final.md
│           └── revisions/
├── exports/
└── logs/
```

## Ownership

- `book_manifest.yaml`: user/authored book configuration.
- `chapter_manifest.yaml`: user/authored chapter scope and automation overrides.
- `pipeline_state.yaml`: framework runtime state.
- `logs/`: generated validation and production records.
- `exports/`: generated output.

## Validation Rules

- `book_manifest.yaml > chapters` defines chapter order.
- Each listed alias must have `chapters/<alias>/chapter_manifest.yaml`.
- Chapter aliases should be used for references, not legacy numeric IDs.
- Check flows should use project-relative paths in issue locations where possible.

## Key Modules

```text
src/bookmaker/manifest/models.py
src/bookmaker/core/paths.py
src/bookmaker/commands/check.py
src/bookmaker/chapter/book_validator.py
tests/cli/test_check_command.py
tests/integration/test_init.py
```
