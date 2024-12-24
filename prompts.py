from functools import partial

UNFINISHED = 'Unfinished Recipe'
COMPLETE = 'Complete Recipe'
MULTIPLE = 'Multiple Recipes'

INITIAL_RECIPE_EXTRACTION_PROMPT = f'''You are analyzing OCR text from a recipe book. Your goal is to identify if the provided text represents a single, complete recipe, is unfinished, or contains multiple recipes. Follow these criteria:

1. **{COMPLETE}**:
   - It has a clear title, ingredient list, and instructions.
   - All sections seem to be present and logically flow together.
   - There is at least one complete recipe contained within the provided text.

2. **{UNFINISHED}**:
   - The text appears to end abruptly.
   - Only part of the recipe is present (e.g., ingredients but no instructions or an incomplete list).
   - The last sentence or section indicates continuation (e.g., "continued on the next page").

3. **{MULTIPLE}**:
   - There are clear separations between sections with distinct titles, ingredient lists, and instructions.
   - The content describes more than one dish.

Now, analyze the following text and respond with one of these categories: "{COMPLETE}," "{UNFINISHED}," or "{MULTIPLE}."

Only provide that answer, do not provide anything else.

Text:
''' + '{ocr_text}'



RECIPE_CONTINUATION_EXTRACTION_PROMPT = '''You are analyzing OCR text from a recipe book. The text may include the continuation of a previous recipe, the beginning of a new recipe, or even multiple recipes. Your goal is to classify the text into the following categories:

1. **Continuation Only**:
   - The text primarily completes a recipe started on the previous page.
   - There are no clear indicators of a new recipe starting.

2. **New Recipe(s)**:
   - The text begins a new recipe, possibly in addition to continuing a previous one.
   - Look for signs of a new title, separate ingredient list, or a distinct set of instructions.

3. **Complete Recipe(s)**:
   - The text contains one or more standalone recipes, which include all essential parts (title, ingredients, and instructions).

Now, analyze the following text and respond with one of these categories: "Continuation Only," "New Recipe(s)," or "Multiple Recipes."

Only provide the answers, do not provide anything else.

Text:
{ocr_text}'''

LEGIBLE = 'Legible'
ILLEGIBLE = 'Illegible'
LEGIBILITY_PROMPT = f'''You are evaluating OCR text extracted from an image of a recipe book. Your task is to determine if the text is legible, relevant, and useful for identifying or extracting recipes. Use the following criteria:

1. **Legible**:
   - The text is mostly clear and free of major errors or distortions.
   - Any errors present do not significantly hinder understanding.

2. **Relevant**:
   - The text appears to contain recipe-related content, such as titles, ingredients, or instructions.
   - It is not unrelated content, like advertisements, page numbers, or decorative elements.

3. **Useful**:
   - The text provides meaningful content for identifying or extracting a recipe, such as complete sections or distinct recipe elements (e.g., a title, ingredient list, or instructions).
   - Text that is incomplete or unclear but partially identifies a recipe can still be useful.

Based on the evaluation, respond with one of the following categories:
- **{LEGIBLE}**: The text is clear and contributes to recipe extraction.
- **{ILLEGIBLE}**: The text is too distorted or unclear to evaluate properly.

Text:''' + '{ocr_text}'

RECIPE_EXTRACTION_PROMPT = ''''
The following text is OCR output from a scanned recipe book. Your task is to extract a complete recipe from the text. If there are multiple recipes, extract only the complete recipes. Do not provide a recipe if it does not provide ingredients, a title, and all related recipe information. A recipe should include the following components:

Title: The name of the recipe.
Description (if present): A brief context or note about the recipe.
Ingredients: A list of ingredients with their quantities.
Instructions: Step-by-step directions to prepare the recipe.
Do not include any irrelevant or incomplete information outside the recipe(s). If parts of the recipe (e.g., ingredients or instructions) are scattered, consolidate them into one complete section. Here's the text:
{ocr_text}

Make sure the output is in the form of:
Title: <title>
Description: <description>
Ingredients: <ingredients>
Instructions: <instructions>

It MUST be in this format.
'''