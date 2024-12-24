import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(
    api_key=os.environ.get('LLM_API_KEY'),
)

def prompt_llm(content, role='user'):
    chat_completion = client.chat.completions.create(
        messages=[dict(role=role, content=content)],
        model=os.environ.get('LLM_MODEL')
    )
    return chat_completion.choices[0].message.content
