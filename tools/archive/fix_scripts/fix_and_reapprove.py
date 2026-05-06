"""Comprehensive fix: stray quotes, unclosed fences, then re-approve all."""
import re
from pathlib import Path
from bookmaker.authoring.pipeline import AuthoringPipeline
from bookmaker.chapter.parser import parse
from bookmaker.chapter.validator import validate

root = Path("book_projects/java-temelleri")
pipe = AuthoringPipeline(root)

# STEP 1: Fix ALL approved files in-place
print("=== STEP 1: Fix approved files ===")

total_stray_fixed = 0
total_unclosed_fixed = 0

for ap in sorted(root.glob("chapters/*/approved/*.md")):
    cid = ap.parent.parent.name
    text = ap.read_text("utf-8")
    changed = False
    
    # Fix 1: Stray quotes after ```java
    new_text = re.sub(r'```java[\u201c\u201d\u2018\u2019\u0022]', "```java", text)
    if new_text != text:
        stray_count = len(re.findall(r'```java[\u201c\u201d\u2018\u2019\u0022]', text))
        total_stray_fixed += stray_count
        print(f"  {cid}: fixed {stray_count} stray quote(s)")
        text = new_text
        changed = True
    
    # Fix 2: Check if last code block is unclosed
    lines = text.splitlines()
    # Find all ``` positions
    fence_positions = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") and len(stripped) <= 5:
            fence_positions.append(i)
    
    # If we have an odd number of fences, the last one is unclosed
    # But this is too simplistic. Let me check if the very last line is code
    # Look for the last fence and check if it has a matching closing
    # Find the last line that starts with ```
    last_fence_line = -1
    last_fence_is_opening = False
    for i in range(len(lines)-1, -1, -1):
        stripped = lines[i].strip()
        if stripped.startswith("```"):
            # Check if this is an opening or closing fence
            # Opening: ```lang (more than 3 backticks + optional lang)
            # Closing: ``` (exactly 3 backticks, no lang)
            if stripped == "```":
                # This is a closing fence - check if it's the last one
                # Find if there's any content after it
                has_content_after = False
                for j in range(i+1, len(lines)):
                    if lines[j].strip():
                        has_content_after = True
                        break
                if not has_content_after:
                    last_fence_line = i
                    last_fence_is_opening = False  # It's a closing fence, so previous one is fine
                break
            else:
                # This is an opening fence - it's the last significant thing
                # Check if there's a closing after it
                has_closing = False
                for j in range(i+1, len(lines)):
                    if lines[j].strip() == "```":
                        has_closing = True
                        break
                if not has_closing:
                    last_fence_line = i
                    last_fence_is_opening = True
                break
    
    if last_fence_is_opening:
        # Add ``` at end
        text = text.rstrip() + "\n```\n"
        changed = True
        total_unclosed_fixed += 1
        lang = lines[last_fence_line].strip()[3:]  # extract lang after ```
        print(f"  {cid}: added closing ``` (opening was: ```{lang})")
    
    if changed:
        ap.write_text(text, encoding="utf-8")

print(f"\n  Stray quotes fixed: {total_stray_fixed}")
print(f"  Unclosed fences fixed: {total_unclosed_fixed}")

# STEP 2: Re-approve all chapters to sync draft->approved
print("\n=== STEP 2: Re-approve all chapters ===")
for cd in sorted(root.glob("chapters/*/")):
    cid = cd.name
    if cid in ["bolum_01", "test-ch"]:
        continue  # skip incomplete
    dp = cd / "draft_versions/v001.md"
    if not dp.exists():
        continue
    try:
        ap = pipe.approve(cid)
        state = pipe.get_state(cid)
        print(f"  {cid}: approved (step={state.current_step})")
    except Exception as e:
        print(f"  {cid}: ERROR - {e}")

# STEP 3: Final validation check
print("\n=== STEP 3: Validation check ===")
from collections import Counter
total_errors = 0
for cd in sorted(root.glob("chapters/*/")):
    cid = cd.name
    if cid in ["bolum_01", "test-ch"]:
        continue
    dp = cd / "draft_versions/v001.md"
    if not dp.exists():
        continue
    parsed = parse(dp)
    issues = validate(parsed)
    errors = [i for i in issues if i.severity.value == "error"]
    warnings = len([i for i in issues if i.severity.value == "warning"])
    if errors:
        total_errors += len(errors)
        by_cat = Counter(i.category for i in errors)
        cat_str = ", ".join(f"{c}={n}" for c, n in sorted(by_cat.items()))
        print(f"  !! {cid}: {len(errors)} errors ({cat_str})")
        for e in errors[:3]:
            print(f"      line {e.location.line}: {e.message[:80]}")
    else:
        print(f"  OK {cid}: {warnings} warnings")

print(f"\nTotal errors: {total_errors}")
