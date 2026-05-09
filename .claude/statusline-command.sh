#!/bin/sh
input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "unknown"')
model=$(echo "$input" | jq -r '.model.display_name // "unknown"')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

# Get git branch (skip optional locks to avoid conflicts)
branch=""
if git -C "$cwd" --no-optional-locks rev-parse --is-inside-work-tree 2>/dev/null | grep -q true; then
  branch=$(git -C "$cwd" --no-optional-locks symbolic-ref --short HEAD 2>/dev/null)
fi

# Build the status line
dir_part=$(printf '\033[34m%s\033[0m' "$cwd")

if [ -n "$branch" ]; then
  branch_part=$(printf ' \033[32m(%s)\033[0m' "$branch")
else
  branch_part=""
fi

model_part=$(printf ' \033[33m[%s]\033[0m' "$model")

if [ -n "$used" ]; then
  ctx_part=$(printf ' \033[36mctx:%s%%\033[0m' "$(printf '%.0f' "$used")")
else
  ctx_part=""
fi

printf '%s%s%s%s\n' "$dir_part" "$branch_part" "$model_part" "$ctx_part"
