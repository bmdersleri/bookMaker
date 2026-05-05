"""Inspect bolum-17 block 1 content."""
import re
from pathlib import Path

text = Path("book_projects/java-temelleri/chapters/bolum-17/approved/bolum-17_v001.md").read_text("utf-8")
blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))

if blocks:
    code = blocks[0].group(1).strip()
    print(f"Block 1 ({len(code)} chars):")
    for i, line in enumerate(code.splitlines()):
        print(f"  {i+1}: |{line}|")
    
    # Check if it looks clean (just mermaid code)
    lines = code.splitlines()
    clean = all(l.startswith(("graph", "    ", "  ")) or not l.strip() for l in lines)
    print(f"\nClean mermaid code: {clean}")
    
    # If not clean, find where non-mermaid starts
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith(("graph", "    ", "  ")) and i > 0:
            print(f"  Non-mermaid content starts at line {i+1}: {line[:80]}")
