"""Count mermaid PNGs per chapter."""
from pathlib import Path

root = Path("book_projects/java-temelleri")

for ch in sorted(root.glob("chapters/bolum-*")):
    pngs = list(ch.glob("approved/mermaid_images/diagram_*.png"))
    if pngs:
        print(f"{ch.name}: {len(pngs)} PNGs {' '.join(f'{p.stat().st_size//1024}KB' for p in pngs)}")

for ch in sorted(root.glob("chapters/ek-*")):
    pngs = list(ch.glob("approved/mermaid_images/diagram_*.png"))
    if pngs:
        print(f"{ch.name}: {len(pngs)} PNGs {' '.join(f'{p.stat().st_size//1024}KB' for p in pngs)}")

total = sorted(root.glob("chapters/*/approved/mermaid_images/*.png"))
print(f"\nTotal: {len(total)} mermaid PNGs")
