# ruff: noqa: E501
from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

console = Console()


def _find_project_root(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / "book_manifest.yaml").exists():
            return candidate
    return None


def check_chapter_command(
    path: Annotated[Path, typer.Argument(help="Bölüm dosyası (.md)")],
    json_output: Annotated[bool, typer.Option("--json", help="JSON raporu logs/reviews altına yaz")] = False,
    final: Annotated[bool, typer.Option("--final", help="Çözümsüz placeholder hata sayılır")] = False,
) -> None:
    """Bölüm Markdown dosyasını doğrular ve kalite raporu üretir."""
    from bookmaker.chapter.parser import parse
    from bookmaker.chapter.scoring import make_report
    from bookmaker.chapter.validator import validate

    if not path.exists():
        console.print(f"[red]Dosya bulunamadı: {path}[/red]")
        raise typer.Exit(1)

    parsed = parse(path)
    issues = validate(parsed, final_mode=final)
    chapter_id = (
        parsed.frontmatter.get("chapter_id")
        or parsed.frontmatter.get("chapter-alias")
        or path.parent.parent.name
        if path.parent.name == "content"
        else path.stem
    )
    report = make_report(str(chapter_id), issues)

    table = Table(title=f"Kalite Raporu — {chapter_id}", show_header=True, header_style="bold")
    table.add_column("Alan", style="cyan")
    table.add_column("Değer", justify="right")
    table.add_row("Skor", str(report.score))
    table.add_row("Karar", str(report.decision.value))
    table.add_row("Hatalar", str(report.error_count))
    table.add_row("Uyarılar", str(report.warning_count))
    console.print(table)

    if issues:
        issue_table = Table(show_header=True, header_style="bold")
        issue_table.add_column("Seviye", style="bold")
        issue_table.add_column("Kategori")
        issue_table.add_column("Satır", justify="right")
        issue_table.add_column("Mesaj")
        for issue in issues:
            color = "red" if issue.severity.value == "error" else "yellow"
            line_str = str(issue.location.line) if issue.location.line else "-"
            issue_table.add_row(
                f"[{color}]{issue.severity.value}[/{color}]",
                issue.category,
                line_str,
                issue.message,
            )
        console.print(issue_table)

    if json_output:
        project_root = _find_project_root(path)
        report_dir = (project_root / "logs" / "reviews") if project_root else Path("logs") / "reviews"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{chapter_id}_quality_report.json"
        report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        console.print(f"\n[dim]JSON raporu: {report_path}[/dim]")

    if report.error_count > 0:
        raise typer.Exit(1)


def check_book_command(
    target: Annotated[
        Path,
        typer.Argument(help="Kitap proje kökü veya chapters dizini", show_default=True),
    ] = Path("."),
    json_output: Annotated[bool, typer.Option("--json", help="JSON raporu logs/reviews altına yaz")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Ayrıntılı çıktı")] = False,
) -> None:
    """Project-based kitap projesini manifest tabanlı doğrular."""
    from bookmaker.chapter.book_validator import validate_book

    target = target.resolve()
    project_root = target.parent if target.name == "chapters" else target

    console.print()
    console.print("[bold cyan]Kitap Düzeyinde Validasyon[/bold cyan]")
    console.print(f"    project_root : {project_root}")
    console.print()

    if not project_root.exists():
        console.print(f"[red]HATA: proje dizini bulunamadı: {project_root}[/red]")
        raise typer.Exit(1)

    result = validate_book(project_root)
    report = result.report

    summary = Table(title="Kitap Kalite Raporu", show_header=True, header_style="bold cyan")
    summary.add_column("Alan", style="cyan")
    summary.add_column("Değer", justify="right")

    decision_color = "green" if report.decision.value in ("pass", "pass_with_warnings") else "red"
    summary.add_row("Skor", f"[bold]{report.score}[/bold]")
    summary.add_row("Karar", f"[{decision_color}]{report.decision.value}[/{decision_color}]")
    summary.add_row("Hatalar", f"[red]{report.error_count}[/red]")
    summary.add_row("Uyarılar", f"[yellow]{report.warning_count}[/yellow]")
    summary.add_row("Toplam Sorun", str(report.error_count + report.warning_count))
    console.print(summary)

    if result.chapter_reports:
        ch_table = Table(title="Bölüm Bazlı Durum", show_header=True, header_style="bold")
        ch_table.add_column("Sıra", justify="right")
        ch_table.add_column("Alias", style="cyan")
        ch_table.add_column("Skor", justify="right")
        ch_table.add_column("Hata", justify="right")
        ch_table.add_column("Uyarı", justify="right")
        ch_table.add_column("Karar", style="bold")
        for alias in result.chapter_order:
            cr = result.chapter_reports.get(alias)
            order = str(result.chapter_orders.get(alias, "-"))
            if cr is None:
                ch_table.add_row(order, alias, "--", "--", "--", "[red]KAYIP[/red]")
                continue
            d_color = "green" if cr.decision.value in ("pass", "pass_with_warnings") else "red"
            ch_table.add_row(
                order,
                alias,
                str(cr.score),
                str(cr.error_count),
                str(cr.warning_count),
                f"[{d_color}]{cr.decision.value}[/{d_color}]",
            )
        console.print(ch_table)

    if verbose and report.issues:
        issue_table = Table(title="Detaylı Sorun Listesi", show_header=True, header_style="bold")
        issue_table.add_column("Seviye", style="bold")
        issue_table.add_column("Kategori")
        issue_table.add_column("Dosya")
        issue_table.add_column("Satır", justify="right")
        issue_table.add_column("Mesaj")
        for issue in report.issues:
            color = "red" if issue.severity.value == "error" else "yellow"
            file_short = issue.location.file or "-"
            line_str = str(issue.location.line) if issue.location.line else "-"
            issue_table.add_row(
                f"[{color}]{issue.severity.value}[/{color}]",
                issue.category,
                file_short,
                line_str,
                issue.message,
            )
        console.print(issue_table)

    if json_output:
        report_dir = project_root / "logs" / "reviews"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "book_quality_report.json"
        report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        console.print(f"\n[dim]JSON raporu: {report_path}[/dim]")

        chapter_dir = report_dir / "chapters"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        for alias, chapter_report in result.chapter_reports.items():
            (chapter_dir / f"{alias}_quality_report.json").write_text(
                chapter_report.model_dump_json(indent=2),
                encoding="utf-8",
            )

    if report.error_count > 0:
        raise typer.Exit(1)
