import os
schema_write_file={
    "type":"function",
    "function":{
        "name":"write_file",
        "description":"retrieve a file and change content, create a new one and write if not exists yet",
        "parameters":{
            "type":"object",
            "properties":{
                "file_path":{
                    "type":"string",
                    "description":"a file relative to the working dir",
            },
                "content":{
                    "type":"string",
                    "description":"content to write in the file",
                }
        },
    },
    },
}
def write_file(working_directory:str,file_path:str,content:str)->str:
    try:
        working_directory_abs=os.path.abspath(working_directory)
        file_path_abs=os.path.normpath(os.path.join(working_directory_abs,file_path))
        is_in_dir=os.path.commonpath([working_directory_abs,file_path_abs])==working_directory_abs
        if not is_in_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory' 
        os.makedirs(os.path.dirname(file_path_abs),exist_ok=True) #exist_ok: idempotent if already exist then ignore 
        with open(file_path_abs,'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error:{e}"

