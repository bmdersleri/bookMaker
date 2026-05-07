"""Pandoc + Mermaid ile Markdown → DOCX donusumu.
book_manifest.yaml -> BookConfig ile yapilandirilir:
  - Referans DOCX (referenceV17_java_temelleri.docx)
  - Lua filter (styles_revised_v17.lua)
  - Mermaid PNG yollari
  - TOC ayarlari
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from bookmaker.core.config import BookConfig, load_config


def pandoc_available() -> bool:
    """Pandoc CLI kullanilabilir mi?"""
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def _render_mermaid_blocks(
    markdown_path: Path,
    image_dir: Path,
    config: BookConfig | None = None,
    naming: str = "diagram_%03d.png",
) -> list[dict]:
    """Markdown'daki Mermaid bloklarini PNG'ye donusturur."""
    text = markdown_path.read_text(encoding="utf-8")
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
    blocks = list(pattern.finditer(text))
    results = []

    image_dir.mkdir(parents=True, exist_ok=True)

    for i, match in enumerate(blocks):
        code = match.group(1).strip()
        png_name = naming % (i + 1)
        png_path = image_dir / png_name
        mmd_path = image_dir / png_name.replace(".png", ".mmd")

        mmd_path.write_text(code, encoding="utf-8")

        # mmdc komutunu config'den al, yoksa varsayilan
        if config:
            mmdc_cmd = config.mermaid_mmdc_cmd
            bg = config.mermaid_background
            timeout_val = config.mermaid_timeout
        else:
            mmdc_cmd = [
                "C:\\Program Files\\PowerShell\\7\\pwsh.exe",
                "-NoProfile", "-Command", "mmdc",
            ]
            bg = "white"
            timeout_val = 30

        mmdc_cmd_full = mmdc_cmd + [
            "-i", str(mmd_path), "-o", str(png_path),
            "-f", "-b", bg,
        ]

        try:
            proc = subprocess.run(
                mmdc_cmd_full,
                capture_output=True, text=True, timeout=timeout_val,
            )
            success = proc.returncode == 0 and png_path.exists()
            results.append({
                "index": i,
                "status": "passed" if success else "failed",
                "path": str(png_path) if success else None,
                "error": proc.stderr if not success else "",
            })
        except Exception as e:
            results.append({"index": i, "status": "error", "error": str(e)})
        finally:
            if mmd_path.exists():
                mmd_path.unlink()

    return results


def export_docx(
    markdown_path: Path,
    output_path: Path,
    reference_doc: Path | None = None,
    lua_filter: Path | None = None,
    toc: bool | None = None,
    toc_depth: int | None = None,
    toc_title: str | None = None,
    render_mermaid: bool = True,
    config: BookConfig | None = None,
) -> dict:
    """Markdown dosyasini Pandoc ile DOCX'e donusturur.

    Config parametresi verilirse referans_doc, lua_filter, toc, mermaid
    ayarlari config'den alinir. Ayri ayrı parametreler config'i ezer.

    Args:
        markdown_path: Giris .md dosyasi
        output_path: Cikis .docx dosyasi
        reference_doc: Referans DOCX (None = config'den)
        lua_filter: Lua filter (None = config'den)
        toc: Icindekiler tablosu (None = config'den)
        toc_depth: TOC derinligi (None = config'den)
        toc_title: TOC basligi (None = config'den)
        render_mermaid: Mermaid bloklarini PNG'ye cevir
        config: Kitap config (None = otomatik bul)

    Returns:
        {'status': 'passed'|'failed'|'timeout'|'error',
         'output': str, 'error': str, 'path': str|None,
         'size': int, 'mermaid_results': list}
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Config otomatik bul (verilmemisse)
    if config is None:
        try:
            config = load_config(start=markdown_path.parent)
        except Exception:
            config = None

    # Referans dosyalari: once parametre, sonra config
    if reference_doc is None and config:
        reference_doc = config.reference_docx_path
    if lua_filter is None and config:
        lua_filter = config.lua_filter_path

    # TOC ayarlari: once parametre, sonra config, sonra varsayilan
    if toc is None:
        toc = config.toc_enabled if config else True
    if toc_depth is None:
        toc_depth = config.toc_depth if config else 2
    if toc_title is None:
        toc_title = config.toc_title if config else "Icindekiler"

    # Mermaid goruntuleri
    mermaid_image_dir = markdown_path.parent / "mermaid_images"
    mermaid_results = []
    if render_mermaid:
        mermaid_results = _render_mermaid_blocks(
            markdown_path, mermaid_image_dir, config=config,
        )
        passed = sum(1 for r in mermaid_results if r["status"] == "passed")
        if passed > 0:
            print(f"    Mermaid: {passed}/{len(mermaid_results)} PNG render edildi")

    # Pandoc'u markdown dizininde calistir (goreceli yollarla)
    cwd = markdown_path.parent.resolve()
    md_name = markdown_path.name

    cmd = ["pandoc", "-f", "markdown+tex_math_single_backslash",
           "-o", str(output_path), md_name]

    if reference_doc and reference_doc.exists():
        cmd.extend(["--reference-doc", str(reference_doc.resolve())])
        print(f"    Referans DOCX: {reference_doc.name}")

    if lua_filter and lua_filter.exists():
        cmd.extend(["--lua-filter", str(lua_filter.resolve())])
        print(f"    Lua filter:    {lua_filter.name}")

    if toc:
        cmd.append("--toc")
        cmd.extend(["--toc-depth", str(toc_depth)])
        cmd.extend(["--metadata", f"toc-title:{toc_title}"])

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120, cwd=str(cwd),
        )
        success = proc.returncode == 0 and output_path.exists()
        size = output_path.stat().st_size if success else 0
        return {
            "status": "passed" if success else "failed",
            "output": proc.stdout,
            "error": proc.stderr,
            "path": str(output_path) if success else None,
            "size": size,
            "mermaid_results": mermaid_results,
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "output": "", "error": "Pandoc timed out (120s)",
                "path": None, "size": 0, "mermaid_results": mermaid_results}
    except FileNotFoundError:
        return {"status": "error", "output": "", "error": "pandoc not found in PATH",
                "path": None, "size": 0, "mermaid_results": mermaid_results}
    except Exception as e:
        return {"status": "error", "output": "", "error": str(e),
                "path": None, "size": 0, "mermaid_results": mermaid_results}


def export_all_chapters(
    project_root: Path | None = None,
    output_dir: Path | None = None,
    config: BookConfig | None = None,
) -> dict[str, dict]:
    """Projedeki tum onaylanmis bolumleri DOCX'e donusturur."""
    if config is None:
        if project_root:
            config = BookConfig(project_root)
        else:
            config = load_config(book_name="java-temelleri")

    output_dir = output_dir or config.exports_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    chapter_ids = config.chapter_order_approved()

    print(f"\nToplu DOCX uretimi: {len(chapter_ids)} bolum\n")

    for cid in chapter_ids:
        md = config.chapter_path(cid)
        if not md:
            print(f"  SKIP {cid}: dosya bulunamadi")
            continue

        out = output_dir / f"{cid}.docx"

        import time
        start = time.time()
        result = export_docx(md, out, config=config)
        elapsed = time.time() - start

        if result["status"] == "passed":
            kb = result["size"] / 1024
            mermaid_ok = sum(1 for r in result.get("mermaid_results", [])
                             if r["status"] == "passed")
            mermaid_total = len(result.get("mermaid_results", []))
            mermaid_str = f", mermaid {mermaid_ok}/{mermaid_total}" if mermaid_total > 0 else ""
            print(f"  OK {cid}: {kb:.0f}KB ({elapsed:.1f}s){mermaid_str}")
        else:
            print(f"  FAIL {cid}: {result.get('error', '')[:80]}")

        results[cid] = result

    print(f"\nToplam: {len(chapter_ids)} bolum islendi.")
    return results
