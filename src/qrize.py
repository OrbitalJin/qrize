from typing import Any, Optional, Tuple
from PIL import Image
import qrcode
import json
import typer

app: typer.Typer = typer.Typer()

type Result[T] = Tuple[Optional[Exception], Optional[T]]


def generate_qr_code(data: Any) -> Result[Image]:
    serialized: Optional[str] = None

    try:
        serialized = json.dumps(data)

    except Exception as e:
        return (e, None)

    qr: qrcode.QRCode = qrcode.QRCode(
        version=1,
        box_size=8,
        border=4,
    )
    qr.add_data(serialized)
    qr.make(fit=True)
    return (None, qr.make_image(fill_color="black", back_color="white"))


@app.command()
def batch():
    err, image = generate_qr_code(data="hello, world!")
    if err:
        typer.echo(f"Error while generating qr: {err}")

    else:
        image.save("./qr.png")  # type: ignore


@app.command()
def foo():
    typer.echo("foo")


if __name__ == "__main__":
    app()
