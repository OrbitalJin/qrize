# QRize

A command-line tool to generate QR codes from JSON data and render printable PDF documents.

## Installation

To try `qrize` through [uv](https://docs.astral.sh/uv/guides/tools/) (Recommended)

```sh
$ uvx qrize

# Or 

$ uv tool run qrize
```

To install it:

```sh 
$ uv tool install qrize
```

On arch, it is available on the aur:

```
$ yay -S qrize
```

> [!WARNING]
> QRize hasn't been deloyed & published yet.

## Commands

`qrize` provides commands to generate single QR codes or create PDF documents containing multiple QR codes from JSON files.

### Generate a Single QR Code (`gen`)

Use the `gen` command to generate a QR code from a string or a JSON file.

#### Usage

```sh
$ qrize gen [OPTIONS]

args:
    --input     - [str]  - default: None     - data or string to encode 
    --source    - [str]  - default: None     - file containing the object to encode
    --size      - [int]  - default: 8        - size of the qr code
    --border    - [int]  - default: 4        - border size surounding the qr code
    --output    - [str]  - default: ./qr.png - name for output file
    --clipboard - [bool] - default: false    - copy to the clipboard
```

#### Options


| Option      | Type  | Default           | Description                              |
|------------|------|-------------------|------------------------------------------|
| `--input`  | str  | `None`            | Data or string to encode                |
| `--source` | str  | `None`            | File containing the JSON object to encode |
| `--size`   | int  | `8`               | Size of the QR code                      |
| `--border` | int  | `4`               | Border size around the QR code           |
| `--output` | str  | `./qr.png`        | Output file name                         |
| `--clipboard` | bool | `false`         | Copy QR code to clipboard (if supported) |

#### Example

```sh
qrize gen --input "I'm stuck in Vim" --size 10 --border 5 --output "./foo.png" --clipboard
```

This generates a QR code with `size=10`, `border=5`, saves it as `./foo.png`, and copies it to the clipboard.

---

### Generate QR Codes in a PDF (`pdf`)

The `pdf` command allows you to generate a PDF file containing multiple QR codes, useful for printing stickers or deployments.

```sh
qrize pdf [SUBCOMMAND] [OPTIONS]
```

#### Bulk Generation (`bulk`)

Processes multiple QR codes based on a JSON array and a common schema.

``` sh
$ qrize pdf bulk [--args]

args:
    --source     - [str] - default: None - input file containing the json array
    --schema     - [str] - default: None - schema file containing the json validation object
    --output     - [str] - default: None - output file
    --identifier - [str] - default: None - key to use to uniquely identify the entry, it must be present in the schema
    --margin     - [int] - default: 10   - margins around each qr code
    --qr_size    - [int] - default: 40   - size of each qr code
    --spacing    - [int] - default: 5    - spacing between each code
```

#### Options

| Option        | Type  | Default  | Description                                      |
|--------------|------|----------|--------------------------------------------------|
| `--source`   | str  | `None`   | JSON file containing an array of objects        |
| `--schema`   | str  | `None`   | JSON schema file for validation                 |
| `--output`   | str  | `None`   | Output PDF file                                 |
| `--identifier` | str  | `None`   | Unique key in the schema for identifying entries |
| `--margin`   | int  | `10`     | Margin around each QR code in the PDF           |
| `--qr_size`  | int  | `40`     | Size of each QR code in the PDF                 |
| `--spacing`  | int  | `5`      | Spacing between QR codes in the PDF             |

#### Example

```sh 
qrize pdf bulk --source "data.json" --output "foo.pdf"
```

---

#### Batch Generation (`batch`)

Generates multiple identical QR codes for bulk distribution (e.g., event passes, inventory labels).

```sh
qrize pdf batch [OPTIONS]
```

#### Options

| Option     | Type  | Default  | Description                         |
|-----------|------|----------|---------------------------------|
| `--input` | str  | `None`   | Data to encode in each QR code     |
| `--count` | int  | `1`      | Number of identical QR codes to generate |
| `--output` | str  | `None`   | Output PDF file                    |
| `--margin` | int  | `10`     | Margin around each QR code         |
| `--qr_size` | int  | `40`    | Size of each QR code               |
| `--spacing` | int  | `5`     | Spacing between QR codes           |

#### Example

```sh
qrize pdf batch --input "https://example.com" --count 50 --output "batch_qr.pdf"
```

This generates a PDF with 50 identical QR codes pointing to `https://example.com`.

---

## Schema and Validation

To ensure consistency and correctness, `qrize` supports JSON schema validation when processing bulk QR code generation. The schema defines the expected structure of each entry in the JSON file.

### Schema Format

A schema file is a JSON object that describes the required fields, their types, and constraints. Example:

```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "description": { "type": "string" },
    "timeout": { "type": "integer" }
  },
  "required": ["title", "description", "timeout"]
}
```
> `schema.json`

### Validation Process

Each entry in the JSON file is checked against the schema. Entries missing required fields are skipped & a 
warning is issued. That way data integrity is enforced before generating QR codes. A convenient side effect
of this approach is the ability to denote a "primary_key" or in this case `identifier` to uniquely label 
the entries when rendered.
    
```json
[
  {
    "title": "Title 1",
    "description": "Description 1",
    "timeout": 4
  },
  {                        <- This will be skipped
    "name": "John Doe",    <- Not valid
    "description": "Description 2",
    "timeout": 2
  },
  {
    "title": "Title 1",
    "description": "Description 1",
    "timeout": 0
  }
]
```
> `data.json`

To use schema validation:

```sh
qrize pdf bulk --source "data.json" --schema "schema.json" --identifier "title" --output "qrcodes.pdf"
```

---

## TODO

- [ ] Migrate file paths to `pathlib.Path`
- [ ] Add support for both Wayland and X11 clipboard operations
- [x] Implement batch operation for PDFs (identical QR codes)
- [x] Implement bulk operation for PDFs (from data file + schema)
- [x] Write QR code images to PDF files
- [x] Add schema validation
- [x] Generate QR code images from input data
