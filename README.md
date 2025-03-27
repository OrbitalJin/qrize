# qrize
A command-line tool to generate QR codes from JSON data and create printable PDF documents.

## Commands

The following commands allow you to generate single QR codes, or to create PDF documents containing QR codes generated from data in JSON files.

#### gen 
```
qrsize gen [--args]

args:
    --input     - [str]  - default: None       - data or string to encode 
    --source    - [str]  - default: None       - file containing the object to encode
    --output    - [str]  - default: ./qr.png   - name for output file
    --clipboard - [bool] - default: false      - copy to the clipboard
```

### pdf

Commands for working with PDF generation.
```
qrize pdf [subcommand] [--args]

```

#### bulk
Processes several entries based on a common schema.
```
qrize pdf bulk [--args]

args:
    --source     - [str] - default: None - input file containing the json array
    --schema     - [str] - default: None - schema file containing the json validation object
    --output     - [str] - default: None - output file
    --identifier - [str] - default: None - key to use to uniquely identify the entry, it must be present in the schema
```

#### batch
```
qrize pdf batch [--args]
```

## TODO
- [ ] add support for both wayland and x11
- [ ] batch operation pdf (identical)
- [x] bulk operation pdf (from data file + schema)
- [x] write qr code image to pdf file
- [x] schema validation
- [x] generate qr code image from data
