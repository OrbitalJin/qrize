import typer


def warn(message: str) -> None:
    typer.echo(
        typer.style(
            f"Warning: {message}",
            fg=typer.colors.YELLOW,
            bold=True,
        ),
        err=True,
    )


def fatal(message: str) -> None:
    typer.echo(
        typer.style(
            f"Error: {message}",
            fg=typer.colors.RED,
            bold=True,
        ),
        err=True,
    )
    raise typer.Exit(1)
