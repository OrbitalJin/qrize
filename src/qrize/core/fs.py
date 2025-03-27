from typing import List, Optional, Dict
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
    if not image:
        return ("Cannot save empty image.", None)

    path: str = os.path.join(os.getcwd(), destination)
    if os.path.exists(path):
        return ("File already exists.", False)

    try:
        image.save(destination)
        return (None, True)

    except Exception as e:
        return (str(e), False)
