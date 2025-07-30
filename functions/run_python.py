import os
import subprocess
from google.genai import types 

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory, optionally with arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file."
            )
        },
        required=["file_path"]
    )
)


def run_python_file(working_directory, file_path, args=[]):
    wd = os.path.join(working_directory, file_path)
    ap = os.path.abspath(wd)
    aps = os.path.abspath(working_directory)
    p, e = os.path.splitext(ap) 
    t  = 30
    
    if not (ap.startswith(aps + os.sep)) : 
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    elif not (os.path.exists(ap)) : 
        return f'Error: File "{file_path}" not found.'

    elif not (e == '.py') : 
        return f'Error: "{ap}" is not a Python file.'

    else : 
        try : 
            command = ['python3', ap] + args
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=t,
                cwd=working_directory
            )
            
            if result.returncode != 0:
                return f'Process exited with code {result.returncode}\nSTDERR: {result.stderr}'
            
            # Combine stdout and stderr to ensure test output is captured
            output = result.stdout
            if result.stderr:
                output += f'\nSTDERR: {result.stderr}'
            if not output.strip():
                return 'No output produced.'
            
            return output

        except Exception as e:
            return f"Error executing Python file: {e}"
