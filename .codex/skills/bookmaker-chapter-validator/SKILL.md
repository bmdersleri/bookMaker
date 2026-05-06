---
name: bookmaker-chapter-validator
description: BookMaker chapter validation and profile-aware test mode workflow. Use when changing src/bookmaker/chapter/validator.py, validation_modes.py, parser/scoring behavior, CODE_META/SECTION_META/MERMAID_META checks, profile-aware test modes, or tests for chapter validation.
---

# BookMaker Chapter Validator

## Core Rules

1. Keep validator public APIs backward-compatible with optional parameters.
2. Keep validation/test mode constants centralized in `src/bookmaker/chapter/validation_modes.py`.
3. Prefer manifest-provided profile when available; preserve path inference only as fallback.
4. Unknown profile should not break legacy behavior unless the task explicitly changes that policy.
5. Flutter book validation must remain `100/pass`.

## Profile Behavior

Canonical profiles:

```text
java
flutter
generic
```

Profile-aware test mode checks must reject Java execution modes for Flutter profiles and Flutter/Dart modes for Java profiles. Non-execution modes remain valid for all profiles.

## Focused Checks

```powershell
$env:UV_CACHE_DIR='.\\.uv-cache'
uv run pytest tests/test_chapter_validation_modes.py tests/test_chapter_validator_profile_modes.py -q --tb=short
uv run ruff check src/bookmaker/chapter tests/test_chapter_validation_modes.py tests/test_chapter_validator_profile_modes.py
```

Run full acceptance checks before finishing.

## References

- Read `references/validator-contract.md` before changing mode lists, profile resolution, or issue categories.
