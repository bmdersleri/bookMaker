"""bookmaker chapter CLI komutları."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from bookmaker.authoring.pipeline import AuthoringPipeline

console = Console()
chapter_app = typer.Typer(help="Bolum yazim islemleri.")


@chapter_app.command("seed")
def seed_chapter(
    chapter_id: Annotated[str, typer.Argument(help="Bolum ID")],
    purpose: Annotated[str, typer.Option("--purpose", "-p", help="Bolum amaci")] = "",
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """Bolum tohumu olusturur."""
    pipe = AuthoringPipeline(path)
    kwargs = {}
    if purpose:
        kwargs["purpose"] = purpose
    seed = pipe.seed(chapter_id, **kwargs)
    console.print(f"[green]Seed olusturuldu:[/green] {chapter_id}")
    console.print(f"  Amac: {seed.purpose or '(bos)'}")


@chapter_app.command("outline")
def outline_command(
    chapter_id: Annotated[str, typer.Argument(help="Bolum ID")],
    action: Annotated[str, typer.Argument(help="Islem: prompt / paste / review")] = "prompt",
    text: Annotated[str, typer.Option("--text", "-t", help="Yapistirilacak outline metni")] = "",
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """Outline islemleri: prompt uret, yapistir, degerlendir."""
    pipe = AuthoringPipeline(path)

    if action == "prompt":
        prompt = pipe.make_outline_prompt(chapter_id)
        console.print(prompt)

    elif action == "paste":
        if not text:
            console.print("[red]--text parametresi gerekli.[/red]")
            raise typer.Exit(1)
        p = pipe.paste_outline(chapter_id, text)
        console.print(f"[green]Outline kaydedildi:[/green] {p}")

    elif action == "review":
        result = pipe.review_outline(chapter_id)
        if result.get("decision") == "pass":
            console.print(f"[green]Outline gecerli. Karar: {result['decision']}[/green]")
        else:
            console.print(f"[red]Outline sorunlu. Karar: {result['decision']}[/red]")
            for iss in result.get("issues", []):
                console.print(f"  - {iss}")

    else:
        console.print(f"[red]Bilinmeyen eylem: {action}[/red]")


@chapter_app.command("draft")
def draft_command(
    chapter_id: Annotated[str, typer.Argument(help="Bolum ID")],
    action: Annotated[str, typer.Argument(help="Islem: prompt / paste / review")] = "prompt",
    text: Annotated[str, typer.Option("--text", "-t", help="Yapistirilacak taslak metni")] = "",
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """Draft islemleri: prompt uret, yapistir, degerlendir."""
    pipe = AuthoringPipeline(path)

    if action == "prompt":
        prompt = pipe.make_draft_prompt(chapter_id)
        console.print(prompt)

    elif action == "paste":
        if not text:
            console.print("[red]--text parametresi gerekli.[/red]")
            raise typer.Exit(1)
        p = pipe.paste_draft(chapter_id, text)
        console.print(f"[green]Draft kaydedildi:[/green] {p}")

    elif action == "review":
        result = pipe.review_draft(chapter_id)
        console.print(
            f"Skor: {result['score']}, Karar: {result['decision']}, "
            f"Hata: {result['error_count']}, Uyari: {result['warning_count']}"
        )

    else:
        console.print(f"[red]Bilinmeyen eylem: {action}[/red]")


@chapter_app.command("approve")
def approve_chapter(
    chapter_id: Annotated[str, typer.Argument(help="Bolum ID")],
    path: Annotated[Path, typer.Option("--path", help="Proje dizini")] = Path("."),
) -> None:
    """Bolumu onaylar (draft -> approved)."""
    pipe = AuthoringPipeline(path)
    try:
        ap = pipe.approve(chapter_id)
        console.print(f"[green]Bolum onaylandi:[/green] {ap}")
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)
