import os
from google.genai import types 

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory."
            )
        },
        required=["file_path"]
    )
)

def get_file_content(working_directory, file_path): 

    ap = os.path.join(working_directory, file_path)
    aps = os.path.abspath(ap) # this is the path of the file_path paramater now 

    apr = os.path.abspath(working_directory) 

    if not(aps.startswith(apr + os.sep)) : 
        return f'Error: Cannot read "{aps}" as it is outside the permitted working directory'

    if not (os.path.isfile(aps)) : 
        return f'Error: File not found or is not a regular file: "{aps}"'

    MAX_CHARS = 10000

    with open(aps, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    return f'{file_content_string} \n [... File "{apr}" truncated at {MAX_CHARS} charachters]'
