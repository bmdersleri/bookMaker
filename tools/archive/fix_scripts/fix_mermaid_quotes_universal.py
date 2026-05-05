"""Fix ALL types of quotes in mermaid labels across all chapters."""
import re
from pathlib import Path

root = Path("book_projects/java-temelleri")

# All types of quotation marks
QUOTES = '\u201c\u201d\u2018\u2019\u0022'

for fp in sorted(root.glob("chapters/*/draft_versions/v001.md")):
    text = fp.read_text("utf-8")
    orig = text
    changed = False
    
    # In mermaid code blocks: replace any quote character inside [...] with '
    def fix_mermaid(match):
        code = match.group(1)
        # Replace quotes inside brackets
        # Pattern: [anything"anything] -> [anything'anything]
        fixed = re.sub(r'\[([^\]]*)[' + QUOTES + r']([^\]]*)\]', 
                      lambda m: '[' + m.group(1) + "'" + m.group(2) + ']', code)
        return match.group(0).replace(code, fixed)
    
    text = re.sub(r"```mermaid\s*\n(.*?)```", fix_mermaid, text, flags=re.DOTALL)
    
    if text != orig:
        fp.write_text(text, encoding="utf-8")
        print(f"  {fp.parent.parent.name}: fixed mermaid quotes")

# Re-approve bolum-17
from bookmaker.authoring.pipeline import AuthoringPipeline
pipe = AuthoringPipeline(root)
pipe.approve("bolum-17")

# Test block 1 rendering
import subprocess
ap17 = root / "chapters/bolum-17/approved/bolum-17_v001.md"
text17 = ap17.read_text("utf-8")
blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text17, re.DOTALL))
if blocks:
    code = blocks[0].group(1).strip()
    print(f"\nBlock 1 ({len(code)} chars):")
    print(code)
    
    mmd = Path("test_b17_b1.mmd")
    png = Path("test_b17_b1.png")
    mmd.write_text(code, "utf-8")
    
    proc = subprocess.run(
        ["C:\\Program Files\\PowerShell\\7\\pwsh.exe", "-NoProfile", "-Command",
         "mmdc", "-i", str(mmd.resolve()), "-o", str(png.resolve()), "-f", "-b", "white"],
        capture_output=True, text=True, timeout=15,
    )
    
    ok = proc.returncode == 0 and png.exists()
    if ok:
        print(f"\nRENDER PASS: {png.stat().st_size} bytes")
        # Copy to approved mermaid_images
        img_dir = ap17.parent / "mermaid_images"
        img_dir.mkdir(exist_ok=True)
        import shutil
        shutil.copy2(png, img_dir / "diagram_001.png")
        print(f"Copied to {img_dir / 'diagram_001.png'}")
    else:
        print(f"\nRENDER FAIL: {proc.stderr[:200]}")
    
    if png.exists(): png.unlink()
    if mmd.exists(): mmd.unlink()

# Final count
print(f"\nFinal: bolum-17 PNGs: {len(list((root/'chapters/bolum-17/approved/mermaid_images').glob('*.png')))}/2")
