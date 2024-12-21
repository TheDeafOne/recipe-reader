import os
from PIL import Image
from dotenv import load_dotenv

import pytesseract
import easyocr
from groq import Groq

load_dotenv()
client = Groq(
    api_key=os.environ.get('LLM_API_KEY'),
)

def ask_llm(role, content):
    chat_completion = client.chat.completions.create(
        messages=[dict(role=role, content=content)],
        model=os.environ.get('LLM_MODEL')
    )
    return chat_completion.choices[0].message.content

print('response:',ask_llm('user','hello how are you. Does this work?'))