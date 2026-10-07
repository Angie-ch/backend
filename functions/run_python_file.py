import os
import subprocess
schema_run_python_file={
    "type":"function",
    "function":{
        "name":"run_python_file",
        "description":"run python file",
        "parameters":{
            "type":"object",
            "properties":{
                "file_path":{
                    "type":"string",
                    "description":"python file location",
                },
                "args":{
                    "type":"string",
                    "description":"",
                },
            },
        },
    },
}
def run_python_file(working_directory:str, file_path:str, args:list[str]|None=None)->str:
    try:
        working_directory_abs=os.path.abspath(working_directory)
        file_path_abs=os.path.normpath(os.path.join(working_directory_abs,file_path))
        is_in_dir=os.path.commonpath([working_directory_abs, file_path_abs])==working_directory_abs
        if not is_in_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command=["python", file_path_abs]
        if args:
            command.extend(args)
        result=subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30, # unit is second
        )
        output=""
        if result.returncode!=0:
            output+="Process exited with code X"
        if result.stdout:
            output+=f"STDOUT:{result.stdout}"
        if result.stderr:
            output+=f"STDERR:{result.stderr}"
        if not result.stdout and not result.stderr:
            output += "No output produced"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"