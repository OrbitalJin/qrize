from qrize.core import qr, fs
import typer

app: typer.Typer = typer.Typer(name="pdf")


#
# Args:
#     source    : path to source file containing json array
#     schema    : path to source for the json schema for validation purposes
#     identifier: key to use to uniquely identify the entry, it must me present inside the schema
#
@app.command()
def bulk(
    source: str = typer.Option(
        ...,
        help="input file containing the json array",
    ),
    schema: str = typer.Option(
        ...,
        help="schema file containing the json validation object",
    ),
    identifer: str = typer.Option(
        ...,
        help="key to use to uniquely identify the entry, it must be present in the schema",
    ),
):
    """
    Processes several entries based on a common schema.
    """
    err, entries = fs.read_source(source)
    if err:
        return typer.echo(err)

    err, image = qr.generate(data=fs.read_source(source))
    if err:
        return typer.echo(f"Error occured while generating qrcode: {err}")

    image.save("./qr.png")  # type: ignore
