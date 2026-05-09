"""Build pipeline: kod çıkarma + derleme + raporlama."""

from __future__ import annotations

from pathlib import Path

from bookmaker.build.extractor import extract_and_report
from bookmaker.build.runner import test_code
from bookmaker.chapter.parser import parse


def build_chapter(chapter_path: Path, build_root: Path | None = None) -> dict:
    """Bölüm dosyasından kod çıkarır, derler ve rapor üretir."""
    build_root = build_root or Path("build")
    chapter = parse(chapter_path)

    # Kod çıkarma
    extracted = extract_and_report(chapter, build_root)

    # Derleme
    compile_results = []
    for item in extracted:
        if item["status"] != "extracted" or not item["path"]:
            continue
        src = Path(item["path"])
        test_mode = item.get("test", "compile")
        cr = test_code(src, test_mode)
        cr["code_id"] = item["code_id"]
        compile_results.append(cr)

    # Rapor
    total = len(extracted)
    extracted_count = sum(1 for e in extracted if e["status"] == "extracted")
    skipped = sum(1 for e in extracted if e["status"] == "skipped")
    errors = sum(1 for e in extracted if e["status"] == "error")
    passed = sum(1 for c in compile_results if c.get("compile_status") == "passed")
    failed = sum(1 for c in compile_results if c.get("compile_status") == "failed")

    report = {
        "chapter": chapter_path.stem,
        "total_code_blocks": total,
        "extracted": extracted_count,
        "skipped": skipped,
        "extract_errors": errors,
        "compiled": passed,
        "compile_failed": failed,
        "extraction": extracted,
        "compile_results": compile_results,
    }

    return report
