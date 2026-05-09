"""bookmaker studio — web arayüzü başlatma komutu."""

from __future__ import annotations

from typing import Annotated

import typer

studio_app = typer.Typer(help="Web arayüzü (Studio).")


@studio_app.command("start")
def studio_start(
    host: Annotated[str, typer.Option("--host", "-h", help="Sunucu host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", "-p", help="Sunucu port")] = 8765,
) -> None:
    """BookMaker Studio web arayüzünü başlatır."""
    try:
        from bookmaker.studio.app import run_studio
        print(f"  bookMaker Studio baslatiliyor: http://{host}:{port}")
        run_studio(host=host, port=port)
    except ImportError as e:
        print(f"  HATA: {e}")
        raise typer.Exit(1)


@studio_app.callback(invoke_without_command=True)
def studio_default(
    host: Annotated[str, typer.Option("--host", "-h", help="Sunucu host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", "-p", help="Sunucu port")] = 8765,
) -> None:
    """Varsayılan: studio start ile aynı."""
    studio_start(host=host, port=port)
