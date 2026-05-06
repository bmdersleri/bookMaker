"""Check mermaid PNG files and DOCX sizes."""
from pathlib import Path

root = Path("book_projects/java-temelleri")

print("=== MERMAID PNG FILES ===")
pngs = sorted(root.glob("chapters/*/approved/mermaid_images/*.png"))
if pngs:
    print(f"Found {len(pngs)} mermaid PNGs:")
    for p in pngs:
        rel = p.relative_to(root)
        print(f"  {rel} ({p.stat().st_size} bytes)")
else:
    print("(none found)")
    # Check if any mermaid_images dirs exist
    dirs = list(root.glob("chapters/*/approved/mermaid_images"))
    if dirs:
        print(f"\nEmpty dirs found: {len(dirs)}")
    else:
        print("No mermaid_images directories found at all")

print("\n=== DOCX EXPORTS ===")
exports = sorted((root / "build/exports").glob("*.docx"))
print(f"Total: {len(exports)} DOCX files")
for e in exports:
    if e.stat().st_size > 10000:
        kb = e.stat().st_size / 1024
        print(f"  {e.stem:35} {kb:>6.0f}KB")
