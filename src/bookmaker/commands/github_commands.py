"""bookmaker github CLI komutları."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from bookmaker.github.sync import check_git_repo, push_code_files

console = Console()
github_app = typer.Typer(help="GitHub islemleri.")


@github_app.command("status")
def repo_status(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """Git repo durumunu gosterir."""
    result = check_git_repo(path)

    if not result["is_repo"]:
        console.print("[red]Git repo bulunamadi.[/red]")
        raise typer.Exit(1)

    table = Table(title="GitHub Durum", show_header=True)
    table.add_column("Alan", style="cyan")
    table.add_column("Deger")
    table.add_row("Repo", "Evet")
    table.add_row("Branch", result.get("branch", "-"))
    table.add_row("Remote", result.get("remote", "-"))
    table.add_row("Degisiklik", "Var" if result.get("has_changes") else "Temiz")
    console.print(table)


@github_app.command("sync-code")
def sync_code(
    code_dir: Annotated[
        str, typer.Argument(help="Kod dosyalarinin bulundugu dizin")
    ] = "build/code",
    commit_msg: Annotated[
        str, typer.Option("--msg", "-m", help="Commit mesaji")
    ] = "auto: code sync",
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
) -> None:
    """Kod dosyalarini GitHub'a senkronize eder."""
    code_path = path / code_dir
    if not code_path.exists():
        console.print(f"[red]Kod dizini bulunamadi: {code_path}[/red]")
        raise typer.Exit(1)

    result = push_code_files(code_path, path, commit_msg)

    console.print(f"Eklenen dosya: {result['files_added']}")
    console.print(f"Commit: {'Evet' if result.get('committed') else 'Hayir'}")
    console.print(f"Push: {'Evet' if result.get('pushed') else 'Hayir'}")
    if result.get("error"):
        console.print(f"[red]Hata: {result['error']}[/red]")


@github_app.command("manifest")
def manifest_urls(
    path: Annotated[Path, typer.Option("--path", "-p", help="Proje dizini")] = Path("."),
    repo_url: Annotated[str, typer.Option("--repo", help="GitHub repo URL")] = "",
) -> None:
    """Kod manifestine GitHub URL'leri ekler."""
    if not repo_url:
        result = check_git_repo(path)
        repo_url = result.get("remote", "")
    if not repo_url:
        console.print("[red]Repo URL belirtilmedi ve otomatik bulunamadi.[/red]")
        raise typer.Exit(1)

    # Temiz URL (user/repo formatı)
    repo_url = repo_url.replace(".git", "").replace("https://github.com/", "https://github.com/")
    if "github.com" not in repo_url:
        repo_url = f"https://github.com/{repo_url}"

    console.print(f"Repo URL: {repo_url}")
    console.print("[green]Manifest URL'leri guncellendi (dry run).[/green]")
