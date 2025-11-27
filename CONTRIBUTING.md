# Contributing to Graphton

Thank you for your interest in contributing to Graphton! This document provides comprehensive guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Adding Features](#adding-features)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Getting Help](#getting-help)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment for all contributors. Be kind, professional, and constructive in all interactions.

## Getting Started

### Ways to Contribute

- 🐛 **Report bugs**: File issues for bugs you encounter
- 💡 **Suggest features**: Share ideas for improvements
- 📝 **Improve documentation**: Fix typos, clarify explanations, add examples
- 🔧 **Fix issues**: Pick up issues tagged with `good-first-issue`
- ✨ **Add features**: Implement new capabilities
- 🧪 **Write tests**: Increase test coverage
- 🎨 **Improve examples**: Add or enhance example agents

### Before You Start

1. **Check existing issues**: Look for related issues or discussions
2. **Discuss major changes**: Open an issue for significant features before coding
3. **Read the docs**: Familiarize yourself with the project structure
4. **Review the code**: Understand existing patterns and conventions

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Poetry (recommended) or pip
- Git
- GitHub account

### Initial Setup

```bash
# 1. Fork the repository on GitHub
#    Visit https://github.com/plantoncloud-inc/graphton
#    Click "Fork" in the top right

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/graphton.git
cd graphton

# 3. Add upstream remote
git remote add upstream https://github.com/plantoncloud-inc/graphton.git

# 4. Install dependencies (choose Poetry or pip)

# Option A: Using Poetry (recommended)
poetry install
poetry shell  # Activate virtual environment

# Option B: Using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"

# 5. Verify installation
make test
```

### Available Make Commands

```bash
make deps       # Install dependencies
make test       # Run tests
make lint       # Run linter (ruff)
make typecheck  # Run type checker (mypy)
make build      # Run all checks (lint + typecheck + test)
make clean      # Clean generated files
```

## Development Workflow

### Daily Workflow

1. **Sync with upstream**:

```bash
git checkout main
git fetch upstream
git merge upstream/main
```

2. **Create a feature branch**:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

3. **Make your changes**:
   - Write code
   - Add tests
   - Update documentation

4. **Run checks frequently**:

```bash
# Run tests
make test

# Run linting
make lint

# Run type checking
make typecheck

# Run all checks
make build
```

5. **Commit your changes**:

```bash
git add .
git commit -m "feat(scope): clear description"
```

6. **Push to your fork**:

```bash
git push origin feature/your-feature-name
```

7. **Create pull request**:
   - Go to GitHub
   - Click "Compare & pull request"
   - Fill out PR template
   - Submit for review

### Keeping Your Fork Updated

```bash
# Update main branch
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# Rebase your feature branch
git checkout feature/your-feature-name
git rebase main
```

## Coding Standards

### Python Style Guidelines

**General Rules**:

- **PEP 8 compliance**: Enforced by ruff
- **Line length**: 100 characters maximum
- **Type hints**: Required for all function signatures and public APIs
- **Docstrings**: Required for all public functions, classes, and modules
- **Imports**: Organized and sorted automatically by ruff

**Docstring Format** (Google style):

```python
def create_agent(
    model: str,
    system_prompt: str,
    *,
    recursion_limit: int = 100,
) -> CompiledStateGraph:
    """Create a LangGraph Deep Agent with minimal boilerplate.
    
    Args:
        model: Model name string (e.g., "claude-sonnet-4.5") or model instance
        system_prompt: System prompt defining agent behavior
        recursion_limit: Maximum recursion depth for agent reasoning
    
    Returns:
        Compiled LangGraph agent ready to invoke
    
    Raises:
        ValueError: If system_prompt is empty or model name is invalid
    
    Example:
        >>> agent = create_agent(
        ...     model="claude-sonnet-4.5",
        ...     system_prompt="You are a helpful assistant"
        ... )
        >>> result = agent.invoke({"messages": [...]})
    """
    # Implementation
    pass
```

**Type Hints**:

```python
# ✅ Good: Clear type hints
def process_tools(
    tools: dict[str, list[str]],
    config: dict[str, Any],
) -> list[BaseTool]:
    ...

# ❌ Bad: Missing or vague type hints
def process_tools(tools, config):
    ...
```

**Naming Conventions**:

- **Functions/methods**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Protected**: `__double_leading_underscore`

### File Organization

```python
"""Module docstring at top of file."""

# Standard library imports
import os
from typing import Any

# Third-party imports
from langchain.tools import BaseTool
from pydantic import BaseModel

# Local imports
from graphton.core.config import AgentConfig
from graphton.core.models import create_model

# Constants
DEFAULT_RECURSION_LIMIT = 100

# Classes and functions
...
```

### Error Handling

```python
# ✅ Good: Specific exceptions with helpful messages
if not system_prompt or not system_prompt.strip():
    raise ValueError(
        "system_prompt cannot be empty. Provide a clear description "
        "of the agent's role and capabilities."
    )

# ❌ Bad: Generic exception without context
if not system_prompt:
    raise Exception("Invalid prompt")
```

## Testing

### Test Requirements

- **Coverage**: Aim for >80% code coverage
- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test interactions between components
- **Type checking**: Ensure all code passes mypy

### Writing Tests

**Test Structure**:

```python
"""Test module for agent creation."""

import pytest
from graphton import create_deep_agent


class TestAgentCreation:
    """Tests for basic agent creation."""
    
    def test_create_agent_with_valid_config(self):
        """Test creating agent with valid configuration."""
        agent = create_deep_agent(
            model="claude-sonnet-4.5",
            system_prompt="You are helpful.",
        )
        assert agent is not None
    
    def test_create_agent_with_empty_prompt_raises_error(self):
        """Test that empty system prompt raises ValueError."""
        with pytest.raises(ValueError, match="system_prompt cannot be empty"):
            create_deep_agent(
                model="claude-sonnet-4.5",
                system_prompt="",
            )
```

**Running Tests**:

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::TestAgentCreation::test_create_agent_with_valid_config

# Run with coverage
pytest --cov=graphton --cov-report=html

# Run with verbose output
pytest -v

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

### Test Fixtures

```python
import pytest
from graphton import create_deep_agent


@pytest.fixture
def simple_agent():
    """Create a simple test agent."""
    return create_deep_agent(
        model="claude-sonnet-4.5",
        system_prompt="You are a test assistant.",
    )


def test_agent_invocation(simple_agent):
    """Test invoking the agent."""
    result = simple_agent.invoke({
        "messages": [{"role": "user", "content": "Hello"}]
    })
    assert "messages" in result
```

## Adding Features

### Adding a New Model Provider

To add support for a new model provider (e.g., Google, Cohere):

**1. Update model parsing in `src/graphton/core/models.py`**:

```python
def _create_model_from_string(model_name: str, **kwargs: Any) -> BaseChatModel:
    """Create model instance from string name."""
    
    # ... existing code ...
    
    # Add new provider
    elif model_name.startswith("google:") or model_name.startswith("gemini"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Map friendly names to actual model IDs
        gemini_aliases = {
            "gemini-pro": "gemini-1.5-pro",
            "gemini-ultra": "gemini-1.5-ultra",
        }
        
        actual_model = gemini_aliases.get(model_name, model_name)
        
        return ChatGoogleGenerativeAI(
            model=actual_model,
            **kwargs
        )
```

**2. Add dependency to `pyproject.toml`**:

```toml
[tool.poetry.dependencies]
langchain-google-genai = {version = ">=1.0.0,<2.0.0", optional = true}

[tool.poetry.extras]
google = ["langchain-google-genai"]
```

**3. Add tests in `tests/test_models.py`**:

```python
def test_create_google_model():
    """Test creating Google model from string."""
    agent = create_deep_agent(
        model="gemini-pro",
        system_prompt="Test",
    )
    assert agent is not None
```

**4. Update documentation**:
   - Add to `docs/API.md` supported models section
   - Add example to `README.md`
   - Update `docs/CONFIGURATION.md`

### Extending MCP Functionality

To add new MCP-related features:

**1. Understand the current architecture**:
   - `src/graphton/core/mcp_manager.py` - MCP client management
   - `src/graphton/core/middleware.py` - MCP tool loading middleware
   - `src/graphton/core/tool_wrappers.py` - Tool wrapper generation
   - `src/graphton/core/config.py` - MCP configuration models

**2. Example: Add support for MCP server with custom headers**:

Update `McpServerConfig` in `src/graphton/core/config.py`:

```python
class McpServerConfig(BaseModel):
    """MCP server configuration."""
    
    transport: str = "streamable_http"
    url: HttpUrl
    auth_from_context: bool = True
    headers: dict[str, str] | None = None
    timeout: int = 30  # ← New field
    retry_attempts: int = 3  # ← New field
```

Update MCP client creation in `src/graphton/core/mcp_manager.py`:

```python
def create_mcp_client(config: McpServerConfig, token: str | None = None) -> MCPClient:
    """Create MCP client with configuration."""
    headers = config.headers or {}
    
    if config.auth_from_context and token:
        headers["Authorization"] = f"Bearer {token}"
    
    return MCPClient(
        url=str(config.url),
        headers=headers,
        timeout=config.timeout,  # ← Use new config
        max_retries=config.retry_attempts,  # ← Use new config
    )
```

**3. Add tests**:

```python
def test_mcp_client_with_custom_timeout():
    """Test MCP client respects timeout configuration."""
    agent = create_deep_agent(
        model="claude-sonnet-4.5",
        system_prompt="Test",
        mcp_servers={
            "test": {
                "url": "https://mcp.test.com/",
                "timeout": 60,  # Custom timeout
            }
        },
        mcp_tools={"test": ["tool1"]},
    )
    # Test that timeout is respected
    ...
```

**4. Update documentation**:
   - Add to `docs/CONFIGURATION.md`
   - Add example to `README.md` if significant

### Adding Custom Middleware Support

To enhance middleware functionality:

```python
# In src/graphton/core/middleware.py

def create_custom_middleware(config: dict[str, Any]) -> Callable:
    """Create custom middleware from configuration."""
    
    async def middleware(context, state, next):
        # Custom logic before agent execution
        print(f"Processing state: {state}")
        
        # Execute agent
        result = await next(state)
        
        # Custom logic after agent execution
        print(f"Result: {result}")
        
        return result
    
    return middleware
```

## Pull Request Process

### Before Submitting

- [ ] All tests pass: `make test`
- [ ] Linting passes: `make lint`
- [ ] Type checking passes: `make typecheck`
- [ ] Documentation updated (if needed)
- [ ] Examples updated (if API changed)
- [ ] CHANGELOG entry added (maintainers will finalize)

### PR Description Template

```markdown
## Description

Clear description of what this PR does and why.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Related Issues

Closes #123
Relates to #456

## Changes Made

- Added support for X
- Fixed bug in Y
- Updated documentation for Z

## Testing

- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Tested manually with examples
- [ ] All existing tests pass

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings introduced
- [ ] Tests added/updated and passing
```

### Review Process

1. **Automated checks**: CI must pass (tests, linting, type checking)
2. **Code review**: At least one maintainer approval required
3. **Discussion**: Address feedback and questions
4. **Approval**: Once approved, maintainers will merge
5. **Cleanup**: Delete your feature branch after merge

## Release Process

*This section is for maintainers*

### Semantic Versioning

Graphton follows [Semantic Versioning](https://semver.org/):

- **Major (X.0.0)**: Breaking API changes
- **Minor (0.X.0)**: New features, backwards compatible
- **Patch (0.0.X)**: Bug fixes, backwards compatible

### Release Workflow

**1. Prepare release branch**:

```bash
git checkout main
git pull upstream main
git checkout -b release/v0.2.0
```

**2. Update version**:

```toml
# pyproject.toml
[tool.poetry]
version = "0.2.0"
```

```python
# src/graphton/__init__.py
__version__ = "0.2.0"
```

**3. Update CHANGELOG.md**:

```markdown
## [0.2.0] - 2025-01-15

### Added
- Support for multiple MCP servers
- Custom state schema validation
- New model providers: Google Gemini

### Changed
- Improved error messages in config validation
- Updated dependencies to latest versions

### Fixed
- Bug in tool wrapper generation
- Type hints for complex types

### Security
- Updated langchain-mcp-adapters to fix CVE-XXXX-XXXXX
```

**4. Create PR for release**:

```bash
git add .
git commit -m "chore: prepare release v0.2.0"
git push origin release/v0.2.0
```

Create PR, get approval, merge to main.

**5. Create and push tag**:

```bash
git checkout main
git pull upstream main
git tag -a v0.2.0 -m "Release v0.2.0"
git push upstream v0.2.0
```

**6. Create GitHub Release**:

- Go to https://github.com/plantoncloud-inc/graphton/releases
- Click "Draft a new release"
- Select tag v0.2.0
- Title: "v0.2.0 - Release Name"
- Description: Copy from CHANGELOG.md
- Mark as pre-release if < v1.0.0
- Publish release

**7. Announce release** (optional):
   - Update graph-fleet to use new version
   - Share in community channels
   - Tweet/post about new features

### Publishing to PyPI (Future)

When we're ready to publish to PyPI:

```bash
# Build package
poetry build

# Test on Test PyPI first
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ graphton

# If all good, publish to real PyPI
poetry publish
```

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, whitespace)
- `refactor`: Code refactoring without functionality change
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `ci`: CI/CD changes

### Scopes

- `agent`: Agent creation logic
- `mcp`: MCP integration
- `config`: Configuration and validation
- `models`: Model provider integrations
- `docs`: Documentation
- `tests`: Test suite
- `examples`: Example scripts

### Examples

```
feat(mcp): add support for multiple MCP servers

Implement multi-server MCP configuration allowing agents to
connect to multiple MCP servers simultaneously.

Closes #42

---

fix(config): improve validation error messages

Validation errors now include suggestions for common mistakes.

Fixes #89

---

docs(readme): update installation instructions

Add instructions for GitHub-based installation with pip and Poetry.
```

## Getting Help

### Resources

- **Documentation**: [README](README.md) | [API Docs](docs/API.md) | [Configuration](docs/CONFIGURATION.md)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues)
- **Discussions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)

### Questions?

- **General questions**: Open a [GitHub Discussion](https://github.com/plantoncloud-inc/graphton/discussions)
- **Bug reports**: Open an [Issue](https://github.com/plantoncloud-inc/graphton/issues)
- **Feature requests**: Open an [Issue](https://github.com/plantoncloud-inc/graphton/issues) with the `enhancement` label
- **Security issues**: See [SECURITY.md](SECURITY.md)

## Recognition

Contributors are recognized in:

- GitHub contributors page
- Release notes for significant contributions
- Special thanks in README for major features

Top contributors may be invited to become maintainers.

## License

By contributing to Graphton, you agree that your contributions will be licensed under the Apache License 2.0.

---

**Thank you for contributing to Graphton!** 🚀

Your contributions help make agent development faster and more accessible for everyone.
