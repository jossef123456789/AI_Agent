from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content 
from functions.run_python import run_python_file 
from functions.write_files import write_file 


function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):
    if verbose : 
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else : 
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name in function_map : 
        try : 
            args = function_call_part.args 
            args['working_directory'] = './calculator'
            t = function_map[function_call_part.name](**args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": t},
                    )
                ],
            )
        except Exception as e : 
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": str(e)},
                    )
                ],
            )


    else : 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    
