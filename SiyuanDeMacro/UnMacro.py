import json
import os
import sys
import re

def escape_string(input_string):
    """
    Escapes special characters in a string, mapping them to a format suitable for use in regular expressions.
    Similar to `repr` but without enclosing quotes.
    
    Args:
        input_string (str): The input string to escape.
    
    Returns:
        str: The escaped string.
    """
    return input_string.encode("unicode_escape").decode("utf-8")

def replace_macros(macro_file, source_file, output_file):
    """
    Replaces macros in a source file using definitions from a JSON macro file and writes the result to an output file.
    
    Args:
        macro_file (str): Path to the JSON file containing macro definitions.
        source_file (str): Path to the source file to process.
        output_file (str): Path to save the output with replaced macros.
    """
    # Load the macro definitions from the JSON file
    with open(macro_file, 'r') as f:
        macros = json.load(f)
    
    # Read the content of the source file
    with open(source_file, 'r') as f:
        output = f.read()
    
    # Replace each macro in the source file with its corresponding replacement
    for macro, replacement in macros.items():
        escaped_macro = escape_string(macro)
        escaped_replacement = escape_string(replacement)
        output = re.sub(escaped_macro + "(?![a-zA-Z])", escaped_replacement, output)
    
    # Write the processed content to the output file
    with open(output_file, 'w') as f:
        f.write(output)

def main():
    """
    Main function to process macro replacements in multiple source files.
    Reads macro definitions from a specified or default JSON file and applies them to source files.
    """
    if len(sys.argv) > 1:
        # If arguments are provided, use them as the macro file and source files
        macro_file = sys.argv[1]
        source_files = sys.argv[2:]
    else:
        # Default macro file and source files in the current directory
        macro_file = 'macros.json'
        source_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    # Check if the macro file exists
    if not os.path.exists(macro_file):
        print(f"Error: Macro file '{macro_file}' not found.")
        return
    
    # Process each source file
    for source_file in source_files:
        if not os.path.exists(source_file):
            print(f"Error: Source file '{source_file}' not found.")
            continue
        
        # Define the output file name by appending "unMacro" to the base name
        output_file = os.path.splitext(source_file)[0] + "unMacro.md"
        replace_macros(macro_file, source_file, output_file)
        print(f"Processed '{source_file}' -> '{output_file}'")

if __name__ == "__main__":
    main()
