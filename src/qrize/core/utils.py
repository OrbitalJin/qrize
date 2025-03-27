from typing import Optional
from PIL.Image import Image
import pyperclip
import base64
import io

from qrize.core import fs, log
from qrize.core.types import Result


def xor(input: Optional[str], source: Optional[str]) -> Result[str]:
    if input:
        return (None, input)

    err, data = fs.read_source(source)
    if err:
        log.fatal(err)

    return (None, data)


def copy_to_clipboard(image: Optional[Image]) -> Result[bool]:
    """
    Copies an image to the clipboard
    """
    if not image:
        return ("No image was provied.", None)

    try:
        buffer: io.BytesIO = io.BytesIO()
        image.save(buffer, "PNG")
        data: bytes = buffer.getvalue()

        encoded: bytes = base64.b64encode(data)
        b64_data = encoded.decode("utf-8")

        pyperclip.copy(b64_data)

        return (None, True)

    except Exception:
        return ("Failed to copy to clipboard", False)
