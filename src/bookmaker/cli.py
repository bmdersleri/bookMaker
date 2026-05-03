import typer

from bookmaker import __version__
from bookmaker.commands.build import build_chapter_command
from bookmaker.commands.check import check_chapter_command
from bookmaker.commands.init import init_command

app = typer.Typer(
    name="bookmaker",
    help="Akademik ve teknik kitap uretim studyosu.",
    no_args_is_help=True,
)

chapter_app = typer.Typer(help="Bolum islemleri.")
version_app = typer.Typer(help="Surum islemleri.")
build_app = typer.Typer(help="Export ve build islemleri.")
check_app = typer.Typer(help="Kalite kontrol islemleri.")

check_app.command("chapter")(check_chapter_command)
build_app.command("chapter")(build_chapter_command)

app.add_typer(chapter_app, name="chapter")
app.add_typer(version_app, name="version")
app.add_typer(build_app, name="build")
app.add_typer(check_app, name="check")
app.command("init")(init_command)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Versiyon goster."),
) -> None:
    if version:
        typer.echo(f"bookmaker {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
