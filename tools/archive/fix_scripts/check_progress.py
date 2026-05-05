"""Check DOCX build progress."""
from pathlib import Path

exports = Path("book_projects/java-temelleri/build/exports")
new_files = sorted(exports.glob("[a-z]*.docx"))  # bolum-*.docx, ek-*.docx - without _v001
old_files = sorted(exports.glob("*_v001.docx"))

print(f"New files (with reference template):")
for f in new_files:
    if f.stat().st_size > 10000:
        print(f"  {f.stem:30} {f.stat().st_size/1024:>6.0f}KB")

print(f"\nOld files (without template): {len(old_files)} files")

# Count how many new files we have
total_expected = 27  # 23 bolum + 4 ek
done = len(new_files)
print(f"\nProgress: {done}/{total_expected}")
if done < total_expected:
    remaining = total_expected - done
    print(f"Remaining: {remaining}")
