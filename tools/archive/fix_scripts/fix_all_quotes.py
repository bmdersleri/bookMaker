p = "src/bookmaker/generation/pipeline.py"
c = open(p, "r", encoding="utf-8").read()

# Find all \"" and \" patterns in the new method section
import re
# Find the start of the new method
start = c.find("    def generate_chapter_with_spec")
if start < 0:
    print("Method not found, searching for escape patterns everywhere")
    # Just fix ALL \" patterns
    fixed = c.replace('\\"', '"')
else:
    # Only fix in the new method section
    end = c.find("    def _fallback_content", start)
    if end < 0:
        end = len(c)
    new_section = c[start:end]
    fixed_section = new_section.replace('\\"', '"')
    fixed = c[:start] + fixed_section + c[end:]

open(p, "w", encoding="utf-8").write(fixed)
print(f"Fixed all escaped quotes. Length: {len(fixed)}")
