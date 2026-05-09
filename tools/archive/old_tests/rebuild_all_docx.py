"""Compare old vs new DOCX output and test the reference template."""
from pathlib import Path

new_p = Path("build/exports/bolum-01_v001.docx")
old_p = Path("book_projects/java-temelleri/build/exports/bolum-01_v001.docx")

if new_p.exists():
    print(f"New (with ref template): {new_p.stat().st_size} bytes")
if old_p.exists():
    print(f"Old (without template):  {old_p.stat().st_size} bytes")
if new_p.exists() and old_p.exists():
    diff = new_p.stat().st_size - old_p.stat().st_size
    print(f"Difference: {diff:+d} bytes ({diff/1024:+.1f}KB)")

# Now rebuild ALL chapters with the new pipeline
import subprocess, sys, time
from bookmaker.production.pandoc import export_all_chapters

root = Path("book_projects/java-temelleri")
out_dir = root / "build" / "exports"

print(f"\n{'='*60}")
print("Toplu DOCX uretimi (Lua filter + Reference template)")
print(f"{'='*60}")

results = export_all_chapters(root, out_dir)

ok = sum(1 for r in results.values() if r["status"] == "passed")
fail = sum(1 for r in results.values() if r["status"] != "passed")
total_size = sum(r["size"] for r in results.values() if r["status"] == "passed")

print(f"\n{'='*60}")
print(f"SONUC: {ok} basarili, {fail} basarisiz")
print(f"Toplam boyut: {total_size/1024:.0f}KB")
if ok:
    print(f"Ortalama: {total_size//1024//ok}KB/bolum")
print(f"{'='*60}")
