"""bookmaker llm CLI komutları."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.llm.config import LLMConfig

console = Console()
llm_app = typer.Typer(help="LLM API islemleri.")


@llm_app.command("configure")
def configure_llm(
    provider: Annotated[str, typer.Option("--provider", help="API saglayicisi (openai, deepseek, anthropic)")] = "",
    key: Annotated[str, typer.Option("--key", "-k", help="API anahtari")] = "",
    model: Annotated[str, typer.Option("--model", "-m", help="Model adi")] = "",
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """LLM API yapilandirmasini yapar."""
    cfg = LLMConfig(path)

    if provider:
        cfg.provider = provider
    if key:
        cfg.api_key = key
    if model:
        cfg.model = model

    console.print("[green]LLM yapilandirmasi guncellendi:[/green]")
    table = Table(show_header=True)
    table.add_column("Alan", style="cyan")
    table.add_column("Deger")
    table.add_row("Saglayici", cfg.provider or "(ayarlanmadi)")
    table.add_row("Model", cfg.model or "(ayarlanmadi)")
    key_masked = cfg.api_key[:8] + "..." if len(cfg.api_key) > 8 else "(bos)"
    table.add_row("API Anahtar", key_masked)
    console.print(table)

    if not cfg.is_configured():
        console.print("[yellow]Eksik alanlar:[/yellow]")
        if not cfg.provider:
            console.print("  --provider (openai, deepseek, anthropic)")
        if not cfg.api_key:
            console.print("  --key <API_ANAHTARI>")
        if not cfg.model:
            console.print("  --model <model_adi>")
        raise typer.Exit(1)


@llm_app.command("test")
def test_llm(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """LLM API baglantisini test eder."""
    cfg = LLMConfig(path)

    if not cfg.is_configured():
        console.print("[red]LLM yapilandirilmamis. Once 'bookmaker llm configure' calistir.[/red]")
        raise typer.Exit(1)

    from bookmaker.llm.openai import OpenAICompatibleClient

    client = OpenAICompatibleClient(
        api_key=cfg.api_key,
        model=cfg.model,
        base_url=cfg.base_url,
    )

    console.print(f"[bold]Test ediliyor:[/bold] {cfg.provider} / {cfg.model}")
    console.print(f"[bold]Base URL:[/bold] {cfg.base_url}")

    result = client.test_connection()
    if result.get("status") == "ok":
        console.print(f"[green]Baglanti basarili![/green]")
        console.print(f"  Model: {result.get('model', '?')}")
        console.print(f"  Yanit: {result.get('response', '?')}")
    else:
        console.print(f"[red]Baglanti hatasi: {result.get('message', 'Bilinmeyen hata')}[/red]")
        raise typer.Exit(1)


@llm_app.command("status")
def llm_status(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """LLM yapilandirma durumunu gosterir."""
    cfg = LLMConfig(path)

    table = Table(title="LLM Yapilandirma", show_header=True)
    table.add_column("Alan", style="cyan")
    table.add_column("Deger")
    table.add_row("Saglayici", cfg.provider or "(ayarlanmadi)")
    table.add_row("Model", cfg.model or "(ayarlanmadi)")
    key_masked = cfg.api_key[:8] + "..." if len(cfg.api_key) > 8 else "(bos)"
    table.add_row("API Anahtar", key_masked)
    table.add_row("Base URL", cfg.base_url or "-")
    table.add_row("Durum", "[green]Hazir[/green]" if cfg.is_configured() else "[red]Eksik[/red]")
    console.print(table)
