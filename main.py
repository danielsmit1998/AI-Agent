import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) == 1:
    print("You need to fill in a prompt")
    exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
]
    
prompt = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

if "--verbose" in sys.argv:
    print(f"User prompt: {sys.argv[1]}")
    print(f"Prompt tokens: {prompt.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {prompt.usage_metadata.candidates_token_count}")

print(prompt.text)