# Migration Guide: From Raw LangGraph to Graphton

Transform your LangGraph agents from 100+ lines of boilerplate to 10 lines of declarative configuration.

## Table of Contents

- [Overview](#overview)
- [Why Migrate?](#why-migrate)
- [Basic Agent Migration](#basic-agent-migration)
- [MCP Tools Migration](#mcp-tools-migration)
- [Advanced Patterns](#advanced-patterns)
- [Migration Checklist](#migration-checklist)
- [Troubleshooting](#troubleshooting)

## Overview

Graphton eliminates the boilerplate required to create LangGraph Deep Agents while maintaining full power and flexibility. This guide walks you through migrating existing agents to Graphton's declarative API.

**Expected Results**:

- 80-90% reduction in boilerplate code
- Consistent patterns across all agents
- Faster agent development
- Easier maintenance and testing
- Same performance and capabilities

## Why Migrate?

### Before: Raw LangGraph

Typical pain points when building agents manually:

1. **Manual Model Instantiation** (~10 lines)
   - Import model classes
   - Configure model parameters
   - Handle different providers
   - Set default tokens and temperature

2. **State Schema Boilerplate** (~5-10 lines)
   - Import FilesystemState or define custom
   - Configure state annotations
   - Handle message types

3. **MCP Tool Setup** (~50-100+ lines per agent)
   - Create MCP client instances
   - Write tool wrapper functions
   - Implement middleware for tool loading
   - Handle per-user authentication
   - Manage async/sync conversions

4. **Graph Creation** (~20 lines)
   - Call create_deep_agent with all configs
   - Set recursion limits
   - Compile graph
   - Add error handling

**Total**: 100-150 lines of setup before writing agent logic.

### After: Graphton

All the above becomes ~10 lines of declarative configuration:

```python
from graphton import create_deep_agent

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=YOUR_PROMPT,
    mcp_servers={...},
    mcp_tools={...}
)
```

## Basic Agent Migration

### Before: Raw LangGraph (~50 lines)

```python
"""Raw LangGraph agent - lots of boilerplate."""

from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent
from deepagents.state import FilesystemState

# Manual model instantiation
model = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    max_tokens=20000,
    temperature=0.5,
)

# System prompt
SYSTEM_PROMPT = """You are a helpful coding assistant.

When asked to write code:
- Use modern best practices
- Include error handling
- Add helpful comments
- Follow PEP 8 style guide
"""

# Create agent with explicit configuration
agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[],  # No tools
    context_schema=FilesystemState,
    recursion_limit=100,
)

# Invoke
result = agent.invoke({
    "messages": [{"role": "user", "content": "Write a hello world"}]
})
```

**Lines**: ~40 lines of setup

**Issues**:

- Manual model instantiation
- Provider-specific code
- Hardcoded model parameters
- Explicit state schema required
- Verbose configuration

### After: Graphton (~10 lines)

```python
"""Graphton agent - minimal boilerplate."""

from graphton import create_deep_agent

# System prompt (same as before)
SYSTEM_PROMPT = """You are a helpful coding assistant.

When asked to write code:
- Use modern best practices
- Include error handling
- Add helpful comments
- Follow PEP 8 style guide
"""

# Create agent - that's it!
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
)

# Invoke (same as before)
result = agent.invoke({
    "messages": [{"role": "user", "content": "Write a hello world"}]
})
```

**Lines**: ~10 lines (75% reduction)

**Benefits**:

- ✅ Friendly model names
- ✅ Sensible defaults
- ✅ No provider-specific code
- ✅ Automatic state schema
- ✅ Clean, declarative API

### Migration Steps for Basic Agents

1. **Replace model instantiation with string**:

```python
# Before
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-sonnet-4-5-20250929", max_tokens=20000)

# After
model = "claude-sonnet-4.5"
```

2. **Remove state schema if using FilesystemState**:

```python
# Before
from deepagents.state import FilesystemState
agent = create_deep_agent(..., context_schema=FilesystemState)

# After (FilesystemState is default)
agent = create_deep_agent(...)
```

3. **Simplify create_deep_agent import**:

```python
# Before
from deepagents import create_deep_agent

# After
from graphton import create_deep_agent
```

4. **Keep system prompt and invocation the same**:
   - System prompts are unchanged
   - Agent invocation API is identical

## MCP Tools Migration

### Before: Manual MCP Setup (~150 lines)

Here's what manual MCP integration looks like (real example from graph-fleet):

**File: `mcp_tools.py` (~40 lines)**

```python
"""Manual MCP tool definitions."""

from langchain.tools import tool
from mcp_client import get_mcp_client

@tool
async def list_organizations() -> str:
    """List all organizations."""
    client = get_mcp_client()
    result = await client.call_tool("list_organizations", {})
    return result

@tool
async def create_cloud_resource(
    org_id: str,
    env_name: str,
    resource_kind: str,
    resource_name: str,
    spec: dict,
) -> str:
    """Create a cloud resource."""
    client = get_mcp_client()
    result = await client.call_tool("create_cloud_resource", {
        "org_id": org_id,
        "env_name": env_name,
        "resource_kind": resource_kind,
        "resource_name": resource_name,
        "spec": spec,
    })
    return result

# ... more tools (repeat pattern for each tool)
```

**File: `mcp_client.py` (~50 lines)**

```python
"""MCP client management."""

import os
from mcp_sdk import MCPClient

_client = None

def get_mcp_client() -> MCPClient:
    """Get or create MCP client."""
    global _client
    if _client is None:
        token = os.getenv("PLANTON_API_KEY")
        _client = MCPClient(
            url="https://mcp.planton.ai/",
            headers={"Authorization": f"Bearer {token}"}
        )
    return _client

def set_user_token(token: str):
    """Update client token for current user."""
    global _client
    _client = MCPClient(
        url="https://mcp.planton.ai/",
        headers={"Authorization": f"Bearer {token}"}
    )
```

**File: `middleware.py` (~30 lines)**

```python
"""Middleware for loading MCP tools."""

from mcp_client import set_user_token

async def load_mcp_tools_middleware(context, state, next):
    """Load MCP tools with user token."""
    # Extract user token from runtime context
    token = context.get("_user_token")
    if token:
        set_user_token(token)
    
    # Continue with agent execution
    return await next(state)
```

**File: `agent.py` (~30 lines)**

```python
"""Agent creation with MCP tools."""

from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent
from mcp_tools import list_organizations, create_cloud_resource
from middleware import load_mcp_tools_middleware

# Model
model = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",
    max_tokens=20000,
)

# System prompt
SYSTEM_PROMPT = """You are a Planton Cloud assistant..."""

# Create agent with MCP tools
agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[list_organizations, create_cloud_resource],
    middleware=[load_mcp_tools_middleware],
    recursion_limit=100,
)

# Invoke with user token
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"_user_token": user_token}}
)
```

**Total**: ~150 lines across 4 files

**Issues**:

- ❌ Manual tool wrapper for every MCP tool
- ❌ Custom MCP client management
- ❌ Complex middleware implementation
- ❌ Per-user authentication handling
- ❌ Error-prone async/sync conversions
- ❌ Lots of repetitive code

### After: Graphton (~15 lines)

All 150 lines become this:

```python
"""Graphton agent with MCP tools - zero boilerplate."""

from graphton import create_deep_agent
import os

# System prompt (same as before)
SYSTEM_PROMPT = """You are a Planton Cloud assistant..."""

# Create agent with MCP tools
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    
    # MCP server configuration (Cursor-compatible format)
    mcp_servers={
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
        }
    },
    
    # Tool selection - specify which tools to load
    mcp_tools={
        "planton-cloud": [
            "list_organizations",
            "create_cloud_resource",
        ]
    }
)

# Invoke with user token (same as before)
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"_user_token": os.getenv("PLANTON_API_KEY")}}
)
```

**Total**: ~15 lines in 1 file (90% reduction)

**Benefits**:

- ✅ No tool wrapper files needed
- ✅ No MCP client management
- ✅ No custom middleware
- ✅ Automatic per-user authentication
- ✅ Handles async/sync automatically
- ✅ Cursor-compatible MCP config format

### Migration Steps for MCP Agents

1. **Delete manual tool wrapper files**:

```bash
# Remove these files:
rm mcp_tools.py
rm mcp_client.py
rm middleware.py
```

2. **Add MCP configuration to agent creation**:

```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    
    # Add MCP server config
    mcp_servers={
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
        }
    },
    
    # List tools you want
    mcp_tools={
        "planton-cloud": [
            "list_organizations",
            "create_cloud_resource",
            # ... add more tools as needed
        ]
    }
)
```

3. **Keep invocation with token the same**:

```python
# This part doesn't change
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"_user_token": user_token}}
)
```

4. **Test with same inputs**:
   - Verify agent behavior is identical
   - Check tool calls work correctly
   - Ensure authentication succeeds

## Advanced Patterns

### Custom State Schema

If your agent uses a custom state schema (not FilesystemState), you can still use Graphton:

**Before**:

```python
from typing import TypedDict, List, Dict

class CustomState(TypedDict):
    messages: List[Dict]
    user_data: Dict
    processing_steps: List[str]

agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    context_schema=CustomState,
)
```

**After** (same):

```python
from typing import TypedDict, List, Dict

class CustomState(TypedDict):
    messages: List[Dict]
    user_data: Dict
    processing_steps: List[str]

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    context_schema=CustomState,  # Still supported!
)
```

### Multiple MCP Servers

Graphton supports multiple MCP servers:

```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    
    # Multiple MCP servers
    mcp_servers={
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
        },
        "github": {
            "transport": "streamable_http",
            "url": "https://mcp.github.com/",
        }
    },
    
    # Tools from different servers
    mcp_tools={
        "planton-cloud": ["list_organizations", "create_cloud_resource"],
        "github": ["list_repos", "create_issue"],
    }
)
```

### Custom Model Parameters

Override defaults when needed:

```python
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    
    # Custom parameters
    temperature=0.9,        # More creative
    max_tokens=5000,        # Shorter responses
    recursion_limit=50,     # Fewer reasoning steps
    
    # Provider-specific parameters
    top_p=0.95,
    top_k=40,
)
```

### Advanced Model Control

For complete control, pass a model instance:

```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-opus-4-20250514",
    max_tokens=30000,
    temperature=0.7,
    top_p=0.95,
    # Any other parameters
)

agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    # Note: temperature, max_tokens kwargs ignored when passing model instance
)
```

### Non-MCP Tools

Graphton works with regular LangChain tools too:

```python
from langchain.tools import tool

@tool
def custom_calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    tools=[custom_calculator],  # Regular LangChain tools
    # Can combine with MCP tools
    mcp_servers={...},
    mcp_tools={...},
)
```

## Migration Checklist

Use this checklist when migrating an agent:

### Planning

- [ ] Identify all files related to the agent
- [ ] Document current agent behavior (tests, examples)
- [ ] Check for custom state schemas or middleware
- [ ] List all MCP tools being used
- [ ] Note any special model parameters

### Code Changes

- [ ] Replace model instantiation with model string (or keep instance if needed)
- [ ] Consolidate system prompt (no changes needed)
- [ ] Convert MCP tool wrappers to `mcp_servers` and `mcp_tools` config
- [ ] Remove custom MCP middleware (if MCP-only)
- [ ] Remove manual tool wrapper files
- [ ] Update imports from `deepagents` to `graphton`
- [ ] Keep custom state schema if used
- [ ] Preserve custom model parameters if needed

### Testing

- [ ] Test agent creation succeeds
- [ ] Test with same inputs as before
- [ ] Verify all tools work correctly
- [ ] Check authentication (if using MCP)
- [ ] Compare outputs with old agent
- [ ] Test error cases
- [ ] Check performance (should be identical)

### Cleanup

- [ ] Delete old tool wrapper files
- [ ] Delete custom MCP client code
- [ ] Delete custom middleware (if not needed)
- [ ] Update tests to use new code
- [ ] Update documentation
- [ ] Remove unused dependencies

### Verification

- [ ] Run test suite (all passing)
- [ ] Compare line count (should be 80-90% reduction)
- [ ] Verify no functionality lost
- [ ] Check linting and type checking
- [ ] Deploy to test environment
- [ ] Monitor behavior in production

## Troubleshooting

### Problem: "Configuration validation failed"

**Cause**: Invalid Graphton configuration.

**Solution**: Check error message for specific issue:

```python
# Common mistakes:
# 1. Empty system prompt
system_prompt = ""  # ❌ Must be non-empty

# 2. MCP servers without tools
mcp_servers = {...}  # ❌ Must also specify mcp_tools

# 3. Server name mismatch
mcp_servers = {"server-a": {...}}
mcp_tools = {"server-b": [...]}  # ❌ Names must match
```

### Problem: Tool not found

**Cause**: Tool name doesn't match MCP server's tool name.

**Solution**: Check exact tool names from MCP server:

```python
# List available tools (manual test)
from mcp import MCPClient
client = MCPClient(url="https://mcp.planton.ai/")
tools = client.list_tools()
print([t.name for t in tools])

# Use exact tool names
mcp_tools = {
    "planton-cloud": [
        "list_organizations",  # ✅ Exact match
        "list-organizations",  # ❌ Wrong format
    ]
}
```

### Problem: Authentication fails

**Cause**: User token not passed or in wrong format.

**Solution**: Ensure token is passed via config:

```python
# ✅ Correct
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"_user_token": token}}
)

# ❌ Wrong - token not in config
result = agent.invoke({"messages": [...]})
```

### Problem: Performance degradation

**Cause**: Should be identical, but check:

1. **Different recursion limit**:

```python
# Before
agent = create_deep_agent(..., recursion_limit=50)

# After - make sure to set the same
agent = create_deep_agent(..., recursion_limit=50)
```

2. **Different model parameters**:

```python
# Before
model = ChatAnthropic(model="...", temperature=0.5, max_tokens=5000)

# After - set the same parameters
agent = create_deep_agent(
    model="...",
    temperature=0.5,
    max_tokens=5000,
)
```

### Problem: Custom middleware not supported

**Cause**: Graphton currently focuses on MCP middleware.

**Solution**: For non-MCP middleware, you can still pass it:

```python
from my_middleware import custom_logging_middleware

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    middleware=[custom_logging_middleware],  # ✅ Still supported
    mcp_servers={...},
    mcp_tools={...},
)
```

Graphton's MCP middleware is auto-injected alongside yours.

### Problem: Type checker errors

**Cause**: Model string not recognized by type checker.

**Solution**: This is expected. Graphton validates at runtime:

```python
# Type checker may complain about string, but it works:
agent = create_deep_agent(
    model="claude-sonnet-4.5",  # Runtime validation
    system_prompt=SYSTEM_PROMPT,
)

# For strict type checking, use model instance:
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model="claude-sonnet-4-5-20250929")
agent = create_deep_agent(model=model, ...)
```

## Real-World Example: graph-fleet Agent

Here's a complete migration of a real agent from graph-fleet (AWS RDS Instance Creator):

### Before: ~180 lines across 5 files

**agent.py** (40 lines), **mcp_tools.py** (60 lines), **mcp_client.py** (40 lines), **middleware.py** (30 lines), **config.py** (10 lines)

### After: ~20 lines in 1 file

```python
"""AWS RDS Instance Creator - Graphton version."""

from graphton import create_deep_agent
import os

SYSTEM_PROMPT = """You are an AWS RDS instance creator agent.

Your job is to help users create AWS RDS instances by:
1. Understanding their requirements
2. Getting the necessary schema
3. Creating the RDS instance with proper configuration

Use the Planton Cloud tools to:
- Get cloud resource schemas
- Create cloud resources
- List environments

Always validate inputs and provide clear feedback.
"""

# Create agent
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt=SYSTEM_PROMPT,
    recursion_limit=150,
    
    mcp_servers={
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
        }
    },
    
    mcp_tools={
        "planton-cloud": [
            "get_cloud_resource_schema",
            "create_cloud_resource",
            "list_environments_for_org",
        ]
    }
)

# Invoke
def create_rds_instance(user_token: str, org_id: str, requirements: str):
    """Create RDS instance based on user requirements."""
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": f"Create RDS instance in org {org_id}: {requirements}"}
            ]
        },
        config={
            "configurable": {"_user_token": user_token}
        }
    )
    return result["messages"][-1]["content"]
```

**Result**: 180 lines → 20 lines (89% reduction), same functionality.

## Next Steps

After migration:

1. **Test thoroughly**: Ensure all functionality works
2. **Update documentation**: Reflect new code structure
3. **Update tests**: Adapt to new patterns
4. **Monitor in production**: Watch for any issues
5. **Share learnings**: Help other teams migrate

## Getting Help

- **Migration Questions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues)
- **Documentation**: [README](../README.md) | [API Docs](API.md) | [Configuration](CONFIGURATION.md)
- **Examples**: [examples/](../examples/)

---

**Happy migrating!** If you discover patterns not covered here, please contribute to this guide.

