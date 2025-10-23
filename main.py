import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from agent.functions.agent_functions import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from agent import run_agent

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Parse command-line arguments for --prompt, --verbose, and --help
    prompt = None
    verbose_flag = False
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--help" or arg == "-h":
            print("AI Agent - Agentic AI with File Operations")
            print()
            print("An autonomous AI agent that can interact with your file system and execute Python code.")
            print("The agent can make function calls and maintain conversation context across interactions.")
            print()
            print("Usage: python main.py --prompt <text> [--verbose]")
            print("   or: python main.py <text> [--verbose]")
            print()
            print("Arguments:")
            print("  --prompt <text>    Your request or question for the AI agent")
            print("  --verbose          Show detailed output including token counts and iterations")
            print("  --help, -h         Show this help message")
            print()
            print("Available Agent Capabilities:")
            print("  📁 List files and directories (with recursive search)")
            print("  📄 Read file contents (with size limits for safety)")
            print("  ✏️  Write and create files (with directory auto-creation)")
            print("  🐍 Execute Python scripts (with timeout protection)")
            print("  🧠 Maintain conversation memory across function calls")
            print("  🔄 Make autonomous decisions and chain multiple operations")
            print()
            print("Example Requests:")
            print("  python main.py \"List all Python files in this project\"")
            print("  python main.py \"Create a hello world script and run it\"")
            print("  python main.py \"Show me the content of README.md\" --verbose")
            print("  python main.py \"Find all test files and run them\"")
            print("  python main.py \"Analyze the project structure and create documentation\"")
            print()
            print("Security Features:")
            print("  • Path validation prevents directory traversal attacks")
            print("  • File content truncation for large files (10KB limit)")
            print("  • Script execution timeout (30 seconds)")
            print("  • All operations are restricted to the current working directory")
            sys.exit(0)
        elif arg == "--prompt" or arg == "-p":
            if i + 1 >= len(sys.argv) or sys.argv[i+1] is None or sys.argv[i+1].startswith("--"):
                print("Error: --prompt requires a value")
                sys.exit(1)
            prompt = sys.argv[i + 1]
            i += 2
        elif arg == "--verbose" or arg == "-v":
            verbose_flag = True
            i += 1
        else:
            # Treat the first positional argument as the prompt if not already set
            if prompt is None:
                prompt = arg
            i += 1
            
    if prompt is None:
        print("Error: --prompt is required.")
        sys.exit(1)
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_get_file_content,
            schema_run_python_file,
        ]
    )

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    
    if verbose_flag:
        print(f"User's prompt: {prompt}")
    
    # Run the agent recursively until no more function calls are made
    max_iterations = 20 # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        messages, has_function_calls = run_agent(client, messages, available_functions, verbose_flag)
        
        if not has_function_calls:
            break
            
        iteration += 1
        if verbose_flag:
            print(f"Agent iteration {iteration} completed")
    
    if iteration >= max_iterations:
        print("Warning: Maximum iterations reached, stopping agent loop")
    

if __name__ == "__main__":
    main()