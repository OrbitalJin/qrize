from typing import Dict, List
from qrize.core import log, pdf, fs
import typer

from qrize.core import validators

app: typer.Typer = typer.Typer(name="pdf")


def filter_entries(entries: List[Dict], validator: Dict) -> List[Dict]:
    """
    Filter out entries that don't match the schema
    """
    for entry in entries:
        if not entry:
            log.warn("Empty entry, skipping.")
            continue

        err, _ = validators.validate_against_schema(entry, validator)
        if err:
            entries.remove(entry)
            log.warn(message=err)

    return entries


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
):
    """
    Processes several entries based on a common schema.
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

    entries = filter_entries(entries=entries, validator=validator)

    pdf.generate_from_entries(entries=entries, identifier=identifier, output=output)
