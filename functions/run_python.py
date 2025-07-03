import os
from google.genai import types
import subprocess

def run_python_file(working_directory, file_path):

    working_path = os.path.abspath(working_directory)
    check_path = os.path.join(working_path, file_path)

    if not os.path.normpath(check_path).startswith(os.path.normpath(working_path)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(check_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            args=["python3", check_path], 
            cwd= working_directory,
            timeout= 30, 
            stdout= subprocess.PIPE, 
            stderr= subprocess.PIPE,
            universal_newlines = True
        ) 
        stdout = result.stdout
        stderr = result.stderr
        output = f"STDOUT: {stdout} \nSTDERR: {stderr}"
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    if stdout == "" and stderr == "":
        return "No output produced."
    
    if result.returncode != 0:
        return output + f"\nProcess exited with code {result.returncode}"
    
    return output

    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file and returns the contents of the script.",
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

     
