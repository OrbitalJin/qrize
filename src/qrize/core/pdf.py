from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from typing import Dict, List, Optional
import typer

from qrize.core import fs, log, qr


def generate_from_counter(
    data: Optional[Dict | str],
    count: int,
    output: str,
    margin: int = 10,
    qr_size: int = 40,
    spacing: int = 5,
):
    if not data:
        return log.fatal("No data provided to the pdf generator.")

    if fs.exists(output):
        return log.fatal("File already exists.")

    margin_: float = margin * mm
    qr_size_: float = qr_size * mm
    spacing_: float = spacing * mm
    label_height: float = 5 * mm

    width, height = A4
    cols = int((width - 2 * margin_) // (qr_size_ + spacing_))
    rows = int((height - 2 * margin_) // (qr_size_ + label_height + spacing_))

    pdf: canvas.Canvas = canvas.Canvas(output, pagesize=A4)

    with typer.progressbar(range(count)) as progress:
        for i in progress:
            row = i // cols
            col = i % cols

            if row >= rows:  # Start a new page if needed
                pdf.showPage()
                row = 0

            x = margin_ + col * (qr_size_ + spacing_)
            y = height - (margin_ + row * (qr_size_ + label_height + spacing_))

            err, img = qr.generate(data)
            if err:
                return log.fatal(err)

            if not img:
                return log.fatal("Failed to generate qr code.")

            pdf.drawInlineImage(img, x, y - qr_size_, width=qr_size_, height=qr_size_)

            pdf.setFont("Helvetica", 10)
            label = str(i)
            pdf.drawString(x + 10, y - qr_size_ - label_height, label)

    pdf.save()


def generate_from_entries(
    entries: Optional[List[Dict]],
    identifier: Optional[str],
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

    margin_: float = margin * mm
    qr_size_: float = qr_size * mm
    spacing_: float = spacing * mm
    label_height: float = 5 * mm

    width, height = A4
    cols = int((width - 2 * margin_) // (qr_size_ + spacing_))
    rows = int((height - 2 * margin_) // (qr_size_ + label_height + spacing_))

    pdf: canvas.Canvas = canvas.Canvas(output, pagesize=A4)

    with typer.progressbar(entries) as progress:  # Wrap the entries with progress
        for idx, data in enumerate(progress):  # Iterate through the progress object
            row = idx // cols
            col = idx % cols

            if row >= rows:  # Start a new page if needed
                pdf.showPage()
                row = 0

            x = margin_ + col * (qr_size_ + spacing_)
            y = height - (margin_ + row * (qr_size_ + label_height + spacing_))

            err, img = qr.generate(data)
            if err:
                return log.fatal(err)

            if not img:
                return log.fatal("Failed to generate qr code.")

            pdf.drawInlineImage(img, x, y - qr_size_, width=qr_size_, height=qr_size_)

            pdf.setFont("Helvetica", 10)
            label = data[identifier] if identifier else str(idx)
            pdf.drawString(x + 10, y - qr_size_ - label_height, label)

    pdf.save()
