---
name: chapter-debug
description: Use when analyzing pipeline test output for quality issues — formatting errors, duplicates, missing sections, mermaid problems.
---

# Chapter Output Debugging Skill

## Trigger
Use when:
- User reports formatting issues in generated chapter output
- Pipeline test completes but quality problems found
- Need to analyze `step4_final.md` for structural problems

## Quick Diagnostic Commands
```bash
GEN=book_projects/java-temelleri/build/generation

# Section headings (find duplicates)
grep -n '^## ' $GEN/step4_final.md

# Code block counts
grep -c '```java' $GEN/step4_final.md
grep -c '```mermaid' $GEN/step4_final.md

# Duplicate class names (assembly bug indicator)
grep -n 'public class' $GEN/step4_final.md | sort -t: -k2 | uniq -f1 -d

# Meta-commentary check (should be 0)
grep -c 'Harika bir' $GEN/step2_normalized.md

# Missing sections
python -c "
import sys; sys.path.insert(0,'src')
from bookmaker.generation.postprocess import detect_missing_sections
text = open('$GEN/step4_final.md', encoding='utf-8').read()
for m in detect_missing_sections(text):
    print(f'[{\"EXISTS\" if m[\"existing\"] else \"MISSING\"}] {m[\"key\"]}')
"

# Word count and structure
wc -l -w $GEN/step4_final.md
```

## Common Issues and Fixes
| Symptom | Root Cause | Fix Location |
|---------|-----------|-------------|
| Same class 10+ times | Enrichment duplicates seed content | `insert_section` dedup |
| `## Bolum ozeti` + `## Özet` both present | Turkish/ASCII heading mismatch | `detect_missing_sections` keys |
| Empty `---` after front matter | LLM adds separator | `_cleanup_whitespace` |
| 4+ blank lines | LLM formatting | `_cleanup_whitespace` |
| 0 mermaid diagrams | Prompt too weak or mermaid optional | `SYSTEM_AUTHOR` / seed prompt |
| LLM meta "Harika bir..." | LLM adds commentary | `normalize_headings` |
| Spec content in chapter | Seed copies spec instead of writing | `build_seed_from_spec_prompt` |
