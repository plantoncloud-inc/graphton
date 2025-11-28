# Changelog

All notable changes to Graphton will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Documentation
- Added comprehensive documentation files (INSTALLATION.md, MIGRATION.md, TROUBLESHOOTING.md)
- Created examples/README.md with detailed usage guides
- Enhanced README.md and CONTRIBUTING.md
- Added SECURITY.md with security best practices
- Added CHANGELOG.md and RELEASE.md

## [0.1.0] - 2025-11-28

Initial release of Graphton - a declarative agent creation framework for LangGraph.

### Added

#### Phase 1: Foundation Setup (2025-11-27)
- **Project Structure**: Modern Python package with src/ layout
- **Build System**: Poetry configuration with Python 3.11+ support
- **Development Tools**:
  - Ruff for linting (100 char line length, E/F/I/D/UP/N/ANN rules)
  - mypy for type checking
  - pytest with coverage reporting
- **Dependencies**:
  - deepagents (>=0.2.4,<0.3.0) - LangGraph deep agent framework
  - langgraph (>=1.0.0,<2.0.0) - Graph-based agent orchestration
  - langchain (>=1.0.0,<2.0.0) - LLM framework
  - langchain-anthropic (>=1.0.0,<2.0.0) - Anthropic integration
  - langchain-openai (>=1.0.0,<2.0.0) - OpenAI integration
  - langchain-mcp-adapters (>=0.1.9,<0.2.0) - MCP protocol adapters
  - pydantic (>=2.0.0,<3.0.0) - Data validation
- **GitHub Infrastructure**:
  - CI/CD workflow with GitHub Actions (Python 3.11, 3.12)
  - Automated testing, linting, and type checking
- **License**: Apache-2.0

#### Phase 2: Agent Factory Implementation (2025-11-27)
- **Core Function**: `create_deep_agent()` - Main entry point for creating agents
- **Model String Parsing**: Support for friendly model names
  - Anthropic: `claude-sonnet-4.5`, `claude-opus-4`, `claude-haiku-4`
  - OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `o1`, `o1-mini`
  - Full model IDs also supported
- **Model Instance Support**: Pass `BaseChatModel` instances directly
- **Sensible Defaults**:
  - Anthropic: 20,000 max_tokens (Deep Agents need high limits)
  - OpenAI: Model-specific defaults
  - Recursion limit: 100
- **Parameter Overrides**: `max_tokens`, `temperature`, `recursion_limit`, and model-specific kwargs
- **Examples**: `simple_agent.py` demonstrating basic usage
- **Tests**: 55+ test cases covering model parsing, parameter handling, and error cases

#### Phase 3: MCP Integration (2025-11-27)
- **Static MCP Configuration**: Tools loaded once at agent creation time
- **MCP Parameters**: 
  - `mcp_servers`: Raw server configurations
  - `mcp_tools`: Tool names to load from each server
- **Automatic Middleware Injection**: MCP tool loading middleware auto-configured
- **Error Handling**: Validation of MCP configuration (server/tool name matching)
- **Examples**: `static_mcp_agent.py` demonstrating static MCP usage
- **Tests**: MCP integration tests with mock servers

#### Phase 4: Configuration Validation (2025-11-27)
- **Pydantic Models**: Type-safe configuration with `AgentConfig`
- **Early Error Detection**: Configuration validated at agent creation time
- **Validation Rules**:
  - System prompt: Cannot be empty, must be at least 10 characters
  - Recursion limit: Must be positive, warning if > 500
  - Temperature: Must be between 0.0 and 2.0
  - MCP: Both `mcp_servers` and `mcp_tools` required together, names must match
  - Tool lists: Cannot be empty, valid tool names only
- **Helpful Error Messages**: Clear, actionable error messages with context
- **IDE Support**: Full autocomplete and type hints
- **Documentation**: Complete configuration reference in `docs/CONFIGURATION.md`
- **Tests**: Configuration validation test suite

#### Phase 5: Universal MCP Authentication Framework (2025-11-28)
- **Template-Based Token Injection**: Support for `{{VAR_NAME}}` placeholders in MCP configs
- **Dynamic Mode**: Templates substituted from `config['configurable']` at invocation time
  - Per-user authentication
  - Tools loaded per-request
  - Secure multi-tenant systems
- **Static Mode**: No templates = tools loaded once at creation
  - Zero runtime overhead
  - Shared credentials
  - Hardcoded or environment-specific auth
- **Automatic Mode Detection**: Framework detects static vs dynamic based on template presence
- **Universal Authentication Support**:
  - Bearer tokens (OAuth, JWT)
  - API Keys
  - Basic Auth
  - Custom headers
  - Any authentication format
- **Template Functions**:
  - `has_templates()`: Check if config contains templates
  - `extract_template_vars()`: Extract template variable names
  - `substitute_templates()`: Perform template substitution
- **Examples**:
  - `mcp_agent.py`: Dynamic authentication with user tokens
  - `multi_auth_agent.py`: Multiple servers with mixed authentication
- **Documentation**: Complete MCP authentication guide in `docs/CONFIGURATION.md`
- **Tests**: Dynamic authentication test suite

#### Phase 6: Documentation and Code Quality (2025-11-28)
- **Comprehensive Docstrings**: Google-style docstrings for all public functions and classes
- **Documentation Files**:
  - `docs/CONFIGURATION.md`: Complete configuration reference (700+ lines)
  - `docs/API.md`: API documentation with examples
  - `README.md`: Project overview and quick start
  - `CONTRIBUTING.md`: Development guidelines
  - `examples/README.md`: Example documentation
- **Code Cleanup**:
  - Removed print statements from core code
  - Added proper logging placeholders
  - Improved error messages
  - Enhanced type hints
- **Type Safety**: Complete type hints throughout codebase

### Features Summary

**Core Capabilities:**
- ✅ Declarative agent creation (3-10 lines vs 100+)
- ✅ Model string support (friendly names, no manual instantiation)
- ✅ Universal MCP authentication (static & dynamic modes)
- ✅ Type-safe configuration with Pydantic validation
- ✅ Automatic middleware injection for MCP tools
- ✅ Template-based token injection for per-user auth
- ✅ Support for custom tools and middleware
- ✅ Full IDE support with autocomplete and type hints

**Supported Models:**
- Anthropic: Claude Sonnet 4.5, Claude Opus 4, Claude Haiku 4
- OpenAI: GPT-4o, GPT-4o Mini, GPT-4 Turbo, o1, o1 Mini
- Custom: Any `BaseChatModel` instance

**MCP Authentication:**
- Static configuration (shared credentials)
- Dynamic configuration (per-user tokens)
- Mixed authentication (multiple servers, different methods)
- Template variables: `{{VAR_NAME}}` in any config field

### Changed

- None (initial release)

### Deprecated

- None (initial release)

### Removed

- None (initial release)

### Fixed

- None (initial release)

### Security

- API key management best practices documented
- Template injection prevention guidelines
- Input validation recommendations
- Rate limiting guidance
- Error handling security considerations

## Development Phases

### Phase 1: Foundation Setup ✅
**Status:** Complete (2025-11-27)  
**Objective:** Project structure, tooling, and GitHub setup

**Deliverables:**
- ✅ Python package with Poetry
- ✅ Development tools (ruff, mypy, pytest)
- ✅ GitHub repository with CI/CD
- ✅ License (Apache-2.0)

### Phase 2: Agent Factory Implementation ✅
**Status:** Complete (2025-11-27)  
**Objective:** Core `create_deep_agent()` with model string support

**Deliverables:**
- ✅ `create_deep_agent()` function
- ✅ Model string parsing (Anthropic, OpenAI)
- ✅ Parameter overrides
- ✅ Examples and tests

### Phase 3: MCP Integration ✅
**Status:** Complete (2025-11-27)  
**Objective:** Static MCP configuration support

**Deliverables:**
- ✅ MCP server configuration
- ✅ MCP tools loading
- ✅ Automatic middleware injection
- ✅ Examples and tests

### Phase 4: Configuration Validation ✅
**Status:** Complete (2025-11-27)  
**Objective:** Type-safe configuration with Pydantic

**Deliverables:**
- ✅ `AgentConfig` Pydantic model
- ✅ Validation rules
- ✅ Helpful error messages
- ✅ Complete documentation

### Phase 5: Universal MCP Authentication ✅
**Status:** Complete (2025-11-28)  
**Objective:** Template-based dynamic authentication

**Deliverables:**
- ✅ Template variable support
- ✅ Static vs dynamic mode detection
- ✅ Template substitution functions
- ✅ Multi-server examples
- ✅ Complete documentation

### Phase 6: Documentation & Open Source Release ✅
**Status:** Complete (2025-11-28)  
**Objective:** Comprehensive documentation and release preparation

**Deliverables:**
- ✅ Installation guide (INSTALLATION.md)
- ✅ Migration guide (MIGRATION.md)
- ✅ Troubleshooting guide (TROUBLESHOOTING.md)
- ✅ Enhanced API documentation
- ✅ Examples documentation
- ✅ Security policy (SECURITY.md)
- ✅ Release guide (RELEASE.md)
- ✅ This changelog (CHANGELOG.md)

## Release History

### v0.1.0 (2025-11-28)
**First stable release**

This release represents the completion of all planned Phase 1-5 features:
- Declarative agent creation framework
- Universal MCP authentication
- Type-safe configuration
- Comprehensive documentation
- Production-ready codebase

**Installation:**
```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

**What's Next:**
- PyPI publication (when external adoption grows)
- Additional model provider support
- Performance optimizations
- Community feedback integration

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## Links

- **Repository**: https://github.com/plantoncloud-inc/graphton
- **Documentation**: https://github.com/plantoncloud-inc/graphton#readme
- **Issues**: https://github.com/plantoncloud-inc/graphton/issues
- **Discussions**: https://github.com/plantoncloud-inc/graphton/discussions

---

[Unreleased]: https://github.com/plantoncloud-inc/graphton/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/plantoncloud-inc/graphton/releases/tag/v0.1.0
