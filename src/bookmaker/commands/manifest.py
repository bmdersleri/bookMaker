"""bookmaker manifest komutları."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.manifest.manager import ManifestManager
from bookmaker.manifest.pipeline import PipelineManager

console = Console()
manifest_app = typer.Typer(help="Manifest ve pipeline islemleri.")


@manifest_app.command("view")
def view_manifest(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """Kitap manifestini gosterir."""
    mgr = ManifestManager(path)
    manifest = mgr.load_or_generate()

    if not manifest.book.title:
        console.print("[yellow]Manifest bulunamadi.[/yellow]")

    console.print(f"\n[bold]Kitap:[/bold] {manifest.book.title or '(isimsiz)'}")
    console.print(f"[bold]Yazar:[/bold] {manifest.book.author or '-'}")
    console.print(f"[bold]Dil:[/bold] {manifest.book.lang}")
    console.print(f"[bold]Profil:[/bold] {manifest.book.automation_profile}")
    console.print(f"\n[bold]Bolumler ({len(manifest.chapters)}):[/bold]")

    table = Table(show_header=True)
    table.add_column("No", justify="right", style="cyan")
    table.add_column("ID")
    table.add_column("Baslik")
    table.add_column("Kaynak")
    for ch in manifest.chapters:
        table.add_row(str(ch.order), ch.chapter_id, ch.title, ch.source)
    console.print(table)


@manifest_app.command("list-chapters")
def list_chapters(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """Bolumleri listeler."""
    mgr = ManifestManager(path)
    manifest = mgr.load_or_generate()

    if not manifest.chapters:
        console.print("[yellow]Bolum bulunamadi.[/yellow]")
        raise typer.Exit()

    console.print(f"\n[bold]{len(manifest.chapters)} bolum:[/bold]")
    for ch in manifest.chapters:
        status = ""
        pipeline = PipelineManager(path)
        ps = pipeline.load()
        if ch.chapter_id in ps.chapters:
            cs = ps.chapters[ch.chapter_id]
            status = f" [{cs.current_step}]"
        console.print(f"  {ch.order}. {ch.chapter_id} — {ch.title}{status}")


@manifest_app.command("validate")
def validate_manifest(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """Manifesti dogrular."""
    mgr = ManifestManager(path)
    issues = mgr.validate()

    if not issues:
        console.print("[green]Manifest gecerli.[/green]")
        return
    for iss in issues:
        console.print(f"  - {iss}")
    raise typer.Exit(1)


@manifest_app.command("pipeline")
def view_pipeline(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """Pipeline durumunu gosterir."""
    mgr = PipelineManager(path)
    state = mgr.load()

    if not state.book_id:
        console.print("[yellow]Pipeline durumu bulunamadi.[/yellow]")
        return

    console.print(f"\n[bold]Kitap ID:[/bold] {state.book_id}")
    console.print(f"[bold]Asama:[/bold] {state.current_stage}")

    if state.chapters:
        table = Table(show_header=True)
        table.add_column("Bolum ID")
        table.add_column("Adim")
        table.add_column("Skor", justify="right")
        table.add_column("Karar")
        for cid, cs in state.chapters.items():
            table.add_row(cid, cs.current_step, str(cs.score), cs.decision)
        console.print(table)
