"""Check and fix bolum-14 block 2."""
import re
from pathlib import Path

text = Path("book_projects/java-temelleri/chapters/bolum-14/approved/bolum-14_v001.md").read_text("utf-8")
blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))

if len(blocks) >= 2:
    code = blocks[1].group(1).strip()
    print(f"Block 2 ({len(code)} chars):")
    print(code)
    print()
    print(f"Lines: {code.splitlines()}")
    
    # Fix: replace quotes in sequenceDiagram interactions
    # In sequenceDiagram, text after : can have quotes but they might break things
    # Actually, sequenceDiagram supports " in messages, so let's check the actual error
    import subprocess
    mmd = Path("test_b14_b2.mmd")
    png = Path("test_b14_b2.png")
    mmd.write_text(code, "utf-8")
    
    proc = subprocess.run(
        ["C:\\Program Files\\PowerShell\\7\\pwsh.exe", "-NoProfile", "-Command",
         "mmdc", "-i", str(mmd.resolve()), "-o", str(png.resolve()), "-f", "-b", "white"],
        capture_output=True, text=True, timeout=15,
    )
    print(f"\nmmdc result: {proc.returncode}")
    print(f"stderr: {proc.stderr[:500]}")
    if png.exists():
        print(f"PNG: {png.stat().st_size} bytes")
        png.unlink()
    mmd.unlink()
