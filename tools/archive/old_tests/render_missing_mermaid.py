"""Test and render bolum-14 and bolum-17 missing mermaid blocks."""
import re, subprocess
from pathlib import Path

root = Path("book_projects/java-temelleri")

for cid in ["bolum-14", "bolum-17"]:
    ap = root / "chapters" / cid / "approved" / f"{cid}_v001.md"
    text = ap.read_text("utf-8")
    blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))
    img_dir = ap.parent / "mermaid_images"
    img_dir.mkdir(parents=True, exist_ok=True)
    
    for i, b in enumerate(blocks):
        code = b.group(1).strip()
        png = img_dir / f"diagram_{i+1:03d}.png"
        
        if png.exists():
            print(f"  {cid} block #{i+1}: already exists ({png.stat().st_size} bytes)")
            continue
        
        if len(code) > 200:
            print(f"  {cid} block #{i+1}: {len(code)} chars - TOO LONG, skipping")
            print(f"    First 80: {code[:80]}")
            continue
        
        mmd = png.with_suffix(".mmd")
        mmd.write_text(code, "utf-8")
        
        proc = subprocess.run(
            ["C:\\Program Files\\PowerShell\\7\\pwsh.exe", "-NoProfile", "-Command",
             "mmdc", "-i", str(mmd.resolve()), "-o", str(png.resolve()), "-f", "-b", "white"],
            capture_output=True, text=True, timeout=15,
        )
        
        if mmd.exists(): mmd.unlink()
        
        if proc.returncode == 0 and png.exists():
            print(f"  {cid} block #{i+1}: {png.stat().st_size} bytes - OK")
        else:
            print(f"  {cid} block #{i+1}: FAILED - {proc.stderr[:100]}")

print("\nDone. Final count:")
print(f"  bolum-14: {len(list((root/'chapters/bolum-14/approved/mermaid_images').glob('*.png')))} PNGs")
print(f"  bolum-17: {len(list((root/'chapters/bolum-17/approved/mermaid_images').glob('*.png')))} PNGs")
