import os
from google.genai import types # type: ignore

def get_files_info(working_directory, directory=None):

    working_path = os.path.abspath(working_directory)
    
    if directory is None:
        check_path = working_path
    else:
        check_path = os.path.join(working_path, directory)

    if not os.path.isdir(check_path):
        return f'Error: "{directory}" is not a directory'

    if not check_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    return_string = []
    try:
        for file in os.listdir(check_path):
            file_size = os.path.getsize(os.path.join(check_path, file))
            is_file = os.path.isdir(os.path.join(check_path, file))

            return_string.append(f"- {file}: file_size={file_size}, is_dir={is_file}")

        return "\n".join(return_string)
    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
