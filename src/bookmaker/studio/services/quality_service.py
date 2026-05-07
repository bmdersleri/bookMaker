"""Kalite servisi — validasyon, raporlama, istatistik, arama, kod derleme."""

from __future__ import annotations

import re
from pathlib import Path

from bookmaker.chapter.book_validator import validate_book
from bookmaker.chapter.parser import parse
from bookmaker.chapter.scoring import make_report
from bookmaker.chapter.validation_modes import resolve_validation_profile_from_manifest
from bookmaker.chapter.validator import validate
from bookmaker.code.runner import select_code_adapter
from bookmaker.manifest.models import ManifestChapter
from bookmaker.models.quality import QualityReport

_PREVIEW_LENGTH = 500
_ERROR_TRUNCATION = 200
_READING_SPEED_WPM = 200


def _chapter_alias(chapter: ManifestChapter) -> str:
    """Return chapter alias from a ManifestChapter instance."""
    return chapter.chapter_id or chapter.alias or ""


def _chapter_matches(chapter: ManifestChapter, chapter_id: str) -> bool:
    """Check if a chapter matches by chapter_id or alias."""
    return chapter_id in {chapter.chapter_id, chapter.alias}


def _chapter_source(chapter: ManifestChapter) -> str:
    """Return default source path for a chapter."""
    alias = _chapter_alias(chapter)
    return chapter.source or f"chapters/{alias}/content/final.md"


def _report_path(chapter_id: str | None = None) -> str:
    if chapter_id:
        return str(
            Path("logs") / "reviews" / "chapters" / f"{chapter_id}_quality_report.json"
        )
    return str(Path("logs") / "reviews" / "book_quality_report.json")


def _issue_rows(report: QualityReport, limit: int = 25) -> list[dict]:
    rows = []
    for issue in report.issues[:limit]:
        rows.append({
            "severity": issue.severity.value,
            "category": issue.category,
            "message": issue.message,
            "file": issue.location.file,
            "line": issue.location.line,
        })
    return rows


def _chapter_report_payload(
    root: Path,
    chapter_id: str,
    report: QualityReport,
) -> dict:
    report_path = _report_path(chapter_id)
    return {
        "chapter_id": chapter_id,
        "score": report.score,
        "decision": report.decision.value,
        "errors": report.error_count,
        "warnings": report.warning_count,
        "info_count": sum(1 for issue in report.issues if issue.severity.value == "info"),
        "total_issues": report.error_count + report.warning_count,
        "report_path": report_path,
        "report_exists": (root / report_path).exists(),
        "issues": _issue_rows(report),
    }


def validate_chapter(project_root: str | Path, chapter_id: str) -> dict:
    """Bölümü valide eder."""
    root = Path(project_root).resolve()
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    profile = resolve_validation_profile_from_manifest(manifest)
    src = next((_chapter_source(ch) for ch in manifest.chapters
                if _chapter_matches(ch, chapter_id)), None)
    if not src:
        return {"error": f"Bölüm bulunamadi: {chapter_id}"}
    p = root / src
    if not p.exists():
        return {"error": f"Dosya bulunamadi: {p}"}
    try:
        parsed = parse(p)
        issues = validate(parsed, profile=profile)
        report = make_report(chapter_id, issues)
        return _chapter_report_payload(root, chapter_id, report)
    except Exception as e:
        return {"error": f"Validasyon hatasi: {str(e)[:_ERROR_TRUNCATION]}"}


def get_chapter_content(project_root: str | Path, chapter_id: str) -> dict:
    """Bölüm içeriğini döndürür."""
    root = Path(project_root).resolve()
    from bookmaker.manifest.manager import ManifestManager
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    src = next((_chapter_source(ch) for ch in manifest.chapters
                if _chapter_matches(ch, chapter_id)), None)
    if not src:
        return {"error": f"Bölüm bulunamadi: {chapter_id}"}
    base = root / "chapters" / chapter_id
    draft = base / "content" / "draft.md"
    final = base / "content" / "final.md"
    legacy_base = base / "approved"
    candidates = [
        root / src,
        final,
        draft,
        legacy_base / f"{chapter_id}_v001.md",
        legacy_base / f"{chapter_id}_v002.md",
        legacy_base / "v001.md",
    ]
    for p in candidates:
        if p.exists():
            text = p.read_text(encoding="utf-8")
            return {"chapter_id": chapter_id,
                    "path": str(p.relative_to(root)),
                    "words": len(text.split()),
                    "chars": len(text),
                    "preview": text[:_PREVIEW_LENGTH], "full": text}
    return {"error": f"İçerik bulunamadi: {chapter_id}"}


def get_quality_report(project_root: str | Path,
                       chapter_id: str | None = None) -> list[dict] | dict:
    """Tüm bölümlerin veya tek bölümün kalite raporunu döndürür."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    profile = resolve_validation_profile_from_manifest(manifest)

    chapters_to_check = []
    if chapter_id:
        chapters_to_check = [chapter_id]
    else:
        chapters_to_check = [_chapter_alias(ch) for ch in manifest.chapters]

    results = []
    for cid in chapters_to_check:
        src = next((_chapter_source(ch) for ch in manifest.chapters
                    if _chapter_matches(ch, cid)), None)
        if not src:
            results.append({"chapter_id": cid, "error": "Bulunamadi"})
            continue
        p = root / src
        if not p.exists():
            results.append({"chapter_id": cid, "error": "Dosya yok",
                            "score": 0, "errors": 0, "warnings": 0})
            continue
        try:
            parsed = parse(p)
            issues = validate(parsed, profile=profile)
            report = make_report(cid, issues)
            results.append(_chapter_report_payload(root, cid, report))
        except Exception as e:
            results.append({"chapter_id": cid, "error": str(e)[:100],
                            "score": 0})
    if chapter_id and results:
        return results[0]
    return results


def get_book_quality_report(project_root: str | Path) -> dict:
    """Kitap seviyesinde validate_book sonucunu Studio icin ozetler."""
    root = Path(project_root).resolve()
    result = validate_book(root)
    report = result.report
    report_path = _report_path()
    chapters = []
    for alias in result.chapter_order:
        chapter_report = result.chapter_reports.get(alias)
        if chapter_report is None:
            chapters.append({
                "chapter_id": alias,
                "score": 0,
                "decision": "missing",
                "errors": 0,
                "warnings": 0,
                "report_path": _report_path(alias),
                "report_exists": False,
            })
            continue
        chapters.append(_chapter_report_payload(root, alias, chapter_report))
    return {
        "chapter_id": "book",
        "score": report.score,
        "decision": report.decision.value,
        "errors": report.error_count,
        "warnings": report.warning_count,
        "total_issues": report.error_count + report.warning_count,
        "report_path": report_path,
        "report_exists": (root / report_path).exists(),
        "issues": _issue_rows(report),
        "chapters": chapters,
    }


def get_book_stats(project_root: str | Path) -> dict:
    """Kitap geneli istatistikleri döndürür."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    total_words = 0
    total_chars = 0
    total_code = 0
    total_mermaid = 0
    total_tables = 0
    word_counts = []

    for ch in manifest.chapters:
        src = _chapter_source(ch)
        p = root / src if src else None
        if p and p.exists():
            text = p.read_text(encoding="utf-8")
            wc = len(text.split())
            total_words += wc
            total_chars += len(text)
            total_code += len(re.findall(r'```', text)) // 2
            total_mermaid += len(re.findall(r'```mermaid', text))
            total_tables += len(re.findall(r'^\|.*\|$', text, re.MULTILINE))
            alias = _chapter_alias(ch)
            word_counts.append({"chapter_id": alias,
                                "words": wc, "title": ch.title or alias})
        else:
            alias = _chapter_alias(ch)
            word_counts.append({"chapter_id": alias,
                                "words": 0, "title": ch.title or alias})

    reading_minutes = round(total_words / _READING_SPEED_WPM)
    chapter_count = len(manifest.chapters)

    # En uzun/kısa bölüm
    if word_counts:
        longest = max(word_counts, key=lambda x: x["words"])
        shortest = min(word_counts, key=lambda x: x["words"])
    else:
        longest = {"chapter_id": "-", "words": 0}
        shortest = {"chapter_id": "-", "words": 0}

    return {"total_words": total_words, "total_chars": total_chars,
            "total_code_blocks": total_code, "total_mermaid": total_mermaid,
            "total_tables": total_tables,
            "reading_minutes": reading_minutes,
            "estimated_hours": round(reading_minutes / 60, 1),
            "chapter_count": chapter_count,
            "average_words": round(total_words / chapter_count) if chapter_count else 0,
            "longest_chapter": longest,
            "shortest_chapter": shortest,
            "word_distribution": word_counts}


def search_content(project_root: str | Path, query: str,
                   chapter_id: str | None = None,
                   use_regex: bool = False) -> list[dict]:
    """Tam metin arama — tüm bölümlerde veya tek bölümde."""
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()

    results = []
    for ch in manifest.chapters:
        if chapter_id and not _chapter_matches(ch, chapter_id):
            continue
        src = _chapter_source(ch)
        p = root / src if src else None
        if not p or not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            try:
                if use_regex:
                    match = re.search(query, line)
                else:
                    match = query.lower() in line.lower()
            except re.error:
                continue
            if match:
                # Bağlam (context): eşleşen satır + 1 önce + 1 sonra
                start = max(0, i - 1)
                end = min(len(lines), i + 2)
                context = "\n".join(lines[start:end])
                results.append({
                    "chapter_id": _chapter_alias(ch),
                    "line": i + 1,
                    "context": context[:_PREVIEW_LENGTH],
                    "text": line[:200],
                })
    return results


def compile_code(project_root: str | Path, chapter_id: str) -> dict:
    """Kod bloklarını profile-aware adapter ile işler."""
    from bookmaker.code.report import summarize_test_results
    from bookmaker.manifest.manager import ManifestManager
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    profile = resolve_validation_profile_from_manifest(manifest)
    code_language = (manifest.style.code_language or "").strip().lower()
    if (
        not code_language
        and (manifest.style.framework or "").strip().lower() == "flutter"
    ):
        code_language = "dart"
    adapter = select_code_adapter(profile, code_language=code_language or None)
    src = next((_chapter_source(ch) for ch in manifest.chapters
                if _chapter_matches(ch, chapter_id)), None)
    if not src:
        return {
            "chapter_id": chapter_id,
            "status": "error",
            "error": f"Bölüm bulunamadi: {chapter_id}",
            "summary": {"ok": 0, "error": 1, "skipped": 0, "total": 0},
            "results": [],
        }
    p = root / src
    if not p.exists():
        return {
            "chapter_id": chapter_id,
            "status": "error",
            "error": f"Dosya bulunamadi: {p}",
            "summary": {"ok": 0, "error": 1, "skipped": 0, "total": 0},
            "results": [],
        }

    text = p.read_text(encoding="utf-8")
    blocks = adapter.extract_blocks(text)
    if not blocks:
        return {
            "chapter_id": chapter_id,
            "adapter": adapter.name,
            "language": adapter.language,
            "blocks": 0,
            "compiled": 0,
            "failed": 0,
            "skipped": 0,
            "status": "empty",
            "summary": {"ok": 0, "error": 0, "skipped": 0, "total": 0},
            "results": [],
        }

    # Geçici dizine yaz
    tmp_dir = root / "build" / "code_check" / chapter_id / adapter.name
    tmp_dir.mkdir(parents=True, exist_ok=True)

    results = adapter.run_tests(blocks, tmp_dir)
    summary = summarize_test_results(results)

    failed = summary["error"]
    skipped = summary["skipped"]
    if failed > 0:
        status = "error"
    elif skipped == summary["total"]:
        status = "skipped"
    else:
        status = "ok"

    return {
        "chapter_id": chapter_id,
        "adapter": adapter.name,
        "language": adapter.language,
        "blocks": summary["total"],
        "compiled": summary["ok"],
        "failed": failed,
        "skipped": skipped,
        "status": status,
        "summary": summary,
        "results": results,
    }


def extract_code_blocks(project_root: str | Path, chapter_id: str,
                        language: str = "java") -> dict:
    """Legacy kod çıkarma yardımı.

    Yeni akışta `quality_service.compile_code()` profile-aware adapter
    kullanır. Bu fonksiyon geriye uyumluluk için tutulur; mümkünse yeni
    adapter hattını tercih edin.
    """
    import warnings

    warnings.warn(
        "quality_service.extract_code_blocks() legacy helper'dir; "
        "compile_code() veya export_service.extract_code() tercih edin.",
        DeprecationWarning,
        stacklevel=2,
    )
    root = Path(project_root).resolve()
    text_data = get_chapter_content(root, chapter_id)
    if "error" in text_data:
        return text_data

    text = text_data.get("full", "")
    blocks = re.findall(rf'```{language}\n(.*?)```', text, re.DOTALL)

    lang_ext = {"java": ".java", "python": ".py", "javascript": ".js",
                "html": ".html", "css": ".css", "xml": ".xml"}
    ext = lang_ext.get(language, ".txt")

    out_dir = root / "build" / "code" / chapter_id
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = 0
    files = []
    for i, block in enumerate(blocks):
        # İlk satırdan sınıf adını bul, yoksa generik
        first_line = block.strip().splitlines()[0] if block.strip() else ""
        class_match = re.search(r'(?:public\s+)?(?:class|func|def|function)\s+(\w+)',
                                first_line)
        base_name = class_match.group(1) if class_match else f"block_{i+1:03d}"
        fname = f"{base_name}{ext}"

        # Aynı dosya varsa index ekle
        idx = 1
        while (out_dir / fname).exists():
            fname = f"{base_name}_{idx:03d}{ext}"
            idx += 1

        (out_dir / fname).write_text(block, encoding="utf-8")
        saved += 1
        files.append(fname)

    return {"chapter_id": chapter_id, "language": language,
            "extracted": saved, "output_dir": str(out_dir.relative_to(root)),
            "files": files}
