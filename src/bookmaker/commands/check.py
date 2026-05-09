"""bookMaker kalite kontrol komutlari."""
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
    from bookmaker.chapter.validation_modes import resolve_validation_profile_from_manifest
    from bookmaker.chapter.validator import validate
    from bookmaker.manifest.models import BookManifest

    if not path.exists():
        console.print(f"[red]Dosya bulunamadı: {path}[/red]")
        raise typer.Exit(1)

    project_root = _find_project_root(path)
    profile = None
    if project_root:
        try:
            profile = resolve_validation_profile_from_manifest(
                BookManifest.load(project_root / "book_manifest.yaml")
            )
        except Exception:
            profile = None

    parsed = parse(path)
    issues = validate(parsed, final_mode=final, profile=profile)
    chapter_id = parsed.frontmatter.get("chapter_id") or parsed.frontmatter.get("chapter-alias")
    if not chapter_id:
        chapter_id = path.parent.parent.name if path.parent.name == "content" else path.stem
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

    # Kitap düzeyi rapor ile bölüm bazlı tablo aynı doğruluk kaynağını
    # temsil etmelidir. validate_book(project_root) kitap raporunu ve
    # bölüm raporlarını ayrı ürettiğinde, bölüm bazlı hata/uyarılar üst
    # rapora yansıtılmazsa CLI çıktısı çelişkili görünür:
    #
    #   Kitap Kalite Raporu: pass
    #   Bölüm Bazlı Durum : bazı bölümler blocked
    #
    # Bu nedenle CLI çıktısı ve JSON raporu için "effective_report"
    # oluşturulur. Bölüm raporları varsa toplam hata/uyarı, en düşük skor,
    # karar ve issue listesi üst rapora yansıtılır.
    chapter_reports = list(result.chapter_reports.values()) if result.chapter_reports else []

    chapter_error_count = sum(cr.error_count for cr in chapter_reports)
    chapter_warning_count = sum(cr.warning_count for cr in chapter_reports)

    effective_error_count = report.error_count + chapter_error_count
    effective_warning_count = report.warning_count + chapter_warning_count

    effective_score = report.score
    if chapter_reports:
        effective_score = min([report.score] + [cr.score for cr in chapter_reports])

    effective_issues = list(report.issues)
    for cr in chapter_reports:
        effective_issues.extend(cr.issues)

    decision_cls = report.decision.__class__
    effective_decision = report.decision

    chapter_has_blocker = any(
        cr.decision.value == "blocked" or cr.error_count > 0
        for cr in chapter_reports
    )

    if effective_error_count > 0 or chapter_has_blocker:
        effective_decision = decision_cls("blocked")
    elif effective_warning_count > 0:
        effective_decision = decision_cls("pass_with_warnings")
    else:
        effective_decision = decision_cls("pass")

    effective_report = report.model_copy(
        update={
            "score": effective_score,
            "decision": effective_decision,
            "error_count": effective_error_count,
            "warning_count": effective_warning_count,
            "issues": effective_issues,
        }
    )

    summary = Table(title="Kitap Kalite Raporu", show_header=True, header_style="bold cyan")
    summary.add_column("Alan", style="cyan")
    summary.add_column("Değer", justify="right")

    decision_color = "green" if effective_report.decision.value in ("pass", "pass_with_warnings") else "red"
    summary.add_row("Skor", f"[bold]{effective_report.score}[/bold]")
    summary.add_row("Karar", f"[{decision_color}]{effective_report.decision.value}[/{decision_color}]")
    summary.add_row("Hatalar", f"[red]{effective_report.error_count}[/red]")
    summary.add_row("Uyarılar", f"[yellow]{effective_report.warning_count}[/yellow]")
    summary.add_row("Toplam Sorun", str(effective_report.error_count + effective_report.warning_count))
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

    if verbose and effective_report.issues:
        issue_table = Table(title="Detaylı Sorun Listesi", show_header=True, header_style="bold")
        issue_table.add_column("Seviye", style="bold")
        issue_table.add_column("Kategori")
        issue_table.add_column("Dosya")
        issue_table.add_column("Satır", justify="right")
        issue_table.add_column("Mesaj")
        for issue in effective_report.issues:
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

    if effective_report.error_count > 0:
        raise typer.Exit(1)


def check_toolchain_command(
    json_output: Annotated[
        bool, typer.Option("--json", help="JSON ciktisi")
    ] = False,
) -> None:
    """Gelistirme araclarinin kurulu olup olmadigini kontrol eder."""
    from bookmaker.core.toolchain import check_toolchain

    result = check_toolchain()

    if json_output:
        import json as _json
        console.print(_json.dumps(result, ensure_ascii=False, indent=2))
    else:
        console.print()
        console.print("[bold cyan]bookMaker Toolchain[/bold cyan]")
        console.print()

        for key, info in result["tools"].items():
            available = info["available"]
            version = info.get("version") or "-"
            if available:
                console.print(f"  [green]✓[/green] {key} {version}")
            else:
                console.print(f"  [yellow]⚠[/yellow] {key} bulunamadi")

        console.print()
        status = result["status"]
        color = "green" if status == "ok" else "yellow" if status == "warning" else "red"
        console.print(f"Status: [{color}]{status}[/{color}]")

        if result["errors"]:
            for err in result["errors"]:
                console.print(f"  [red]HATA:[/red] {err}")
        if result["warnings"]:
            for warn in result["warnings"]:
                console.print(f"  [yellow]UYARI:[/yellow] {warn}")

    raise typer.Exit(0 if result["status"] != "error" else 1)
