import os
from google.genai import types # type: ignore

def get_file_content(working_directory, file_path):

    working_path = os.path.abspath(working_directory)
    check_path = os.path.join(working_path, file_path)
    MAX_chars = 10000

    if not check_path.startswith(working_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(check_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(check_path, "r") as f:
            file_content = f.read()
        
            if len(file_content) > MAX_chars:
                return file_content[:MAX_chars] + '[...File "' + file_path + '" truncated at 10000 characters]'
        
            return file_content
    except Exception as e:
        return f'Error: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the files content and returns this, it gets truncated to a max of 10000 characters",
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
        },
    ),
)