import os


import pytesseract
import prompts  
from llm import prompt_llm
from consts import PARSED_FILES_DIR




def extract_recipes_from_directory(recipe_section):
    ongoing_recipe_text = ''
    related_images = []
    recipe_file_names = sorted(
        filter(lambda file: '.txt' in file, os.listdir(recipe_section)),
        key=lambda filename: int(filename.split('-')[0])
    )
    
    for i, recipe_file_name in enumerate(recipe_file_names):
        recipe_text_file = open(os.path.join(recipe_section, recipe_file_name), 'r')
        ongoing_recipe_text += recipe_text_file.read()
        related_images.append(recipe_file_name.replace('.txt','.png'))
        response = prompt_llm(prompts.INITIAL_RECIPE_EXTRACTION_PROMPT.format(ocr_text=ongoing_recipe_text)) 
   
        if prompts.COMPLETE in response or prompts.MULTIPLE in response:
            parsed_recipe_text = prompt_llm(prompts.RECIPE_EXTRACTION_PROMPT.format(ocr_text=ongoing_recipe_text))
            parsed_recipe_title = parsed_recipe_text[:parsed_recipe_text.index("Description")].split('Title:')[-1].split('\n')[0][2:]
            print(parsed_recipe_title)
            # complete_recipe_package_file = open(recipe_section)

            # clear data package info
            ongoing_recipe_text = ''
            related_images = []

        

if __name__ == "__main__":
    extract_recipes_from_directory('./recipes/parsed/02-soups')