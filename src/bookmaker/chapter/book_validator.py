"""Kitap duzeyinde validasyon — 27 bolumun tamamini tarar, capraz kontroller yapar."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from bookmaker.chapter.parser import parse, ParsedChapter, Heading
from bookmaker.chapter.validator import validate as validate_chapter
from bookmaker.chapter.scoring import make_report as make_chapter_report
from bookmaker.core.ids import new_issue_id
from bookmaker.models.quality import (
    QualityReport,
    Decision,
    Issue,
    IssueLocation,
    IssueStatus,
    Severity,
)

CHAPTER_ORDER: list[str] = [
    "bolum-01", "bolum-02", "bolum-03", "bolum-04", "bolum-05", "bolum-06",
    "bolum-07", "bolum-08", "bolum-09", "bolum-10", "bolum-11",
    "bolum-12", "bolum-13", "bolum-14", "bolum-15", "bolum-16",
    "bolum-17", "bolum-18", "bolum-19", "bolum-20", "bolum-21",
    "bolum-22", "bolum-23",
    "ek-a", "ek-b", "ek-c", "ek-d",
]

EXPECTED_NUMBERS: dict[str, str] = {
    "bolum-01": "1", "bolum-02": "2", "bolum-03": "3",
    "bolum-04": "4", "bolum-05": "5", "bolum-06": "6",
    "bolum-07": "7", "bolum-08": "8", "bolum-09": "9",
    "bolum-10": "10", "bolum-11": "11", "bolum-12": "12",
    "bolum-13": "13", "bolum-14": "14", "bolum-15": "15",
    "bolum-16": "16", "bolum-17": "17", "bolum-18": "18",
    "bolum-19": "19", "bolum-20": "20", "bolum-21": "21",
    "bolum-22": "22", "bolum-23": "23",
    "ek-a": "A", "ek-b": "B", "ek-c": "C", "ek-d": "D",
}

MIN_CHARS = 5_000


def _add(
    issues: list[Issue],
    severity: str,
    category: str,
    message: str,
    file: str = "",
    line: int | None = None,
    context: str = "",
) -> None:
    issues.append(Issue(
        issue_id=new_issue_id(),
        severity=Severity(severity),
        category=category,
        location=IssueLocation(file=file, line=line),
        message=message,
        current=context,
    ))


def _fmt_path(slug: str) -> str:
    return f"chapters/{slug}/draft_versions/v001.md"


class BookCheckResult:
    """Kitap validasyonu sonucu — bolum bazli ayrintilar + genel rapor."""

    def __init__(self, report: QualityReport) -> None:
        self.report = report
        self.chapter_details: dict[str, dict] = {}
        self.chapter_reports: dict[str, QualityReport] = {}
        self.chapter_sizes: dict[str, int] = {}
        self.chapter_issues: dict[str, list[Issue]] = {}


def _check_file_existence(
    chapters_dir: Path, issues: list[Issue],
) -> dict[str, Optional[Path]]:
    found: dict[str, Optional[Path]] = {}
    for slug in CHAPTER_ORDER:
        path = chapters_dir / slug / "draft_versions" / "v001.md"
        if path.exists():
            found[slug] = path
        else:
            found[slug] = None
            _add(issues, "error", "file.missing",
                 f"Dosya bulunamadi: {_fmt_path(slug)}",
                 file=_fmt_path(slug))
    return found


def _check_numbering_continuity(
    chapter_paths: dict[str, Optional[Path]],
    issues: list[Issue],
) -> None:
    """Bolum numaralandirma — numbering 'auto' veya beklenen deger kabul."""
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            parsed = parse(path)
        except Exception as exc:
            _add(issues, "error", "parse.failed",
                 f"Parse hatasi: {slug} — {exc}", file=_fmt_path(slug))
            continue

        expected = EXPECTED_NUMBERS.get(slug, "")
        actual = parsed.frontmatter.get("numbering", "")
        # 'auto' gecerli bir Pandoc degeridir
        if actual not in (expected, "auto", ""):
            _add(issues, "warning", "numbering.mismatch",
                 f"numbering={actual!r}, beklenen={expected!r} veya 'auto'",
                 file=_fmt_path(slug), line=1, context=actual)


def _check_frontmatter_consistency(
    chapter_paths: dict[str, Optional[Path]],
    issues: list[Issue],
) -> dict[str, dict[str, str]]:
    required = [
        "title", "chapter_id", "chapter_type", "numbering",
        "automation_profile", "processing_stage",
    ]
    frontmatters: dict[str, dict[str, str]] = {}
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            parsed = parse(path)
        except Exception:
            continue
        fm = parsed.frontmatter
        frontmatters[slug] = fm
        for field in required:
            if field not in fm:
                _add(issues, "warning", "frontmatter.missing_field",
                     f"{slug}: frontmatter'da '{field}' eksik",
                     file=_fmt_path(slug), line=1)

    seen_ids: dict[str, str] = {}
    for slug, fm in frontmatters.items():
        cid = fm.get("chapter_id", "")
        if cid and cid in seen_ids:
            _add(issues, "error", "frontmatter.duplicate_chapter_id",
                 f"Tekrar eden chapter_id '{cid}': {seen_ids[cid]} ve {slug}",
                 file=_fmt_path(slug), line=1)
        if cid:
            seen_ids[cid] = slug

    return frontmatters


def _check_cross_references(
    chapter_paths: dict[str, Optional[Path]],
    frontmatters: dict[str, dict[str, str]],
    issues: list[Issue],
) -> None:
    valid_refs: set[str] = set()
    for slug in CHAPTER_ORDER:
        fm = frontmatters.get(slug, {})
        cid = fm.get("chapter_id", slug)
        valid_refs.add(cid)
        title = fm.get("title", slug)
        if title:
            valid_refs.add(title.casefold())

    ref_pattern = re.compile(
        r"(?:Bolum|Bolum|Chapter|Ek|Appendix)\s+(\d+|[A-Da-d])",
        re.IGNORECASE,
    )
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for match in ref_pattern.finditer(text):
            pass  # Cozumlenmeyen referanslar icin genisletilebilir


def _check_mermaid_id_collisions(
    chapter_paths: dict[str, Optional[Path]],
    issues: list[Issue],
) -> None:
    seen_ids: dict[str, str] = {}
    seen_titles: dict[str, str] = {}
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            parsed = parse(path)
        except Exception:
            continue
        for mb in parsed.meta_blocks:
            if mb.kind != "MERMAID_META":
                continue
            mid = mb.data.get("id", "")
            title = mb.data.get("title", "")
            if mid:
                if mid in seen_ids:
                    _add(issues, "error", "mermaid.duplicate_id",
                         f"Mermaid ID '{mid}' tekrar: {seen_ids[mid]} vs {slug}",
                         file=_fmt_path(slug), line=mb.line)
                else:
                    seen_ids[mid] = slug
            if title:
                key = title.strip().casefold()
                if key in seen_titles:
                    _add(issues, "warning", "mermaid.duplicate_title",
                         f"Mermaid title '{title}' tekrar: {seen_titles[key]} vs {slug}",
                         file=_fmt_path(slug), line=mb.line)
                else:
                    seen_titles[key] = slug


def _check_heading_hierarchy(
    chapter_paths: dict[str, Optional[Path]],
    issues: list[Issue],
) -> None:
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            parsed = parse(path)
        except Exception:
            continue
        headings = parsed.headings
        if not headings:
            _add(issues, "warning", "headings.none",
                 f"{slug}: hic heading bulunamadi",
                 file=_fmt_path(slug))
            continue

        h1s = [h for h in headings if h.level == 1]
        if len(h1s) == 0:
            _add(issues, "error", "heading.no_h1",
                 f"{slug}: H1 basligi bulunamadi",
                 file=_fmt_path(slug))
        elif len(h1s) > 1:
            for h in h1s:
                _add(issues, "error", "heading.multiple_h1",
                     f"{slug}: birden fazla H1: '{h.title}'",
                     file=_fmt_path(slug), line=h.line)

        prev_level = 0
        for h in headings:
            if h.level > prev_level + 1 and prev_level > 0:
                _add(issues, "warning", "heading.level_skip",
                     f"{slug}: hiyerarsi atlamasi: H{prev_level} -> H{h.level} ('{h.title}')",
                     file=_fmt_path(slug), line=h.line)
            prev_level = h.level


def _check_placeholders(
    chapter_paths: dict[str, Optional[Path]],
    issues: list[Issue],
) -> None:
    placeholder_pattern = re.compile(
        r"(?:\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b|\[\.\.\.\]|\(\.\.\.\)|<!--.*?TODO)",
        re.IGNORECASE,
    )
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        fm_end = text.find("---", 3)
        body = text[fm_end + 3:] if fm_end > 0 else text

        for match in placeholder_pattern.finditer(body):
            line_no = text[:match.start()].count("\n") + 1
            _add(issues, "warning", "placeholder.found",
                 f"Placeholder: '{match.group().strip()}'",
                 file=_fmt_path(slug), line=line_no,
                 context=match.group().strip())


def _check_mermaid_pngs(
    chapter_paths: dict[str, Optional[Path]],
    images_dir: Path,
    issues: list[Issue],
) -> None:
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            parsed = parse(path)
        except Exception:
            continue
        for mb in parsed.meta_blocks:
            if mb.kind != "MERMAID_META":
                continue
            out_file = mb.data.get("output_file", "")
            if not out_file:
                _add(issues, "warning", "mermaid.no_output_file",
                     f"{slug}: MERMAID_META'da output_file eksik (id={mb.data.get('id','')})",
                     file=_fmt_path(slug), line=mb.line)
                continue
            png_path = images_dir / out_file
            if not png_path.exists():
                _add(issues, "error", "mermaid.png_missing",
                     f"PNG bulunamadi: {out_file} (id={mb.data.get('id','')})",
                     file=_fmt_path(slug), line=mb.line)


def _check_chapter_length(
    chapter_paths: dict[str, Optional[Path]],
    issues: list[Issue],
) -> dict[str, int]:
    sizes: dict[str, int] = {}
    all_sizes: list[int] = []
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            size = path.stat().st_size
        except Exception:
            continue
        sizes[slug] = size
        all_sizes.append(size)

        if size < MIN_CHARS:
            _add(issues, "warning", "length.too_short",
                 f"{slug}: cok kisa ({size} bytes < {MIN_CHARS})",
                 file=_fmt_path(slug))

    if all_sizes:
        avg = sum(all_sizes) / len(all_sizes)
        for slug, size in sizes.items():
            if size > avg * 2.5:
                _add(issues, "warning", "length.too_long",
                     f"{slug}: cok uzun ({size} bytes, ortalama {avg:.0f}'nin 2.5 kati)",
                     file=_fmt_path(slug))

    return sizes


def _run_chapter_validations(
    chapter_paths: dict[str, Optional[Path]],
) -> dict[str, QualityReport]:
    reports: dict[str, QualityReport] = {}
    for slug, path in chapter_paths.items():
        if path is None:
            continue
        try:
            parsed = parse(path)
            issues = validate_chapter(parsed)
            report = make_chapter_report(slug, issues)
            reports[slug] = report
        except Exception as exc:
            issues = [
                Issue(
                    issue_id=new_issue_id(),
                    severity=Severity.error,
                    category="validate.failed",
                    location=IssueLocation(file=_fmt_path(slug)),
                    message=f"Validasyon basarisiz: {exc}",
                )
            ]
            reports[slug] = make_chapter_report(slug, issues)
    return reports


def validate_book(
    chapters_dir: Path,
    images_dir: Optional[Path] = None,
) -> BookCheckResult:
    all_issues: list[Issue] = []

    chapter_paths = _check_file_existence(chapters_dir, all_issues)
    _check_numbering_continuity(chapter_paths, all_issues)
    frontmatters = _check_frontmatter_consistency(chapter_paths, all_issues)
    _check_cross_references(chapter_paths, frontmatters, all_issues)
    _check_mermaid_id_collisions(chapter_paths, all_issues)
    _check_heading_hierarchy(chapter_paths, all_issues)
    _check_placeholders(chapter_paths, all_issues)

    if images_dir is not None:
        _check_mermaid_pngs(chapter_paths, images_dir, all_issues)

    chapter_sizes = _check_chapter_length(chapter_paths, all_issues)
    chapter_reports = _run_chapter_validations(chapter_paths)

    report = QualityReport(
        report_id=new_issue_id(),
        artifact_type="book",
        artifact_version="production",
        chapter_id="book",
        issues=all_issues,
        checks=[],
    )
    report.compute_score()

    result = BookCheckResult(report)
    result.chapter_sizes = chapter_sizes
    result.chapter_reports = chapter_reports

    return result


def validate_book_cli(
    chapters_dir: str = "chapters",
    images_dir: str = "build/output/images",
    json_output: bool = False,
) -> BookCheckResult:
    cdir = Path(chapters_dir)
    idir = Path(images_dir) if Path(images_dir).exists() else None
    result = validate_book(cdir, idir)
    return result
