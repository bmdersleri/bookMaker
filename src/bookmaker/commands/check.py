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


# ---------------------------------------------------------------------------
# book check -- tüm kitap validasyonu
# ---------------------------------------------------------------------------

def check_book_command(
    chapters_dir: Annotated[
        str, typer.Argument(help="chapters/ dizini (varsayilan: chapters)")
    ] = "chapters",
    images_dir: Annotated[
        str, typer.Option("--images", "-i", help="build/output/images dizini")
    ] = "build/output/images",
    json_output: Annotated[
        bool, typer.Option("--json", help="JSON raporu build/reports/ altina yaz")
    ] = False,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Ayrintili cikti")
    ] = False,
) -> None:
    """Tum kitabi (27 bolum) dogrular ve kitap duzeyinde kalite raporu uretir."""
    from bookmaker.chapter.book_validator import CHAPTER_ORDER, validate_book

    console.print()
    console.print("[bold cyan]Kitap Duzeyinde Validasyon[/bold cyan]")
    console.print(f"    chapters/  : {Path(chapters_dir).resolve()}")
    console.print(f"    images/    : {Path(images_dir).resolve() if Path(images_dir).exists() else '(yok)'}")
    console.print()

    chapters_path = Path(chapters_dir)
    images_path = Path(images_dir) if Path(images_dir).exists() else None

    if not chapters_path.exists():
        console.print(f"[red]HATA: chapters dizini bulunamadi: {chapters_path}[/red]")
        raise typer.Exit(1)

    result = validate_book(chapters_path, images_path)
    report = result.report

    # ---- ÖZET TABLOSU ----
    console.print()
    summary = Table(title="Kitap Kalite Raporu", show_header=True, header_style="bold cyan")
    summary.add_column("Alan", style="cyan")
    summary.add_column("Deger", justify="right")

    decision_color = "green" if report.decision.value in ("pass", "pass_with_warnings") else "red"
    summary.add_row("Skor", f"[bold]{report.score}[/bold]")
    summary.add_row("Karar", f"[{decision_color}]{report.decision.value}[/{decision_color}]")
    summary.add_row("Hatalar", f"[red]{report.error_count}[/red]")
    summary.add_row("Uyarilar", f"[yellow]{report.warning_count}[/yellow]")
    summary.add_row("Toplam Sorun", str(report.error_count + report.warning_count))

    # Bölüm istatistikleri
    if result.chapter_sizes:
        sizes = list(result.chapter_sizes.values())
        total_chars = sum(sizes)
        avg_char = total_chars / len(sizes)
        min_char = min(sizes)
        max_char = max(sizes)
        summary.add_row("Toplam Boyut", f"{total_chars:,} bytes")
        summary.add_row("Ortalama", f"{avg_char:,.0f} bytes")
        summary.add_row("En Kisa", f"{min_char:,} bytes")
        summary.add_row("En Uzun", f"{max_char:,} bytes")

    console.print(summary)

    # ---- BÖLÜM BAZLI SKORLAR ----
    if result.chapter_reports:
        console.print()
        ch_table = Table(title="Bolum Bazli Skorlar", show_header=True, header_style="bold")
        ch_table.add_column("Bölüm", style="cyan")
        ch_table.add_column("Skor", justify="right")
        ch_table.add_column("Hata", justify="right")
        ch_table.add_column("Uyari", justify="right")
        ch_table.add_column("Karar", style="bold")
        for slug in CHAPTER_ORDER:
            if slug not in result.chapter_reports:
                ch_table.add_row(slug, "--", "--", "--", "[red]KAYIP[/red]")
                continue
            cr = result.chapter_reports[slug]
            d_color = "green" if cr.decision.value in ("pass", "pass_with_warnings") else "red"
            ch_table.add_row(
                slug,
                str(cr.score),
                str(cr.error_count),
                str(cr.warning_count),
                f"[{d_color}]{cr.decision.value}[/{d_color}]",
            )
        console.print(ch_table)

    # ---- SORUN LISTESI (verbose mod) ----
    if verbose and report.issues:
        console.print()
        iss_table = Table(title="Detayli Sorun Listesi", show_header=True, header_style="bold")
        iss_table.add_column("Seviye", style="bold")
        iss_table.add_column("Kategori")
        iss_table.add_column("Dosya")
        iss_table.add_column("Satir", justify="right")
        iss_table.add_column("Mesaj")
        for iss in report.issues:
            color = "red" if iss.severity.value == "error" else "yellow"
            line_str = str(iss.location.line) if iss.location.line else "-"
            file_short = iss.location.file.split("/")[-1] if iss.location.file else "-"
            iss_table.add_row(
                f"[{color}]{iss.severity.value}[/{color}]",
                iss.category,
                file_short,
                line_str,
                iss.message,
            )
        console.print(iss_table)

    # ---- ÖZET ----
    console.print()
    if report.error_count > 0:
        console.print(f"[red]{report.error_count} hata bulundu. Kitap revize gerektiriyor.[/red]")
    elif report.warning_count > 0:
        console.print(f"[yellow]{report.warning_count} uyari bulundu, hata yok.[/yellow]")
    else:
        console.print("[green]Kitap temiz! Hata veya uyari yok.[/green]")

    # ---- JSON ÇIKTISI ----
    if json_output:
        report_dir = Path("build") / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "book_quality_report.json"
        report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
        console.print(f"\n[dim]JSON raporu: {report_path}[/dim]")

        # Bölüm bazlı JSON'lar
        ch_dir = report_dir / "chapters"
        ch_dir.mkdir(parents=True, exist_ok=True)
        for slug, cr in result.chapter_reports.items():
            ch_path = ch_dir / f"{slug}_quality_report.json"
            ch_path.write_text(cr.model_dump_json(indent=2), encoding="utf-8")

    if report.error_count > 0:
        raise typer.Exit(1)
