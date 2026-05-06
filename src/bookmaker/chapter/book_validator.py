# ruff: noqa: E501
"""Project-based kitap validasyonu.

Yeni mimaride bölüm sırası ve beklenen dosyalar book_manifest.yaml içinden türetilir.
Sabit Java bölüm listesi veya draft_versions/v001.md varsayımı kullanılmaz.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from bookmaker.chapter.parser import parse
from bookmaker.chapter.scoring import make_report as make_chapter_report
from bookmaker.chapter.validator import validate as validate_chapter
from bookmaker.core.ids import new_issue_id
from bookmaker.models.quality import Issue, IssueLocation, QualityReport, Severity

_yaml = YAML()


CHAPTER_ORDER: tuple[str, ...] = ()
"""Legacy public symbol; project-based validation reads order from book_manifest.yaml."""


class BookCheckResult:
    """Kitap validasyonu sonucu."""

    def __init__(self, report: QualityReport) -> None:
        self.report = report
        self.chapter_order: list[str] = []
        self.chapter_orders: dict[str, int] = {}
        self.chapter_reports: dict[str, QualityReport] = {}
        self.chapter_sizes: dict[str, int] = {}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = _yaml.load(f) or {}
    return data if isinstance(data, dict) else {}


def _add(
    issues: list[Issue],
    severity: str,
    category: str,
    message: str,
    file: str = "",
    line: int | None = None,
    context: str = "",
) -> None:
    issues.append(
        Issue(
            issue_id=new_issue_id(),
            severity=Severity(severity),
            category=category,
            location=IssueLocation(file=file, line=line),
            message=message,
            current=context,
        )
    )


def _relative(project_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(project_root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _chapter_aliases(book_manifest: dict[str, Any]) -> list[str]:
    chapters = book_manifest.get("chapters", [])
    aliases: list[str] = []
    if isinstance(chapters, list):
        for item in chapters:
            if isinstance(item, dict) and item.get("alias"):
                aliases.append(str(item["alias"]))
    return aliases


def _validate_project_root(project_root: Path, issues: list[Issue]) -> dict[str, Any]:
    manifest_path = project_root / "book_manifest.yaml"
    if not manifest_path.exists():
        _add(
            issues,
            "error",
            "book_manifest.missing",
            "book_manifest.yaml bulunamadı.",
            file=_relative(project_root, manifest_path),
        )
        return {}

    try:
        manifest = _load_yaml(manifest_path)
    except Exception as exc:
        _add(
            issues,
            "error",
            "book_manifest.parse_failed",
            f"book_manifest.yaml okunamadı: {exc}",
            file="book_manifest.yaml",
        )
        return {}

    for required in ["book", "production", "style", "chapters"]:
        if required not in manifest:
            _add(
                issues,
                "error",
                "book_manifest.required_missing",
                f"book_manifest.yaml içinde zorunlu alan eksik: {required}",
                file="book_manifest.yaml",
            )

    book = manifest.get("book", {}) if isinstance(manifest.get("book"), dict) else {}
    if not book.get("alias"):
        _add(issues, "error", "book_manifest.alias_missing", "book.alias eksik.", "book_manifest.yaml")

    aliases = _chapter_aliases(manifest)
    if not aliases:
        _add(
            issues,
            "error",
            "book_manifest.chapters_empty",
            "book_manifest.yaml içinde chapters listesi boş veya geçersiz.",
            file="book_manifest.yaml",
        )

    if len(aliases) != len(set(aliases)):
        duplicates = sorted({alias for alias in aliases if aliases.count(alias) > 1})
        _add(
            issues,
            "error",
            "book_manifest.duplicate_alias",
            f"Tekrar eden bölüm alias değerleri: {', '.join(duplicates)}",
            file="book_manifest.yaml",
        )

    return manifest


def _validate_required_dirs(project_root: Path, issues: list[Issue]) -> None:
    required_dirs = [
        "prompts",
        "chapters",
        "exports",
        "exports/docx",
        "exports/pdf",
        "exports/md",
        "logs",
        "logs/production",
        "logs/errors",
        "logs/reviews",
    ]
    for rel in required_dirs:
        path = project_root / rel
        if not path.exists():
            _add(issues, "error", "directory.missing", f"Klasör bulunamadı: {rel}", file=rel)


def _validate_prompts(project_root: Path, issues: list[Issue]) -> None:
    for rel in ["prompts/default_chapter.md", "prompts/default_review.md"]:
        path = project_root / rel
        if not path.exists():
            _add(issues, "error", "prompt.missing", f"Prompt dosyası bulunamadı: {rel}", file=rel)
        elif path.stat().st_size < 20:
            _add(issues, "warning", "prompt.too_short", f"Prompt dosyası çok kısa: {rel}", file=rel)


def _validate_pipeline_state(
    project_root: Path,
    aliases: list[str],
    issues: list[Issue],
) -> None:
    path = project_root / "pipeline_state.yaml"
    if not path.exists():
        _add(issues, "warning", "pipeline_state.missing", "pipeline_state.yaml bulunamadı.", "pipeline_state.yaml")
        return

    try:
        state = _load_yaml(path)
    except Exception as exc:
        _add(issues, "error", "pipeline_state.parse_failed", f"pipeline_state.yaml okunamadı: {exc}", "pipeline_state.yaml")
        return

    pipeline = state.get("pipeline", {}) if isinstance(state.get("pipeline"), dict) else {}
    if not pipeline.get("book_alias"):
        _add(issues, "warning", "pipeline_state.book_alias_missing", "pipeline.book_alias eksik.", "pipeline_state.yaml")

    state_chapters = state.get("chapters", [])
    state_aliases = [
        str(item.get("alias"))
        for item in state_chapters
        if isinstance(item, dict) and item.get("alias")
    ]
    if state_aliases and state_aliases != aliases:
        _add(
            issues,
            "warning",
            "pipeline_state.chapter_sync",
            "pipeline_state.yaml chapters listesi book_manifest.yaml sırası ile birebir eşleşmiyor.",
            file="pipeline_state.yaml",
            context=f"manifest={aliases}; pipeline={state_aliases}",
        )


def _validate_chapter_manifest(
    project_root: Path,
    alias: str,
    order: int,
    valid_aliases: set[str],
    issues: list[Issue],
) -> dict[str, Any]:
    chapter_root = project_root / "chapters" / alias
    manifest_path = chapter_root / "chapter_manifest.yaml"
    if not manifest_path.exists():
        _add(
            issues,
            "error",
            "chapter_manifest.missing",
            f"Bölüm manifesti bulunamadı: chapters/{alias}/chapter_manifest.yaml",
            file=_relative(project_root, manifest_path),
        )
        return {}

    try:
        manifest = _load_yaml(manifest_path)
    except Exception as exc:
        _add(
            issues,
            "error",
            "chapter_manifest.parse_failed",
            f"chapter_manifest.yaml okunamadı: {exc}",
            file=_relative(project_root, manifest_path),
        )
        return {}

    chapter = manifest.get("chapter", {}) if isinstance(manifest.get("chapter"), dict) else {}
    if chapter.get("alias") != alias:
        _add(
            issues,
            "error",
            "chapter_manifest.alias_mismatch",
            f"chapter.alias={chapter.get('alias')!r}, beklenen={alias!r}",
            file=_relative(project_root, manifest_path),
        )
    if chapter.get("order") != order:
        _add(
            issues,
            "warning",
            "chapter_manifest.order_mismatch",
            f"chapter.order={chapter.get('order')!r}, beklenen={order}",
            file=_relative(project_root, manifest_path),
        )

    for ref in chapter.get("references", []) or []:
        if isinstance(ref, dict) and ref.get("alias") and ref["alias"] not in valid_aliases:
            _add(
                issues,
                "error",
                "chapter_reference.unknown_alias",
                f"Bilinmeyen bölüm referansı: {ref['alias']}",
                file=_relative(project_root, manifest_path),
            )

    for required in ["scope", "structure", "automation"]:
        if required not in manifest:
            _add(
                issues,
                "warning",
                "chapter_manifest.section_missing",
                f"chapter_manifest.yaml içinde önerilen alan eksik: {required}",
                file=_relative(project_root, manifest_path),
            )

    return manifest


def _validate_chapter_files(
    project_root: Path,
    alias: str,
    issues: list[Issue],
) -> tuple[Path | None, Path | None]:
    chapter_root = project_root / "chapters" / alias
    expected = [
        chapter_root,
        chapter_root / "prompt.md",
        chapter_root / "content",
        chapter_root / "content" / "revisions",
    ]
    for path in expected:
        if not path.exists():
            _add(
                issues,
                "error",
                "chapter_file.missing",
                f"Gerekli bölüm yolu bulunamadı: {_relative(project_root, path)}",
                file=_relative(project_root, path),
            )

    draft = chapter_root / "content" / "draft.md"
    final = chapter_root / "content" / "final.md"
    for path in [draft, final]:
        if not path.exists():
            _add(
                issues,
                "error",
                "chapter_content.missing",
                f"İçerik dosyası bulunamadı: {_relative(project_root, path)}",
                file=_relative(project_root, path),
            )
        elif path.stat().st_size < 20:
            _add(
                issues,
                "warning",
                "chapter_content.too_short",
                f"İçerik dosyası çok kısa: {_relative(project_root, path)}",
                file=_relative(project_root, path),
            )
    return (draft if draft.exists() else None, final if final.exists() else None)


def _run_content_validation(path: Path | None, alias: str) -> QualityReport | None:
    if path is None:
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    # Placeholder-only draft/final files should not fail deep markdown validation.
    if len(text.strip()) < 80 or "henüz" in text.casefold():
        return make_chapter_report(alias, [])

    try:
        parsed = parse(path)
        issues = validate_chapter(parsed)
        return make_chapter_report(alias, issues)
    except Exception as exc:
        issue = Issue(
            issue_id=new_issue_id(),
            severity=Severity.error,
            category="chapter.validate_failed",
            location=IssueLocation(file=str(path)),
            message=f"Bölüm içerik validasyonu başarısız: {exc}",
        )
        return make_chapter_report(alias, [issue])


def validate_book(project_root: Path, images_dir: Path | None = None) -> BookCheckResult:
    """Validate a project-based book root."""
    project_root = project_root.resolve()
    all_issues: list[Issue] = []

    manifest = _validate_project_root(project_root, all_issues)
    aliases = _chapter_aliases(manifest)
    valid_aliases = set(aliases)

    _validate_required_dirs(project_root, all_issues)
    _validate_prompts(project_root, all_issues)
    _validate_pipeline_state(project_root, aliases, all_issues)

    chapter_reports: dict[str, QualityReport] = {}
    chapter_sizes: dict[str, int] = {}
    chapter_orders: dict[str, int] = {}

    for order, alias in enumerate(aliases, start=1):
        chapter_orders[alias] = order
        _validate_chapter_manifest(project_root, alias, order, valid_aliases, all_issues)
        draft, final = _validate_chapter_files(project_root, alias, all_issues)
        content_for_validation = final if final and final.stat().st_size > 80 else draft
        report = _run_content_validation(content_for_validation, alias)
        if report is not None:
            chapter_reports[alias] = report
        if draft and draft.exists():
            chapter_sizes[alias] = draft.stat().st_size

    # Detect orphan chapter folders not listed in book_manifest.yaml.
    chapters_dir = project_root / "chapters"
    if chapters_dir.exists():
        for child in chapters_dir.iterdir():
            if child.is_dir() and child.name not in valid_aliases:
                _add(
                    all_issues,
                    "warning",
                    "chapter.orphan_folder",
                    f"book_manifest.yaml içinde olmayan bölüm klasörü: {child.name}",
                    file=_relative(project_root, child),
                )

    report = QualityReport(
        report_id=new_issue_id(),
        artifact_type="book",
        artifact_version="project-based",
        chapter_id="book",
        issues=all_issues,
        checks=[],
    )
    report.compute_score()

    result = BookCheckResult(report)
    result.chapter_order = aliases
    result.chapter_orders = chapter_orders
    result.chapter_reports = chapter_reports
    result.chapter_sizes = chapter_sizes
    return result


def validate_book_cli(
    project_root: str = ".",
    images_dir: str = "",
    json_output: bool = False,
) -> BookCheckResult:
    root = Path(project_root)
    idir = Path(images_dir) if images_dir and Path(images_dir).exists() else None
    return validate_book(root, idir)
