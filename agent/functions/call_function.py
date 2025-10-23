import os
from .agent_functions import get_files_info, get_file_content, write_file, run_python_file

def call_function(function_call_part, verbose=False):
    """
    Execute a function call based on the function call part from the AI response.
    
    Args:
        function_call_part: The function call object from the AI response
        verbose (bool): Whether to print verbose output during execution
        
    Returns:
        str: The result of the function call or an error message
    """
    if verbose:
        print(f"Executing function: {function_call_part.name} with arguments: {function_call_part.args}")
    else:
        print(f"Executing function: {function_call_part.name}")
    
    # Get the working directory (current directory)
    working_directory = os.getcwd()
    
    # Execute the appropriate function based on the function name
    if function_call_part.name == "get_files_info":
        directory = function_call_part.args.get("directory", ".")
        result = get_files_info(working_directory, directory)
        return result
    
    elif function_call_part.name == "get_file_content":
        file_path = function_call_part.args.get("file_path")
        if file_path is None:
            return "Error: file_path parameter is required for get_file_content"
        result = get_file_content(working_directory, file_path)
        return result
    
    elif function_call_part.name == "write_file":
        file_path = function_call_part.args.get("file_path")
        content = function_call_part.args.get("content")
        if file_path is None or content is None:
            return "Error: file_path and content parameters are required for write_file"
        result = write_file(working_directory, file_path, content)
        return result
    
    elif function_call_part.name == "run_python_file":
        file_path = function_call_part.args.get("file_path")
        args = function_call_part.args.get("args", [])
        if file_path is None:
            return "Error: file_path parameter is required for run_python_file"
        result = run_python_file(working_directory, file_path, args)
        return result
    
    else:
        return f"Error: Unknown function '{function_call_part.name}'"
