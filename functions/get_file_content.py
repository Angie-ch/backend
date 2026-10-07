from config import MAX_CHARS
import os
schema_get_file_content={
    "type":"function",
    "function":{
        "name":"get_file_content",
        "description":"extracting first 10000 characters from a file",
        "parameters":{
            "type":"object",
            "properties":{
                "file_path":{
                    "type":"string",
                    "description":"the file to get content from,relative to the working dir"
                },
            },
        },
    },
}
def get_file_content(working_directory:str, file_path:str)->str:
    try:
        working_directory_abs=os.path.abspath(working_directory)
        file_path_abs=os.path.normpath(os.path.join(working_directory_abs,file_path))
        is_in_working_dir=os.path.commonpath([working_directory_abs,file_path_abs])==working_directory_abs
        if not is_in_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(file_path_abs,'r') as f:
            content=f.read(MAX_CHARS) #save the content  
            if f.read(1):
                content+=f'[...File"{file_path}" truncated at{MAX_CHARS}characters]'
        return content
    except Exception as e:
        return f"Error:{e}"
    