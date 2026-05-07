"""Export readiness checks for Studio and production export flow."""

from __future__ import annotations

import subprocess
from pathlib import Path

from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.pipeline import PipelineManager


def _chapter_alias(chapter) -> str:
    return chapter.chapter_id or chapter.alias or ""


def _chapter_matches(chapter, chapter_id: str) -> bool:
    return chapter_id in {chapter.chapter_id, chapter.alias}


def _final_required_for_export(root: Path) -> bool:
    state = PipelineManager(root).load()
    try:
        return bool(state.quality_gates.per_chapter.final_required_for_export)
    except Exception:
        return True


def _chapter_candidates(root: Path, chapter) -> list[tuple[Path, str]]:
    alias = _chapter_alias(chapter)
    candidates: list[tuple[Path, str]] = []

    if chapter.source:
        candidates.append(((root / chapter.source).resolve(), "manifest"))

    base = root / "chapters" / alias
    candidates.extend(
        [
            ((base / "content" / "final.md").resolve(), "final"),
            ((base / "content" / "draft.md").resolve(), "draft"),
            ((base / "approved" / f"{alias}_v001.md").resolve(), "legacy"),
            ((base / "approved" / f"{alias}_v002.md").resolve(), "legacy"),
            ((base / "approved" / "v001.md").resolve(), "legacy"),
        ]
    )
    return candidates


def _check_pandoc() -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except FileNotFoundError:
        return False, "pandoc bulunamadi."
    except subprocess.TimeoutExpired:
        return False, "pandoc versiyon kontrolu zaman asimina ugradi."
    if proc.returncode != 0:
        msg = proc.stderr.strip() or "pandoc versiyon kontrolu basarisiz."
        return False, msg[:200]
    return True, "ok"


def check_export_readiness(
    project_root: str | Path,
    fmt: str | None = None,
    chapter_ids: list[str] | None = None,
) -> dict:
    """Validate if project is ready for export."""
    root = Path(project_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    chapters: list[dict] = []
    normalized_fmt = (fmt or "docx").strip().lower()

    manifest_path = root / "book_manifest.yaml"
    if not manifest_path.exists():
        return {
            "ready": False,
            "format": normalized_fmt,
            "errors": ["book_manifest.yaml bulunamadi."],
            "warnings": [],
            "chapters": [],
        }

    manifest = ManifestManager(root).load_or_generate()
    if not manifest.chapters:
        return {
            "ready": False,
            "format": normalized_fmt,
            "errors": ["Manifestte export icin bolum bulunamadi."],
            "warnings": [],
            "chapters": [],
        }

    selected = []
    if chapter_ids:
        for cid in chapter_ids:
            chapter = next(
                (ch for ch in manifest.chapters if _chapter_matches(ch, cid)),
                None,
            )
            if chapter is None:
                errors.append(f"Bölüm manifestte bulunamadi: {cid}")
                continue
            selected.append(chapter)
    else:
        selected = list(manifest.chapters)

    final_required = _final_required_for_export(root)

    for chapter in selected:
        alias = _chapter_alias(chapter)
        resolved_path: Path | None = None
        resolved_kind = ""
        for candidate, kind in _chapter_candidates(root, chapter):
            if candidate.exists():
                resolved_path = candidate
                resolved_kind = kind
                break

        if resolved_path is None:
            errors.append(f"Bölüm içeriği bulunamadi: {alias}")
            chapters.append(
                {
                    "chapter_id": alias,
                    "ready": False,
                    "source": None,
                    "source_kind": None,
                }
            )
            continue

        chapter_ready = True
        if final_required and resolved_kind != "final":
            chapter_ready = False
            errors.append(
                f"Bölüm final.md gerektiriyor ancak farklı kaynak bulundu: {alias}"
            )
        elif resolved_kind in {"draft", "legacy"}:
            warnings.append(f"Bölüm final yerine fallback kaynakla export edilecek: {alias}")

        chapters.append(
            {
                "chapter_id": alias,
                "ready": chapter_ready,
                "source": str(resolved_path.relative_to(root)),
                "source_kind": resolved_kind,
            }
        )

    if normalized_fmt in {"docx", "pdf", "epub", "html"}:
        ok, message = _check_pandoc()
        if not ok:
            errors.append(message)

    return {
        "ready": len(errors) == 0,
        "format": normalized_fmt,
        "final_required_for_export": final_required,
        "errors": errors,
        "warnings": warnings,
        "chapters": chapters,
    }

