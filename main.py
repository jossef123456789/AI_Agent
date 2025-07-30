import os 
import sys
from google import genai
from google.genai import types 

from dotenv import load_dotenv # We have a file caleed '.env' so we are importing this tool to load the enviroment variables from the .env and the next line it will be loaded . 

from functions.get_files_info import schema_get_files_info 
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python 
from functions.write_files import schema_write_file
from functions import call_function 

load_dotenv() #this is the line of loading the variables .

api_key = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key = api_key)

messages = [
        types.Content (role = 'user', parts = [types.Part(text = sys.argv[1]) ] ) 
        ]

sys_pro = """
You are an AI agent that performs file operations within a working directory. Based on the user’s request, choose the appropriate function to call:

- To list files and directories, call `get_files_info(directory)`.
- To read a file’s contents, call `get_file_content(file_path)`.
- To execute a Python file with optional arguments, call `run_python_file(file_path, args)`.
- To write or overwrite a file, call `write_file(file_path, content)`.

Examples:
- "list the files in the current directory" → `get_files_info(".")`
- "read the contents of main.py" → `get_file_content("main.py")`
- "run main.py with arguments 'arg1' and 'arg2'" → `run_python_file("main.py", ["arg1", "arg2"])`
- "write 'hello' to main.txt" → `write_file("main.txt", "hello")`

Analyze the user’s request and generate the correct function call with the appropriate parameters.
"""


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file
    ]
)


def main():
    verbose = '--verbose' in sys.argv
    #if '--verbose' in sys.argv : 
        #response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages, config=types.GenerateContentConfig(system_instruction=sys_pro)) # In this line it will return the object that have many properties and details one of them is text which represent the response of the model and to do it see the line under this one .
        #print(f'User prompt: {sys.argv[1]}')
        #print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        #print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

    if len(sys.argv) > 0 : 
        c = 0
        t = True
        while c < 20 : 
            try : 
                response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=sys_pro))
                if response.text : 
                    print(response.text)
                    break


            except Exception as e : 
                print(f'this is an : {e}')

            for i in response.candidates : 
                content = i.content
                if content is None or content.parts is None or len(content.parts) == 0:
                    continue
                messages.append(content)

                for j in i.content.parts : 

                    if j.function_call : 

                        messages.append(
                            types.Content(
                                role='model',
                                parts=[types.Part(function_call=j.function_call)]
                            )
                        )


                        res = call_function.call_function(j.function_call, verbose = '--verbose' in sys.argv)

                        messages.append(
                                types.Content(role = 'tool', parts = res.parts)
                                )

                        if verbose:
                            response_part = res.parts[0].function_response.response
                            if 'result' in response_part:
                                print(f"-> {response_part['result']}")
                            elif 'error' in response_part:
                                print(f"Error: {response_part['error']}")
                        #elif j.text:
                            #print(j.text)


                    elif j.text : 
                            print(j.text)
                            t = False 
            if t == False : 
                break 
            c += 1


        #print(response.text)
        #print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        #print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    #else : 
    #    raise Exception("you don't provide a prompt ")
    #    sys.exit(1)

if __name__ == "__main__":
    main()
