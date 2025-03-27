from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from typing import Dict, List, Optional

from qrize.core import fs, log, qr


def generate_from_entries(
    entries: Optional[List[Dict]],
    identifier: str,
    output: str,
    margin: int = 10,
    qr_size: int = 40,
    spacing: int = 5,
):
    """
    Create a PDF with multiple QR codes arranged in a grid
    """

    if not entries:
        return log.fatal("No entries provided to the pdf generator.")

    if fs.exists(output):
        return log.fatal("File already exists.")

    # PDF settings
    margin_ = margin * mm  # 20mm margin
    qr_size_ = qr_size * mm  # 50mm QR code size
    spacing_ = spacing * mm  # 10mm spacing between QR codes
    label_height = 5 * mm  # Height for the label text

    # Calculate how many QR codes can fit in a row and column
    page_width, page_height = A4
    cols = int((page_width - 2 * margin_) // (qr_size_ + spacing_))
    rows = int((page_height - 2 * margin_) // (qr_size_ + label_height + spacing_))

    # Create PDF
    c = canvas.Canvas(output, pagesize=A4)

    for idx, data in enumerate(entries):
        # Calculate position for this QR code
        row = idx // cols
        col = idx % cols

        if row >= rows:  # Start a new page if needed
            c.showPage()
            row = 0

        # Calculate x and y positions
        x = margin_ + col * (qr_size_ + spacing_)
        y = page_height - (margin_ + row * (qr_size_ + label_height + spacing_))

        # Create QR code
        err, img = qr.generate(data)
        if err:
            return log.fatal(err)

        if not img:
            return log.fatal("Failed to generate qr code.")

        # Draw QR code
        c.drawInlineImage(img, x, y - qr_size_, width=qr_size_, height=qr_size_)

        # Draw label
        c.setFont("Helvetica", 10)
        label = data[identifier]
        c.drawString(x + 10, y - qr_size_ - label_height, label)

    c.save()
