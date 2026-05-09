---
name: pipeline-dev
description: Use when editing generation pipeline, prompts, spec, or postprocess code. Provides the full edit → validate → test workflow.
---

# Pipeline Development Skill

## Trigger
Use this skill when the user asks to edit or improve any of:
- `src/bookmaker/generation/prompts.py`
- `src/bookmaker/generation/spec.py`
- `src/bookmaker/generation/pipeline.py`
- `src/bookmaker/generation/postprocess.py`

## Workflow

### Step 1: Understand the change
- Read the relevant file(s) and understand the current behavior
- Confirm the change with the user before editing
- Prefer `Edit` tool over rewriting entire files

### Step 2: Implement
- Make the change as small and focused as possible
- Update both the main code AND any related prompt builders

### Step 3: Validate (do this BEFORE committing)
```bash
# Syntax check all modified files
python -m py_compile src/bookmaker/generation/prompts.py
python -m py_compile src/bookmaker/generation/spec.py
python -m py_compile src/bookmaker/generation/pipeline.py
python -m py_compile src/bookmaker/generation/postprocess.py

# Prompt contract validation (40 checks)
python tools/validate_prompt_changes.py
```

### Step 4: Test (optional, uses API — costly)
```bash
# Clean previous output and run full pipeline test
rm -rf book_projects/java-temelleri/build/generation/*
python tools/test_pipeline_full.py
```

## Key Rules
- `prompts.py`: SYSTEM_AUTHOR + build_seed_prompt + all build_enrich_* functions
- `spec.py`: build_spec_prompt + build_seed_from_spec_prompt + build_spec_validation_prompt
- Enrichment prompt builders accept `concepts` parameter (Optional[list[str]])
- `detect_missing_sections` returns ASCII keys (ozet, sozluk, soru, etc.)
- `insert_section` supports `turkish_terms` for dedup
- After pipeline changes, always run `validate_prompt_changes.py`
