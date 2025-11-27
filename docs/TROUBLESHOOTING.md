# Troubleshooting Guide

Common issues and solutions when using Graphton.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Issues](#runtime-issues)
- [Configuration Issues](#configuration-issues)
- [MCP Integration Issues](#mcp-integration-issues)
- [Performance Issues](#performance-issues)
- [Deployment Issues](#deployment-issues)
- [Development Issues](#development-issues)
- [Getting Help](#getting-help)

## Installation Issues

### Problem: `pip install` fails with "Could not find a version"

**Symptoms**:

```bash
$ pip install git+https://github.com/plantoncloud-inc/graphton.git
ERROR: Could not find a version that satisfies the requirement graphton
```

**Causes**:

- Git is not installed
- Git is not in PATH
- Network connectivity issues

**Solutions**:

```bash
# 1. Check if git is installed
git --version

# If not installed:
# macOS: brew install git
# Ubuntu/Debian: sudo apt install git
# Windows: Download from git-scm.com

# 2. Verify network connectivity
ping github.com

# 3. Try with verbose output to see error
pip install -v git+https://github.com/plantoncloud-inc/graphton.git
```

### Problem: `fatal: could not read Username for 'https://github.com'`

**Symptoms**:

```bash
$ pip install git+https://github.com/plantoncloud-inc/graphton.git
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

**Causes**:

- Trying to access private repository without authentication
- GitHub SSH keys not configured
- HTTPS auth not set up

**Solutions**:

```bash
# Graphton is public, ensure you're using HTTPS URL (not SSH):
pip install git+https://github.com/plantoncloud-inc/graphton.git

# If using private fork, configure Git credentials:
git config --global credential.helper store

# Or use SSH URL if you have SSH keys set up:
pip install git+ssh://git@github.com/plantoncloud-inc/graphton.git
```

### Problem: Dependency conflicts with LangChain/LangGraph

**Symptoms**:

```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
  graphton 0.1.0 requires langgraph>=1.0.0,<2.0.0, but you have langgraph 0.9.5.
```

**Causes**:

- Conflicting versions of dependencies
- Old versions of LangChain ecosystem packages

**Solutions**:

```bash
# 1. Use a fresh virtual environment
python -m venv fresh-env
source fresh-env/bin/activate  # Windows: fresh-env\Scripts\activate
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# 2. Upgrade all LangChain packages first
pip install --upgrade langchain langgraph langchain-anthropic langchain-openai
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# 3. Use Poetry (better dependency resolution)
poetry add git+https://github.com/plantoncloud-inc/graphton.git#v0.1.0
```

### Problem: `ModuleNotFoundError: No module named 'graphton'`

**Symptoms**:

```python
>>> from graphton import create_deep_agent
ModuleNotFoundError: No module named 'graphton'
```

**Causes**:

- Graphton not installed in current environment
- Using wrong Python interpreter
- Virtual environment not activated

**Solutions**:

```bash
# 1. Check which Python you're using
which python
which pip

# 2. Verify virtual environment is activated
# Look for (venv) or (env) in your prompt

# 3. Check if graphton is installed
pip list | grep graphton

# 4. Install if missing
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# 5. Verify import works
python -c "from graphton import create_deep_agent; print('✅ Success')"
```

### Problem: Slow installation

**Symptoms**:

Installation takes several minutes.

**Causes**:

- Git cloning entire repository history
- Slow network connection
- Large dependency tree

**Solutions**:

```bash
# 1. Use specific version tag (smaller download)
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# 2. Use --depth flag (if supported)
pip install "git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0#egg=graphton" --depth=1

# 3. Install from cached wheels (after first install)
pip install --no-deps git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# 4. Use faster mirror (if available)
# Set up PyPI mirror in pip.conf
```

## Runtime Issues

### Problem: "Model API key not found"

**Symptoms**:

```python
AuthenticationError: No API key found for Anthropic.
```

**Causes**:

- API key not set in environment
- Wrong environment variable name
- API key not accessible to Python process

**Solutions**:

```bash
# 1. Set the API key before running
export ANTHROPIC_API_KEY="sk-ant-..."  # macOS/Linux
set ANTHROPIC_API_KEY=sk-ant-...      # Windows CMD
$env:ANTHROPIC_API_KEY="sk-ant-..."   # Windows PowerShell

# 2. Set in Python code (not recommended for production)
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."

# 3. Use .env file with python-dotenv
pip install python-dotenv
# Create .env file:
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...

# In your code:
from dotenv import load_dotenv
load_dotenv()

# 4. Verify key is accessible
import os
print(os.getenv("ANTHROPIC_API_KEY"))  # Should print key
```

### Problem: "Recursion limit exceeded"

**Symptoms**:

```python
GraphRecursionError: Recursion limit of 100 reached without hitting a stop condition
```

**Causes**:

- Agent requires more reasoning steps
- Agent stuck in loop
- Agent behavior needs debugging

**Solutions**:

```python
# 1. Increase recursion limit
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    recursion_limit=200,  # Increase from default 100
)

# 2. Check system prompt for clarity
# Ensure agent knows when to stop
SYSTEM_PROMPT = """You are a helpful assistant.

When you have completed the task:
- Provide your final answer
- Do not continue reasoning
- Do not ask for more information unless necessary
"""

# 3. Debug with lower limit to fail faster
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    recursion_limit=10,  # Debug mode
)

# 4. Check for circular tool calls
# Review agent trace to see if it's calling the same tools repeatedly
```

### Problem: Agent responses are too slow

**Symptoms**:

Agent takes 30+ seconds to respond for simple queries.

**Causes**:

- Using powerful model unnecessarily
- High recursion limit
- Network latency
- Complex tool calls

**Solutions**:

```python
# 1. Use faster model for simple tasks
agent = create_deep_agent(
    model="claude-haiku-4",  # Faster than sonnet/opus
    system_prompt=SYSTEM_PROMPT,
)

# 2. Lower recursion limit
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    recursion_limit=20,  # Lower for simple tasks
)

# 3. Reduce max_tokens for shorter responses
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    max_tokens=1000,  # Limit response length
)

# 4. Profile to find bottlenecks
import time
start = time.time()
result = agent.invoke({"messages": [...]})
print(f"Took {time.time() - start:.2f}s")
```

## Configuration Issues

### Problem: `ValidationError` on agent creation

**Symptoms**:

```python
ValidationError: 1 validation error for AgentConfig
system_prompt
  system_prompt cannot be empty. Provide a clear description... (type=value_error)
```

**Causes**:

- Invalid configuration parameters
- Missing required fields
- Type mismatches

**Solutions**:

```python
# Read the error message carefully - it tells you what's wrong

# Common mistake 1: Empty system prompt
system_prompt = ""  # ❌
system_prompt = "You are a helpful assistant."  # ✅

# Common mistake 2: MCP servers without tools
mcp_servers = {"server": {...}}  # ❌
mcp_tools = None

# Fix: Add mcp_tools
mcp_tools = {"server": ["tool1", "tool2"]}  # ✅

# Common mistake 3: Server name mismatch
mcp_servers = {"server-a": {...}}
mcp_tools = {"server-b": [...]}  # ❌ Names don't match

# Fix: Use same names
mcp_servers = {"server-a": {...}}
mcp_tools = {"server-a": [...]}  # ✅

# Common mistake 4: Invalid recursion limit
recursion_limit = 0  # ❌ Must be positive
recursion_limit = 100  # ✅
```

### Problem: Model name not recognized

**Symptoms**:

```python
ValueError: Unknown model name: claude-sonnet-5
```

**Causes**:

- Typo in model name
- Model not yet supported
- Using outdated model name

**Solutions**:

```python
# 1. Use supported model names (see docs/API.md)
# Anthropic:
"claude-sonnet-4.5"  # ✅
"claude-opus-4"      # ✅
"claude-haiku-4"     # ✅

# OpenAI:
"gpt-4o"             # ✅
"gpt-4o-mini"        # ✅

# 2. Use full model ID if alias not recognized
"claude-sonnet-4-5-20250929"  # ✅ Full ID

# 3. Use model instance for complete control
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-sonnet-4-5-20250929")
agent = create_deep_agent(model=model, ...)
```

## MCP Integration Issues

### Problem: MCP tool authentication fails

**Symptoms**:

```python
MCPError: Authentication failed: 401 Unauthorized
```

**Causes**:

- Token not passed in config
- Token expired or invalid
- Wrong token format

**Solutions**:

```python
# 1. Ensure token is passed via config
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "_user_token": token  # ← Must be here
        }
    }
)

# 2. Verify token format
import os
token = os.getenv("PLANTON_API_KEY")
print(f"Token: {token[:10]}...")  # Check it's not None

# 3. Test token directly with MCP server
import requests
response = requests.get(
    "https://mcp.planton.ai/health",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.status_code)  # Should be 200

# 4. Check token hasn't expired
# Get new token from provider if needed
```

### Problem: "Tool 'xyz' not found"

**Symptoms**:

```python
ToolNotFoundError: Tool 'list_organizations' not found in MCP server
```

**Causes**:

- Tool name typo
- Tool not available in MCP server
- Wrong MCP server URL

**Solutions**:

```python
# 1. Check exact tool name from MCP server
# Test MCP server directly:
from mcp import MCPClient
client = MCPClient(url="https://mcp.planton.ai/")
tools = client.list_tools()
print([t.name for t in tools])  # Get exact names

# 2. Verify MCP server URL
mcp_servers = {
    "planton-cloud": {
        "url": "https://mcp.planton.ai/",  # ✅ Correct
        # Not: "https://api.planton.ai/" or other URLs
    }
}

# 3. Use exact tool name from server
mcp_tools = {
    "planton-cloud": [
        "list_organizations",  # ✅ Exact match
        # Not: "list-organizations" or "listOrganizations"
    ]
}
```

### Problem: MCP tools not loading

**Symptoms**:

Agent created successfully but tools don't work when invoked.

**Causes**:

- Tools not loaded due to auth failure
- Middleware not executing
- Silent errors in tool loading

**Solutions**:

```python
# 1. Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

agent = create_deep_agent(...)
result = agent.invoke(...)  # Check logs for errors

# 2. Test tool loading separately
from graphton.core.mcp_manager import MCPManager
manager = MCPManager(mcp_servers_config={...}, mcp_tools_config={...})
tools = manager.load_tools(user_token="...")
print(f"Loaded {len(tools)} tools")

# 3. Verify middleware is present
# Graphton should auto-inject MCP middleware
# Check agent configuration includes middleware

# 4. Test without MCP first
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="Test without MCP",
    # No MCP config
)
result = agent.invoke({"messages": [...]})
# If this works, issue is with MCP configuration
```

## Performance Issues

### Problem: High latency in tool calls

**Symptoms**:

Tool calls take 5-10 seconds each.

**Causes**:

- Network latency to MCP server
- MCP server response time
- Multiple round-trips

**Solutions**:

```python
# 1. Batch operations when possible
# Instead of multiple separate calls, use batch endpoints

# 2. Add timeout configuration (future feature)
mcp_servers = {
    "planton-cloud": {
        "url": "https://mcp.planton.ai/",
        "timeout": 30,  # Future: configure timeout
    }
}

# 3. Use caching for repeated queries
# Cache results in your application layer

# 4. Monitor MCP server health
# Check if MCP server is experiencing issues
```

### Problem: High memory usage

**Symptoms**:

Python process using >2GB memory.

**Causes**:

- Large conversation history
- Many tool results stored
- Model embedding large contexts

**Solutions**:

```python
# 1. Limit conversation history
messages = result["messages"]
# Keep only last N messages
recent_messages = messages[-10:]
result = agent.invoke({"messages": recent_messages})

# 2. Summarize long conversations
# Use agent to summarize before continuing

# 3. Use smaller model
agent = create_deep_agent(
    model="claude-haiku-4",  # Uses less memory
    system_prompt=SYSTEM_PROMPT,
)

# 4. Clear context between invocations
# Don't reuse state across independent queries
```

## Deployment Issues

### Problem: Works locally, fails in LangGraph Cloud

**Symptoms**:

Agent works fine locally but fails when deployed to LangGraph Cloud.

**Causes**:

- Environment variable not set
- Dependencies not included
- Python version mismatch
- Context variables not working

**Solutions**:

```python
# 1. Verify all dependencies in requirements.txt
graphton @ git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
langchain>=1.0.0
langgraph>=1.0.0
# ... all other dependencies

# 2. Set environment variables in LangGraph Cloud
# Configure ANTHROPIC_API_KEY in deployment settings

# 3. Use config for runtime values (not environment)
# ✅ Good: Pass via config
result = agent.invoke(
    {...},
    config={"configurable": {"_user_token": token}}
)

# ❌ Bad: Rely on environment
token = os.getenv("USER_TOKEN")  # May not be available

# 4. Test with same Python version
# Check LangGraph Cloud Python version and match locally
```

### Problem: Cold start latency

**Symptoms**:

First invocation after deployment is very slow (30+ seconds).

**Causes**:

- Model initialization
- Dependency loading
- MCP connection establishment

**Solutions**:

```python
# 1. Use warm-up request after deployment
# Send dummy request to initialize everything

# 2. Keep agent instance warm
# Reuse same agent instance across requests
# Don't create new agent per request

# 3. Pre-load dependencies
# Import all modules at startup, not lazily

# 4. Use LangGraph Cloud warm pools (if available)
# Configure minimum instances to stay warm
```

## Development Issues

### Problem: Type checker (mypy) errors

**Symptoms**:

```bash
$ make typecheck
error: Incompatible types in assignment
```

**Causes**:

- Missing type hints
- Incorrect type annotations
- Model string not recognized by type checker

**Solutions**:

```bash
# 1. Check specific error file and line
mypy src/graphton/core/agent.py

# 2. Add type ignores for known issues
model: str | BaseChatModel = "claude-sonnet-4.5"  # type: ignore[assignment]

# 3. Update type hints
def create_agent(
    model: str | BaseChatModel,  # ← Clear union type
    system_prompt: str,
) -> CompiledStateGraph:  # ← Explicit return type
    ...

# 4. Run mypy with verbose output
mypy --show-error-codes --show-error-context src/
```

### Problem: Tests failing locally

**Symptoms**:

```bash
$ make test
FAILED tests/test_agent.py::test_create_agent - AssertionError
```

**Causes**:

- Missing environment variables
- Outdated dependencies
- Test isolation issues

**Solutions**:

```bash
# 1. Run specific failing test with verbose output
pytest -v tests/test_agent.py::test_create_agent

# 2. Set required environment variables
export ANTHROPIC_API_KEY="test-key"
export OPENAI_API_KEY="test-key"
make test

# 3. Update dependencies
poetry install
# or
pip install -e ".[dev]"

# 4. Clean and reinstall
make clean
rm -rf .pytest_cache
make deps
make test
```

### Problem: Linter (ruff) failures

**Symptoms**:

```bash
$ make lint
src/graphton/core/agent.py:42:1: E501 line too long (120 > 100 characters)
```

**Causes**:

- Code style violations
- Line length issues
- Import organization

**Solutions**:

```bash
# 1. Auto-fix most issues
ruff check --fix src/

# 2. Format code
ruff format src/

# 3. Check specific file
ruff check src/graphton/core/agent.py

# 4. See detailed error
ruff check --show-fixes src/

# 5. Ignore specific rules (if necessary)
# Add # noqa: E501 to end of line
long_string = "very long string..."  # noqa: E501
```

## Getting Help

### Before Asking for Help

1. **Search existing issues**: Someone may have had the same problem
2. **Read error messages carefully**: They often contain the solution
3. **Check documentation**: [README](../README.md), [API docs](API.md), [Configuration](CONFIGURATION.md)
4. **Try examples**: Run [examples](../examples/) to isolate the issue
5. **Check versions**: Ensure you're using compatible versions

### How to Ask for Help

When opening an issue or asking a question, include:

1. **Graphton version**:

```bash
pip show graphton
```

2. **Python version**:

```bash
python --version
```

3. **Operating system**:

```bash
uname -a  # macOS/Linux
# or System Information on Windows
```

4. **Minimal reproduction**:

```python
from graphton import create_deep_agent

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="Test",
)

result = agent.invoke({"messages": [...]})
# Error occurs here
```

5. **Full error message** (not screenshots):

```
Traceback (most recent call last):
  File "test.py", line 5, in <module>
    agent = create_deep_agent(...)
  ...
ValueError: Invalid configuration
```

6. **What you've tried**:
   - List troubleshooting steps attempted
   - What worked/didn't work

### Where to Get Help

- **Installation/Usage Questions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues) with `enhancement` label
- **Security Issues**: See [SECURITY.md](../SECURITY.md)
- **Documentation**: [README](../README.md) | [API](API.md) | [Configuration](CONFIGURATION.md) | [Migration](MIGRATION.md)

---

**Still stuck?** Open a [GitHub Discussion](https://github.com/plantoncloud-inc/graphton/discussions) and we'll help you out!

