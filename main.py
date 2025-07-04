import os
from dotenv import load_dotenv # type: ignore
from google import genai
from google.genai import types # type: ignore
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

client = genai.Client(api_key=api_key)


if len(sys.argv) == 1:
    print("You need to fill in a prompt")
    exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
]
    
for i in range(20):
    prompt = client.models.generate_content(
        model= "gemini-2.0-flash-001", 
        contents= messages,
        config= types.GenerateContentConfig(
            tools= [available_functions],
            system_instruction= system_prompt))

    function_call = prompt.function_calls
    verbose = False

    for candidate in prompt.candidates:
        messages.append(candidate.content)

    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {prompt.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {prompt.usage_metadata.candidates_token_count}")
        verbose = True

    if function_call:
        for function_call_part in function_call:
            response = call_function(function_call_part, verbose=verbose)

            if not response.parts or not response.parts[0].function_response:
                raise Exception("Invalid response structure")
            else:
                messages.append(response)

            if verbose:
                result = response.parts[0].function_response.response["result"]
                formatted_result = result.replace("\\n", "\n")
                print(f"-> {formatted_result}")
    else:
        print(prompt.text)
        break