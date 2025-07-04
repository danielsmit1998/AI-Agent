from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from google.genai import types # type: ignore

def call_function(function_call_part, verbose=False):
    
    function_name = function_call_part.name
    function_call_part.args['working_directory'] = './calculator'

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    
    functions = {'get_files_info': get_files_info, 
                'get_file_content': get_file_content,
                'write_file' : write_file,
                'run_python_file' : run_python_file
                }

    if function_name in functions:
        function_result = functions[function_name](**function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )   
    
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)