"""
Debug pandoc with fresh merged file + centralized mermaid.
"""
import subprocess
from pathlib import Path

root = Path("book_projects/java-temelleri").resolve()
build_dir = root / "build"

# 1. Re-create merged file
chapter_order = [f"bolum-{i:02d}" for i in range(1, 24)] + [f"ek-{c}" for c in "abcd"]
combined = []
for cid in chapter_order:
    a = sorted(root.glob(f"chapters/{cid}/approved/*.md"))
    if a:
        combined.append(a[0].read_text("utf-8"))

merged_text = "\n\n\\newpage\n\n".join(combined)
merged_path = build_dir / ".merged_book.md"
merged_path.write_text(merged_text, encoding="utf-8")
print(f"Merged file: {merged_path} ({merged_path.stat().st_size//1024}KB, {len(combined)} chapters)")

# 2. Check mermaid
mermaid_dir = build_dir / "mermaid_images"
print(f"Mermaid: {len(list(mermaid_dir.glob('*.png')))} PNGs")
print(f"  diagram_001.png: {(mermaid_dir/'diagram_001.png').exists()}")
print(f"  diagram_055.png: {(mermaid_dir/'diagram_055.png').exists()}")

# 3. Run pandoc
output = build_dir / "exports" / "java-programlamaya-giris.docx"
output.parent.mkdir(parents=True, exist_ok=True)
ref_doc = build_dir / "referenceV17_java_temelleri.docx"
lua = build_dir / "styles_revised_v17.lua"

cmd = ["pandoc",
    "-f", "markdown+tex_math_single_backslash",
    "-o", str(output),
    "--toc", "--toc-depth=2", "--metadata", "toc-title:Icindekiler",
    str(merged_path)]
if ref_doc.exists():
    cmd.extend(["--reference-doc", str(ref_doc)])
if lua.exists():
    cmd.extend(["--lua-filter", str(lua)])

print(f"\nPandoc CWD: {build_dir}")
proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(build_dir))

print(f"\nExit code: {proc.returncode}")
print(f"STDOUT ({len(proc.stdout)} chars):")
print(proc.stdout[:1000] if proc.stdout else "(empty)")
print(f"\nSTDERR ({len(proc.stderr)} chars):")
print(proc.stderr[:2000] if proc.stderr else "(empty)")

ok = proc.returncode == 0 and output.exists() and output.stat().st_size > 0
print(f"\nOutput: {output}")
print(f"Size: {output.stat().st_size} bytes ({output.stat().st_size//1024}KB)")
print(f"Status: {'OK' if ok else 'FAILED'}")
