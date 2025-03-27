import os
from qrize.core.types import Result
from PIL.Image import Image
import json


def read_schema(): ...


def read_source(source: str) -> Result[str]:
    """
    Read the entries from the source file
    """
    try:
        with open(source, "r") as src:
            data = json.load(src)

        return (None, data)

    except FileNotFoundError:
        return ("File not found.", None)

    except json.JSONDecodeError:
        return ("Failed to deserialize contents, check for integrity.", None)


def save_image(qr: Image, destination: str) -> Result[bool]:
    path: str = os.path.join(os.getcwd(), destination)
    if os.path.exists(path):
        return ("File already exists.", False)

    try:
        qr.save(destination)
        return (None, True)

    except Exception as e:
        return (str(e), False)
