# Installation Guide

Complete installation guide for Graphton, covering multiple installation methods, version management, and troubleshooting.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation Methods](#installation-methods)
  - [Install with pip](#install-with-pip)
  - [Install with Poetry](#install-with-poetry)
  - [Install from Source](#install-from-source)
- [Version Pinning](#version-pinning)
- [Dependency Management](#dependency-management)
- [Environment Setup](#environment-setup)
- [Verification](#verification)
- [Upgrading](#upgrading)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)

## Quick Start

**Requirements:**
- Python 3.11 or higher
- pip or Poetry

**Basic installation:**

```bash
# Using pip
pip install git+https://github.com/plantoncloud/graphton.git

# Using Poetry
poetry add git+https://github.com/plantoncloud/graphton.git
```

## Installation Methods

### Install with pip

#### Latest Version (main branch)

```bash
pip install git+https://github.com/plantoncloud/graphton.git
```

#### Specific Version (recommended for production)

```bash
# Install specific release tag
pip install git+https://github.com/plantoncloud/graphton.git@v0.1.0

# Install specific commit
pip install git+https://github.com/plantoncloud/graphton.git@9a24cf7
```

#### With Extras (if available)

```bash
# Install with all extras
pip install "git+https://github.com/plantoncloud/graphton.git[dev]"

# Install with specific extras
pip install "git+https://github.com/plantoncloud/graphton.git[test]"
```

#### In requirements.txt

Add to your `requirements.txt`:

```
# Latest version
git+https://github.com/plantoncloud/graphton.git

# Specific version (recommended)
git+https://github.com/plantoncloud/graphton.git@v0.1.0

# With extras
git+https://github.com/plantoncloud/graphton.git@v0.1.0#egg=graphton[dev]
```

Then install:

```bash
pip install -r requirements.txt
```

### Install with Poetry

#### Add to Project

```bash
# Latest version
poetry add git+https://github.com/plantoncloud/graphton.git

# Specific version (recommended)
poetry add git+https://github.com/plantoncloud/graphton.git#v0.1.0

# Specific commit
poetry add git+https://github.com/plantoncloud/graphton.git#9a24cf7
```

#### In pyproject.toml

Add to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
python = ">=3.11,<4.0"

# Latest version
graphton = {git = "https://github.com/plantoncloud/graphton.git"}

# Specific tag (recommended for production)
graphton = {git = "https://github.com/plantoncloud/graphton.git", tag = "v0.1.0"}

# Specific branch
graphton = {git = "https://github.com/plantoncloud/graphton.git", branch = "main"}

# Specific commit
graphton = {git = "https://github.com/plantoncloud/graphton.git", rev = "9a24cf7"}
```

Then install:

```bash
poetry install
```

### Install from Source

For development or contributing:

```bash
# Clone repository
git clone https://github.com/plantoncloud/graphton.git
cd graphton

# Install with pip (editable mode)
pip install -e .

# Or install with Poetry
poetry install

# Install with development dependencies
poetry install --with dev
```

## Version Pinning

### Why Pin Versions?

Version pinning ensures reproducible builds and prevents unexpected breaking changes.

### Recommended Practices

**For Production:**

```toml
# pyproject.toml - Pin to specific tag
graphton = {git = "https://github.com/plantoncloud/graphton.git", tag = "v0.1.0"}
```

**For Development:**

```toml
# pyproject.toml - Use branch for latest features
graphton = {git = "https://github.com/plantoncloud/graphton.git", branch = "main"}
```

**For Testing Specific Changes:**

```toml
# pyproject.toml - Pin to specific commit
graphton = {git = "https://github.com/plantoncloud/graphton.git", rev = "9a24cf7"}
```

### Version History

Check available versions:

```bash
# List all tags
git ls-remote --tags https://github.com/plantoncloud/graphton.git

# View releases on GitHub
open https://github.com/plantoncloud/graphton/releases
```

## Dependency Management

### Core Dependencies

Graphton depends on:

- **deepagents** (>=0.2.4,<0.3.0) - LangGraph deep agent framework
- **langgraph** (>=1.0.0,<2.0.0) - Graph-based agent orchestration
- **langchain** (>=1.0.0,<2.0.0) - LLM framework
- **langchain-anthropic** (>=1.0.0,<2.0.0) - Anthropic integration
- **langchain-openai** (>=1.0.0,<2.0.0) - OpenAI integration
- **langchain-mcp-adapters** (>=0.1.9,<0.2.0) - MCP protocol adapters
- **pydantic** (>=2.0.0,<3.0.0) - Data validation

### Dependency Conflicts

If you encounter dependency conflicts:

**With pip:**

```bash
# Use dependency resolver
pip install --use-feature=2020-resolver git+https://github.com/plantoncloud/graphton.git

# Or install in isolated environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install git+https://github.com/plantoncloud/graphton.git
```

**With Poetry:**

```bash
# Update lock file
poetry lock --no-update

# Or clear cache and reinstall
poetry cache clear pypi --all
poetry install
```

### Checking Installed Dependencies

```bash
# List all dependencies
pip list | grep -E "(graphton|langgraph|langchain|deepagents)"

# Or with Poetry
poetry show | grep -E "(graphton|langgraph|langchain|deepagents)"

# Show dependency tree
pip install pipdeptree
pipdeptree -p graphton
```

## Environment Setup

### API Keys

Graphton requires API keys for LLM providers:

**Anthropic:**

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**OpenAI:**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Persistent Configuration:**

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."
```

Or use a `.env` file with `python-dotenv`:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

```python
# Load in your application
from dotenv import load_dotenv
load_dotenv()
```

### Python Version Management

**Using pyenv (recommended):**

```bash
# Install Python 3.11
pyenv install 3.11

# Set for project
cd graphton
pyenv local 3.11

# Verify
python --version  # Should show Python 3.11.x
```

**Using system Python:**

```bash
# Verify version
python3 --version

# Must be 3.11 or higher
```

## Verification

### Verify Installation

```bash
# Check if package is installed
pip show graphton

# Or with Poetry
poetry show graphton
```

### Test Import

```bash
python -c "from graphton import create_deep_agent; print('✅ Graphton installed successfully')"
```

### Run Example

Create `test_graphton.py`:

```python
from graphton import create_deep_agent

# Create simple agent
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful assistant.",
)

# Test invocation
result = agent.invoke({
    "messages": [{"role": "user", "content": "Say hello!"}]
})

print("✅ Agent created and invoked successfully!")
print("Response:", result["messages"][-1]["content"])
```

Run:

```bash
python test_graphton.py
```

### Verify Version

```python
import graphton
print(f"Graphton version: {graphton.__version__}")
```

## Upgrading

### Upgrade to Latest Version

**With pip:**

```bash
# Upgrade to latest main branch
pip install --upgrade git+https://github.com/plantoncloud/graphton.git

# Upgrade to specific version
pip install --upgrade git+https://github.com/plantoncloud/graphton.git@v0.2.0
```

**With Poetry:**

```bash
# Update to latest version (based on pyproject.toml spec)
poetry update graphton

# Change version in pyproject.toml first, then:
poetry lock
poetry install
```

### Migration Between Versions

See [MIGRATION.md](MIGRATION.md) for detailed migration guides when upgrading between versions.

### Breaking Changes

Check [CHANGELOG.md](../CHANGELOG.md) for breaking changes before upgrading.

## Uninstalling

**With pip:**

```bash
pip uninstall graphton
```

**With Poetry:**

```bash
poetry remove graphton
```

**Remove virtual environment:**

```bash
# If using venv
rm -rf venv

# If using Poetry
poetry env remove $(poetry env info -p)
```

## Troubleshooting

### Installation Issues

#### "Python version 3.11 or higher required"

**Problem:** Your Python version is too old.

**Solution:**

```bash
# Check current version
python --version

# Install Python 3.11+ using pyenv
pyenv install 3.11
pyenv global 3.11

# Or download from python.org
open https://www.python.org/downloads/
```

#### "Could not find a version that satisfies the requirement"

**Problem:** Dependency conflict or network issue.

**Solution:**

```bash
# Try with verbose output
pip install -v git+https://github.com/plantoncloud/graphton.git

# Check your network connection
ping github.com

# Try with different resolver
pip install --use-feature=2020-resolver git+https://github.com/plantoncloud/graphton.git

# Or use isolated environment
python -m venv clean_env
source clean_env/bin/activate
pip install git+https://github.com/plantoncloud/graphton.git
```

#### "Permission denied" errors

**Problem:** Insufficient permissions for global installation.

**Solution:**

```bash
# Install for user only
pip install --user git+https://github.com/plantoncloud/graphton.git

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/plantoncloud/graphton.git
```

#### "Git not found" or "Git command failed"

**Problem:** Git is not installed or not in PATH.

**Solution:**

```bash
# Install git
# On macOS:
brew install git

# On Ubuntu/Debian:
sudo apt-get install git

# On Windows: Download from git-scm.com

# Verify installation
git --version
```

#### SSH vs HTTPS for Git Installation

**Problem:** SSH key authentication issues with git+ssh:// URLs.

**Solution:** Use HTTPS URLs instead:

```bash
# Use HTTPS (recommended)
pip install git+https://github.com/plantoncloud/graphton.git

# Instead of SSH
# pip install git+ssh://git@github.com/plantoncloud/graphton.git
```

### Import Issues

#### "ModuleNotFoundError: No module named 'graphton'"

**Problem:** Package not installed or wrong Python environment.

**Solution:**

```bash
# Verify installation
pip list | grep graphton

# Verify you're in correct environment
which python
python -c "import sys; print(sys.prefix)"

# Reinstall if needed
pip install --force-reinstall git+https://github.com/plantoncloud/graphton.git
```

#### "ImportError: cannot import name 'create_deep_agent'"

**Problem:** Outdated or corrupted installation.

**Solution:**

```bash
# Reinstall
pip uninstall graphton
pip install git+https://github.com/plantoncloud/graphton.git

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Dependency Issues

#### Conflicting langchain versions

**Problem:** Multiple langchain packages with incompatible versions.

**Solution:**

```bash
# Check versions
pip list | grep langchain

# Upgrade all langchain packages together
pip install --upgrade langchain langchain-core langchain-anthropic langchain-openai

# Or use constraints file
pip install -c constraints.txt git+https://github.com/plantoncloud/graphton.git
```

#### "No matching distribution found for deepagents"

**Problem:** deepagents dependency not available.

**Solution:**

```bash
# Install deepagents explicitly first
pip install deepagents>=0.2.4

# Then install graphton
pip install git+https://github.com/plantoncloud/graphton.git
```

### Getting Help

If you encounter issues not covered here:

1. **Check existing issues:** https://github.com/plantoncloud/graphton/issues
2. **Search discussions:** https://github.com/plantoncloud/graphton/discussions
3. **Open new issue:** Include:
   - Python version (`python --version`)
   - pip version (`pip --version`)
   - Installation method used
   - Full error message
   - Operating system

## Next Steps

After successful installation:

1. **Read the [Configuration Guide](CONFIGURATION.md)** to understand agent configuration
2. **Explore [Examples](../examples/)** for usage patterns
3. **Check [API Documentation](API.md)** for complete API reference
4. **Review [Troubleshooting](TROUBLESHOOTING.md)** for common runtime issues
