"""Fix ALL unclosed mermaid blocks and special characters in labels."""
import re
from pathlib import Path

root = Path("book_projects/java-temelleri")

# Check ALL chapters for: unclosed mermaid blocks, quotes in labels
for fp in sorted(root.glob("chapters/*/draft_versions/v001.md")):
    cid = fp.parent.parent.name
    text = fp.read_text("utf-8")
    orig = text
    changed = False
    
    # Find ALL mermaid blocks
    # The problem is that `(.*?)``` is lazy but the closing ``` might be far away
    # Let's manually find mermaid blocks by tracking fence states
    
    lines = text.splitlines()
    in_mermaid = False
    mermaid_start = -1
    mermaid_content = []
    closing_added = 0
    label_quotes_fixed = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if not in_mermaid and stripped.startswith("```mermaid"):
            in_mermaid = True
            mermaid_start = i
            mermaid_content = []
            i += 1
            continue
        
        if in_mermaid:
            if stripped == "```":
                # Proper closing
                in_mermaid = False
                i += 1
                continue
            
            mermaid_content.append(line)
            
            # Check if this line looks like non-mermaid content (CODE_META, MERMAID_META, headings)
            if stripped.startswith("<!--") or stripped.startswith("#"):
                # This shouldn't be in a mermaid block - the ``` was never closed
                # Fix: add closing ``` BEFORE this line
                lines.insert(i, "```")
                closing_added += 1
                in_mermaid = False
                i += 1  # Skip the inserted ```
                continue
            
            # Fix quotes inside brackets [text with "quotes"]
            if "[" in stripped and '"' in stripped:
                # Replace " inside [...] with '
                new_line = re.sub(r'\[([^\]]*)"([^\]]*)\]', lambda m: '[' + m.group(1) + "'" + m.group(2) + ']', line)
                if new_line != line:
                    lines[i] = new_line
                    label_quotes_fixed += 1
            
            # Also handle Unicode quotes
            if "[" in line and ('\u201c' in line or '\u201d' in line or '\u2018' in line or '\u2019' in line):
                new_line = line.replace('\u201c', "'").replace('\u201d', "'").replace('\u2018', "'").replace('\u2019', "'")
                lines[i] = new_line
                if not label_quotes_fixed:
                    label_quotes_fixed += 1  # approximate
        
        i += 1
    
    # If still in mermaid at end of file, close it
    if in_mermaid:
        lines.append("```")
        closing_added += 1
    
    text = "\n".join(lines)
    
    if text != orig:
        fp.write_text(text, encoding="utf-8")
        changed = True
    
    if closing_added > 0 or label_quotes_fixed > 0:
        print(f"  {cid}: +{closing_added} closing ```, {label_quotes_fixed} quote fixes")

# Re-approve all
print("\n=== Re-approving ===")
from bookmaker.authoring.pipeline import AuthoringPipeline
pipe = AuthoringPipeline(root)
for cd in sorted(root.glob("chapters/*/")):
    cid = cd.name
    if cid in ["bolum_01", "test-ch"]:
        continue
    dp = cd / "draft_versions/v001.md"
    if not dp.exists():
        continue
    pipe.approve(cid)
    print(f"  {cid}: approved")

print("\n=== Test fixed blocks ===")
# Test the previously problematic blocks
import subprocess, os

def test_mermaid(code, label):
    mmd = Path(f"test_{label}.mmd")
    png = Path(f"test_{label}.png")
    mmd.write_text(code, "utf-8")
    
    proc = subprocess.run(
        ["C:\\Program Files\\PowerShell\\7\\pwsh.exe", "-NoProfile", "-Command",
         "mmdc", "-i", str(mmd.resolve()), "-o", str(png.resolve()), "-f", "-b", "white"],
        capture_output=True, text=True, timeout=15,
    )
    ok = proc.returncode == 0 and png.exists()
    if png.exists(): png.unlink()
    if mmd.exists(): mmd.unlink()
    return ok

# Check problematic chapters
for cid in ["bolum-14", "bolum-17"]:
    ap = root / "chapters" / cid / "approved" / f"{cid}_v001.md"
    text = ap.read_text("utf-8")
    
    blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))
    print(f"\n{cid}: {len(blocks)} mermaid blocks")
    
    for i, b in enumerate(blocks):
        code = b.group(1).strip()
        if len(code) > 500:
            print(f"  Block #{i+1}: {len(code)} chars - TOO LONG, failed")
            print(f"    First 100: {code[:100]}")
        else:
            ok = test_mermaid(code, f"{cid}_b{i+1}")
            print(f"  Block #{i+1}: {len(code)} chars - {'PASS' if ok else 'FAIL'}")
