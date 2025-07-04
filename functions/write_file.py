import os
from google.genai import types # type: ignore

def write_file(working_directory, file_path, content):
    
    working_path = os.path.abspath(working_directory)
    check_path = os.path.join(working_path, file_path)

    if not check_path.startswith(working_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.dirname(check_path), exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
    
    try:
        with open(check_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Looks for a file and overwrites the contents of the file, if it doesn't exists it creates the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory that is used to look for the file.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to look for in the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that is written to the file.",
            )
        },
    ),
)