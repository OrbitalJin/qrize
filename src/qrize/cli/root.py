from qrize.cli.commands import pdf
from qrize.core import log, fs, qr, utils

from typing import Optional
import typer

qrize: typer.Typer = typer.Typer()

qrize.add_typer(pdf.app)


def xor(input: Optional[str], source: Optional[str]) -> str:
    if input:
        return input

    err, data = fs.read_source(source)  # type: ignore
    if err:
        log.fatal(err)

    return data  # type: ignore


@qrize.command()
def generate(
    input: Optional[str] = typer.Option(None, help="Data to encode"),
    source: Optional[str] = typer.Option(None, help="File to encode"),
    clipboard: bool = typer.Option(default=False, help="Copy to clipboard"),
    output: Optional[str] = typer.Option(None, help="Output file name"),
):
    if input and source:
        raise typer.BadParameter(
            "--input and --source are mutually exclusive.  Provide one or the other."
        )

    if not input and not source:
        raise typer.BadParameter("Either --source or --input must be provided.")

    if not clipboard and not output:
        raise typer.BadParameter(
            "Either --clipboard or --output (or both) must be provided."
        )

    data: str = xor(input=input, source=source)
    err, image = qr.generate(data=data)

    if err:
        log.fatal(message=f"Error occured during generation: {err}")

    if output:
        err, _ = fs.save_image(image, output)  # type: ignore
        if err:
            log.fatal(message=err)

    if clipboard:
        err, _ = utils.copy_to_clipboard(image)  # type: ignore
        if err:
            log.fatal(message=err)
