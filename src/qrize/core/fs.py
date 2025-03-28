from typing import Any, List, Optional, Dict

import typer
from qrize.core import validators
from qrize.core.types import Result
from PIL.Image import Image
import json
import os


def read_source(source: Optional[str]) -> Result[str]:
    """
    Read the entries from the source file
    """
    if not source:
        return ("No file provied.", None)
    try:
        with open(source, "r") as src:
            data = json.load(src)

        return (None, data)

    except FileNotFoundError:
        return ("File not found.", None)

    except json.JSONDecodeError:
        return ("Failed to deserialize content, check for integrity.", None)


def read_entry(source: str) -> Result[Any]:
    """
    Read the entries from the source file
    """
    try:
        with open(source, "r") as src:
            data = json.load(src)

        if isinstance(data, list):
            if len(data) != 0:
                typer.echo("Data is of type Array, only first value will be used.")
                return (None, data[0])

            else:
                return ("An empty array cannot will not be encoded.", None)

        return (None, data)

    except FileNotFoundError:
        return ("File not found.", None)

    except json.JSONDecodeError:
        return ("Failed to deserialize content, check for integrity.", None)


def read_entries(source: str) -> Result[List[Dict]]:
    """
    Read the entries from the source file
    """
    try:
        with open(source, "r") as src:
            data: List[Dict] = json.load(src)

        return (None, data)

    except FileNotFoundError:
        return ("File not found.", None)

    except json.JSONDecodeError:
        return ("Failed to deserialize content, check for integrity.", None)


def read_schema(source: Optional[str]) -> Result[Dict]:
    """
    Read the entries from the source file
    """
    if not source:
        return ("No file provied.", None)
    try:
        with open(source, "r") as src:
            data: Dict = json.load(src)

        err, _ = validators.validate_schema(data)

        return (err, data)

    except FileNotFoundError:
        return ("File not found.", None)

    except json.JSONDecodeError:
        return ("Failed to deserialize content, check for integrity.", None)


def save_image(image: Optional[Image], destination: str) -> Result[bool]:
    """
    Persist a qr code on the filesystem
    """
    if not image:
        return ("Cannot save empty image.", None)

    if exists(destination):
        return ("File already exists.", False)

    try:
        image.save(destination)
        return (None, True)

    except Exception as e:
        return (str(e), False)


def exists(file: str) -> bool:
    path: str = os.path.join(os.getcwd(), file)
    return os.path.exists(path)
