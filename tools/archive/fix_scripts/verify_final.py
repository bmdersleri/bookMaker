"""Verify final DOCX with mermaid - compare sizes."""
import datetime
from pathlib import Path

exports = Path("book_projects/java-temelleri/build/exports")
docx_files = sorted(exports.glob("[a-z]*.docx"))
new_docx = [f for f in docx_files if "_v001" not in f.name and f.stat().st_size > 30000]

print("=== Final DOCX Reports with Mermaid ===")
total = 0
for f in new_docx:
    dt = datetime.datetime.fromtimestamp(f.stat().st_mtime)
    kb = f.stat().st_size // 1024
    total += kb
    print(f"  {f.stem:30} {kb:>4}KB  [{dt.strftime('%H:%M:%S')}]")

print(f"\nTotal: {len(new_docx)} chapters, {total}KB, avg {total//len(new_docx)}KB/chapter")

# Check mermaid_ok count
mermaid_chapters = 0
for ch in sorted(Path("book_projects/java-temelleri/chapters").glob("*")):
    pngs = list(ch.glob("approved/mermaid_images/*.png"))
    if pngs:
        mermaid_chapters += 1

print(f"Mermaid chapters: {mermaid_chapters}/16")
