import fitz
from os import listdir
import os
import easyocr
import prompts

from llm import prompt_llm

from consts import UNPARSED_FILES_DIR, PARSED_FILES_DIR
reader = easyocr.Reader(['en'])

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
            parse_pdf(UNPARSED_FILES_DIR + "/" + file_path)

def parse_pdf(file_path):
    print('parsing pdf:',file_path)
    
    # check if parsed dir exists, make it if it doesn't
    file_name = ''.join(file_path.split('.')[:-1]).split('/')[-1]
    parsed_file_dir = PARSED_FILES_DIR + '/' + file_name
    if not os.path.exists(parsed_file_dir):
        os.mkdir(parsed_file_dir)

    # objectify pdf. For each page, make an image of that page, and save it to the parsed dir
    pdf = fitz.open(file_path)
    for page_number in range(len(pdf)):
        print('   page:',page_number)
        page_img_path = f'{parsed_file_dir}/{page_number+1}-{file_name}.png'
        page = pdf.load_page(page_number)
        pixel_map = page.get_pixmap(matrix=PDF_ZOOM_MATRIX)
        pixel_map.save(page_img_path)

        # extract the text from the image using ocr
        print('   extracting text...')
        ocr_text = extract_text_from_img(page_img_path)

        # recipe is illegible, ignore
        if ocr_text == None:
            continue
        
        print('   saving text...')
        # save to a txt file in the same parsed dir
        ocr_text_path = f'{parsed_file_dir}/{page_number+1}-{file_name}.txt'
        file = open(ocr_text_path, 'w')
        file.write(' '.join(ocr_text))
        file.close()
    pdf.close()
    print('done\n')

def extract_text_from_img(img_path):
    result = reader.readtext(img_path, detail=0)
    llm_response = prompt_llm(prompts.LEGIBILITY_PROMPT.format(ocr_text=result))
    if prompts.ILLEGIBLE in llm_response:
        return None
    
    return result

if __name__ == "__main__":
    parse_files()