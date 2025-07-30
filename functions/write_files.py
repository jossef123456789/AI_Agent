import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the specified file with the given content within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            )
        },
        required=["file_path", "content"]
    )
)

def write_file(working_directory, file_path, content): 
    wd = os.path.join(working_directory, file_path)
    ap = os.path.abspath(wd)
    aps = os.path.abspath(working_directory)
    
    if not (ap.startswith(aps + os.sep)) : 
        return f'Error: Cannot write to "{ap}" as it is outside the permitted working directory' 

    else : 
        try :  
            with open(ap, 'w') as f : 
                f.write(content)
            return f'Successfully wrote to "{ap}" ({len(content)} characters written)'

        except : 
                raise Exception ("dnslqj")
