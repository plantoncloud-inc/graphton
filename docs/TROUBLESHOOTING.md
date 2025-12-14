# Troubleshooting Guide

Comprehensive troubleshooting guide covering 50+ common issues across installation, runtime, configuration, MCP integration, performance, and deployment.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Errors](#runtime-errors)
- [Configuration Issues](#configuration-issues)
- [MCP Integration Issues](#mcp-integration-issues)
- [Authentication Issues](#authentication-issues)
- [Performance Issues](#performance-issues)
- [Deployment Issues](#deployment-issues)
- [Development Issues](#development-issues)
- [Getting Help](#getting-help)

## Installation Issues

### "Python version 3.11 or higher required"

**Symptoms:**
```
ERROR: Python 3.11 or higher is required
```

**Cause:** Your Python version is too old.

**Solution:**
```bash
# Check current version
python --version

# Install Python 3.11+ using pyenv
pyenv install 3.11
pyenv global 3.11

# Verify
python --version  # Should show 3.11.x or higher
```

### "Could not find a version that satisfies the requirement"

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement graphton
```

**Causes:**
1. Network connectivity issues
2. Dependency conflicts
3. Wrong installation method

**Solutions:**

```bash
# Try with verbose output to see what's failing
pip install -v git+https://github.com/plantoncloud/graphton.git

# Check network connectivity
ping github.com

# Try in clean environment
python -m venv clean_env
source clean_env/bin/activate
pip install git+https://github.com/plantoncloud/graphton.git

# If still failing, check specific dependency versions
pip install deepagents>=0.2.4  # Install manually first
```

### "Permission denied" errors

**Symptoms:**
```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Cause:** Insufficient permissions for global installation.

**Solutions:**

```bash
# Option 1: Install for user only
pip install --user git+https://github.com/plantoncloud/graphton.git

# Option 2: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install git+https://github.com/plantoncloud/graphton.git
```

### "Git not found" or "Git command failed"

**Symptoms:**
```
ERROR: Cannot find command 'git' - do you have 'git' installed and in your PATH?
```

**Cause:** Git is not installed or not in PATH.

**Solutions:**

```bash
# Install git
# macOS:
brew install git

# Ubuntu/Debian:
sudo apt-get install git

# Windows: Download from git-scm.com

# Verify installation
git --version
```

## Runtime Errors

### "ModuleNotFoundError: No module named 'graphton'"

**Symptoms:**
```python
ModuleNotFoundError: No module named 'graphton'
```

**Causes:**
1. Package not installed
2. Wrong Python environment
3. Installation failed silently

**Solutions:**

```bash
# Verify installation
pip list | grep graphton

# Check which Python you're using
which python
python -c "import sys; print(sys.prefix)"

# Reinstall if needed
pip install --force-reinstall git+https://github.com/plantoncloud/graphton.git
```

### "ANTHROPIC_API_KEY not found"

**Symptoms:**
```python
AnthropicAPIKeyNotFoundError: The api_key client option must be set
```

**Cause:** Environment variable not set.

**Solutions:**

```bash
# Set for current session
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify
echo $ANTHROPIC_API_KEY

# Make permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc

# Or use .env file
echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env
```

```python
# Load from .env in Python
from dotenv import load_dotenv
load_dotenv()
```

### "Rate limit exceeded"

**Symptoms:**
```python
RateLimitError: Error code: 429 - {'type': 'error', 'error': {'type': 'rate_limit_error', ...}}
```

**Cause:** Too many API requests to LLM provider.

**Solutions:**

```python
# Add retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
def invoke_agent(agent, messages):
    return agent.invoke({"messages": messages})

# Use it
result = invoke_agent(agent, messages)
```

```python
# Reduce recursion limit to use fewer tokens
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    recursion_limit=20,  # Lower limit = fewer API calls
)
```

### "RecursionError: maximum recursion depth exceeded"

**Symptoms:**
```python
RecursionError: maximum recursion depth exceeded
```

**Cause:** Agent reasoning loop exceeded recursion limit.

**Solutions:**

```python
# Increase recursion limit
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    recursion_limit=200,  # Increase from default 100
)
```

```python
# Or refine system prompt to guide agent to complete faster
system_prompt = """You are a helpful assistant.

IMPORTANT: Be concise and complete your responses quickly.
Avoid unnecessary follow-up questions unless critical.
"""
```

## Configuration Issues

### "system_prompt cannot be empty"

**Symptoms:**
```python
ValueError: Configuration validation failed:
system_prompt cannot be empty
```

**Cause:** Empty or missing system prompt.

**Solution:**

```python
# ❌ Wrong
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="",  # Empty
)

# ✅ Correct
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful assistant that answers questions clearly.",
)
```

### "system_prompt is too short"

**Symptoms:**
```python
ValueError: Configuration validation failed:
system_prompt is too short (5 chars). Provide at least 10 characters.
```

**Cause:** System prompt is less than 10 characters.

**Solution:**

```python
# ❌ Wrong
system_prompt = "Helper"  # Too short

# ✅ Correct
system_prompt = "You are a helpful assistant."  # At least 10 chars
```

### "recursion_limit must be positive"

**Symptoms:**
```python
ValueError: Configuration validation failed:
recursion_limit must be positive, got 0
```

**Cause:** Invalid recursion limit value.

**Solution:**

```python
# ❌ Wrong
recursion_limit = 0  # Must be > 0
recursion_limit = -10  # Must be > 0

# ✅ Correct
recursion_limit = 10  # Minimum sensible value
recursion_limit = 100  # Default
```

### "temperature must be between 0.0 and 2.0"

**Symptoms:**
```python
ValueError: Configuration validation failed:
temperature must be between 0.0 and 2.0, got 5.0
```

**Cause:** Invalid temperature value.

**Solution:**

```python
# ❌ Wrong
temperature = -0.5  # Too low
temperature = 3.0   # Too high

# ✅ Correct
temperature = 0.0   # Deterministic
temperature = 0.7   # Balanced
temperature = 1.0   # Creative
```

### "Unsupported model"

**Symptoms:**
```python
ValueError: Unsupported model: gpt-5-ultra
```

**Cause:** Invalid or unsupported model name.

**Solution:**

```python
# Supported Anthropic models
model = "claude-sonnet-4.5"  # → claude-sonnet-4-5-20250929
model = "claude-opus-4"      # → claude-opus-4-20250514
model = "claude-haiku-4"     # → claude-haiku-4-20250313

# Supported OpenAI models
model = "gpt-4o"
model = "gpt-4o-mini"
model = "gpt-4-turbo"
model = "o1"
model = "o1-mini"

# Or pass full model ID
model = "claude-sonnet-4-5-20250929"

# Or pass model instance
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="custom-model")
```

## MCP Integration Issues

### "mcp_servers provided but mcp_tools is missing"

**Symptoms:**
```python
ValueError: Configuration validation failed:
mcp_servers provided but mcp_tools is missing
```

**Cause:** `mcp_servers` provided without `mcp_tools`.

**Solution:**

```python
# ❌ Wrong - servers without tools
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={"planton-cloud": {...}},
    # Missing mcp_tools!
)

# ✅ Correct - both servers and tools
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={"planton-cloud": {...}},
    mcp_tools={"planton-cloud": ["list_organizations"]},
)
```

### "Server name mismatch between mcp_servers and mcp_tools"

**Symptoms:**
```python
ValueError: Configuration validation failed:
Server(s) configured but no tools specified: {'server-a'}
Tools specified for undefined server(s): {'server-b'}
```

**Cause:** Server names don't match between `mcp_servers` and `mcp_tools`.

**Solution:**

```python
# ❌ Wrong - mismatched names
mcp_servers = {"server-a": {...}}
mcp_tools = {"server-b": [...]}  # Different name!

# ✅ Correct - matching names
mcp_servers = {"planton-cloud": {...}}
mcp_tools = {"planton-cloud": [...]}  # Same name
```

### "Empty tool list for server"

**Symptoms:**
```python
ValueError: Configuration validation failed:
Empty tool list for server 'planton-cloud'
```

**Cause:** Tool list is empty.

**Solution:**

```python
# ❌ Wrong - empty list
mcp_tools = {"planton-cloud": []}

# ✅ Correct - at least one tool
mcp_tools = {"planton-cloud": ["list_organizations"]}
```

### "Template variable not provided"

**Symptoms:**
```python
ValueError: Template variable 'USER_TOKEN' not found in config
```

**Cause:** Template variable in MCP config but not provided at invocation.

**Solution:**

```python
# Config has template
mcp_servers = {
    "planton-cloud": {
        "headers": {"Authorization": "Bearer {{USER_TOKEN}}"}
    }
}

# ❌ Wrong - no token in config
result = agent.invoke({"messages": [...]})

# ✅ Correct - provide token
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "USER_TOKEN": "sk-..."  # Must provide!
        }
    }
)
```

### "MCP connection failed"

**Symptoms:**
```python
MCPConnectionError: Failed to connect to MCP server 'planton-cloud'
```

**Causes:**
1. Invalid server URL
2. Network connectivity issues
3. Server is down
4. Invalid authentication

**Solutions:**

```bash
# Check server URL
curl https://mcp.planton.ai/

# Check network connectivity
ping mcp.planton.ai

# Verify authentication token
export PLANTON_API_KEY="your-key-here"
echo $PLANTON_API_KEY
```

```python
# Add error handling
try:
    result = agent.invoke(
        {"messages": [...]},
        config={"configurable": {"USER_TOKEN": token}}
    )
except Exception as e:
    print(f"MCP connection failed: {e}")
    # Fall back to agent without MCP tools
```

### "Tool not found on MCP server"

**Symptoms:**
```python
MCPToolNotFoundError: Tool 'invalid_tool' not found on server 'planton-cloud'
```

**Cause:** Requested tool doesn't exist on the server.

**Solution:**

```python
# List available tools from server
# (Requires MCP client inspection - consult server docs)

# Remove invalid tool from config
mcp_tools = {
    "planton-cloud": [
        "list_organizations",  # ✅ Valid
        # "invalid_tool",  # ❌ Remove invalid
    ]
}
```

## Authentication Issues

### "Invalid API key"

**Symptoms:**
```python
AuthenticationError: Error code: 401 - {'type': 'error', 'error': {'type': 'authentication_error', ...}}
```

**Cause:** Invalid or expired API key.

**Solutions:**

```bash
# Verify API key format
echo $ANTHROPIC_API_KEY  # Should start with sk-ant-
echo $OPENAI_API_KEY     # Should start with sk-

# Check key is not expired (check provider dashboard)

# Try with new key
export ANTHROPIC_API_KEY="sk-ant-new-key"
```

### "Insufficient permissions for MCP server"

**Symptoms:**
```python
MCPAuthorizationError: 403 Forbidden - Insufficient permissions
```

**Cause:** Token doesn't have required permissions.

**Solutions:**

```bash
# Check token permissions in provider dashboard

# Generate new token with correct scopes

# Update token in environment
export PLANTON_API_KEY="new-token-with-permissions"
```

## Performance Issues

### "Agent invocation is very slow"

**Symptoms:** Agent takes minutes to respond.

**Causes:**
1. High recursion limit
2. Complex system prompt
3. Too many tools
4. Network latency

**Solutions:**

```python
# Reduce recursion limit
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    recursion_limit=20,  # Lower limit = faster
)
```

```python
# Simplify system prompt
system_prompt = """You are a helpful assistant.
Be concise and complete tasks quickly."""  # Simple & clear
```

```python
# Load only necessary tools
mcp_tools = {
    "planton-cloud": [
        "list_organizations",  # Only what you need
        # Don't load all available tools
    ]
}
```

### "High memory usage"

**Symptoms:** Agent process uses excessive RAM.

**Causes:**
1. Long conversation history
2. Too many tools loaded
3. Large MCP responses

**Solutions:**

```python
# Limit message history
def truncate_history(messages, max_messages=10):
    if len(messages) > max_messages:
        # Keep system message + last N messages
        return [messages[0]] + messages[-max_messages:]
    return messages

messages = truncate_history(state["messages"])
result = agent.invoke({"messages": messages})
```

```python
# Load tools selectively
mcp_tools = {
    "planton-cloud": ["list_organizations"]  # Only needed tools
}
```

### "Token limit exceeded"

**Symptoms:**
```python
InvalidRequestError: This model's maximum context length is 200000 tokens
```

**Cause:** Input + output exceeds model's context window.

**Solutions:**

```python
# Reduce max_tokens
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    max_tokens=5000,  # Lower limit
)
```

```python
# Truncate conversation history (see above)

# Simplify system prompt
system_prompt = "You are a helpful assistant."  # Brief
```

## Deployment Issues

### "Import error in production"

**Symptoms:**
```python
ModuleNotFoundError: No module named 'graphton'
```

**Cause:** Graphton not installed in production environment.

**Solutions:**

```dockerfile
# Add to Dockerfile
RUN pip install git+https://github.com/plantoncloud/graphton.git@v0.1.0
```

```yaml
# Add to requirements.txt
git+https://github.com/plantoncloud/graphton.git@v0.1.0
```

```yaml
# Add to pyproject.toml
[tool.poetry.dependencies]
graphton = {git = "https://github.com/plantoncloud/graphton.git", tag = "v0.1.0"}
```

### "Environment variables not set in production"

**Symptoms:**
```python
AnthropicAPIKeyNotFoundError: The api_key client option must be set
```

**Cause:** API keys not configured in production.

**Solutions:**

```bash
# Kubernetes secret
kubectl create secret generic api-keys \
  --from-literal=ANTHROPIC_API_KEY=sk-ant-... \
  --from-literal=OPENAI_API_KEY=sk-...
```

```yaml
# Add to deployment.yaml
env:
  - name: ANTHROPIC_API_KEY
    valueFrom:
      secretKeyRef:
        name: api-keys
        key: ANTHROPIC_API_KEY
```

```python
# Or use secrets management
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

os.environ['ANTHROPIC_API_KEY'] = get_secret('anthropic-key')
```

### "MCP servers unreachable from production"

**Symptoms:**
```python
MCPConnectionError: Connection timed out
```

**Causes:**
1. Firewall rules blocking outbound connections
2. Network policies
3. VPC configuration

**Solutions:**

```bash
# Check network connectivity from pod
kubectl exec -it <pod> -- curl https://mcp.planton.ai/

# Update firewall rules to allow outbound HTTPS

# Check VPC settings allow external connections
```

## Development Issues

### "Type checking errors with mypy"

**Symptoms:**
```
error: Argument 1 to "create_deep_agent" has incompatible type "str"; expected "BaseChatModel"
```

**Cause:** Type checker doesn't understand Graphton's union types.

**Solution:**

```python
# Use type: ignore if needed
agent = create_deep_agent(
    model="claude-sonnet-4.5",  # type: ignore[arg-type]
    system_prompt="...",
)

# Or satisfy type checker with instance
from langchain_anthropic import ChatAnthropic
model: BaseChatModel = ChatAnthropic(model="claude-sonnet-4-5-20250929")
agent = create_deep_agent(model=model, system_prompt="...")
```

### "Linter warnings about imports"

**Symptoms:**
```
F401 'graphton.create_deep_agent' imported but unused
```

**Cause:** Linter doesn't recognize usage pattern.

**Solution:**

```python
# Use noqa comment if needed
from graphton import create_deep_agent  # noqa: F401

# Or configure ruff/flake8 to ignore
# .flake8 or pyproject.toml
per-file-ignores =
    tests/*: F401
```

### "Tests failing with mock models"

**Symptoms:**
```python
TypeError: Expected BaseChatModel, got Mock
```

**Cause:** Mock doesn't implement required interface.

**Solution:**

```python
# Properly mock BaseChatModel
from unittest.mock import Mock
from langchain_core.language_models.chat_models import BaseChatModel

mock_model = Mock(spec=BaseChatModel)
mock_model.invoke.return_value = {"content": "Test response"}

agent = create_deep_agent(
    model=mock_model,
    system_prompt="Test agent",
)
```

## Getting Help

### Before Opening an Issue

1. **Check this troubleshooting guide**
2. **Search existing issues:** https://github.com/plantoncloud/graphton/issues
3. **Review documentation:**
   - [Configuration Guide](CONFIGURATION.md)
   - [Installation Guide](INSTALLATION.md)
   - [Migration Guide](MIGRATION.md)

### When Opening an Issue

Include:

1. **Environment info:**
   ```bash
   python --version
   pip list | grep -E "(graphton|langgraph|langchain|deepagents)"
   ```

2. **Minimal reproduction:**
   ```python
   from graphton import create_deep_agent
   
   agent = create_deep_agent(
       model="claude-sonnet-4.5",
       system_prompt="...",
   )
   # ... code that fails
   ```

3. **Full error message:**
   ```python
   # Include complete traceback
   ```

4. **What you expected:** Describe expected behavior

5. **What happened:** Describe actual behavior

### Community Resources

- **GitHub Issues:** https://github.com/plantoncloud/graphton/issues
- **Discussions:** https://github.com/plantoncloud/graphton/discussions
- **Examples:** https://github.com/plantoncloud/graphton/tree/main/examples

### Emergency Workarounds

If you're blocked, you can always fall back to raw deepagents:

```python
# Temporary workaround
from deepagents import create_deep_agent as deepagents_create_deep_agent
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model_name="claude-sonnet-4-5-20250929")
agent = deepagents_create_deep_agent(
    model=model,
    tools=[],
    system_prompt="...",
    middleware=[],
)
```

Then open an issue so we can fix the problem in Graphton!
