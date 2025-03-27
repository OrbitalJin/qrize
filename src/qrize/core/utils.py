from PIL.Image import Image
import pyperclip
import base64
import io

from qrize.core.types import Result


def copy_to_clipboard(image: Image) -> Result[bool]:
    """
    Copies an image to the clipboard
    """

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
