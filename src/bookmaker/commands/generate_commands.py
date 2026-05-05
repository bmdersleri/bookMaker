"""bookmaker generate CLI komutları."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.generation.pipeline import ChapterGenerator as GenerationPipeline
from bookmaker.llm.config import LLMConfig

console = Console()
generate_app = typer.Typer(help="LLM ile icerik uretimi.")


@generate_app.command("chapter")
def generate_chapter(
    chapter_id: Annotated[str, typer.Argument(help="Bolum ID")],
    title: Annotated[str, typer.Option("--title", "-t", help="Bolum basligi")] = "",
    purpose: Annotated[str, typer.Option("--purpose", "-p", help="Bolum amaci")] = "",
    concepts: Annotated[
        str, typer.Option("--concepts", "-c", help="Zorunlu kavramlar (virgulle ayrilmis)")
    ] = "",
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """LLM ile bolum metni uretir."""
    cfg = LLMConfig(path)
    if not cfg.is_configured():
        console.print("[red]LLM yapilandirilmamis. Once 'bookmaker llm configure' calistir.[/red]")
        raise typer.Exit(1)

    pipe = GenerationPipeline(path)
    concept_list = [c.strip() for c in concepts.split(",") if c.strip()] if concepts else None

    console.print(f"[bold]Bolum uretiliyor:[/bold] {chapter_id}")

    try:
        result = pipe.generate_chapter_with_spec(
            chapter_id=chapter_id,
            title=title or chapter_id,
            concepts=concept_list or [],
        )
        console.print(f"[green]Bolum uretildi ({len(result.get('final', ''))} karakter).[/green]")
    except RuntimeError as e:
        console.print(f"[red]Hata: {e}[/red]")
        raise typer.Exit(1)


@generate_app.command("outline")
def generate_outline(
    chapter_id: Annotated[str, typer.Argument(help="Bolum ID")],
    topic: Annotated[str, typer.Option("--topic", "-t", help="Konu")],
    purpose: Annotated[str, typer.Option("--purpose", "-p", help="Amac")] = "",
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """LLM ile outline uretir."""
    cfg = LLMConfig(path)
    if not cfg.is_configured():
        console.print("[red]LLM yapilandirilmamis.[/red]")
        raise typer.Exit(1)

    pipe = GenerationPipeline(path)
    console.print(f"[bold]Outline uretiliyor:[/bold] {chapter_id} — {topic}")

    try:
        outline = pipe.generate_outline(chapter_id, topic, purpose)
        console.print("\n[green]Outline uretildi:[/green]\n")
        console.print(outline)
    except RuntimeError as e:
        console.print(f"[red]Hata: {e}[/red]")
        raise typer.Exit(1)


@generate_app.command("book")
def generate_book(
    topic: Annotated[str, typer.Argument(help="Kitap konusu")],
    language: Annotated[str, typer.Option("--lang", "-l", help="Dil")] = "tr-TR",
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """LLM ile kitap uretir (outline + ilk 3 bolum)."""
    cfg = LLMConfig(path)
    if not cfg.is_configured():
        console.print("[red]LLM yapilandirilmamis.[/red]")
        raise typer.Exit(1)

    pipe = GenerationPipeline(path)
    console.print(f"[bold]Kitap uretiliyor:[/bold] {topic}")

    try:
        result = pipe.generate_full_book(topic, language)

        table = Table(title="Kitap Uretim Raporu", show_header=True)
        table.add_column("Asama", style="cyan")
        table.add_column("Durum")
        table.add_row("Konu", topic)
        table.add_row("Outline", f"{len(result.get('outline', ''))} karakter")
        table.add_row("Bolumler", str(len(result.get('chapters', []))))

        for ch in result.get("chapters", []):
            status_color = "green" if ch["status"] == "generated" else "red"
            table.add_row(f"  {ch['id']}", f"[{status_color}]{ch['status']}[/{status_color}]")

        console.print(table)

    except RuntimeError as e:
        console.print(f"[red]Hata: {e}[/red]")
        raise typer.Exit(1)
