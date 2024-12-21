import os
from PIL import Image
from dotenv import load_dotenv

import pytesseract
import easyocr
import prompts  
from groq import Groq
from consts import PARSED_FILES_DIR

load_dotenv()
reader = easyocr.Reader(['en'])
client = Groq(
    api_key=os.environ.get('LLM_API_KEY'),
)

def ask_llm(content, role='user'):
    chat_completion = client.chat.completions.create(
        messages=[dict(role=role, content=content)],
        model=os.environ.get('LLM_MODEL')
    )
    return chat_completion.choices[0].message.content



def extract_recipes(recipe_section):
    image_index = 0
    unparsed_recipe = ''
    recipe_image_file_names = os.listdir(recipe_section)
    
    while image_index < len(recipe_image_file_names):
        # extract text
        img_path = PARSED_FILES_DIR + "/" + recipe_image_file_names[image_index]
        ocr_text = reader.readtext(img_path, detail=0)
        unparsed_recipe += ocr_text
        
        # check with llm if recipe is complete
        response = ask_llm(prompts.INITIAL_RECIPE_EXTRACTION_PROMPT.format(ocr_text=unparsed_recipe))
        print(response)
        break


def extract_text_from_img(img_path):
    result = reader.readtext(img_path, detail=0)
    llm_response = ask_llm(prompts.LEGIBILITY_PROMPT.format(ocr_text=result))
    if prompts.ILLEGIBLE in llm_response:
        return None
    
    return result

