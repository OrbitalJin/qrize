from qrize.cli.commands import pdf
from qrize.core import log, fs, qr, utils

from typing import Optional
import typer

qrize: typer.Typer = typer.Typer()

qrize.add_typer(pdf.app)


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

    err, data = utils.xor(input=input, source=source)
    if err:
        log.fatal(err)

    err, image = qr.generate(data=data)
    if err:
        log.fatal(message=err)

    if output:
        err, _ = fs.save_image(image, output)
        if err:
            log.fatal(message=err)

    if clipboard:
        err, _ = utils.copy_to_clipboard(image)
        if err:
            log.fatal(message=err)
