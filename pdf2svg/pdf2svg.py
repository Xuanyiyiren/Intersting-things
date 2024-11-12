import fitz
import os
import argparse

def pdf2svg(pdf_file, page=0):
    ''' 
    Convert a specific page of a PDF file to SVG format.
    pdf_file: the path of your pdf file to be converted. 
    page: which page to be converted (0-indexed). 
    ''' 
    pdf_extension = os.path.splitext(pdf_file)[1] 
    if pdf_extension != '.pdf':
        raise TypeError("Not pdf!") 

    svg_file = os.path.splitext(pdf_file)[0] + '.svg'
    
    doc = fitz.open(pdf_file) 
    page = doc.load_page(page) 
    svg = page.get_svg_image() 
    with open(svg_file, 'w') as f: 
        f.write(svg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert PDF to SVG.')
    parser.add_argument('pdf_files', type=str, nargs='+', help='Input PDF file paths.')
    parser.add_argument('--page', type=int, default=0, help='Page number to convert (default: 0).')

    args = parser.parse_args()
    
    for pdf_file in args.pdf_files:
        try:
            pdf2svg(pdf_file, args.page)
            print(f'Successfully converted {pdf_file} (page {args.page}) to {os.path.splitext(pdf_file)[0]}.svg.')
        except Exception as e:
            print(f'Error: {e}')
