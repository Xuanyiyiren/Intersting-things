# PDF to SVG Converter

## Overview

This Python script converts a specific page of a PDF file to SVG format. It uses the `PyMuPDF` library (also known as `fitz`) to handle PDF files and `argparse` for command-line argument parsing.

## Requirements

- Python 3.x
- PyMuPDF (fitz)
- argparse (standard library, no need to install separately)

## Installation

1. **Install Python**: Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install PyMuPDF**: Use `pip` to install the required library:

   ```bash
   pip install pymupdf

## Usage

### Command-Line Interface

Run the script from the command line with the following syntax:

```
python pdf2svg.py <pdf_file> [--page <page_number>]
```

- `<pdf_file>`: The path to the PDF file you want to convert. You can specify multiple PDF files.
- `--page <page_number>`: (Optional) The page number to convert (0-indexed). Default is 0 (the first page).

### Examples

- Convert the first page of a single PDF file:

   ```
   python pdf2svg.py example.pdf
   ```

   This will convert the first page of `example.pdf` to `example.svg`.

- Convert a specific page of a single PDF file:

   ```
   python pdf2svg.py example.pdf --page 2
   ```

   This will convert the third page (page number 2) of `example.pdf` to `example.svg`.

- Convert multiple PDF files:

   ```
   python pdf2svg.py file1.pdf file2.pdf file3.pdf
   ```

   This will convert the first page of each PDF file to their respective SVG files (`file1.svg`, `file2.svg`, `file3.svg`).

## Output

The script will generate an SVG file for each specified PDF file in the same directory as the original PDF file. The SVG file will have the same name as the PDF file but with a `.svg` extension.

## Error Handling

If the script encounters an error (e.g., the input file is not a PDF), it will print an error message to the console.

## Script Details

### Function: `pdf2svg(pdf_file, page=0)`

**Parameters**:

- `pdf_file`: The path to the PDF file to be converted.
- `page`: The page number to be converted (0-indexed). Default is 0.

**Raises**:

- `TypeError`: If the input file is not a PDF file.

**Description**:

- Opens the PDF file using `fitz.open()`.
- Loads the specified page.
- Converts the page to SVG format using `page.get_svg_image()`.
- Writes the SVG content to a file with the same name as the PDF file but with a `.svg` extension.

## License

This project is licensed under the MIT License. See the LICENSE file for details.