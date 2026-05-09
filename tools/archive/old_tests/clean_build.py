"""
Clean build: centralized mermaid_images + single pandoc pass.
1. Merge all approved chapters
2. Render ALL mermaid blocks to centralized mermaid_images/diagram_%03d.png
3. Single pandoc call
4. Clean up
"""
import subprocess, shutil, re, time
from pathlib import Path

def clean_build(project_root="book_projects/java-temelleri"):
    root = Path(project_root).resolve()
    build_dir = root / "build"
    merged_path = build_dir / ".merged_book.md"
    output_path = build_dir / "exports" / "java-programlamaya-giris.docx"
    mermaid_dir = build_dir / "mermaid_images"

    # === 1. MERGE ALL CHAPTERS ===
    print("1. Merging 27 chapters...")
    chapter_order = [f"bolum-{i:02d}" for i in range(1, 24)] + [f"ek-{c}" for c in "abcd"]
    combined, seen = [], []
    for cid in chapter_order:
        approved = sorted(root.glob(f"chapters/{cid}/approved/*.md"))
        if approved:
            combined.append(approved[0].read_text("utf-8"))
            seen.append(cid)
    merged = "\n\n\\newpage\n\n".join(combined)
    merged_path.parent.mkdir(parents=True, exist_ok=True)
    merged_path.write_text(merged, encoding="utf-8")
    print(f"   {len(seen)} chapters merged -> {merged_path.name}")

    # === 2. CENTRALIZED MERMAID RENDER ===
    print(f"\n2. Rendering mermaid blocks to {mermaid_dir.name}/...")
    if mermaid_dir.exists():
        shutil.rmtree(mermaid_dir)
    mermaid_dir.mkdir(parents=True)

    total_blocks = 0
    failed_blocks = 0
    global_idx = 0

    for cid in seen:
        approved = sorted(root.glob(f"chapters/{cid}/approved/*.md"))
        if not approved:
            continue
        text = approved[0].read_text("utf-8")
        blocks = list(re.finditer(r"```mermaid\s*\n(.*?)```", text, re.DOTALL))

        for i, b in enumerate(blocks):
            code = b.group(1).strip()
            if not code:
                continue

            global_idx += 1
            png = mermaid_dir / f"diagram_{global_idx:03d}.png"

            # Check if existing PNG from chapter directory
            existing = approved[0].parent / "mermaid_images" / f"diagram_{i+1:03d}.png"
            if existing.exists() and existing.stat().st_size > 1000:
                shutil.copy2(existing, png)
                total_blocks += 1
                print(f"   [{global_idx:3d}/{global_idx:3d}] {cid} blok#{i+1}: cached ({existing.stat().st_size//1024}KB)")
            else:
                # Render fresh
                mmd = mermaid_dir / f"_{global_idx:03d}.mmd"
                mmd.write_text(code, "utf-8")
                try:
                    proc = subprocess.run(
                        ["C:\\Program Files\\PowerShell\\7\\pwsh.exe", "-NoProfile", "-Command",
                         "mmdc", "-i", str(mmd), "-o", str(png), "-f", "-b", "white"],
                        capture_output=True, text=True, timeout=15,
                    )
                    ok = proc.returncode == 0 and png.exists()
                    if ok:
                        total_blocks += 1
                        size = png.stat().st_size // 1024
                        print(f"   [{global_idx:3d}/{global_idx:3d}] {cid} blok#{i+1}: rendered ({size}KB)")
                    else:
                        failed_blocks += 1
                        print(f"   [{global_idx:3d}/{global_idx:3d}] {cid} blok#{i+1}: FAILED")
                except:
                    failed_blocks += 1
                    print(f"   [{global_idx:3d}/{global_idx:3d}] {cid} blok#{i+1}: ERROR")
                finally:
                    if mmd.exists(): mmd.unlink()

    print(f"\n   Mermaid: {total_blocks} OK, {failed_blocks} FAILED")

    # === 3. SINGLE PANDOC BUILD ===
    print(f"\n3. Running pandoc (single pass)...")
    ref_doc = build_dir / "referenceV17_java_temelleri.docx"
    lua = build_dir / "styles_revised_v17.lua"

    cmd = ["pandoc",
           "-f", "markdown+tex_math_single_backslash",
           "-o", str(output_path),
           "--toc", "--toc-depth=2", "--metadata", "toc-title:Icindekiler",
           str(merged_path)]
    if ref_doc.exists():
        cmd.extend(["--reference-doc", str(ref_doc)])
    if lua.exists():
        cmd.extend(["--lua-filter", str(lua)])

    start = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=str(build_dir))
    elapsed = time.time() - start
    ok = proc.returncode == 0 and output_path.exists()
    size_kb = output_path.stat().st_size // 1024 if ok else 0

    print(f"   Pandoc: {'OK' if ok else 'FAILED'} ({elapsed:.1f}s)")
    print(f"   Output: {output_path.name} ({size_kb}KB)")

    # === 4. CLEANUP ===
    print(f"\n4. Cleaning up...")
    if merged_path.exists(): merged_path.unlink()
    # Remove scattered chapter mermaid dirs
    for md in root.glob("chapters/*/approved/mermaid_images"):
        shutil.rmtree(md)
    # Old v1 exports (keep only combined)
    for old in (build_dir / "exports").glob("bolum-*.docx"):
        old.unlink()
    for old in (build_dir / "exports").glob("ek-*.docx"):
        old.unlink()
    for old in (build_dir / "exports").glob("*_v001.docx"):
        old.unlink()

    print("   Temp files cleaned")
    print(f"\n{'='*50}")
    print(f"DONE! Final output:")
    print(f"  {output_path} ({size_kb}KB, {elapsed:.1f}s)")
    print(f"  Mermaid: {mermaid_dir} ({total_blocks} PNGs)")
    print(f"{'='*50}")

    return output_path, mermaid_dir, total_blocks

if __name__ == "__main__":
    clean_build()
