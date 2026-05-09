"""Smart fix: close unclosed mermaid blocks by detecting non-mermaid lines."""
import re
from pathlib import Path

root = Path("book_projects/java-temelleri")

# Patterns that indicate non-mermaid content inside mermaid blocks
NON_MERMAID_PATTERNS = [
    r"^[A-Za-z0-9_-]+:",       # YAML-style fields (code_id:, chapter_id:)
    r"^id:",                    # id field
    r"^order:",                 # order field
    r"^<!--",                   # HTML comments
    r"^rev\|",                  # Revision markers
    r"^-->",                    # End of HTML comments
    r"^#",                      # Markdown headings
]

for fp in sorted(root.glob("chapters/*/draft_versions/v001.md")):
    cid = fp.parent.parent.name
    text = fp.read_text("utf-8")
    lines = text.splitlines()
    new_lines = []
    in_mermaid = False
    mermaid_code_lines = []
    closing_added = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if not in_mermaid and stripped.startswith("```mermaid"):
            in_mermaid = True
            new_lines.append(line)
            i += 1
            continue
        
        if in_mermaid:
            if stripped == "```":
                # Proper closing
                in_mermaid = False
                new_lines.append(line)
                i += 1
                continue
            
            # Check if this line doesn't look like mermaid
            is_non_mermaid = False
            for pattern in NON_MERMAID_PATTERNS:
                if re.match(pattern, stripped):
                    is_non_mermaid = True
                    break
            
            # Also check for CODE_META-like content  
            if re.match(r"^[a-z_]+:\s+\S", stripped) and not stripped.startswith(("participant", "note ", "rect", "loop", "alt", "opt", "par", "break", "critical")):
                is_non_mermaid = True
            
            if is_non_mermaid:
                # Close the mermaid block before this line
                new_lines.append("```")
                closing_added += 1
                in_mermaid = False
                # Don't consume this line, let it be processed normally
                continue
            
            mermaid_code_lines.append(line)
            new_lines.append(line)
        
        if not in_mermaid:
            new_lines.append(line)
        
        i += 1
    
    # If still in mermaid at end, close it
    if in_mermaid:
        new_lines.append("```")
        closing_added += 1
    
    result = "\n".join(new_lines)
    if result != text:
        fp.write_text(result, encoding="utf-8")
        if closing_added > 0:
            print(f"  {cid}: +{closing_added} closing ```")

# Re-approve and test
from bookmaker.authoring.pipeline import AuthoringPipeline
pipe = AuthoringPipeline(root)
for cid in ["bolum-14"]:
    pipe.approve(cid)
    print(f"  {cid}: re-approved")

# Test
import subprocess
text14 = Path("book_projects/java-temelleri/chapters/bolum-14/approved/bolum-14_v001.md").read_text("utf-8")
blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text14, re.DOTALL))
print(f"\nbolum-14: {len(blocks)} mermaid blocks after fix")

for i, b in enumerate(blocks):
    code = b.group(1).strip()
    if len(code) > 200:
        print(f"  Block #{i+1}: {len(code)} chars - TOO LONG")
        print(f"    First 100: {code[:100]}")
        print(f"    Last 100:  {code[-100:]}")
    else:
        # Test rendering
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
            print(f"    stderr: {proc.stderr[:200]}")

print("\n=== All done ===")
