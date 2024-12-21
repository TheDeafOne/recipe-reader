import fitz
from os import listdir
import os

UNPARSED_FILES_DIR  = './recipes/unparsed'
PARSED_FILES_DIR = './recipes/parsed'
VALID_FILE_TYPES = ['pdf']

PDF_ZOOM = 10
PDF_ZOOM_MATRIX = fitz.Matrix(PDF_ZOOM, PDF_ZOOM)

def parse_files():
    for file_path in listdir(UNPARSED_FILES_DIR):
        file_type = file_path.split('.')[-1]
        # ignore invalid file types
        if file_type not in VALID_FILE_TYPES:
            print(f'ignoring {file_path}')
            continue
        
        if file_type == 'pdf':
            extract_pdf(UNPARSED_FILES_DIR + "/" + file_path)

def extract_pdf(file_path):
    file_name = ''.join(file_path.split('.')[:-1]).split('/')[-1]
    parsed_file_dir = PARSED_FILES_DIR + '/' + file_name
    if not os.path.exists(parsed_file_dir):
        os.mkdir(parsed_file_dir)
    
    pdf = fitz.open(file_path)
    for page_number in range(len(pdf)):
        page_image_name = f'{parsed_file_dir}/{page_number+1}-{file_name}.png'
        page = pdf.load_page(page_number)
        pixel_map = page.get_pixmap(matrix=PDF_ZOOM_MATRIX)
        pixel_map.save(page_image_name)
    pdf.close()

parse_files()