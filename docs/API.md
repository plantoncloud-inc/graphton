# Graphton API Documentation

This document provides detailed API documentation for Graphton's core functions and classes.

## Core Functions

### `create_deep_agent()`

The main entry point for creating LangGraph Deep Agents with minimal boilerplate.

```python
def create_deep_agent(
    model: str | BaseChatModel,
    system_prompt: str,
    mcp_servers: dict[str, dict[str, Any]] | None = None,
    mcp_tools: dict[str, list[str]] | None = None,
    tools: Sequence[BaseTool] | None = None,
    middleware: Sequence[Any] | None = None,
    context_schema: type[Any] | None = None,
    recursion_limit: int = 100,
    max_tokens: int | None = None,
    temperature: float | None = None,
    **model_kwargs: Any,
) -> CompiledStateGraph
```

#### Parameters

**`model`** (str | BaseChatModel)
- Model name string (e.g., "claude-sonnet-4.5", "gpt-4o") or a LangChain model instance
- String format supports friendly model names that automatically map to full model IDs
- Examples: `"claude-sonnet-4.5"`, `"gpt-4o"`, `"claude-haiku-4"`

**`system_prompt`** (str)
- The system prompt that defines the agent's role, capabilities, and behavior
- Must be non-empty
- This is the primary way to control agent behavior

**`mcp_servers`** (dict[str, dict[str, Any]] | None, default: None)
- Optional MCP server configurations
- Format compatible with Cursor's mcp.json
- See [MCP Integration](#mcp-integration) section for details

**`mcp_tools`** (dict[str, list[str]] | None, default: None)
- Optional MCP tools to load from configured servers
- Must be provided if mcp_servers is specified
- See [MCP Integration](#mcp-integration) section for details

**`tools`** (Sequence[BaseTool] | None, default: None)
- Optional list of LangChain tools the agent can use
- Defaults to empty list if not provided
- Can be combined with MCP tools

**`middleware`** (Sequence[Any] | None, default: None)
- Optional list of middleware to run before/after agent execution
- Defaults to empty list if not provided
- MCP tool loading middleware is auto-injected when mcp_servers is specified

**`context_schema`** (type[Any] | None, default: None)
- Optional state schema for the agent
- Defaults to FilesystemState from deepagents if not provided
- Use this to define custom state structure for your agent

**`recursion_limit`** (int, default: 100)
- Maximum recursion depth for the agent
- Prevents infinite loops in agent reasoning
- Must be positive (> 0)
- Higher values allow more complex reasoning chains

**`max_tokens`** (int | None, default: None)
- Override default max_tokens for the model
- Defaults depend on provider:
  - Anthropic: 20000 (Deep Agents need high limits)
  - OpenAI: Model default
- Ignored if `model` is a model instance (not a string)

**`temperature`** (float | None, default: None)
- Override default temperature for the model
- Higher values (0.7-1.0) make output more creative
- Lower values (0.0-0.3) make it more deterministic
- Ignored if `model` is a model instance (not a string)

**`**model_kwargs`** (Any)
- Additional model-specific parameters
- Examples: `top_p`, `top_k` for Anthropic
- Ignored if `model` is a model instance (not a string)

#### Returns

**CompiledStateGraph**
- A compiled LangGraph agent ready to invoke with messages
- Can be invoked using `.invoke()` method
- Supports streaming and other LangGraph features

#### Raises

**ValueError**
- If `system_prompt` is empty or whitespace-only
- If `recursion_limit` is not positive
- If `model` string is invalid or unsupported

#### Examples

**Basic usage:**
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

**With custom parameters:**
```python
agent = create_deep_agent(
    model="gpt-4o",
    system_prompt="You are a code reviewer.",
    temperature=0.3,
    max_tokens=5000,
    recursion_limit=50,
)
```

**With model instance (advanced):**
```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-opus-4-20250514",
    max_tokens=30000,
    temperature=0.7,
)

agent = create_deep_agent(
    model=model,
    system_prompt="You are a research assistant.",
)
```

**With custom state schema:**
```python
from typing import TypedDict

class CustomState(TypedDict):
    messages: list
    user_data: dict

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful assistant.",
    context_schema=CustomState,
)
```

#### Notes

- When passing a model instance, `max_tokens`, `temperature`, and `**model_kwargs` are ignored and a warning is issued
- Model name strings are case-sensitive
- Provider prefixes are supported: `"anthropic:claude-sonnet-4.5"`, `"openai:gpt-4o"`
- The recursion limit is applied via LangGraph's configuration system

---

## Model Name Parsing

### Supported Model Names

#### Anthropic Models

Graphton provides friendly aliases for Anthropic models:

| Alias | Full Model ID |
|-------|--------------|
| `claude-sonnet-4.5` | `claude-sonnet-4-5-20250929` |
| `claude-opus-4` | `claude-opus-4-20250514` |
| `claude-haiku-4` | `claude-haiku-4-20250313` |

You can also use full model IDs directly:
```python
agent = create_deep_agent(
    model="claude-sonnet-4-5-20250929",
    system_prompt="...",
)
```

**Default Parameters for Anthropic:**
- `max_tokens`: 20000 (suitable for Deep Agents with reasoning)

#### OpenAI Models

OpenAI model names are passed through without aliases:
- `gpt-4o`
- `gpt-4o-mini`
- `gpt-4-turbo`
- `o1`
- `o1-mini`

**Default Parameters for OpenAI:**
- No special defaults (uses OpenAI's model defaults)

#### Provider Prefixes

You can explicitly specify the provider:
```python
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4.5",
    system_prompt="...",
)

agent = create_deep_agent(
    model="openai:gpt-4o",
    system_prompt="...",
)
```

---

## Agent Invocation

Once you've created an agent, you invoke it with messages:

### Basic Invocation

```python
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 2+2?"}
    ]
})

# Extract the response
response = result["messages"][-1]["content"]
print(response)
```

### Multi-Turn Conversations

To maintain conversation context, pass the messages back to the agent:

```python
# First turn
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 5+3?"}
    ]
})

# Second turn - continue conversation
messages = result["messages"]
messages.append({"role": "user", "content": "And what is that times 2?"})

result = agent.invoke({"messages": messages})
```

### With Configuration

You can pass additional configuration at invoke time:

```python
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            # Phase 3: User tokens for MCP authentication
            "_user_token": "your-token-here",
        },
        "recursion_limit": 200,  # Override default
    }
)
```

---

## Error Handling

### Common Errors

**Empty System Prompt**
```python
# ❌ Raises ValueError
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="",
)
```

**Invalid Recursion Limit**
```python
# ❌ Raises ValueError
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are helpful.",
    recursion_limit=0,  # Must be > 0
)
```

**Invalid Model Name**
```python
# ❌ Raises ValueError
agent = create_deep_agent(
    model="invalid-model",
    system_prompt="You are helpful.",
)
```

**Model Instance with Extra Parameters**
```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-sonnet-4-5-20250929", max_tokens=10000)

# ⚠️ Issues UserWarning (parameters ignored)
agent = create_deep_agent(
    model=model,
    system_prompt="You are helpful.",
    max_tokens=15000,  # This will be ignored
)
```

### Best Practices

1. **Use string model names for simplicity:**
   ```python
   # ✅ Recommended
   agent = create_deep_agent(model="claude-sonnet-4.5", ...)
   ```

2. **Only use model instances when you need fine-grained control:**
   ```python
   # ✅ For advanced use cases
   model = ChatAnthropic(model="claude-opus-4", max_tokens=30000, top_p=0.95)
   agent = create_deep_agent(model=model, ...)
   ```

3. **Validate your system prompt is non-empty:**
   ```python
   # ✅ Good
   if not system_prompt or not system_prompt.strip():
       raise ValueError("System prompt required")
   
   agent = create_deep_agent(model="claude-sonnet-4.5", system_prompt=system_prompt)
   ```

4. **Set appropriate recursion limits:**
   ```python
   # ✅ For simple Q&A
   agent = create_deep_agent(model="claude-haiku-4", ..., recursion_limit=10)
   
   # ✅ For complex reasoning
   agent = create_deep_agent(model="claude-sonnet-4.5", ..., recursion_limit=200)
   ```

---

## Type Hints

Graphton is fully type-hinted and includes a `py.typed` marker for type checkers:

```python
from graphton import create_deep_agent
from langgraph.graph.state import CompiledStateGraph

# Type checker knows the return type
agent: CompiledStateGraph = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are helpful.",
)
```

---

## Advanced Usage

### Custom State Schema

Define custom state structure for your agent:

```python
from typing import TypedDict, List, Dict, Any

class MyAgentState(TypedDict):
    """Custom state for my agent."""
    messages: List[Dict[str, str]]
    user_data: Dict[str, Any]
    processing_steps: List[str]

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a data processor.",
    context_schema=MyAgentState,
)

# Invoke with custom state
result = agent.invoke({
    "messages": [...],
    "user_data": {"user_id": "123"},
    "processing_steps": [],
})
```

### Model-Specific Parameters

Pass provider-specific parameters:

```python
# Anthropic-specific parameters
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    top_p=0.9,
    top_k=40,
)

# OpenAI-specific parameters
agent = create_deep_agent(
    model="gpt-4o",
    system_prompt="...",
    presence_penalty=0.1,
    frequency_penalty=0.1,
)
```

---

## MCP Integration

Graphton provides first-class support for MCP (Model Context Protocol) tools with zero boilerplate.

### MCP Parameters

#### mcp_servers: dict[str, dict[str, Any]] | None = None

Configuration for MCP servers.

**Format** (compatible with Cursor's mcp.json):

```python
mcp_servers={
    "server-name": {
        "transport": "streamable_http",  # Only streamable_http supported currently
        "url": "https://mcp.example.com/",  # MCP server URL
        "auth_from_context": True,  # Extract token from runtime (default)
        "headers": {  # Optional additional headers
            "Custom-Header": "value"
        }
    }
}
```

**Multiple Servers**:

```python
mcp_servers={
    "planton-cloud": {
        "transport": "streamable_http",
        "url": "https://mcp.planton.ai/",
    },
    "github": {
        "transport": "streamable_http",
        "url": "https://mcp.github.com/",
    }
}
```

#### mcp_tools: dict[str, list[str]] | None = None

Specify which tools to load from each MCP server.

**Format**:

```python
mcp_tools={
    "server-name": [
        "tool1",
        "tool2",
        "tool3",
    ]
}
```

**Example**:

```python
mcp_tools={
    "planton-cloud": [
        "list_organizations",
        "create_cloud_resource",
        "get_cloud_resource_schema",
    ],
    "github": [
        "list_repos",
        "create_issue",
    ]
}
```

**Tool Name Requirements**:

- Must be exact tool names from MCP server
- Use lowercase with underscores (snake_case)
- No duplicates within a server

### Complete MCP Example

```python
from graphton import create_deep_agent
import os

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a Planton Cloud assistant.",
    
    # MCP server configuration
    mcp_servers={
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
        }
    },
    
    # Tool selection
    mcp_tools={
        "planton-cloud": [
            "list_organizations",
            "create_cloud_resource",
        ]
    }
)

# Invoke with per-user authentication
result = agent.invoke(
    {"messages": [{"role": "user", "content": "List my organizations"}]},
    config={
        "configurable": {
            "_user_token": os.getenv("PLANTON_API_KEY")
        }
    }
)
```

### Per-User Authentication

MCP tools support per-user authentication via config:

```python
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "_user_token": user_token  # User's API token
        }
    }
)
```

**How it works**:

1. Token passed via config (not environment)
2. Graphton extracts token at runtime
3. Token added to MCP client Authorization header
4. Each invocation can use different user's token

**Benefits**:

- ✅ Multi-tenant support
- ✅ Works in LangGraph Cloud
- ✅ Secure (no tokens in code)
- ✅ Per-request authentication

### Tool Wrapper Auto-Generation

Graphton automatically generates tool wrappers for MCP tools. No manual `@tool` decorators needed.

**Without Graphton** (~20 lines per tool):

```python
from langchain.tools import tool

@tool
async def list_organizations() -> str:
    """List all organizations."""
    client = get_mcp_client()
    result = await client.call_tool("list_organizations", {})
    return result

# Repeat for every tool...
```

**With Graphton** (0 lines):

```python
# Just list the tools you want
mcp_tools = {
    "planton-cloud": [
        "list_organizations",
        "create_cloud_resource",
        # ... add more tools
    ]
}
```

### Validation

MCP configuration is validated at agent creation time:

```python
# ❌ Error: MCP servers without tools
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={"server": {...}},
    mcp_tools=None,  # Missing
)
# ValidationError: mcp_servers provided but mcp_tools is missing

# ❌ Error: Server name mismatch
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={"server-a": {...}},
    mcp_tools={"server-b": [...]},  # Names don't match
)
# ValidationError: Server names don't match
```

For complete MCP documentation, see [examples/mcp_agent.py](../examples/mcp_agent.py) and [Configuration Guide](CONFIGURATION.md).

---

## See Also

- [README.md](../README.md) - Project overview and quick start
- [examples/](../examples/) - Working code examples
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - Underlying framework
- [Deep Agents](https://github.com/langchain-ai/deepagents) - Deep Agent pattern

