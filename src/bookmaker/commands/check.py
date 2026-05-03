from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

console = Console()


def check_chapter_command(
    path: Annotated[Path, typer.Argument(help="Bolum dosyasi (.md)")],
    json_output: Annotated[
        bool, typer.Option("--json", help="JSON raporu build/reports/ altina yaz")
    ] = False,
    final: Annotated[
        bool, typer.Option("--final", help="Cozumsuz placeholder hata sayilir")
    ] = False,
) -> None:
    """Bolumu dogrular ve kalite raporu uretir."""
    from bookmaker.chapter.parser import parse
    from bookmaker.chapter.scoring import make_report
    from bookmaker.chapter.validator import validate

    if not path.exists():
        console.print(f"[red]Dosya bulunamadi: {path}[/red]")
        raise typer.Exit(1)

    parsed = parse(path)
    issues = validate(parsed, final_mode=final)
    chapter_id = parsed.frontmatter.get("chapter_id", path.stem)
    report = make_report(chapter_id, issues)

    # Özet tablosu
    console.print()
    table = Table(title=f"Kalite Raporu — {chapter_id}", show_header=True, header_style="bold")
    table.add_column("Alan", style="cyan")
    table.add_column("Deger", justify="right")
    table.add_row("Skor", str(report.score))
    table.add_row("Karar", str(report.decision.value))
    table.add_row("Hatalar", str(report.error_count))
    table.add_row("Uyarilar", str(report.warning_count))
    console.print(table)

    if issues:
        console.print()
        issue_table = Table(show_header=True, header_style="bold")
        issue_table.add_column("Seviye", style="bold")
        issue_table.add_column("Kategori")
        issue_table.add_column("Satir", justify="right")
        issue_table.add_column("Mesaj")
        for iss in issues:
            color = "red" if iss.severity.value == "error" else "yellow"
            line_str = str(iss.location.line) if iss.location.line else "-"
            issue_table.add_row(
                f"[{color}]{iss.severity.value}[/{color}]",
                iss.category,
                line_str,
                iss.message,
            )
        console.print(issue_table)

    if json_output:
        report_dir = Path("build") / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{chapter_id}_quality_report.json"
        report_path.write_text(
            report.model_dump_json(indent=2),
            encoding="utf-8",
        )
        console.print(f"\n[dim]JSON raporu: {report_path}[/dim]")

    if report.error_count > 0:
        raise typer.Exit(1)
