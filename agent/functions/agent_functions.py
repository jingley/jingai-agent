import os
import subprocess
from pathlib import Path
from .config import MAX_FILE_CONTENT_LENGTH
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory. If the directory is not found immediately, searches recursively to locate it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of the given file as a string, constrained to the working directory. If the file is not found immediately, searches recursively to locate it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts additionals CLI args as an optional array. If the file is not found immediately, searches recursively to locate it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="An optional array of strings to be used as the CLI args for the Python file.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or Overwrites an existing file to a new file (and creates required parent dirs safely). Constrained to the working directory. If writing to an existing file that is not found immediately, searches recursively to locate it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file, as a string.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    """
    Get information about files in a directory.
    
    Args:
        working_directory (str): The base working directory that limits access
        directory (str): The target directory to examine (relative to working_directory)
        
    Returns:
        str: Information about files in the directory, or
        str: Error message if there's an issue accessing the directory
    """
    # Convert to Path objects for easier manipulation
    working_dir = Path(working_directory).resolve()
    
    # Handle nested directory paths properly
    if directory == ".":
        target_dir = working_dir
    else:
        target_dir = (working_dir / directory).resolve()
    
    # Security check: ensure target directory is within working directory
    try:
        target_dir.relative_to(working_dir)
    except ValueError:
        return f"Access denied: Directory '{directory}' is outside the allowed working directory '{working_directory}'"
    
    # Check if target directory exists, if not try to find it recursively
    if not target_dir.exists() and directory != ".":
        # Try to find the directory recursively in the working directory
        found_dirs = list(working_dir.rglob(directory))
        if found_dirs:
            # Use the first match
            target_dir = found_dirs[0]
            # Re-check security for the found directory
            try:
                target_dir.relative_to(working_dir)
            except ValueError:
                return f"Access denied: Found directory '{directory}' is outside the allowed working directory"
        else:
            return f"Directory '{directory}' does not exist"
    
    if not target_dir.is_dir():
        return f"'{directory}' is not a directory"
    
    # Collect file information
    items_info = []
    
    try:
        for item in target_dir.iterdir():
            if item.is_file():
                file_size = item.stat().st_size
                is_dir = False
                items_info.append(f"{item.name}: file_size={file_size}, is_dir={is_dir}")
            elif item.is_dir():
                file_size = 0  # Directories don't have a meaningful file size
                is_dir = True
                items_info.append(f"{item.name}: file_size={file_size}, is_dir={is_dir}")
    except PermissionError:
        return f"Permission denied accessing directory '{directory}'"
    
    return "\n".join(items_info)


def get_file_content(working_directory, file_path):
    """
    Get the content of a file.
    
    Args:
        working_directory (str): The base working directory that limits access
        file_path (str): The path to the file to read (relative to working_directory)
        
    Returns:
        str: The file content (truncated if over MAX_FILE_CONTENT_LENGTH characters),
             or error message if there's an issue accessing the file
    """
    # Convert to Path objects for easier manipulation
    working_dir = Path(working_directory).resolve()
    
    # Handle nested file paths properly
    target_file = (working_dir / file_path).resolve()
    
    # Security check: ensure target file is within working directory
    try:
        target_file.relative_to(working_dir)
    except ValueError:
        return f"Error: Access denied: File '{file_path}' is outside the allowed working directory '{working_directory}'"
    
    # Check if target file exists, if not try to find it recursively
    if not target_file.exists():
        # Try to find the file recursively in the working directory
        file_name = Path(file_path).name
        found_files = list(working_dir.rglob(file_name))
        if found_files:
            # Use the first match
            target_file = found_files[0]
            # Re-check security for the found file
            try:
                target_file.relative_to(working_dir)
            except ValueError:
                return f"Error: Found file '{file_path}' is outside the allowed working directory"
        else:
            return f"Error: File '{file_path}' not found"
    
    if not target_file.is_file():
        return f"Error: '{file_path}' is not a regular file"
    
    # Read file content with error handling
    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Truncate if content is too long
        if len(content) > MAX_FILE_CONTENT_LENGTH:
            content = content[:MAX_FILE_CONTENT_LENGTH]
            content += f"\n[...File \"{file_path}\" truncated at {MAX_FILE_CONTENT_LENGTH} characters]"
            
        return content
        
    except UnicodeDecodeError:
        return f"Error: Cannot read file '{file_path}' - file appears to be binary or uses unsupported encoding"
    except PermissionError:
        return f"Error: Permission denied reading file '{file_path}'"
    except OSError as e:
        return f"Error: Failed to read file '{file_path}': {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error reading file '{file_path}': {str(e)}"
    
    
def write_file(working_directory, file_path, content):
    """
    Write content to a file.
    
    Args:
        working_directory (str): The base working directory that limits access
        file_path (str): The path to the file to write (relative to working_directory)
        content (str): The content to write to the file
        
    Returns:
        str: Success message with character count, or error message if there's an issue
    """
    # Convert to Path objects for easier manipulation
    working_dir = Path(working_directory).resolve()
    
    # Handle nested file paths properly
    target_file = (working_dir / file_path).resolve()
    
    # Security check: ensure target file is within working directory
    try:
        target_file.relative_to(working_dir)
    except ValueError:
        return f"Error: Access denied: File '{file_path}' is outside the allowed working directory '{working_directory}'"
    
    # If the file exists but the direct path doesn't work, try to find it recursively
    if not target_file.exists() and not target_file.parent.exists():
        # Check if we're trying to overwrite an existing file
        file_name = Path(file_path).name
        found_files = list(working_dir.rglob(file_name))
        if found_files:
            # Use the first match for overwriting
            target_file = found_files[0]
            # Re-check security for the found file
            try:
                target_file.relative_to(working_dir)
            except ValueError:
                return f"Error: Found file '{file_path}' is outside the allowed working directory"
    
    # Write file content with error handling
    try:
        # Create parent directories if they don't exist
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file (creates new file or overwrites existing)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except PermissionError:
        return f"Error: Permission denied writing to file '{file_path}'"
    except OSError as e:
        return f"Error: Failed to write file '{file_path}': {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error writing file '{file_path}': {str(e)}"

def run_python_file(working_directory, file_path, args=[]):
    """
    Run a Python file with optional arguments.
    
    Args:
        working_directory (str): The base working directory that limits access
        file_path (str): The path to the Python file to run (relative to working_directory)
        args (list): List of command-line arguments to pass to the Python script
        
    Returns:
        str: Success message with execution output, or error message if there's an issue
    """
    # Convert to Path objects for easier manipulation
    working_dir = Path(working_directory).resolve()
    
    # Handle nested file paths properly
    target_file = (working_dir / file_path).resolve()
    
    # Security check: ensure target file is within working directory
    try:
        target_file.relative_to(working_dir)
    except ValueError:
        return f"Error: Access denied: File '{file_path}' is outside the allowed working directory '{working_directory}'"
    
    # Check if target file exists, if not try to find it recursively
    if not target_file.exists():
        # Try to find the file recursively in the working directory
        file_name = Path(file_path).name
        found_files = list(working_dir.rglob(file_name))
        if found_files:
            # Use the first match
            target_file = found_files[0]
            # Re-check security for the found file
            try:
                target_file.relative_to(working_dir)
            except ValueError:
                return f"Error: Found file '{file_path}' is outside the allowed working directory"
        else:
            return f"Error: File '{file_path}' not found"
    
    # Check if it's a regular file
    if not target_file.is_file():
        return f"Error: '{file_path}' is not a regular file"
    
    # Check if file has .py extension
    if not file_path.lower().endswith('.py'):
        return f"Error: '{file_path}' is not a Python file (must end with .py)"
    
    # Execute the Python file
    try:
        # Build command with python executable and target file
        cmd = ["python", str(target_file)]
        
        # Add additional arguments if provided
        if args:
            cmd.extend(args)
        
        # Execute with timeout and capture output
        completed_process = subprocess.run(
            cmd,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=str(working_dir)
        )
        
        # Format output
        output_parts = []
        
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        # Check if process exited with non-zero code
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        # Return formatted output or "No output produced."
        if output_parts:
            return "\n\n".join(output_parts)
        else:
            return "No output produced."
            
    except subprocess.TimeoutExpired:
        return f"Error: Python script '{file_path}' timed out after 30 seconds"
    except FileNotFoundError:
        return f"Error: Python interpreter not found - please ensure Python is installed and in PATH"
    except Exception as e:
        return f"Error: Failed to execute Python script '{file_path}': {str(e)}"
    