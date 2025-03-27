# qrize
A command-line tool to generate QR codes from JSON data and create printable PDF documents.

## Commands

#### gen 
```
qrsize gen [--args]

args:
    --clipboard - [bool] - default: false      - copies the images to the clipboard
    --output    - [str]  - default: "./qr.png" - name for output file
    --from-file - [str]  - default: ""         - generates a qrcode using the contents of the given from-file
```

### pdf

```
qrize pdf [subcommand] [--args]
```

#### bulk
```
qrize pdf bulk [--args]
```

#### batch
```
qrize pdf batch [--args]
```

## TODO
- [ ] add support for both wayland and x11
- [ ] write qr code image to pdf file
- [ ] schema validation
- [ ] batch operation pdf (identical)
- [ ] batch operation pdf (from data file + schema)
- [x] generate qr code image from data
