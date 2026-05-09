"""Quick check: latest DOCX sizes and mermaid PNGs."""
from pathlib import Path

root = Path("book_projects/java-temelleri")
exports = root / "build/exports"

print("=== Latest DOCX (with mermaid) ===")
# Get the most recent DOCX files
docx_files = sorted(exports.glob("[a-z]*.docx"))
new_docx = [f for f in docx_files if "_v001" not in f.name and f.stat().st_size > 30000]

for f in new_docx:
    modified = f.stat().st_mtime
    import datetime
    dt = datetime.datetime.fromtimestamp(modified).strftime("%H:%M:%S")
    print(f"  {f.stem:35} {f.stat().st_size//1024:>4}KB  [{dt}]")

print(f"\nTotal: {len(new_docx)} DOCX files")

# Check if bolum-14 and bolum-17 have mermaid images
for cid in ["bolum-14", "bolum-17"]:
    pngs = list(root.glob(f"chapters/{cid}/approved/mermaid_images/*.png"))
    print(f"\n{cid}: {len(pngs)} mermaid PNGs")
    for p in pngs:
        print(f"  {p.name} ({p.stat().st_size} bytes)")
