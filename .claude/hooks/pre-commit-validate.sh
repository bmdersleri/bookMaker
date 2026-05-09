#!/bin/bash
# Pre-commit validation hook
# Runs quick-validate before allowing git commit on Python files
# Called by Claude Code PreToolUse hook

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('arguments',{}).get('command',''))" 2>/dev/null)

# Only intercept git commit commands
if [[ ! "$COMMAND" =~ ^git\ commit ]]; then
    echo '{"continue": true}'
    exit 0
fi

echo "  HOOK: pre-commit validation..." >&2

# Run py_compile checks
for f in src/bookmaker/generation/prompts.py \
         src/bookmaker/generation/spec.py \
         src/bookmaker/generation/pipeline.py \
         src/bookmaker/generation/postprocess.py; do
    if [ -f "$f" ]; then
        python3 -m py_compile "$f" 2>&1 || {
            echo '{"continue": false, "message": "Syntax error in '"$f"'. Fix before commit."}'
            exit 0
        }
    fi
done

# Run prompt validation
python3 tools/validate_prompt_changes.py > /dev/null 2>&1 || {
    echo '{"continue": false, "message": "Prompt validation failed. Run: python tools/validate_prompt_changes.py"}'
    exit 0
}

echo '{"continue": true}'
