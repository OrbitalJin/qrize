from typing import Any, List, Optional, Dict, Callable
from PIL.Image import Image
from pathlib import Path
import typer
import json

from qrize.core import validators
from qrize.core.types import Result


def read_source(source: Optional[str]) -> Result[str]:
    """
    Read raw data from source file
    """
    return read_json_file(source)


def read_entry(source: str) -> Result[Any]:
    """
    Read single entry from source file
    """
    return read_json_file(source, process_single_entry)


def read_entries(source: str) -> Result[List[Dict]]:
    """
    Read multiple entries from source file
    """
    return read_json_file(source)


def read_schema(source: Optional[str]) -> Result[Dict]:
    """
    Read and validate schema from source file
    """
    return read_json_file(source, process_schema)


def read_json_file[
    T
](
    source: Optional[str],
    processor: Optional[Callable[[Any], Result[T]]] = None,
) -> Result[T]:
    """
    Generic JSON file reader with optional post-processing
    """
    if not source:
        return ("No file provided.", None)

    try:
        with open(source, "r") as src:
            data = json.load(src)

        if processor:
            return processor(data)

        return (None, data)

    except FileNotFoundError:
        return ("File not found.", None)

    except json.JSONDecodeError:
        return ("Failed to deserialize content, check for integrity.", None)


def process_single_entry(data: Any) -> Result[Any]:
    """
    Process data to return single entry
    """
    if not isinstance(data, list):
        return (None, data)

    if not data:
        return ("An empty array cannot be encoded.", None)

    typer.echo("Data is of type Array, only first value will be used.")
    return (None, data[0])


def process_schema(data: Dict) -> Result[Dict]:
    """
    Process and validate schema data
    """
    err, _ = validators.validate_schema(data)
    return (err, data)


def save_file(
    data: Optional[Any],
    destination: str,
    saver: Callable[[Any, str], None],
) -> Result[bool]:
    """
    Generic file saving function
    """

    if not data:
        return ("Cannot save empty data.", None)

    if Path(destination).exists():
        return ("File already exists.", False)

    try:
        saver(data, destination)
        return (None, True)

    except Exception as e:
        return (str(e), False)


def save_image(image: Optional[Image], destination: str) -> Result[bool]:
    """
    Save PIL Image to file
    """
    return save_file(image, destination, lambda img, dest: img.save(dest))


def exists(file: str) -> bool:
    """
    Check if file exists using absolute path
    """
    return Path(file).absolute().exists()
