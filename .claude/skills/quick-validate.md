---
name: quick-validate
description: Fast pre-commit validation — syntax check, prompt checks, and import test. Runs in <5 seconds, no API calls.
---

# Quick Validation Skill

## Trigger
Use BEFORE every commit that touches Python source files. Always run this before `git commit`.

## Run
```bash
# All-in-one fast check (<5 seconds, no API)
python -m py_compile src/bookmaker/generation/prompts.py && \
python -m py_compile src/bookmaker/generation/spec.py && \
python -m py_compile src/bookmaker/generation/pipeline.py && \
python -m py_compile src/bookmaker/generation/postprocess.py && \
python tools/validate_prompt_changes.py && \
echo "===== ALL CHECKS PASSED ====="
```

## What it checks
1. Python syntax (`py_compile`) — cataches typos, bad indentation, missing imports
2. Prompt contracts (40 assertions) — SYSTEM_AUTHOR has 6-step chain, enrichment prompts accept concepts, spec has depth rules
3. Import smoke test — verifies the modules can be imported

## When checks fail
- **Syntax error**: fix the file, re-run
- **Prompt contract fail**: check which assertion broke (the output shows it), fix the prompt, re-run
- **Import error**: usually a missing dependency, run `uv sync`

## Don't commit if any check fails
Broken syntax or prompt contracts will break the CI pipeline.
