from pathlib import Path
r = Path("book_projects/java-temelleri")
print("Mermaid PNG dosyalari:")
for d in sorted(r.glob("chapters/*/approved/mermaid_images")):
    cid = d.parent.parent.name
    pngs = sorted(d.glob("*.png"))
    if pngs:
        sizes = [f"{p.stat().st_size//1024}KB" for p in pngs]
        print(f"  {cid}: {len(pngs)} PNG {' '.join(sizes)}")
    else:
        print(f"  {cid}: (bos)")
total = list(r.glob("chapters/*/approved/mermaid_images/*.png"))
print(f"\nToplam: {len(total)} PNG dosyasi")
