from typing import Optional
from qrize.core import log, pdf, fs, qr, utils
import typer

from qrize.core import validators

app: typer.Typer = typer.Typer(name="pdf")


@app.command()
def bulk(
    source: str = typer.Option(help="input file containing the json array"),
    schema: str = typer.Option(
        help="schema file containing the json validation object"
    ),
    output: str = typer.Option(help="output file"),
    identifier: str = typer.Option(
        help="key to use to uniquely identify the entry, it must be present in the schema"
    ),
    margin: int = typer.Option(default=10, help="margins around each qr code"),
    size: int = typer.Option(default=40, help="size of each qr code"),
    spacing: int = typer.Option(default=5, help="spacing between each code"),
):
    """
    Processes several entries based on a common schema. And renders a pdf file.
    """
    err, validator = fs.read_schema(schema)
    if err:
        log.fatal(message=err)

    if not validator:
        return log.fatal(message="No validator was found.")

    if not validators.has_property(validator, identifier):
        return log.fatal(message=f"Identifier must be a valid key of the schema.")

    err, entries = fs.read_entries(source)
    if err:
        return log.fatal(message=err)

    if not entries:
        return log.fatal("No entries have been provided.")

    entries = qr.filter_entries(entries=entries, validator=validator)

    try:
        pdf.generate_from_entries(
            entries=entries,
            identifier=identifier,
            output=str(output),
            margin=margin,
            qr_size=size,
            spacing=spacing,
        )
    except Exception as e:
        log.fatal(f"Error generating PDF: {e}")


@app.command()
def batch(
    input: Optional[str] = typer.Option(None, help="Data to encode"),
    source: Optional[str] = typer.Option(None, help="File to encode"),
    count: int = typer.Option(default=5, help="Number of copies"),
    output: str = typer.Option(help="Output file name"),
    margin: int = typer.Option(default=10, help="margins around each qr code"),
    size: int = typer.Option(default=40, help="size of each qr code"),
    spacing: int = typer.Option(default=5, help="spacing between each code"),
):
    """
    Generates a PDF with multiple copies of the same QR code.
    Data can be provided directly or read from a file.
    """

    if input and source:
        raise typer.BadParameter(
            "--input and --source are mutually exclusive.  Provide one or the other."
        )

    if not input and not source:
        raise typer.BadParameter("Either --source or --input must be provided.")

    if input:
        return pdf.generate_from_counter(
            data=input,
            count=count,
            output=output,
            margin=margin,
            qr_size=size,
            spacing=spacing,
        )

    if source:
        err, data = fs.read_entry(source)
        if err:
            return log.fatal(message=err)

        if not data:
            return log.fatal("No data has been provided.")

        return pdf.generate_from_counter(
            data=data,
            count=count,
            output=output,
            margin=margin,
            qr_size=size,
            spacing=spacing,
        )
