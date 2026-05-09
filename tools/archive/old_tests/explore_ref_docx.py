"""Explore reference DOCX structure and batch file."""
import zipfile, os
from pathlib import Path

# 1. Check batch file
bat_path = "D:/bookMaker_Deepseek/book_projects/java-temelleri/build/donustur.bat"
bat_size = os.path.getsize(bat_path)
print(f"=== donustur.bat ({bat_size} bytes) ===")
if bat_size > 0:
    print(open(bat_path, encoding="utf-8").read())
else:
    print("(empty file)")
print()

# 2. Explore reference DOCX
ref_path = "D:/bookMaker_Deepseek/book_projects/java-temelleri/build/referenceV17_java_temelleri.docx"
print(f"=== referenceV17_java_temelleri.docx ===")
print(f"Size: {os.path.getsize(ref_path)} bytes")
print()

z = zipfile.ZipFile(ref_path)
print("All files in DOCX:")
for i in z.infolist():
    if not i.filename.endswith("/"):
        print(f"  {i.filename:60} {i.file_size:>8} bytes")

# 3. Extract and show key files
print("\n=== word/styles.xml (first 3000 chars) ===")
styles_text = z.read("word/styles.xml").decode("utf-8")
print(styles_text[:3000])

print("\n=== word/numbering.xml (first 1000 chars) ===")
num_text = z.read("word/numbering.xml").decode("utf-8")
print(num_text[:1000])

print("\n=== [Content_Types].xml (styles/lists) ===")
ct_text = z.read("[Content_Types].xml").decode("utf-8")
import re
for m in re.finditer(r'Override PartName="([^"]+)"', ct_text):
    print(f"  {m.group(1)}")
