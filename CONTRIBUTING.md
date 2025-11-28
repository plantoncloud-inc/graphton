# Contributing to Graphton

Thank you for your interest in contributing to Graphton! This guide will help you get started with development.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Poetry (Python dependency management)

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/plantoncloud-inc/graphton.git
   cd graphton
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment variables** (for running examples):
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   # or for OpenAI
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Verify installation**:
   ```bash
   make build
   ```

## Development Workflow

We use Make commands for common development tasks. Run `make help` to see all available commands.

### Available Commands

- **`make deps`** - Install dependencies with Poetry
- **`make test`** - Run test suite with coverage reporting
- **`make lint`** - Run ruff linter to check code quality
- **`make typecheck`** - Run mypy type checker
- **`make build`** - Run all checks (lint + typecheck + test)
- **`make clean`** - Clean cache files and build artifacts
- **`make release version=vx.y.z`** - Create and push release tag (maintainers only)

### Development Cycle

1. Make your changes
2. Run linter: `make lint`
3. Run type checker: `make typecheck`
4. Run tests: `make test`
5. Or run all checks at once: `make build`

## Code Quality Standards

### Linting with Ruff

We use [Ruff](https://github.com/astral-sh/ruff) for fast Python linting:

- **Line length**: 100 characters
- **Target version**: Python 3.11
- **Enabled rules**: E (pycodestyle errors), F (pyflakes), I (isort), D (pydocstyle), UP (pyupgrade), N (pep8-naming), ANN (annotations)

Configuration is in `pyproject.toml` under `[tool.ruff]`.

### Type Checking with mypy

All code must pass mypy type checking:

```bash
make typecheck
```

Configuration is in `mypy.ini`.

### Code Style

- Use type hints for all function parameters and return values
- Write docstrings for public functions and classes (Google style)
- Keep functions focused and single-purpose
- Prefer explicit over implicit
- Use descriptive variable names

## Testing

### Running Tests

```bash
# Run all tests with coverage
make test

# Run specific test file
poetry run pytest tests/test_agent.py -v

# Run specific test
poetry run pytest tests/test_agent.py::test_create_agent -v

# Run with coverage report
poetry run pytest tests/ -v --cov=graphton --cov-report=term-missing
```

### Test Organization

- **Location**: `tests/` directory
- **Naming**: Test files are named `test_*.py`
- **Framework**: pytest with pytest-asyncio for async tests
- **Coverage**: Aim for high test coverage of core functionality

### Writing Tests

- Write tests for new features and bug fixes
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Use fixtures for common setup
- Mock external dependencies (API calls, file I/O, etc.)

## Pull Request Process

1. **Fork the repository** and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the code quality standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Ensure all checks pass**:
   ```bash
   make build
   ```
   This runs linting, type checking, and tests.

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Clear description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changes were made and why
   - Include examples if adding new features

7. **CI/CD Checks**:
   - GitHub Actions will automatically run tests on Python 3.11 and 3.12
   - All checks must pass before merging
   - Review any feedback from maintainers

## Project Structure

```
graphton/
├── src/graphton/          # Source code
│   ├── core/              # Core functionality
│   │   ├── agent.py       # Main agent creation logic
│   │   ├── config.py      # Configuration models
│   │   ├── mcp_manager.py # MCP server management
│   │   └── ...
│   └── utils/             # Utility functions
├── tests/                 # Test suite
│   ├── test_agent.py      # Agent creation tests
│   ├── test_mcp_*.py      # MCP integration tests
│   └── ...
├── examples/              # Usage examples
│   ├── simple_agent.py    # Basic agent
│   ├── mcp_agent.py       # MCP integration
│   └── ...
├── docs/                  # Documentation
│   ├── API.md             # API reference
│   └── CONFIGURATION.md   # Configuration guide
├── pyproject.toml         # Project metadata and dependencies
├── Makefile              # Development commands
└── README.md             # Project overview
```

## Documentation

When adding new features:

- Update relevant documentation in `docs/`
- Add examples to `examples/` if appropriate
- Update README.md if the feature is significant
- Include docstrings in code for API documentation

## Questions or Issues?

- **Bug reports**: Open an issue on GitHub with details and reproduction steps
- **Feature requests**: Open an issue describing the feature and use case
- **Questions**: Open a discussion on GitHub or contact the maintainers

## License

By contributing to Graphton, you agree that your contributions will be licensed under the Apache-2.0 License.
