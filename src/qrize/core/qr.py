from qrize.core.types import Result
from typing import Any, Optional
from PIL import Image
import qrcode
import json


def generate(data: Any) -> Result[Image.Image]:
    """
    Generate and return a qrcode image
    """
    serialized: Optional[str] = None
    try:
        serialized = json.dumps(data)

    except Exception as e:
        return (str(e), None)

    qr: qrcode.QRCode = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4,
    )
    qr.add_data(serialized)
    qr.make(fit=True)
    return (None, qr.make_image(fill_color="black", back_color="white"))
