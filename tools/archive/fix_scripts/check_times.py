"""Check if DOCX files have been updated by the current build."""
import datetime
from pathlib import Path

exports = Path("book_projects/java-temelleri/build/exports")
docx_files = sorted(exports.glob("[a-z]*.docx"))
new_docx = [f for f in docx_files if "_v001" not in f.name and f.stat().st_size > 30000]

for f in new_docx:
    dt = datetime.datetime.fromtimestamp(f.stat().st_mtime)
    print(f"{f.stem:30} {dt.strftime('%H:%M:%S')} {f.stat().st_size//1024:>4}KB")
