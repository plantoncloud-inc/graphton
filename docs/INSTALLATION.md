# Installation Guide

Complete guide for installing and upgrading Graphton.

## Table of Contents

- [Quick Install](#quick-install)
- [Installation Methods](#installation-methods)
- [Version Pinning](#version-pinning)
- [Development Installation](#development-installation)
- [Upgrading Graphton](#upgrading-graphton)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)
- [Future: PyPI Distribution](#future-pypi-distribution)

## Quick Install

**Recommended for most users:**

```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

This installs the latest stable release (v0.1.0) from GitHub.

## Installation Methods

### Using pip

**Latest stable release (recommended):**

```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

**Latest from main branch (bleeding edge):**

```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git
```

**Specific commit (for testing or bisecting):**

```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git@abc123def456
```

**With extras (if we add optional dependencies in future):**

```bash
# Future: pip install "git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0#egg=graphton[dev]"
```

### Using Poetry

**Add to existing project:**

```bash
# Specific version (recommended)
poetry add git+https://github.com/plantoncloud-inc/graphton.git#v0.1.0

# Latest from main
poetry add git+https://github.com/plantoncloud-inc/graphton.git
```

**In pyproject.toml:**

```toml
[tool.poetry.dependencies]
graphton = {git = "https://github.com/plantoncloud-inc/graphton.git", tag = "v0.1.0"}
```

Or for the latest:

```toml
[tool.poetry.dependencies]
graphton = {git = "https://github.com/plantoncloud-inc/graphton.git", branch = "main"}
```

### Using requirements.txt

**Pinned to specific version:**

```
graphton @ git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

**Latest from main:**

```
graphton @ git+https://github.com/plantoncloud-inc/graphton.git
```

**With hash for security:**

```
graphton @ git+https://github.com/plantoncloud-inc/graphton.git@abc123def456
```

### Using pipenv

```bash
# Specific version
pipenv install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Latest from main
pipenv install git+https://github.com/plantoncloud-inc/graphton.git
```

## Version Pinning

### Why Pin Versions?

For production deployments, always pin to a specific version tag to ensure reproducible builds:

```bash
# ✅ Good: Reproducible
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# ❌ Bad: May break on updates
pip install git+https://github.com/plantoncloud-inc/graphton.git
```

### Version Tags

Graphton follows semantic versioning (SemVer):

- **v0.1.0** - Current stable release (Phase 1-4 complete)
- **v0.2.0** - Future: After graph-fleet migration (Phase 6)
- **v1.0.0** - Future: Production-ready with stable API

### Finding Available Versions

```bash
# List all tags
git ls-remote --tags https://github.com/plantoncloud-inc/graphton.git

# Or visit GitHub releases page:
# https://github.com/plantoncloud-inc/graphton/releases
```

## Development Installation

For contributing to Graphton or running examples:

### 1. Clone Repository

```bash
git clone https://github.com/plantoncloud-inc/graphton.git
cd graphton
```

### 2. Install Dependencies

**Using Poetry (recommended for development):**

```bash
# Install all dependencies including dev dependencies
poetry install

# Activate virtual environment
poetry shell
```

**Using pip:**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 3. Verify Installation

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

### 4. Set Up Pre-commit Hooks (Optional)

```bash
# Future: pre-commit install
```

## Upgrading Graphton

### Upgrading to Latest Release

```bash
# Using pip
pip install --upgrade git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Using Poetry
poetry update graphton
```

### Upgrading to Specific Version

```bash
# Using pip - uninstall and reinstall
pip uninstall graphton
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.2.0

# Using Poetry - update pyproject.toml and run
poetry update graphton
```

### Checking Current Version

```python
import graphton
print(graphton.__version__)  # Future: Add __version__ to __init__.py
```

Or check installed packages:

```bash
pip show graphton
# or
poetry show graphton
```

## Verifying Installation

### Basic Verification

```python
# Test import
from graphton import create_deep_agent

# Create a simple agent
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful assistant.",
)

print("✅ Graphton installed successfully!")
```

### Full Verification

Run the example scripts:

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run simple agent example
python examples/simple_agent.py

# If you have Planton Cloud access:
export PLANTON_API_KEY="your-token-here"
python examples/mcp_agent.py
```

### Check Dependencies

```bash
# Verify all dependencies are installed
pip check

# Or with Poetry
poetry check
```

## Troubleshooting

### Problem: `pip install` fails with "Could not find a version"

**Cause**: Git is not installed or not in PATH.

**Solution**:

```bash
# Install git
# macOS: brew install git
# Ubuntu: sudo apt install git
# Windows: Download from git-scm.com

# Verify git is available
git --version
```

### Problem: `pip install` fails with "fatal: could not read Username"

**Cause**: GitHub repository is private and you're not authenticated.

**Solution**:

```bash
# For public repos (Graphton is public), use HTTPS:
pip install git+https://github.com/plantoncloud-inc/graphton.git

# If you need SSH (for private repos):
pip install git+ssh://git@github.com/plantoncloud-inc/graphton.git
```

### Problem: Dependency conflicts

**Cause**: Conflicting versions of LangChain, LangGraph, or other dependencies.

**Solution**:

```bash
# Use a fresh virtual environment
python -m venv fresh-env
source fresh-env/bin/activate
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Or with Poetry (handles conflicts better)
poetry add git+https://github.com/plantoncloud-inc/graphton.git#v0.1.0
```

### Problem: `ModuleNotFoundError: No module named 'graphton'`

**Cause**: Graphton not installed in current environment.

**Solution**:

```bash
# Check which Python you're using
which python
which pip

# Ensure you're in the right virtual environment
# Install Graphton
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Verify installation
pip list | grep graphton
```

### Problem: Slow installation

**Cause**: Git needs to clone the entire repository.

**Solution**:

```bash
# Use shallow clone (faster)
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0 --depth=1

# Note: Not all pip versions support --depth flag
```

### Problem: Can't upgrade to newer version

**Cause**: pip caches git repositories.

**Solution**:

```bash
# Clear pip cache
pip cache purge

# Force reinstall
pip install --force-reinstall git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

### Problem: Import works but type hints don't (IDE issues)

**Cause**: IDE not recognizing installed package.

**Solution**:

```bash
# Restart IDE/Python language server

# For VS Code, reload window:
# Cmd+Shift+P -> "Developer: Reload Window"

# Verify py.typed marker is present:
python -c "import graphton; import os; print(os.path.dirname(graphton.__file__))"
# Check that py.typed file exists in that directory
```

## Future: PyPI Distribution

When Graphton is published to PyPI (planned for when external adoption grows), installation will be simpler:

```bash
# Future: Simple PyPI install
pip install graphton

# With version
pip install graphton==0.2.0

# Upgrade
pip install --upgrade graphton
```

**Why GitHub-only for now?**

- ✅ Simpler workflow for maintainers (no PyPI publishing)
- ✅ Faster iteration (push to GitHub = released)
- ✅ Perfect for internal use and early adopters
- ✅ No functional limitations (pip/Poetry fully support GitHub)
- ✅ Can add PyPI later without breaking changes

**When will PyPI be added?**

We'll publish to PyPI when:

- Significant external adoption (dozens of users outside Planton Cloud)
- Users request PyPI for discoverability
- Graphton becomes a dependency of other PyPI packages
- API stabilizes (v1.0.0)

## Getting Help

- **Installation Issues**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **General Questions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues)
- **Documentation**: [README](../README.md) | [API Docs](API.md) | [Configuration](CONFIGURATION.md)

---

**Next Steps**: After installing, see the [Quick Start](../README.md#quick-start) guide or explore [examples](../examples/).

