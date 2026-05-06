"""Targeted fix: close mermaid block before non-mermaid fragment lines."""
import re
from pathlib import Path

root = Path("book_projects/java-temelleri")

# Direct fix: in bolum-14 approved file, find the 2nd mermaid block
# and close it properly before the fragment line
ap14 = root / "chapters/bolum-14/approved/bolum-14_v001.md"
text = ap14.read_text("utf-8")

# Find ALL ```mermaid blocks and close them before non-mermaid fragments
# Strategy: find ```mermaid, then look for lines that contain "_kod" or YAML-like content
# These are fragments from CODE_META blocks that got mixed in

def fix_mermaid_closing(text):
    lines = text.splitlines()
    new_lines = []
    in_mermaid = False
    mermaid_start = -1
    
    # Non-mermaid content indicators
    bad_fragments = [
        r"_kod\d+",       # code_id fragments: bolum-14_kod03
        r"^[a-z_]+:",     # YAML fields: code_id:, chapter_id:
        r"^<!--",         # HTML comments
        r"^-->",          # End of comments
        r"^#",            # Markdown headings
    ]
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if not in_mermaid and stripped.startswith("```mermaid"):
            in_mermaid = True
            mermaid_start = i
            new_lines.append(line)
            continue
        
        if in_mermaid:
            if stripped == "```":
                in_mermaid = False
                new_lines.append(line)
                continue
            
            # Check if this line contains non-mermaid fragments
            is_bad = False
            for pat in bad_fragments:
                if re.search(pat, stripped):
                    is_bad = True
                    break
            
            if is_bad:
                # Close mermaid block before this line
                new_lines.append("```")
                new_lines.append(line)
                in_mermaid = False
                continue
        
        new_lines.append(line)
    
    return "\n".join(new_lines)

fixed = fix_mermaid_closing(text)
if fixed != text:
    ap14.write_text(fixed, encoding="utf-8")
    print("Fixed bolum-14 approved: closed mermaid blocks before fragments")
else:
    print("bolum-14: no changes needed")

# Also fix draft
dp14 = root / "chapters/bolum-14/draft_versions/v001.md"
fixed2 = fix_mermaid_closing(dp14.read_text("utf-8"))
if fixed2 != dp14.read_text("utf-8"):
    dp14.write_text(fixed2, encoding="utf-8")
    print("Fixed bolum-14 draft: closed mermaid blocks before fragments")

# Re-approve and test
from bookmaker.authoring.pipeline import AuthoringPipeline
pipe = AuthoringPipeline(root)
pipe.approve("bolum-14")
print("bolum-14 re-approved")

# Test all mermaid blocks
import subprocess
text14 = ap14.read_text("utf-8")
blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text14, re.DOTALL))
print(f"\nbolum-14: {len(blocks)} blocks after fix")

for i, b in enumerate(blocks):
    code = b.group(1).strip()
    if len(code) > 200:
        print(f"  Block #{i+1}: {len(code)} chars - TOO LONG")
        print(f"    Content: {code[:150]}")
    else:
        mmd = Path(f"test_b14_b{i+1}.mmd")
        png = Path(f"test_b14_b{i+1}.png")
        mmd.write_text(code, "utf-8")
        proc = subprocess.run(
            ["C:\\Program Files\\PowerShell\\7\\pwsh.exe", "-NoProfile", "-Command",
             "mmdc", "-i", str(mmd.resolve()), "-o", str(png.resolve()), "-f", "-b", "white"],
            capture_output=True, text=True, timeout=15,
        )
        ok = proc.returncode == 0 and png.exists()
        if png.exists(): png.unlink()
        if mmd.exists(): mmd.unlink()
        print(f"  Block #{i+1}: {len(code)} chars - {'PASS' if ok else 'FAIL'}")
        if not ok:
            print(f"    Code: {repr(code[:150])}")
            print(f"    Error: {proc.stderr[:200]}")
