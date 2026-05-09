"""Quick fix for problematic mermaid blocks."""
import re
from pathlib import Path

root = Path("book_projects/java-temelleri")

# FIX 1: bolum-14 - add closing ``` to unclosed mermaid block
print("=== Fix 1: bolum-14 unclosed mermaid block ===")
ap14 = root / "chapters/bolum-14/approved/bolum-14_v001.md"
dp14 = root / "chapters/bolum-14/draft_versions/v001.md"

for fp in [ap14, dp14]:
    if not fp.exists():
        continue
    text = fp.read_text("utf-8")
    
    # Find the mermaid block
    m = re.search(r"```mermaid\s*\n(.*?)(?=\n```|```java|\n#|\n##)", text, re.DOTALL)
    if m:
        code = m.group(1).strip()
        lines = code.splitlines()
        if lines and "graph" in lines[0]:
            # This is a mermaid block - check if it has proper closing
            rest = text[m.start():]
            close = re.search(r"\n```\s*\n", rest[m.end()-m.start():])
            if not close or m.end() - close.end() > 200:
                # Add closing ```
                print(f"  Found unclosed mermaid: {len(lines)} lines, first: {lines[0][:60]}")
                # Find where the actual mermaid code ends (before the MERMAID_META or other content)
                # The actual mermaid code is just the graph TD lines
                actual_end = m.start()
                for j, line in enumerate(text[m.start():].splitlines(True)):
                    if line.strip().startswith("graph") or j == 0:
                        continue
                    if not line.strip():
                        actual_end = m.start() + sum(len(l) for l in text[m.start():].splitlines(True)[:j+1])
                        break
                    if not line.strip().startswith(("A[", "B[", "C[", "D[", "E[", "F[", "G[", "    ")):
                        actual_end = m.start() + sum(len(l) for l in text[m.start():].splitlines(True)[:j])
                        break
                
                # Add closing ``` right after the graph code
                text = text[:actual_end] + "\n```\n" + text[actual_end:]
                fp.write_text(text, encoding="utf-8")
                print(f"  Added closing ``` at position {actual_end}")

# FIX 2: bolum-17 - remove quotes from mermaid node labels
print("\n=== Fix 2: bolum-17 quotes in mermaid labels ===")
ap17 = root / "chapters/bolum-17/approved/bolum-17_v001.md"
dp17 = root / "chapters/bolum-17/draft_versions/v001.md"

for fp in [ap17, dp17]:
    if not fp.exists():
        continue
    text = fp.read_text("utf-8")
    
    # Find mermaid blocks and fix quotes inside brackets
    def fix_mermaid_labels(code):
        # In graph TD nodes like [text with "quotes"], remove the quotes
        # Replace " inside [...] with '
        return re.sub(r'\[([^\]]*)"([^\]]*)\]', lambda m: '[' + m.group(1) + "'" + m.group(2) + ']', code)
    
    # Find ALL mermaid blocks and fix them
    def fix_block(m):
        code = m.group(1)
        fixed = fix_mermaid_labels(code)
        if fixed != code:
            print(f"  Fixed quotes in mermaid code")
        return m.group(0).replace(code, fixed)
    
    text = re.sub(r"```mermaid\s*\n(.*?)```", fix_block, text, flags=re.DOTALL)
    fp.write_text(text, encoding="utf-8")
    print(f"  Fixed {fp.parent.parent.name}/{fp.stem}")

# FIX 3: Also check bolum-14 for quotes in mermaid  
print("\n=== Fix 3: Check all mermaid blocks for common issues ===")
for cid in ["bolum-14", "bolum-17", "bolum-15", "bolum-18", "bolum-19", "bolum-20"]:
    for fp in [root / f"chapters/{cid}/approved/{cid}_v001.md"]:
        if not fp.exists():
            continue
        text = fp.read_text("utf-8")
        changed = False
        
        # Check all mermaid blocks
        blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))
        for i, b in enumerate(blocks):
            code = b.group(1)
            
            # Fix quotes in labels
            fixed_code = re.sub(r'\[([^\]]*)"([^\]]*)\]', lambda m: '[' + m.group(1) + "'" + m.group(2) + ']', code)
            if fixed_code != code:
                text = text.replace(b.group(0), b.group(0).replace(code, fixed_code))
                changed = True
                print(f"  {cid} block #{i+1}: removed quotes from labels")
        
        if changed:
            fp.write_text(text, encoding="utf-8")

# Re-approve
from bookmaker.authoring.pipeline import AuthoringPipeline
pipe = AuthoringPipeline(root)
for cid in ["bolum-14", "bolum-17"]:
    pipe.approve(cid)
    print(f"  {cid}: re-approved")

print("\n=== Done ===")
