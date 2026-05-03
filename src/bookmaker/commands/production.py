"""bookmaker production CLI komutları."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.production.pandoc import pandoc_available
from bookmaker.production.pipeline import run as run_production

console = Console()
production_app = typer.Typer(help="Production islemleri.")


@production_app.command("full")
def full_build(
    path: Annotated[Path, typer.Argument(help="Bolum dosyasi (.md)")],
    check_pandoc: Annotated[
        bool, typer.Option("--check-pandoc", help="Pandoc varligini kontrol et")
    ] = False,
) -> None:
    """Full production build: derle + mermaid + qr + docx."""
    if not path.exists():
        console.print(f"[red]Dosya bulunamadi: {path}[/red]")
        raise typer.Exit(1)

    if check_pandoc and not pandoc_available():
        console.print("[yellow]Uyari: pandoc PATH'te bulunamadi. DOCX export atlanabilir.[/yellow]")

    console.print(f"\n[bold]Production build basliyor: {path.stem}[/bold]")

    result = run_production(path)

    table = Table(title="Production Build Raporu", show_header=True)
    table.add_column("Asama", style="cyan")
    table.add_column("Durum", justify="right")

    # Build
    b = result.get("build", {})
    table.add_row("Derleme", f"{b.get('compiled', 0)}/{b.get('extracted', 0)} gecti")

    # Mermaid
    m = result.get("mermaid", [])
    m_passed = sum(1 for r in m if r["status"] == "passed")
    table.add_row("Mermaid", f"{m_passed}/{len(m)}")

    # QR
    q = result.get("qrcode", [])
    q_passed = sum(1 for r in q if r["status"] == "passed")
    table.add_row("QR", f"{q_passed}/{len(q)}")

    # DOCX
    d = result.get("docx", {})
    table.add_row("DOCX", d.get("status", "-"))

    console.print(table)

    errors = (b.get("compile_failed", 0) or 0)
    if errors:
        raise typer.Exit(1)


@production_app.command("mermaid")
def render_mermaid(
    path: Annotated[Path, typer.Argument(help="Bolum dosyasi (.md)")],
) -> None:
    """Mermaid semalarini PNG'ye donusturur."""
    from bookmaker.production.mermaid import render_from_file

    if not path.exists():
        console.print(f"[red]Dosya bulunamadi: {path}[/red]")
        raise typer.Exit(1)

    out_dir = Path("build") / "assets" / "mermaid"
    results = render_from_file(path, out_dir)

    passed = sum(1 for r in results if r["status"] == "passed")
    console.print(f"\nMermaid: {passed}/{len(results)} render edildi.")
    if passed < len(results):
        raise typer.Exit(1)


@production_app.command("docx")
def export_to_docx(
    path: Annotated[Path, typer.Argument(help="Bolum dosyasi (.md)")],
) -> None:
    """Markdown bolumunu DOCX'e donusturur."""
    from bookmaker.production.pandoc import export_docx

    if not path.exists():
        console.print(f"[red]Dosya bulunamadi: {path}[/red]")
        raise typer.Exit(1)

    out_dir = Path("build") / "exports"
    out = out_dir / f"{path.stem}.docx"
    result = export_docx(path, out)

    if result["status"] == "passed":
        console.print(f"[green]DOCX export basarili: {result['path']}[/green]")
    else:
        console.print(f"[red]DOCX export basarisiz: {result['error']}[/red]")
        raise typer.Exit(1)
