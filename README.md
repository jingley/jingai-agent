# AI Agent Project

An agentic AI system built with Google Gemini that can perform file operations, execute Python code, and engage in multi-turn conversations with memory. This project demonstrates the fundamentals of building autonomous AI agents that can interact with the file system and execute code safely.

This is just a personal project with minimal security in place. Please do not just download this and let it run wild.

## 🎯 Project Overview

This project is based on a **freeCodeCamp guide** for creating agentic AI systems. It showcases how to build an AI agent that can:

- 📁 **File Operations**: Read, write, and search for files with security constraints
- 🐍 **Code Execution**: Run Python files and capture their output  
- 🧠 **Memory & Context**: Maintain conversation history across interactions
- 🔄 **Recursive Calling**: Make autonomous decisions and chain function calls
- 🛡️ **Security**: Prevent directory traversal and validate file operations

## 🚀 Learning Journey

### Background Context
As a **Java developer** in my day-to-day work, this project was an excellent opportunity to explore Python while learning about agentic AI systems. I leveraged **GitHub Copilot** extensively throughout development, which turned out to be an incredible learning experience on two fronts:

1. **Agentic AI Architecture**: Understanding how autonomous agents work under the hood
2. **AI-Enhanced Development**: Experiencing firsthand how AI tools can boost productivity and accelerate learning in unfamiliar languages

### Key Learning Outcomes
- 🤖 **Agent Design Patterns**: Message history, function calling, recursive execution
- 🔧 **Python Best Practices**: Virtual environments, package structure, testing frameworks
- 🧪 **Test-Driven Development**: Comprehensive unit testing with mocking strategies
- 🛡️ **Security Considerations**: Path validation, input sanitization, execution timeouts
- 📋 **Code Organization**: Modular architecture and clean separation of concerns

## 🏗️ Architecture

### Core Components

```
aiagent/
├── 🎯 main.py               # CLI interface and agentic execution loop
├── agent/                   # Core agent package
│   ├── 🤖 agent.py          # Core agent logic with conversation memory
│   ├── functions/           # Agent functions and utilities
│   │   ├── 🔧 agent_functions.py # File operations with recursive search
│   │   ├── 📞 call_function.py   # Function dispatcher and parameter routing
│   │   └── ⚙️ config.py          # Configuration constants
│   └── __init__.py         # Package initialization
├── calculator/              # Example package for testing
│   ├── 🧮 main.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
└── tests/                   # Comprehensive test suite
    ├── test_main.py
    ├── test_agent_functions.py
    └── test_calculator.py
```

### Agent Functions

| Function | Purpose | Security Features |
|----------|---------|-------------------|
| `get_files_info()` | List directory contents with recursive search | Path traversal prevention |
| `get_file_content()` | Read file contents with size limits | Content truncation, encoding validation |
| `write_file()` | Create/update files safely | Directory creation, overwrite protection |
| `run_python_file()` | Execute Python scripts with timeouts | Subprocess isolation, 30-second timeout |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Google Gemini API key

### Installation

#### Option 1: Using uv (Recommended)
```bash
# Clone and navigate to project
cd aiagent

# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv add google-genai python-dotenv

# Set up environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

#### Option 2: Using pip with venv
```bash
# Clone and navigate to project
cd aiagent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install google-genai python-dotenv

# Set up environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### Usage
```bash
# Interactive mode
uv run main.py

# Direct prompt
uv run main.py -p "List all Python files in this project"

# Verbose output
uv run main.py -v -p "Create a simple calculator function"
```

## 🧪 Testing

Comprehensive test suite covering all major functionality:

```bash
# Run all tests
uv run python -m unittest discover -s tests -p "test_*.py"

# Individual test files
uv run python tests/test_main.py           # CLI interface tests
uv run python tests/test_agent_functions.py # File operations tests  
```

## 🔒 Security Features

- **Path Validation**: Prevents directory traversal attacks using `pathlib.Path.relative_to()`
- **File Size Limits**: Content truncation for large files (10KB default)
- **Execution Timeouts**: 30-second limit on subprocess execution
- **Input Sanitization**: Parameter validation and type checking
- **Error Handling**: Graceful failure with informative error messages

## 🎓 Skills Developed

### Technical Skills
- **Python Development**: From Java background to Python proficiency
- **AI Integration**: Working with Google Gemini API and function calling
- **Testing Strategies**: Unit testing, mocking, integration testing
- **Security Practices**: Input validation, safe file operations, process isolation

### AI-Enhanced Development
- **GitHub Copilot Usage**: Leveraging AI for code generation and learning
- **Prompt Engineering**: Crafting effective prompts for code assistance
- **Debugging with AI**: Using AI tools to understand and fix issues
- **Documentation**: AI-assisted README and comment generation

## 🚀 Future Directions

### Corporate Readiness Areas
The next phase of learning will focus on making agentic AI systems enterprise-ready:

- 🔐 **Advanced Security**: Authentication, authorization, role-based access control
- 🏢 **Enterprise Integration**: Database connections, API security, audit logging
- 📊 **Monitoring & Observability**: Performance metrics, usage tracking, error monitoring  
- 🔧 **Deployment & Scaling**: Containerization, load balancing, fault tolerance
- 📋 **Compliance**: Data privacy, regulatory requirements, security standards

## 🤝 Acknowledgments

- **freeCodeCamp**: For the excellent agentic AI tutorial and guidance
- **GitHub Copilot**: For being an invaluable learning companion and development accelerator
- **Google Gemini**: For providing the AI capabilities that power this agent

## 📚 Resources

- [freeCodeCamp Agentic AI Guide](https://www.freecodecamp.org)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

---

*This project represents a journey from Java expertise to Python proficiency, demonstrating how AI tools can accelerate learning while building foundational knowledge in agentic AI systems. Lol obviously this was written by AI*
