"""Export servisi — kitap birleştirme, format dönüşümü, yedekleme, Mermaid PNG."""

from __future__ import annotations

import re
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

from bookmaker.manifest.manager import ManifestManager


def _chapter_alias(chapter) -> str:
    return chapter.chapter_id or chapter.alias or ""


def _chapter_matches(chapter, chapter_id: str) -> bool:
    return chapter_id in {chapter.chapter_id, chapter.alias}


def _chapter_source(chapter) -> str:
    alias = _chapter_alias(chapter)
    return chapter.source or f"chapters/{alias}/content/final.md"


def _output_dir(root: Path, *parts: str) -> Path:
    out = root / "exports" / Path(*parts)
    out.mkdir(parents=True, exist_ok=True)
    return out


def _detect_code_language(root: Path) -> str:
    manifest = ManifestManager(root).load_or_generate()
    lang = (manifest.style.code_language or "").strip().lower()
    if lang:
        return lang
    framework = (manifest.style.framework or "").strip().lower()
    if framework == "flutter":
        return "dart"
    return "java"


def get_export_targets(project_root: str | Path) -> dict:
    """Return project-based output targets for the Build/Export panel."""
    root = Path(project_root).resolve()
    language = _detect_code_language(root)
    targets = {
        "markdown": str(Path("exports") / "md"),
        "docx": str(Path("exports") / "docx"),
        "pdf": str(Path("exports") / "pdf"),
        "epub": str(Path("exports") / "epub"),
        "html": str(Path("exports") / "html"),
        "code": str(Path("exports") / "code" / language),
        "mermaid": str(Path("exports") / "assets" / "mermaid"),
        "backups": str(Path("exports") / "backups"),
    }
    for rel in targets.values():
        (root / rel).mkdir(parents=True, exist_ok=True)
    return {
        "root": str(Path("exports")),
        "code_language": language,
        "targets": targets,
    }


def assemble_book(project_root: str | Path,
                  chapter_ids: list[str] | None = None) -> dict:
    """Tüm bölüm markdown'larını birleştirip kitap.md olarak kaydeder."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    targets = []
    for ch in manifest.chapters:
        cid = _chapter_alias(ch)
        if chapter_ids and not any(_chapter_matches(ch, item) for item in chapter_ids):
            continue
        src = _chapter_source(ch)
        p = root / src
        if p and p.exists():
            targets.append((ch.order, cid, ch.title or cid, p))

    targets.sort(key=lambda x: x[0])

    out_dir = _output_dir(root, "md")

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
                     chapter_ids: list[str] | None = None,
                     reference_doc: str | None = None,
                     lua_filter: str | None = None,
                     toc_depth: int | None = None) -> dict:
    """Birleştirilmiş kitabı hedef formata dönüştürür.

    fmt: "docx", "pdf", "epub", "html"
    reference_doc: Referans DOCX yolu (None = manifest veya varsayilan)
    lua_filter: Lua filter yolu (None = manifest veya varsayilan)
    toc_depth: TOC derinligi (None = manifest veya varsayilan 2)
    """
    root = Path(project_root).resolve()

    # Manifest'ten varsayilanlari oku
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    pandoc_cfg = manifest.pandoc

    # Parametreleri cozumle: verilen > manifest > varsayilan
    ref_doc = reference_doc
    if ref_doc is None and pandoc_cfg:
        ref_doc = pandoc_cfg.reference_doc
    if ref_doc:
        ref_path = (root / ref_doc).resolve()
        if not ref_path.exists():
            ref_path = None
    else:
        ref_path = None

    lua = lua_filter
    if lua is None and pandoc_cfg:
        lua = pandoc_cfg.filter
    if lua:
        lua_path = (root / lua).resolve()
        if not lua_path.exists():
            lua_path = None
    else:
        lua_path = None

    depth = toc_depth
    if depth is None and pandoc_cfg:
        depth = pandoc_cfg.toc_depth
    if depth is None:
        depth = 2

    # Önce birleştir
    assembled = assemble_book(root, chapter_ids)
    if "error" in assembled:
        return assembled

    md_path = root / assembled["path"]
    fmt_map = {
        "docx": ("docx", ".docx", "docx"),
        "pdf": ("pdf", ".pdf", "pdf"),
        "epub": ("epub", ".epub", "epub"),
        "html": ("html", ".html", "html"),
    }

    if fmt not in fmt_map:
        return {"error": f"Desteklenmeyen format: {fmt}. docx/pdf/epub/html desteklenir."}

    pandoc_fmt, ext, target_dir = fmt_map[fmt]
    out_dir = _output_dir(root, target_dir)
    out_path = out_dir / f"kitap{ext}"

    cmd = [
        "pandoc", str(md_path),
        "-f", "markdown+tex_math_single_backslash",
        "-t", pandoc_fmt,
        "-o", str(out_path),
        "--toc", f"--toc-depth={depth}",
    ]

    if ref_path and ref_path.exists():
        cmd.extend(["--reference-doc", str(ref_path)])

    if lua_path and lua_path.exists():
        cmd.extend(["--lua-filter", str(lua_path)])

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
        chapters_to_scan = [_chapter_alias(ch) for ch in manifest.chapters]

    out_dir = _output_dir(root, "assets", "mermaid")

    rendered = 0
    errors = []
    images: list[str] = []

    manifest = ManifestManager(root).load_or_generate()
    for cid in chapters_to_scan:
        src = next((_chapter_source(ch) for ch in manifest.chapters
                    if _chapter_matches(ch, cid)), None)
        p = root / src if src else None
        if not p or not p.exists():
            errors.append(f"{cid}: icerik bulunamadi")
            continue
        text = p.read_text(encoding="utf-8")
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
    """Tüm veya tek bölümden profile-aware kod bloklarını ayıklar."""
    root = Path(project_root).resolve()
    language = _detect_code_language(root)

    if chapter_id:
        chapters_to_extract = [chapter_id]
    else:
        mgr = ManifestManager(root)
        manifest = mgr.load_or_generate()
        chapters_to_extract = [_chapter_alias(ch) for ch in manifest.chapters]

    out_dir = _output_dir(root, "code", language)
    total_extracted = 0
    results = []
    lang_ext = {"dart": ".dart", "java": ".java", "python": ".py",
                "javascript": ".js", "html": ".html", "css": ".css",
                "xml": ".xml"}
    ext = lang_ext.get(language, ".txt")
    manifest = ManifestManager(root).load_or_generate()

    for cid in chapters_to_extract:
        src = next((_chapter_source(ch) for ch in manifest.chapters
                    if _chapter_matches(ch, cid)), None)
        p = root / src if src else None
        if not p or not p.exists():
            results.append({"chapter_id": cid, "extracted": 0,
                            "error": "Icerik yok"})
            continue
        text = p.read_text(encoding="utf-8")
        blocks = re.findall(rf'```{re.escape(language)}\n(.*?)```', text, re.DOTALL)

        ch_dir = out_dir / cid
        ch_dir.mkdir(parents=True, exist_ok=True)
        ch_extracted = 0

        for i, block in enumerate(blocks):
            first_line = block.strip().splitlines()[0] if block.strip() else ""
            name_match = re.search(
                r'(?:class|void|Future<[^>]+>|Widget|State<[^>]+>|func|def|function)\s+(\w+)',
                first_line,
            )
            base_name = name_match.group(1) if name_match else f"block_{i+1:03d}"
            fname = f"{base_name}{ext}"
            fpath = ch_dir / fname

            idx = 1
            while fpath.exists():
                fname = f"{base_name}_{idx:03d}{ext}"
                fpath = ch_dir / fname
                idx += 1

            fpath.write_text(block, encoding="utf-8")
            ch_extracted += 1
            total_extracted += 1

        results.append({"chapter_id": cid, "extracted": ch_extracted})

    return {
        "total_extracted": total_extracted,
        "language": language,
        "output_dir": str(out_dir.relative_to(root)),
        "details": results,
    }


def create_backup(project_root: str | Path) -> dict:
    """Projenin .zip yedeğini oluşturur."""
    root = Path(project_root).resolve()
    backup_dir = _output_dir(root, "backups")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{root.name}_{timestamp}.zip"
    zip_path = backup_dir / zip_name

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for item in root.rglob("*"):
                # Runtime/cache dizinlerini yedek içine tekrar alma.
                rel = item.relative_to(root)
                parts = rel.parts
                if len(parts) > 1 and parts[0] in {"build", "exports"}:
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
    zip_path = zip_path.resolve()

    if not zip_path.exists():
        return {"error": f"Dosya bulunamadi: {zip_path}"}
    if not zip_path.is_relative_to(root):
        return {"error": "Yedek dosyasi proje disinda olamaz."}

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                target = (root / member).resolve()
                if not target.is_relative_to(root):
                    return {"error": "Yedek arsivinde guvensiz yol var."}
            zf.extractall(root)
        return {"restored": True, "files": len(zf.namelist())}
    except Exception as e:
        return {"error": f"Geri yukleme hatasi: {str(e)[:200]}"}
