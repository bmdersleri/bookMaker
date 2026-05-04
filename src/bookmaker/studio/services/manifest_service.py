"""Manifest servisi — proje manifest, pipeline state, bölüm CRUD."""

from __future__ import annotations

from pathlib import Path

from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.pipeline import PipelineManager


def load_manifest(project_root: str | Path) -> dict:
    """Proje manifest'ini yükler."""
    mgr = ManifestManager(Path(project_root).resolve())
    return mgr.load_or_generate()


def get_pipeline_state(project_root: str | Path) -> dict:
    """Pipeline durumunu döndürür."""
    pm = PipelineManager(Path(project_root).resolve())
    ps = pm.load()
    return {
        "pipeline_id": ps.pipeline_id,
        "current_stage": ps.current_stage,
        "chapters": {
            cid: {
                "current_step": cs.current_step,
                "score": cs.score,
                "decision": cs.decision,
                "error_count": cs.error_count,
                "warning_count": cs.warning_count,
            }
            for cid, cs in ps.chapters.items()
        },
    }


def get_project_info(project_root: str | Path) -> dict:
    """Proje bilgisini döndürür."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    pipe = PipelineManager(root)
    ps = pipe.load()

    ch_count = len(manifest.chapters)
    stages = {"planned": 0, "approved": 0, "full_text_pasted": 0}
    for ch_data in ps.chapters.values():
        s = ch_data.current_step
        if s in stages:
            stages[s] += 1

    return {
        "title": manifest.book.title or "(isimsiz)",
        "chapters": ch_count,
        "author": manifest.book.author or "—",
        "stage": ps.current_stage,
        "stage_counts": stages,
    }


def get_chapter_list(project_root: str | Path) -> list[dict]:
    """Bölüm listesini döndürür."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    pm = PipelineManager(root)
    ps = pm.load()
    result = []
    for ch in manifest.chapters:
        cs = ps.chapters.get(ch.chapter_id)
        result.append({
            "chapter_id": ch.chapter_id,
            "title": ch.title or f"Bölüm {ch.order}",
            "order": ch.order,
            "status": ch.status,
            "current_step": cs.current_step if cs else "planned",
            "score": cs.score if cs else 0,
            "decision": cs.decision if cs else "unknown",
            "errors": cs.error_count if cs else 0,
        })
    return result


def add_chapter(project_root: str | Path, chapter_id: str, title: str,
                order: int | None = None) -> dict:
    """Yeni bölüm ekler."""
    from bookmaker.manifest.models import ManifestChapter

    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    for ch in manifest.chapters:
        if ch.chapter_id == chapter_id:
            return {"error": f"Bölüm zaten var: {chapter_id}"}
    if order is None:
        order = len(manifest.chapters) + 1
    new_ch = ManifestChapter(
        chapter_id=chapter_id, title=title, order=order,
        status="planned",
        source=f"chapters/{chapter_id}/approved/{chapter_id}_v001.md",
    )
    manifest.chapters.append(new_ch)
    manifest.chapters.sort(key=lambda c: c.order)
    mgr.save(manifest)
    return {"chapter_id": chapter_id, "title": title, "order": order}


def remove_chapter(project_root: str | Path, chapter_id: str) -> dict:
    """Bölüm siler."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    for i, ch in enumerate(manifest.chapters):
        if ch.chapter_id == chapter_id:
            manifest.chapters.pop(i)
            for j, c in enumerate(manifest.chapters):
                c.order = j + 1
            mgr.save(manifest)
            return {"chapter_id": chapter_id, "deleted": True}
    return {"error": f"Bölüm bulunamadi: {chapter_id}"}


def reorder_chapters(project_root: str | Path, chapter_ids: list[str]) -> dict:
    """Bölüm sırasını günceller."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    id_map = {ch.chapter_id: ch for ch in manifest.chapters}
    new_order = []
    for cid in chapter_ids:
        if cid in id_map:
            new_order.append(id_map[cid])
    for ch in manifest.chapters:
        if ch not in new_order:
            new_order.append(ch)
    for i, ch in enumerate(new_order):
        ch.order = i + 1
    manifest.chapters = new_order
    mgr.save(manifest)
    return {"reordered": True, "count": len(new_order)}


def update_chapter(project_root: str | Path, chapter_id: str,
                   data: dict) -> dict:
    """Bölüm bilgilerini günceller."""
    root = Path(project_root).resolve()
    mgr = ManifestManager(root)
    manifest = mgr.load_or_generate()
    for ch in manifest.chapters:
        if ch.chapter_id == chapter_id:
            if "title" in data:
                ch.title = data["title"]
            if "order" in data:
                ch.order = data["order"]
            if "status" in data:
                ch.status = data["status"]
            mgr.save(manifest)
            return {"chapter_id": chapter_id, "updated": True}
    return {"error": f"Bölüm bulunamadi: {chapter_id}"}
