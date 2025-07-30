import os
from google.genai import types  


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files and directories in the specified directory, including their sizes, within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Use '.' for the current directory."
            )
        },
        required=["directory"]
    )
)

def get_files_info(working_directory, directory="."):
    if directory == '.' :
        ld = "Result for current directory:"
    else : 
        ld = f"Result for '{directory} directory:'"

    wp = os.path.join(working_directory, directory)
    ap = os.path.abspath(wp) # This is the absoulout path of the directory (the second paramater)
    # For example the wd = calaculator and the dir = tt so it is = .../calculator/tt 

    apd = os.path.abspath(working_directory) # This is the absolout path of the working dir (the first paramater)
    # Here for example calculator is the wd and the dir is '.' so it will stop until where we are now ..../curent_dir

    if not (ap == apd or ap.startswith(apd + os.sep)) : 
        return (f'{ld} \n Error: Cannot list "{directory}" as it is outside the permitted working directory \n')
    elif (not (os.path.isdir(ap))) : 
        return (f'{ld} \n Error: "{directory}" is not a directory \n')
    else : 
        lisd = os.listdir(ap)
        for i in lisd :
            if i == '__pycache__' : 
                continue 
            k = os.path.join(ap, i)
            fn = k 
            fs = os.path.getsize(fn)
            isd = os.path.isdir(k)
            ld = ld + '\n' + f'- {i} : file_size={fs} bytes, is_dir={isd} \n '
        return (ld)
