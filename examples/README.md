# Graphton Examples

This directory contains working examples demonstrating Graphton's features.

## Prerequisites

- **Python 3.11+**
- **Graphton installed**: See [installation instructions](../docs/INSTALLATION.md)
- **API keys**: Required for running examples (see below)

## Quick Start

```bash
# Install Graphton
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run an example
python examples/simple_agent.py
```

## Examples Overview

### 1. simple_agent.py - Basic Agent

**Purpose**: Demonstrates creating a basic Deep Agent without MCP tools.

**What it shows**:
- Creating agent with model string and system prompt
- Single-turn and multi-turn conversations
- Custom parameters (temperature, max_tokens)
- How little code is needed (~10 lines)

**Requirements**:
- `ANTHROPIC_API_KEY` environment variable

**Run**:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python examples/simple_agent.py
```

**Expected output**:

```
Creating agent and asking a question...
------------------------------------------------------------
User: What is the capital of France?
Agent: The capital of France is Paris.
------------------------------------------------------------

Multi-turn conversation example:
------------------------------------------------------------
User: What is 7 times 8?
Agent: 56
User: And what is that plus 10?
Agent: 66
------------------------------------------------------------

Agent with custom parameters:
------------------------------------------------------------
User: Describe a sunset in three sentences.
Creative Agent: [Poetic description]
------------------------------------------------------------

✅ Examples completed successfully!
```

**What you'll learn**:
- Basic agent creation syntax
- How to invoke agents
- Multi-turn conversation patterns
- Parameter customization

### 2. mcp_agent.py - Agent with MCP Tools

**Purpose**: Demonstrates creating an agent with MCP tools from Planton Cloud.

**What it shows**:
- MCP server configuration
- Tool selection from MCP server
- Per-user authentication
- Real tool usage in agent
- How MCP integration reduces boilerplate

**Requirements**:
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` environment variable
- `PLANTON_API_KEY` environment variable (get from [console.planton.cloud](https://console.planton.cloud))

**Run**:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export PLANTON_API_KEY="your-planton-token"
python examples/mcp_agent.py
```

**Expected output**:

```
Creating agent with MCP tools from Planton Cloud...
Agent created successfully!

Asking agent to list organizations...
------------------------------------------------------------
Agent: You have 3 organizations:
1. My Org (my-org)
2. Dev Team (dev-team)
3. Production (prod)
------------------------------------------------------------

Asking agent to search for cloud resources...
------------------------------------------------------------
Agent: Found 2 Kubernetes deployments in dev environment:
- web-app (KubernetesDeployment)
- api-service (KubernetesDeployment)
------------------------------------------------------------

✅ Example completed successfully!
```

**What you'll learn**:
- MCP server configuration format
- How to select specific tools
- Passing user credentials via config
- Real-world agent with tools

## Running All Examples

```bash
# Set API keys
export ANTHROPIC_API_KEY="sk-ant-..."
export PLANTON_API_KEY="your-token"  # Optional, only for mcp_agent.py

# Run simple agent example
python examples/simple_agent.py

# Run MCP agent example (requires Planton API key)
python examples/mcp_agent.py
```

## Modifying Examples

### Change the Model

```python
# Use different model
agent = create_deep_agent(
    model="gpt-4o",  # Instead of claude-sonnet-4.5
    system_prompt=SYSTEM_PROMPT,
)

# Use OpenAI instead of Anthropic
export OPENAI_API_KEY="sk-..."
```

### Adjust Agent Behavior

```python
# More creative responses
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    temperature=0.9,  # Higher creativity
)

# Shorter responses
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    max_tokens=500,  # Limit length
)

# More reasoning steps
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    recursion_limit=200,  # More steps
)
```

### Add Your Own Tools

```python
from langchain.tools import tool

@tool
def custom_calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a math assistant.",
    tools=[custom_calculator],  # Add custom tool
)
```

### Use Different MCP Server

```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    
    # Your own MCP server
    mcp_servers={
        "my-server": {
            "transport": "streamable_http",
            "url": "https://mcp.myservice.com/",
        }
    },
    
    mcp_tools={
        "my-server": [
            "tool1",
            "tool2",
        ]
    }
)
```

## Testing Examples

### Test in Fresh Environment

```bash
# Create clean environment
python -m venv test-env
source test-env/bin/activate  # Windows: test-env\Scripts\activate

# Install Graphton
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Run examples
python examples/simple_agent.py
python examples/mcp_agent.py
```

### Verify Examples Work

```bash
# Check exit codes
python examples/simple_agent.py && echo "✅ simple_agent passed"
python examples/mcp_agent.py && echo "✅ mcp_agent passed"
```

## Common Issues

### Issue: "API key not found"

**Solution**: Set environment variable before running:

```bash
export ANTHROPIC_API_KEY="your-key"
python examples/simple_agent.py
```

### Issue: "MCP authentication failed"

**Solution**: Verify Planton API key is valid:

```bash
# Get key from https://console.planton.cloud
export PLANTON_API_KEY="your-token"
python examples/mcp_agent.py
```

### Issue: "ModuleNotFoundError: No module named 'graphton'"

**Solution**: Install Graphton first:

```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

### Issue: Examples run but output is unexpected

**Solution**: Check you're using the correct model and API key:

```python
# Verify API key is set
import os
print(os.getenv("ANTHROPIC_API_KEY"))  # Should not be None

# Try with explicit key (for testing only)
os.environ["ANTHROPIC_API_KEY"] = "your-key"
```

## Creating Your Own Example

```python
"""my_example.py - Custom agent example."""

from graphton import create_deep_agent

# Define your system prompt
SYSTEM_PROMPT = """You are a [description].

Your capabilities:
- [Capability 1]
- [Capability 2]

Guidelines:
- [Guideline 1]
- [Guideline 2]
"""

# Create agent
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    # Add your configuration
)

# Test it
if __name__ == "__main__":
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": "Your test query"}
        ]
    })
    
    response = result["messages"][-1]["content"]
    print(f"Agent: {response}")
```

## Example Use Cases

### Code Review Agent

```python
SYSTEM_PROMPT = """You are a code review assistant.

When reviewing code:
- Check for bugs and potential issues
- Suggest improvements
- Verify best practices
- Provide constructive feedback
"""

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    temperature=0.3,  # More deterministic
)
```

### Creative Writing Agent

```python
SYSTEM_PROMPT = """You are a creative writing assistant.

Help users:
- Brainstorm ideas
- Develop characters
- Craft compelling narratives
- Improve their writing
"""

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    temperature=0.9,  # More creative
    max_tokens=2000,
)
```

### Data Analysis Agent

```python
from langchain.tools import tool

@tool
def analyze_data(data: str) -> str:
    """Analyze data and return insights."""
    # Your analysis logic
    return "Analysis results..."

SYSTEM_PROMPT = """You are a data analyst.

Analyze data and provide:
- Key insights
- Trends and patterns
- Actionable recommendations
"""

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    tools=[analyze_data],
)
```

## Next Steps

After exploring these examples:

1. **Read the documentation**: [README](../README.md) | [API Docs](../docs/API.md) | [Configuration](../docs/CONFIGURATION.md)
2. **Try the migration guide**: [Migrate your existing agents](../docs/MIGRATION.md)
3. **Build your own agent**: Start with an example and customize it
4. **Contribute**: Share your examples by opening a PR

## Getting Help

- **Questions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)
- **Issues**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues)
- **Documentation**: [docs/](../docs/)
- **Troubleshooting**: [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)

---

**Happy coding with Graphton!** 🚀

Share your examples and use cases in [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)!

