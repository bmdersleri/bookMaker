from pathlib import Path

r = Path("book_projects/java-temelleri/build")
exports = list(r.glob("exports/*"))
mermaid = list(r.glob("mermaid_images/*.png"))

print("=== build/ icerigi ===")
for f in sorted(r.iterdir()):
    if f.is_dir():
        size = sum(fi.stat().st_size for fi in f.rglob("*") if fi.is_file())
        print(f"  {f.name}/ ({len(list(f.iterdir()))} items, {size//1024}KB)")
    else:
        kb = f.stat().st_size // 1024 if f.stat().st_size > 0 else 0
        print(f"  {f.name} ({kb}KB)")

print(f"\n=== exports/ ({len(exports)} dosya) ===")
for e in exports:
    kb = e.stat().st_size // 1024
    print(f"  {e.name} ({kb}KB)")

print(f"\n=== mermaid_images/ ({len(mermaid)} PNG) ===")
for m in mermaid:
    kb = m.stat().st_size // 1024
    print(f"  {m.name} ({kb}KB)")
