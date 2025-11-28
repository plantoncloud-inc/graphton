# Graphton Examples

Comprehensive examples demonstrating Graphton features and usage patterns.

## Table of Contents

- [Overview](#overview)
- [Available Examples](#available-examples)
- [Running Examples](#running-examples)
- [Example Details](#example-details)
- [Modification Guides](#modification-guides)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Overview

These examples demonstrate how to use Graphton to create production-ready LangGraph agents with minimal boilerplate. Each example is self-contained and includes:

- Clear documentation and comments
- Environment setup instructions
- Expected output descriptions
- Modification guides for customization

## Available Examples

| Example | Description | Complexity | Features |
|---------|-------------|------------|----------|
| [simple_agent.py](#simple_agentpy) | Basic agent without MCP | ⭐ Basic | Model strings, custom parameters |
| [static_mcp_agent.py](#static_mcp_agentpy) | Static MCP configuration | ⭐⭐ Intermediate | MCP tools, shared credentials |
| [mcp_agent.py](#mcp_agentpy) | Dynamic MCP authentication | ⭐⭐⭐ Advanced | Template variables, per-user auth |
| [multi_auth_agent.py](#multi_auth_agentpy) | Multiple servers, mixed auth | ⭐⭐⭐⭐ Expert | Multi-server, mixed static/dynamic |

## Running Examples

### Prerequisites

1. **Python 3.11+** installed
2. **Graphton** installed:
   ```bash
   pip install git+https://github.com/plantoncloud-inc/graphton.git
   ```

3. **LLM API Keys** (at least one):
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   # Or
   export OPENAI_API_KEY="sk-..."
   ```

4. **MCP API Keys** (for MCP examples):
   ```bash
   export PLANTON_API_KEY="your-token-here"
   ```

### Run an Example

```bash
# From repository root
python examples/simple_agent.py

# Or from examples directory
cd examples
python simple_agent.py
```

## Example Details

### simple_agent.py

**Description:** Basic Deep Agent without MCP tools. Demonstrates the simplest possible agent creation.

**Features:**
- Model string usage (no manual instantiation)
- Simple Q&A interaction
- Multi-turn conversation
- Custom parameters (temperature, max_tokens)

**Prerequisites:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or
export OPENAI_API_KEY="sk-..."
```

**Run:**
```bash
python examples/simple_agent.py
```

**Expected Output:**
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
Creative Agent: [Creative, poetic response about sunset]
------------------------------------------------------------

✅ Examples completed successfully!
```

**Key Code:**
```python
from graphton import create_deep_agent

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful assistant.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Hello!"}]
})
```

**Modifications:** See [Modifying simple_agent.py](#modifying-simple_agentpy)

---

### static_mcp_agent.py

**Description:** Agent with static MCP configuration. Tools are loaded once at agent creation time.

**Features:**
- Static MCP server configuration
- Shared credentials (hardcoded or environment-specific)
- Zero runtime overhead for tool loading

**Use When:**
- Credentials are hardcoded or environment-specific
- All users share the same authentication
- MCP server doesn't require user-specific tokens

**Prerequisites:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# MCP_API_KEY is hardcoded in the example
```

**Run:**
```bash
python examples/static_mcp_agent.py
```

**Expected Output:**
```
Creating agent with static MCP configuration...
(Tools will be loaded once at creation time)

Agent created successfully!
Tools are ready to use.

Querying the agent...
------------------------------------------------------------
User: What information do you have access to?
Agent: I have access to a public API with search and fetch capabilities.
I can help you search for information and retrieve data.
------------------------------------------------------------

✅ Static MCP example completed successfully!
```

**Key Code:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={
        "public-api": {
            "transport": "http",
            "url": "https://api.example.com/mcp",
            "headers": {
                "X-API-Key": "hardcoded-key-123"  # No template variables
            }
        }
    },
    mcp_tools={
        "public-api": ["search", "fetch"]
    }
)

# No config needed - credentials already in config
result = agent.invoke({"messages": [...]})
```

**Modifications:** See [Modifying static_mcp_agent.py](#modifying-static_mcp_agentpy)

---

### mcp_agent.py

**Description:** Agent with dynamic MCP authentication using template variables. Tools are loaded per-request with user-specific tokens.

**Features:**
- Dynamic token injection with `{{USER_TOKEN}}` templates
- Per-user authentication
- Runtime template substitution

**Use When:**
- Multi-tenant systems
- User-specific API tokens required
- Different users need different permissions

**Prerequisites:**
```bash
export PLANTON_API_KEY="your-token-here"
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Run:**
```bash
python examples/mcp_agent.py
```

**Expected Output:**
```
Creating agent with MCP tools from Planton Cloud...

Agent created successfully!
MCP tools will be loaded at invocation time with user-specific token.

Querying the agent...
------------------------------------------------------------
User: List my organizations
Agent: [Lists actual organizations from Planton Cloud API]
------------------------------------------------------------

✅ MCP agent example completed successfully!
```

**Key Code:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a Planton Cloud assistant.",
    mcp_servers={
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
            "headers": {
                "Authorization": "Bearer {{USER_TOKEN}}"  # Template variable
            }
        }
    },
    mcp_tools={
        "planton-cloud": ["list_organizations", "search_cloud_resources"]
    },
)

# Provide user token at invocation
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "USER_TOKEN": os.getenv("PLANTON_API_KEY")  # Substituted at runtime
        }
    }
)
```

**Modifications:** See [Modifying mcp_agent.py](#modifying-mcp_agentpy)

---

### multi_auth_agent.py

**Description:** Agent with multiple MCP servers using mixed authentication methods.

**Features:**
- Multiple MCP servers in one agent
- Mixed static and dynamic authentication
- Different auth methods (Bearer token, API Key, etc.)

**Use When:**
- Need to integrate multiple external services
- Different services require different authentication
- Some services use shared credentials, others use user-specific tokens

**Prerequisites:**
```bash
export PLANTON_API_KEY="your-planton-token"
export EXTERNAL_API_KEY="your-external-key"
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Run:**
```bash
python examples/multi_auth_agent.py
```

**Expected Output:**
```
Creating agent with multiple MCP servers (mixed authentication)...

Agent created successfully!
Connected to 3 MCP servers:
  - planton-cloud (dynamic: Bearer token)
  - external-api (dynamic: API key)
  - public-api (static: Client ID)

Querying the agent...
------------------------------------------------------------
User: What resources are available?
Agent: [Uses tools from multiple servers to provide comprehensive answer]
------------------------------------------------------------

✅ Multi-auth example completed successfully!
```

**Key Code:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a multi-cloud assistant.",
    mcp_servers={
        # Dynamic: Bearer token
        "planton-cloud": {
            "headers": {"Authorization": "Bearer {{USER_TOKEN}}"}
        },
        # Dynamic: API Key
        "external-api": {
            "headers": {"X-API-Key": "{{API_KEY}}"}
        },
        # Static: Client ID
        "public-api": {
            "headers": {"X-Client-ID": "client-123"}
        }
    },
    mcp_tools={
        "planton-cloud": ["list_organizations"],
        "external-api": ["search"],
        "public-api": ["get_info"]
    }
)

# Provide dynamic values, static ones already in config
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "USER_TOKEN": os.getenv("PLANTON_API_KEY"),
            "API_KEY": os.getenv("EXTERNAL_API_KEY")
        }
    }
)
```

**Modifications:** See [Modifying multi_auth_agent.py](#modifying-multi_auth_agentpy)

## Modification Guides

### Modifying simple_agent.py

#### Change the Model

```python
# Use different Anthropic model
agent = create_deep_agent(
    model="claude-opus-4",  # More capable model
    system_prompt="...",
)

# Use OpenAI model
agent = create_deep_agent(
    model="gpt-4o",
    system_prompt="...",
)

# Use model instance for custom config
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="custom-model", max_tokens=50000)
agent = create_deep_agent(model=model, system_prompt="...")
```

#### Adjust Temperature

```python
# More deterministic (for code, facts)
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    temperature=0.0,
)

# More creative (for content, ideas)
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    temperature=1.0,
)
```

#### Change Recursion Limit

```python
# Simple Q&A (fewer steps)
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    recursion_limit=20,
)

# Complex reasoning (more steps)
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    recursion_limit=200,
)
```

### Modifying static_mcp_agent.py

#### Use Real MCP Server

```python
# Replace with actual server
mcp_servers = {
    "my-server": {
        "transport": "http",
        "url": "https://my-api.example.com/mcp",
        "headers": {
            "X-API-Key": os.getenv("MY_API_KEY")  # From environment
        }
    }
}
```

#### Add More Tools

```python
mcp_tools = {
    "my-server": [
        "search",
        "fetch",
        "create",  # Add more tools
        "update",
        "delete",
    ]
}
```

#### Combine with Custom Tools

```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> float:
    """Calculate a math expression."""
    return eval(expression)

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    tools=[calculate],  # Custom tools
    mcp_servers={...},   # MCP tools
    mcp_tools={...},
)
```

### Modifying mcp_agent.py

#### Change MCP Server

```python
# Use different MCP server
mcp_servers = {
    "my-service": {
        "transport": "streamable_http",
        "url": "https://mcp.my-service.com/",
        "headers": {
            "Authorization": "Bearer {{USER_TOKEN}}"
        }
    }
}
```

#### Add Multiple Template Variables

```python
mcp_servers = {
    "my-service": {
        "transport": "http",
        "url": "{{BASE_URL}}/api",
        "headers": {
            "Authorization": "Bearer {{USER_TOKEN}}",
            "X-Tenant-ID": "{{TENANT_ID}}"
        }
    }
}

# Provide all variables at invocation
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "BASE_URL": "https://api.example.com",
            "USER_TOKEN": "user-token",
            "TENANT_ID": "tenant-123"
        }
    }
)
```

#### Customize System Prompt

```python
SYSTEM_PROMPT = """You are a specialized assistant for {service_name}.

Your capabilities:
- List and search resources
- Create new resources
- Provide status updates

Important guidelines:
- Always verify before making changes
- Explain your actions clearly
- Ask for confirmation on destructive operations
"""
```

### Modifying multi_auth_agent.py

#### Add More Servers

```python
mcp_servers = {
    "planton-cloud": {...},
    "external-api": {...},
    "public-api": {...},
    "aws-tools": {  # Add another server
        "transport": "http",
        "url": "https://aws-mcp.example.com",
        "headers": {"X-AWS-Key": "{{AWS_KEY}}"}
    },
}

mcp_tools = {
    "planton-cloud": [...],
    "external-api": [...],
    "public-api": [...],
    "aws-tools": ["list_ec2", "list_s3"],
}
```

#### Mix Different Auth Methods

```python
mcp_servers = {
    # Bearer token
    "service-a": {
        "headers": {"Authorization": "Bearer {{TOKEN_A}}"}
    },
    # Basic auth
    "service-b": {
        "headers": {"Authorization": "Basic {{BASIC_CREDS}}"}
    },
    # API key
    "service-c": {
        "headers": {"X-API-Key": "{{API_KEY}}"}
    },
    # Custom headers
    "service-d": {
        "headers": {
            "X-Client-ID": "{{CLIENT_ID}}",
            "X-Client-Secret": "{{CLIENT_SECRET}}"
        }
    },
}
```

## Common Use Cases

### Use Case 1: Q&A Assistant

**Example:** [simple_agent.py](#simple_agentpy)

**Characteristics:**
- No external tools needed
- Simple conversation flow
- Low recursion limit (10-20)

**Template:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful Q&A assistant.",
    temperature=0.7,
    recursion_limit=20,
)
```

### Use Case 2: Code Generation

**Example:** [simple_agent.py](#simple_agentpy) with modifications

**Characteristics:**
- Deterministic output (temperature=0.0)
- Higher token limit for long code
- Clear, structured system prompt

**Template:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="""You are an expert Python developer.
    
    Write clean, well-documented code following PEP 8.
    Include type hints and docstrings.
    Provide explanations for complex logic.
    """,
    temperature=0.0,  # Deterministic
    max_tokens=10000,  # Allow longer responses
    recursion_limit=50,
)
```

### Use Case 3: Multi-Tenant SaaS

**Example:** [mcp_agent.py](#mcp_agentpy)

**Characteristics:**
- Per-user authentication
- Dynamic token injection
- User-specific resource access

**Template:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a SaaS assistant.",
    mcp_servers={
        "api": {
            "url": "https://api.example.com",
            "headers": {
                "Authorization": "Bearer {{USER_TOKEN}}",
                "X-Tenant-ID": "{{TENANT_ID}}"
            }
        }
    },
    mcp_tools={"api": ["list_resources", "create_resource"]},
)

# Different token per user
def handle_user_request(user_id, message):
    user_token = get_user_token(user_id)
    tenant_id = get_tenant_id(user_id)
    
    return agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={
            "configurable": {
                "USER_TOKEN": user_token,
                "TENANT_ID": tenant_id
            }
        }
    )
```

### Use Case 4: Integration Hub

**Example:** [multi_auth_agent.py](#multi_auth_agentpy)

**Characteristics:**
- Multiple external services
- Mixed authentication methods
- Unified interface across services

**Template:**
```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You integrate data from multiple services.",
    mcp_servers={
        "service-a": {...},  # Dynamic auth
        "service-b": {...},  # Static auth
        "service-c": {...},  # Different auth method
    },
    mcp_tools={
        "service-a": ["query_a"],
        "service-b": ["query_b"],
        "service-c": ["query_c"],
    },
)
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'graphton'"

**Solution:**
```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git
```

### "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or for OpenAI
export OPENAI_API_KEY="sk-..."
```

### "PLANTON_API_KEY not found" (MCP examples)

**Solution:**
```bash
export PLANTON_API_KEY="your-token-here"
# Get from: https://console.planton.cloud
```

### "Template variable 'USER_TOKEN' not found"

**Solution:** Provide template variables in config:
```python
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "USER_TOKEN": os.getenv("PLANTON_API_KEY")  # Must provide!
        }
    }
)
```

### "MCP connection failed"

**Solutions:**
1. Check network connectivity: `ping mcp.planton.ai`
2. Verify API token is valid
3. Check server URL is correct
4. Review [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)

### Examples run slowly

**Solutions:**
1. Reduce `recursion_limit` to 20-50
2. Simplify system prompt
3. Load only necessary tools
4. Use faster model (`claude-haiku-4`, `gpt-4o-mini`)

## Next Steps

After exploring examples:

1. **Read [Configuration Guide](../docs/CONFIGURATION.md)** for all configuration options
2. **Check [API Documentation](../docs/API.md)** for complete reference
3. **Review [Migration Guide](../docs/MIGRATION.md)** if migrating from raw LangGraph
4. **See [Troubleshooting](../docs/TROUBLESHOOTING.md)** for common issues

## Contributing

Found an issue or want to add an example?

1. Open an issue: https://github.com/plantoncloud-inc/graphton/issues
2. Submit a PR with your example
3. Follow [Contributing Guidelines](../CONTRIBUTING.md)

## License

These examples are part of Graphton and are licensed under Apache-2.0.
