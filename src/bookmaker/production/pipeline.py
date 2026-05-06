"""Production pipeline — Mermaid, QR, DOCX export.
book_profile.yaml -> BookConfig ile yapilandirilir."""

from __future__ import annotations

from pathlib import Path

from bookmaker.build.pipeline import build_chapter
from bookmaker.core.config import BookConfig, load_config
from bookmaker.production.mermaid import render_from_file
from bookmaker.production.pandoc import export_docx
from bookmaker.production.qrcode import generate_qr


def run(
    chapter_path: Path,
    build_root: Path | None = None,
    config: BookConfig | None = None,
) -> dict:
    """Full production pipeline: compile → mermaid → qr → docx.

    Args:
        chapter_path: Bolum .md dosyasi
        build_root: Build dizini (None = config.build_dir)
        config: Kitap config (None = otomatik bul)
    """
    if config is None:
        try:
            config = load_config(start=chapter_path.parent)
        except Exception:
            config = None

    build_root = build_root or (config.build_dir if config else Path("build"))
    chapter_id = chapter_path.stem

    result: dict = {
        "chapter": chapter_id,
        "build": None,
        "mermaid": None,
        "qrcode": None,
        "docx": None,
    }

    # 1. Compile
    build_result = build_chapter(chapter_path, build_root)
    result["build"] = build_result

    # 2. Mermaid render
    assets_dir = build_root / "assets"
    (assets_dir / "mermaid").mkdir(parents=True, exist_ok=True)
    mermaid_results = render_from_file(
        chapter_path, assets_dir / "mermaid", config=config,
    )
    result["mermaid"] = mermaid_results

    # 3. QR — kodlar icin QR uret
    qr_dir = build_root / "assets" / "qr"
    qr_dir.mkdir(parents=True, exist_ok=True)
    qr_results: list[dict] = []
    for item in build_result.get("extraction", []):
        if item["status"] == "extracted":
            url = (
                f"https://github.com/bmdersleri/bookMaker"
                f"/blob/main/build/code/{item['code_id']}/{item['file']}"
            )
            qr_out = qr_dir / f"{item['code_id']}_qr.png"
            qr_result = generate_qr(url, qr_out)
            qr_result["code_id"] = item["code_id"]
            qr_results.append(qr_result)
    result["qrcode"] = qr_results

    # 4. DOCX export
    docx_dir = build_root / "exports"
    docx_dir.mkdir(parents=True, exist_ok=True)
    docx_path = docx_dir / f"{chapter_id}.docx"
    docx_result = export_docx(chapter_path, docx_path, config=config)
    result["docx"] = docx_result

    return result
