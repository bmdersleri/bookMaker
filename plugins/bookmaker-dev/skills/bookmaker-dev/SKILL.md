---
name: bookmaker-dev
description: BookMaker repository development workflow for Codex. Use when changing Python source, tests, CLI commands, Studio services, migration work, validation behavior, or session notes in the D:\bookMaker_clean repo; includes branch hygiene, required checks, and project-specific guardrails.
---

# BookMaker Dev

## Workflow

1. Read `SESSION.md` and `MIGRATION.md` before making assumptions about the active phase.
2. Work only in `D:\bookMaker_clean` unless the user explicitly redirects.
3. Check `git status --short`, branch, and recent log before edits.
4. Preserve user changes; do not reset, clean, or checkout files unless explicitly requested.
5. Prefer small patches that follow existing module boundaries and tests.
6. Run focused tests first, then acceptance checks before finalizing.
7. Update `SESSION.md` at the end of substantial work.

## Required Checks

Use repo-local uv cache if the user cache fails:

```powershell
$env:UV_CACHE_DIR='.\\.uv-cache'
uv run ruff check src/ tests/
uv run pytest tests/ -q --tb=short
uv run bookmaker check book book_projects/flutter-ile-mobil-uygulama-gelistirme --json --verbose
git diff --check
```

## Git Hygiene

- Do not commit generated logs, temporary scripts, stack dumps, local config secrets, or cache folders.
- Keep `SESSION.md` commits separate from code commits when practical.
- If Git reports `C:\Users\ismai/.config/git/ignore` permission warnings, continue unless the command failed.
- If staging or committing fails on `.git/index.lock` permission, request escalation for the exact Git command.

## References

- Read `references/repo-map.md` for high-signal paths and commands.
