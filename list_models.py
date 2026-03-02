import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

print("Available models:")
for model in client.models.list():
    if "gemini" in model.name:
        print(model.name)
