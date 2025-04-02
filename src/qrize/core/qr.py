from qrize.core import validators, log
from qrize.core.types import Result

from typing import Any, Optional, List, Dict
from PIL import Image
import qrcode
import json


def generate(data: Any, size: int = 8, border: int = 4) -> Result[Image.Image]:
    """
    Generate and return a qrcode image
    """
    serialized: Optional[str] = None
    try:
        serialized = json.dumps(data)

    except Exception as e:
        return (str(e), None)

    qr: qrcode.QRCode = qrcode.QRCode(
        version=2,
        box_size=size,
        border=border,
    )
    qr.add_data(serialized)
    qr.make(fit=True)
    return (None, qr.make_image(fill_color="black", back_color="white"))


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
