"""Export servisi — kitap birleştirme, format dönüşümü, yedekleme, Mermaid PNG."""

from __future__ import annotations

import re
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

from bookmaker.manifest.manager import ManifestManager


def assemble_book(project_root: str | Path,
                  chapter_ids: list[str] | None = None) -> dict:
    """Tüm bölüm markdown'larını birleştirip kitap.md olarak kaydeder."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    targets = []
    for ch in manifest.chapters:
        if chapter_ids and ch.chapter_id not in chapter_ids:
            continue
        src = ch.source
        p = root / src if src else None
        if p and p.exists():
            targets.append((ch.order, ch.chapter_id, ch.title or ch.chapter_id, p))

    targets.sort(key=lambda x: x[0])

    out_dir = root / "build"
    out_dir.mkdir(parents=True, exist_ok=True)

    toc_lines = ["# İçindekiler\n"]
    body_parts = []

    for order, cid, title, path in targets:
        text = path.read_text(encoding="utf-8")
        toc_lines.append(f"{order}. [{title}](#{cid})")
        body_parts.append(f"\n\n---\n\n{text}")

    full_text = "\n".join(toc_lines) + "\n\n---\n\n" + "\n".join(body_parts).lstrip("\n")
    out_path = out_dir / "kitap_birlestirilmis.md"
    out_path.write_text(full_text, encoding="utf-8")

    return {
        "path": str(out_path.relative_to(root)),
        "words": len(full_text.split()),
        "chars": len(full_text),
        "chapters": len(targets),
        "output": full_text[:500],
    }


def export_to_format(project_root: str | Path, fmt: str,
                     chapter_ids: list[str] | None = None) -> dict:
    """Birleştirilmiş kitabı hedef formata dönüştürür.

    fmt: "docx", "pdf", "epub", "html"
    """
    root = Path(project_root).resolve()

    # Önce birleştir
    assembled = assemble_book(root, chapter_ids)
    if "error" in assembled:
        return assembled

    md_path = root / assembled["path"]
    out_dir = root / "build" / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)

    fmt_map = {
        "docx": ("docx", ".docx"),
        "pdf": ("pdf", ".pdf"),
        "epub": ("epub", ".epub"),
        "html": ("html", ".html"),
    }

    if fmt not in fmt_map:
        return {"error": f"Desteklenmeyen format: {fmt}. docx/pdf/epub/html desteklenir."}

    pandoc_fmt, ext = fmt_map[fmt]
    out_path = out_dir / f"kitap{ext}"

    cmd = [
        "pandoc", str(md_path),
        "-f", "markdown+tex_math_single_backslash",
        "-t", pandoc_fmt,
        "-o", str(out_path),
        "--toc", "--toc-depth=2",
    ]

    # DOCX için referans şablon
    ref_docx = root / "build" / "referenceV17_java_temelleri.docx"
    if fmt == "docx" and ref_docx.exists():
        cmd.extend(["--reference-doc", str(ref_docx)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return {"error": f"Pandoc hatasi: {result.stderr[:300]}",
                    "command": " ".join(cmd)}

        return {
            "format": fmt,
            "path": str(out_path.relative_to(root)),
            "size_bytes": out_path.stat().st_size,
            "cmd": " ".join(cmd),
        }
    except FileNotFoundError:
        return {"error": "pandoc bulunamadi. Pandoc kurulu oldugundan emin olun."}
    except subprocess.TimeoutExpired:
        return {"error": "Pandoc zamani asimi (120s)."}


def render_mermaid(project_root: str | Path,
                   chapter_id: str | None = None) -> dict:
    """Mermaid şemalarını PNG'e dönüştürür.

    mmdc CLI kullanir: https://github.com/mermaid-js/mermaid-cli
    """
    root = Path(project_root).resolve()

    if chapter_id:
        chapters_to_scan = [chapter_id]
    else:
        mgr = ManifestManager(root)
        manifest = mgr.load_or_generate()
        chapters_to_scan = [ch.chapter_id for ch in manifest.chapters]

    out_dir = root / "build" / "mermaid_images"
    out_dir.mkdir(parents=True, exist_ok=True)

    rendered = 0
    errors = []
    images: list[str] = []

    for cid in chapters_to_scan:
        # Bölüm metnini bul
        for path_candidate in [
            root / "chapters" / cid / "approved",
        ]:
            if not path_candidate.exists():
                continue
            for f in sorted(path_candidate.glob("*.md")):
                text = f.read_text(encoding="utf-8")
                blocks = re.findall(r'```mermaid\n(.*?)```', text, re.DOTALL)
                for i, block in enumerate(blocks):
                    mmd_path = out_dir / f"{cid}_diagram_{i+1:03d}.mmd"
                    mmd_path.write_text(block.strip(), encoding="utf-8")

                    png_path = mmd_path.with_suffix(".png")
                    try:
                        proc = subprocess.run(
                            ["mmdc", "-i", str(mmd_path), "-o", str(png_path),
                             "-b", "white"],
                            capture_output=True, text=True, timeout=30)
                        if proc.returncode == 0:
                            rendered += 1
                            images.append(str(png_path.relative_to(root)))
                        else:
                            errors.append(f"{cid}:{i+1} -> {proc.stderr[:100]}")
                    except FileNotFoundError:
                        errors.append("mmdc bulunamadi. npm install -g @mermaid-js/mermaid-cli")
                        break
                    except subprocess.TimeoutExpired:
                        errors.append(f"{cid}:{i+1} -> Timeout")
                    except Exception as e:
                        errors.append(f"{cid}:{i+1} -> {str(e)[:50]}")
                break  # sadece ilk dosyayı tara
            break

    result = {
        "rendered": rendered,
        "output_dir": str(out_dir.relative_to(root)),
        "images": images[:20],  # ilk 20 PNG yolu
    }
    if errors:
        result["errors"] = errors[:5]
    return result


def extract_code(project_root: str | Path,
                 chapter_id: str | None = None) -> dict:
    """Tüm veya tek bölümden Java kod bloklarını ayıklar."""
    root = Path(project_root).resolve()

    if chapter_id:
        chapters_to_extract = [chapter_id]
    else:
        mgr = ManifestManager(root)
        manifest = mgr.load_or_generate()
        chapters_to_extract = [ch.chapter_id for ch in manifest.chapters]

    out_dir = root / "build" / "code"
    total_extracted = 0
    results = []

    for cid in chapters_to_extract:
        for path_candidate in [root / "chapters" / cid / "approved"]:
            if not path_candidate.exists():
                results.append({"chapter_id": cid, "extracted": 0,
                                "error": "Klasor yok"})
                break
            for f in sorted(path_candidate.glob("*.md")):
                text = f.read_text(encoding="utf-8")
                blocks = re.findall(r'```java\n(.*?)```', text, re.DOTALL)

                ch_dir = out_dir / cid
                ch_dir.mkdir(parents=True, exist_ok=True)
                ch_extracted = 0

                for i, block in enumerate(blocks):
                    first_line = block.strip().splitlines()[0] if block.strip() else ""
                    class_match = re.search(r'class\s+(\w+)', first_line)
                    base_name = class_match.group(1) if class_match else f"block_{i+1:03d}"
                    fname = f"{base_name}.java"
                    fpath = ch_dir / fname

                    idx = 1
                    while fpath.exists():
                        fname = f"{base_name}_{idx:03d}.java"
                        fpath = ch_dir / fname
                        idx += 1

                    fpath.write_text(block, encoding="utf-8")
                    ch_extracted += 1
                    total_extracted += 1

                results.append({"chapter_id": cid, "extracted": ch_extracted})
                break
            break

    return {
        "total_extracted": total_extracted,
        "output_dir": str(out_dir.relative_to(root)),
        "details": results,
    }


def create_backup(project_root: str | Path) -> dict:
    """Projenin .zip yedeğini oluşturur."""
    root = Path(project_root).resolve()
    backup_dir = root / "build" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{root.name}_{timestamp}.zip"
    zip_path = backup_dir / zip_name

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for item in root.rglob("*"):
                # build/backups ve build/.pytest_cache'ı hariç tut
                rel = item.relative_to(root)
                parts = rel.parts
                if len(parts) > 1 and parts[0] == "build":
                    if parts[1] in ("backups", ".pytest_cache", "__pycache__",
                                    ".ruff_cache", ".continue"):
                        continue
                if item.is_file():
                    zf.write(item, rel)

        size_mb = zip_path.stat().st_size / (1024 * 1024)
        return {
            "path": str(zip_path.relative_to(root)),
            "size_mb": round(size_mb, 1),
            "files": len(zipfile.ZipFile(zip_path).namelist()),
        }
    except Exception as e:
        return {"error": f"Yedekleme hatasi: {str(e)[:200]}"}


def restore_backup(project_root: str | Path, zip_path_str: str) -> dict:
    """Yedek dosyasından projeyi geri yükler."""
    root = Path(project_root).resolve()
    zip_path = Path(zip_path_str)

    if not zip_path.is_absolute():
        zip_path = root / zip_path_str

    if not zip_path.exists():
        return {"error": f"Dosya bulunamadi: {zip_path}"}

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(root)
        return {"restored": True, "files": len(zf.namelist())}
    except Exception as e:
        return {"error": f"Geri yukleme hatasi: {str(e)[:200]}"}
