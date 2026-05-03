from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from bookmaker.core.ids import new_event_id
from bookmaker.core.time import now_iso
from bookmaker.models.versioning import ActiveVersion, ChapterStep, EventType, VersionEvent
from bookmaker.storage.files import active_version_path, append_event, version_log_path
from bookmaker.storage.sqlite import ensure_schema

console = Console()

PRESETS = ["java-temelleri"]


def init_command(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
    preset: Annotated[str, typer.Option("--preset", help=f"Kitap preseti: {PRESETS}")] = "",
    author: Annotated[str, typer.Option("--author", help="Yazar adi")] = "",
) -> None:
    """Yeni bir bookmaker kitap projesi olusturur."""
    if preset and preset not in PRESETS:
        console.print(f"[red]Bilinmeyen preset: {preset}[/red]")
        console.print(f"Gecerli presetler: {', '.join(PRESETS)}")
        raise typer.Exit(1)

    project_root = path.resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    # Preset seç
    if preset == "java-temelleri":
        from bookmaker.templates.presets.java_temelleri import (
            make_book_architecture,
            make_book_profile,
        )
        book_id = project_root.name.lower().replace("-", "_").replace(" ", "_")
        profile = make_book_profile(book_id=book_id, author=author)
        architecture = make_book_architecture(book_id=book_id)
    else:
        console.print("[yellow]Preset belirtilmedi, bos proje olusturuluyor.[/yellow]")
        from bookmaker.models.book import BookArchitecture, BookProfile
        book_id = project_root.name.lower().replace("-", "_").replace(" ", "_")
        profile = BookProfile(book_id=book_id, title=project_root.name, author=author)
        architecture = BookArchitecture(book_id=book_id)

    # book_profile.yaml
    profile.to_yaml(project_root / "book_profile.yaml")

    # book_architecture.yaml
    architecture.to_yaml(project_root / "book_architecture.yaml")

    # Dizin yapısı
    for subdir in ["chapters", "prompts", "assets/images", "assets/mermaid",
                   "assets/screenshots", "assets/qr", "build/merged",
                   "build/code", "build/reports", "exports/docx"]:
        (project_root / subdir).mkdir(parents=True, exist_ok=True)

    # Her bölüm için workspace
    for chapter in architecture.chapters:
        cid = chapter.chapter_id
        ws = project_root / "chapters" / cid
        for sub in ["seed", "outline_versions", "draft_versions", "approved", "technical_reports"]:
            (ws / sub).mkdir(parents=True, exist_ok=True)

        # active_version.yaml
        av = ActiveVersion(chapter_id=cid, current_step=ChapterStep.planned)
        av.to_yaml(active_version_path(project_root, cid))

        # version_log.jsonl — ilk event
        ev = VersionEvent(
            event_id=new_event_id(),
            created_at=now_iso(),
            chapter_id=cid,
            event_type=EventType.seed_created,
            notes="init ile olusturuldu",
        )
        append_event(version_log_path(project_root, cid), ev)

    # SQLite
    db_path = project_root / "bookmaker.sqlite"
    ensure_schema(db_path)

    # pipeline_state.yaml (minimal)
    from ruamel.yaml import YAML
    _yaml = YAML()
    state = {
        "book_id": profile.book_id,
        "pipeline_id": profile.quality_profile,
        "current_stage": "authoring",
        "chapters": {c.chapter_id: {"current_step": "planned"} for c in architecture.chapters},
    }
    with open(project_root / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        _yaml.dump(state, f)

    # Özet
    console.print(Panel(
        f"[green]Proje olusturuldu:[/green] {project_root}\n"
        f"Kitap ID : {profile.book_id}\n"
        f"Baslik   : {profile.title}\n"
        f"Bolumler : {len(architecture.chapters)}\n"
        f"Preset   : {preset or 'bos'}",
        title="bookmaker init",
        border_style="green",
    ))
