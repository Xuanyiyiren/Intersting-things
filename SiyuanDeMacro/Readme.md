# Macro Replacer

A Python script to replace macros in text files based on definitions provided in a JSON file. This tool is especially useful for automating text processing in markdown or other text-based formats.

## Features

- Supports macro replacement in multiple source files.
- Escapes special characters for seamless macro substitution.
- Generates new output files with replaced macros.

## Requirements

- Python 3.6 or later

## Usage

### Command Line Arguments

Run the script by providing a macro file and one or more source files:

```bash
python UnMacro.py <macro_file> <source_file1> <source_file2> ...
```

For example:

```bash
python UnMacro.py macros.json file1.md file2.md
```

### Default Behavior

If no arguments are provided, the script will:

1. Use `macros.json` as the default macro file.
2. Process all `.md` files in the current directory.

```bash
python UnMacro.py
```

### Output

For each source file, the script generates an output file with the suffix `unMacro` added to the base filename. For example:

- `file1.md` → `file1unMacro.md`

## Macro File Format

The macro file should be in JSON format, with each macro and its replacement defined as key-value pairs:

```json
{
    "macro1": "replacement1",
    "macro2": "replacement2"
}
```

This originates from [SiYuan](https://b3log.org/siyuan/)'s KaTeX macro.

## Contribute

I am not a professional in computer science or software engineering. If someone is willing to turn it into a plugin for SiYuan, that would be even better. In pursuit of the stability of personal tools, I have used a very simple implementation as much as possible.