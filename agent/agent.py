import os
from google import genai
from google.genai import types
from .functions.agent_functions import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from .functions.call_function import call_function

def run_agent(client, messages, available_functions, verbose_flag=False):
    """
    Run the AI agent with the given messages and return updated messages list.
    
    Args:
        client: The Gemini API client
        messages: List of conversation messages
        available_functions: The tool configuration for available functions
        verbose_flag: Whether to print verbose output
        
    Returns:
        tuple: (updated_messages_list, has_function_calls)
    """
    
    system_prompt = """
You are a helpful AI coding agent. You can help the user with any files/directories in the current working directory of the terminal.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories (shows immediate contents only - you may need to explore subdirectories)
- Read file contents
- Write files
- Run Python scripts

IMPORTANT BEHAVIOR NOTES:
- The get_files_info function only lists immediate directory contents, not recursive
- When looking for "all files" of a type (e.g., "all Python files"), you need to:
  1. First list the root directory with get_files_info(".")
  2. Then explore each subdirectory you find to search for more files
  3. Continue this pattern to find files in nested directories like pkg/, tests/, etc.
- All paths you provide should be relative to the working directory
- You do not need to specify the working directory in your function calls as it is automatically injected for security reasons
- Always be thorough when searching - users expect complete results across the entire project structure
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
    except Exception as e:
        print(f"Error calling LLM service: {str(e)}")
        print("This could be due to:")
        print("- Network connectivity issues")
        print("- API rate limits")
        print("- Invalid API key")
        print("- Service temporarily unavailable")
        return messages, False
    
    if verbose_flag:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Check for malformed response first
    if response is None or response.usage_metadata is None:
        print("Response is malformed")
        return messages, False
    
    # Check for candidates and append their content to messages if available
    if response.candidates:
        for candidate in response.candidates:
            if candidate is not None and candidate.content is not None:
                messages.append(candidate.content)
    
    has_function_calls = False
    
    # Process function calls if any
    if response.function_calls:
        has_function_calls = True
        for function_call in response.function_calls:
            result = call_function(function_call, verbose_flag)
            # Add function call result to messages for context in future interactions
            messages.append(types.Content(role="user", parts=[types.Part(text=f"Function result: {result}")]))
    else:
        print(response.text)
    
    return messages, has_function_calls
