"""bookmaker build komutları."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.build.pipeline import build_chapter

console = Console()


def build_chapter_command(
    path: Annotated[Path, typer.Argument(help="Bolum dosyasi (.md)")],
    json_output: Annotated[
        bool, typer.Option("--json", help="JSON raporu build/reports/ altina yaz")
    ] = False,
) -> None:
    """Bolumdeki Java kodlarini cikarir, derler ve raporlar."""
    if not path.exists():
        console.print(f"[red]Dosya bulunamadi: {path}[/red]")
        raise typer.Exit(1)

    report = build_chapter(path)

    # Özet
    console.print()
    table = Table(title=f"Build Raporu — {report['chapter']}", show_header=True)
    table.add_column("Asama", style="cyan")
    table.add_column("Deger", justify="right")
    table.add_row("Kod Blogu", str(report["total_code_blocks"]))
    table.add_row("Cikarilan", str(report["extracted"]))
    table.add_row("Atlanan", str(report["skipped"]))
    table.add_row("Cikarma Hatasi", f"[red]{report['extract_errors']}[/red]")
    table.add_row("Derlenen", f"[green]{report['compiled']}[/green]")
    table.add_row("Derleme Hatasi", f"[red]{report['compile_failed']}[/red]")
    console.print(table)

    # Derleme detayları
    if report["compile_results"]:
        console.print()
        detay = Table(show_header=True)
        detay.add_column("Kod ID", style="bold")
        detay.add_column("Dosya")
        detay.add_column("Durum")
        for cr in report["compile_results"]:
            status = cr.get("compile_status", "?")
            color = "green" if status == "passed" else "red"
            detay.add_row(
                cr.get("code_id", "?"),
                Path(cr.get("file", "")).name,
                f"[{color}]{status}[/{color}]",
            )
        console.print(detay)

    if json_output:
        report_dir = Path("build") / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{report['chapter']}_build_report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"\n[dim]JSON raporu: {report_path}[/dim]")

    if report["compile_failed"] > 0 or report["extract_errors"] > 0:
        raise typer.Exit(1)
