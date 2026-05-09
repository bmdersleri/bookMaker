"""Check actual last fence content in approved files."""
from pathlib import Path
import re

root = Path("book_projects/java-temelleri")

# Check bolum-01 and bolum-02 to see what the last "fence" actually is
for cid in ["bolum-01", "bolum-02", "bolum-15", "bolum-19"]:
    ap = root / "chapters" / cid / "approved" / f"{cid}_v001.md"
    text = ap.read_text("utf-8")
    lines = text.splitlines()
    
    # Find the LAST ``` in the file
    last_pos = text.rfind("```")
    context_start = max(0, last_pos - 200)
    before = text[context_start:last_pos]
    after = text[last_pos:last_pos+50]
    
    print(f"\n=== {cid}: last ``` at byte {last_pos} (line {text[:last_pos].count(chr(10))+1}) ===")
    print(f"  Before: {repr(before[-100:])}")
    print(f"  At:     {repr(after[:50])}")
    
    # Check if the last 100 chars look like a proper end
    tail = text[-100:]
    # A proper end should be:
    # ...code\n```\n
    # or ...code\n```    (no trailing newline)
    print(f"  File tail (last 100 chars): {repr(tail)}")
