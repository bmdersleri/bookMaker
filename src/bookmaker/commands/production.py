"""bookmaker production CLI komutlari — BookConfig destekli."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.core.config import BookConfig, load_config
from bookmaker.production.pandoc import pandoc_available
from bookmaker.production.pipeline import run as run_production

console = Console()
production_app = typer.Typer(help="Production islemleri.")


def _resolve_config(project: str | None = None,
                    path: Path | None = None) -> BookConfig:
    """Config'i cozumler — path varsa ondan, yoksa proje adindan."""
    try:
        if path:
            return load_config(start=path.parent if path.is_file() else path)
        return load_config(book_name=project or "java-temelleri")
    except Exception as e:
        console.print(f"[yellow]Uyari: Config yuklenemedi: {e}[/yellow]")
        return None


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

    config = _resolve_config(path=path)

    if check_pandoc and not pandoc_available():
        console.print("[yellow]Uyari: pandoc PATH'te bulunamadi. DOCX export atlanabilir.[/yellow]")

    console.print(f"\n[bold]Production build basliyor: {path.stem}[/bold]")
    if config:
        console.print(f"  Kitap: {config.title} ({config.book_id})")
        console.print(f"  Referans DOCX: {config.reference_docx_path}")
        console.print(f"  Lua filter:    {config.lua_filter_path}")

    result = run_production(path, config=config)

    table = Table(title="Production Build Raporu", show_header=True)
    table.add_column("Asama", style="cyan")
    table.add_column("Durum", justify="right")

    b = result.get("build", {})
    table.add_row("Derleme", f"{b.get('compiled', 0)}/{b.get('extracted', 0)} gecti")

    m = result.get("mermaid", [])
    m_passed = sum(1 for r in m if r["status"] == "passed")
    table.add_row("Mermaid", f"{m_passed}/{len(m)}")

    q = result.get("qrcode", [])
    q_passed = sum(1 for r in q if r["status"] == "passed")
    table.add_row("QR", f"{q_passed}/{len(q)}")

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

    config = _resolve_config(path=path)
    out_dir = config.mermaid_dir if config else Path("exports") / "assets" / "mermaid"
    results = render_from_file(path, out_dir, config=config)

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

    config = _resolve_config(path=path)
    out_dir = config.exports_dir if config else Path("exports")
    out = out_dir / f"{path.stem}.docx"
    result = export_docx(path, out, config=config)

    if result["status"] == "passed":
        console.print(f"[green]DOCX export basarili: {result['path']}[/green]")
    else:
        console.print(f"[red]DOCX export basarisiz: {result.get('error')}[/red]")
        raise typer.Exit(1)


@production_app.command("info")
def show_info(
    project: Annotated[str | None, typer.Option("--project", "-p",
                        help="Proje adi (varsayilan: java-temelleri)")] = None,
) -> None:
    """Kitap yapilandirma bilgisini gosterir."""
    try:
        config = _resolve_config(project=project)
    except Exception as e:
        console.print(f"[red]Hata: {e}[/red]")
        raise typer.Exit(1)

    if not config:
        console.print("[red]Config bulunamadi.[/red]")
        raise typer.Exit(1)

    table = Table(title=f"Kitap Profili: {config.title}", show_header=True)
    table.add_column("Alan", style="cyan")
    table.add_column("Deger")

    table.add_row("Kitap ID", config.book_id)
    table.add_row("Yazar", config.author)
    table.add_row("Seviye", config.level)
    table.add_row("Bolum Sayisi", str(config.chapter_count))
    table.add_row("Onayli Bolum", f"{len(config.approved_chapters)}/{config.chapter_count}")
    table.add_row("Toplam Kelime", f"{config.total_words:,}")
    table.add_row("Mermaid Diyagram", str(config.total_mermaid_diagrams))
    table.add_row("Referans DOCX", str(config.reference_docx_path) or "-")
    table.add_row("Lua Filter", str(config.lua_filter_path) or "-")
    table.add_row("DOCX Cikti", str(config.output_docx_path))
    table.add_row("Mermaid PNG Dizini", str(config.mermaid_dir))
    table.add_row("DOCX Aktif", "Evet" if config.docx_enabled else "Hayir")
    table.add_row("PDF Aktif", "Evet" if config.pdf_enabled else "Hayir")
    table.add_row("Proje Koku", str(config.project_root))

    console.print(table)

    # Bolum listesi
    chapter_table = Table(title="Bolum Listesi", show_header=True)
    chapter_table.add_column("#", style="dim")
    chapter_table.add_column("ID")
    chapter_table.add_column("Baslik")
    chapter_table.add_column("Durum")

    for i, c in enumerate(config.chapters, 1):
        cid = c.get("chapter_id", "")
        title = c.get("title", {})
        if isinstance(title, dict):
            title = title.get("tr", cid)
        status = c.get("status", "?")
        chapter_table.add_row(str(i), cid, title, status)

    console.print(chapter_table)


@production_app.command("build-all")
def build_all_chapters(
    project: Annotated[str | None, typer.Option("--project", "-p",
                        help="Proje adi")] = None,
) -> None:
    """Tum onaylanmis bolumleri tek tek DOCX'e donusturur."""
    from bookmaker.production.pandoc import export_all_chapters

    config = _resolve_config(project=project)
    if not config:
        console.print("[red]Config bulunamadi.[/red]")
        raise typer.Exit(1)

    results = export_all_chapters(config=config)
    passed = sum(1 for r in results.values() if r.get("status") == "passed")
    console.print(f"\n[green]{passed}/{len(results)} basarili.[/green]")

    if passed < len(results):
        raise typer.Exit(1)


@production_app.command("build-book")
def build_book(
    project: Annotated[str | None, typer.Option("--project", "-p",
                        help="Proje adi")] = None,
) -> None:
    """Tum bolumleri tek bir DOCX'te birlestirir."""
    import subprocess
    import sys

    config = _resolve_config(project=project)
    if not config:
        console.print("[red]Config bulunamadi.[/red]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Kitap DOCX derleniyor: {config.title}[/bold]")
    console.print(f"  Bolum sayisi: {config.chapter_count}")
    console.print(f"  Cikti: {config.output_docx_path}")

    # build_book_docx.py'yi calistir
    tool = Path(__file__).resolve().parent.parent.parent.parent / "tools" / "build_book_docx.py"
    if not tool.exists():
        console.print(f"[red]Arac bulunamadi: {tool}[/red]")
        raise typer.Exit(1)

    result = subprocess.run(
        [sys.executable, str(tool)],
        cwd=str(config.project_root.parent.parent),
        capture_output=True, text=True, timeout=180,
    )

    if result.returncode == 0:
        console.print(f"[green]{result.stdout}[/green]")
    else:
        console.print(f"[red]Hata: {result.stderr[:500]}[/red]")
        raise typer.Exit(1)
