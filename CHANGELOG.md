# Changelog

All notable changes to Graphton will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- PyPI distribution (when external adoption grows)
- Support for additional MCP transports (stdio, SSE)
- React Agent support (beyond Deep Agents)
- Subagent composition patterns
- Enhanced test utilities for agent development
- CLI for scaffolding new agents

## [0.1.0] - 2025-11-27

### Added

#### Phase 1: Foundation
- Project structure with Poetry packaging
- Development tooling: ruff (linting), mypy (type checking), pytest (testing)
- CI/CD setup with GitHub Actions
- Comprehensive Makefile for development commands
- Apache 2.0 license
- Basic README and contributing guidelines

#### Phase 2: Agent Factory
- `create_deep_agent()` function as main entry point
- Model name parsing with friendly aliases:
  - Anthropic: `claude-sonnet-4.5`, `claude-opus-4`, `claude-haiku-4`
  - OpenAI: `gpt-4o`, `gpt-4o-mini`, `o1`, `o1-mini`
- Automatic model instantiation from string names
- Support for direct model instances (advanced use)
- System prompt handling with validation
- State schema configuration (FilesystemState default)
- Parameter overrides: `temperature`, `max_tokens`, `recursion_limit`
- Comprehensive unit and integration tests

#### Phase 3: MCP Integration
- MCP server configuration (Cursor-compatible format)
- Tool loading with per-user authentication
- Automatic tool wrapper generation (zero boilerplate)
- Dynamic middleware injection for MCP tools
- Context-based token storage using `contextvars`
- Support for multiple MCP servers
- Tool-to-server mapping
- Works in both local and LangGraph Cloud deployments
- Integration tests with real and mock MCP servers

#### Phase 4: Configuration Validation
- Top-level `AgentConfig` Pydantic model
- Enhanced `McpServerConfig` validation:
  - URL scheme warnings (HTTP vs HTTPS)
  - Header conflict detection
  - Transport type validation
- Enhanced `McpToolsConfig` validation:
  - Tool name format validation
  - Duplicate detection
  - Empty list detection
- Server name consistency validation
- Comprehensive error messages with actionable suggestions
- Type hints throughout (mypy clean)
- 37 validation tests
- Configuration documentation

#### Phase 5: Documentation & Open Source
- Comprehensive README with examples
- Complete API documentation
- Configuration reference guide
- Installation guide (GitHub-based distribution)
- Migration guide from raw LangGraph
- Troubleshooting guide with common issues
- Enhanced CONTRIBUTING guide with development workflows
- Examples README with use cases
- Working examples:
  - `simple_agent.py` - Basic agent without tools
  - `mcp_agent.py` - Agent with MCP tools
- GitHub repository prepared for open source:
  - Issue templates (bug report, feature request, question)
  - Pull request template
  - Security policy (SECURITY.md)
  - Changelog (this file)

### Changed
- Installation now via GitHub (not PyPI initially)
- Simplified agent creation from 100+ lines to ~10 lines
- MCP tool integration from 150+ lines to ~15 lines

### Technical Details

**Core Components**:
- `graphton.core.agent` - Agent factory and creation logic
- `graphton.core.models` - Model name parsing and instantiation
- `graphton.core.config` - Pydantic configuration models
- `graphton.core.mcp_manager` - MCP client management
- `graphton.core.middleware` - MCP tool loading middleware
- `graphton.core.tool_wrappers` - Automatic tool wrapper generation
- `graphton.core.context` - Context variable management

**Dependencies**:
- Python 3.11+
- deepagents >= 0.2.4
- langgraph >= 1.0.0
- langchain >= 1.0.0
- langchain-anthropic >= 1.0.0
- langchain-openai >= 1.0.0
- langchain-mcp-adapters >= 0.1.9
- pydantic >= 2.0.0

**Development Dependencies**:
- ruff >= 0.6.0 (linting and formatting)
- mypy >= 1.10.0 (type checking)
- pytest >= 8.0.0 (testing)
- pytest-asyncio >= 0.24.0
- pytest-cov >= 5.0.0

### Breaking Changes

None (initial release)

### Migration Guide

For users of raw LangGraph, see [docs/MIGRATION.md](docs/MIGRATION.md) for detailed migration instructions.

### Known Issues

- Currently only supports `streamable_http` MCP transport
- Model string validation happens at runtime (not compile time)
- Some type checkers may complain about model strings (expected)

### Contributors

- Suresh Attaluri (@sureshattaluri) - Core development
- Planton Cloud Engineering Team - Testing and feedback

## [0.0.1] - 2025-11-27 (Internal)

### Added
- Initial internal development setup
- Proof of concept for MCP integration
- Early prototypes and experiments

---

## Version History

- **[0.1.0]** - 2025-11-27 - Initial public release
  - Phase 1-5 complete
  - GitHub-based distribution
  - Comprehensive documentation
  - Production-ready for internal and early external use

## Upgrade Guide

### From Pre-release to 0.1.0

If you were using Graphton before v0.1.0:

```bash
# Uninstall old version
pip uninstall graphton

# Install v0.1.0
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# No code changes required - API is stable
```

## Future Releases

### v0.2.0 (Planned)

After Phase 6 (graph-fleet migration and validation):
- Production validation with real workloads
- Performance optimizations discovered from production use
- Additional model providers based on feedback
- Enhanced error messages based on real-world issues

### v1.0.0 (Future)

When API is considered stable:
- API stability guarantee
- PyPI distribution
- Expanded MCP capabilities
- Enhanced tooling and CLI
- Comprehensive documentation site

---

**Note**: For detailed information about each release, see the [GitHub Releases](https://github.com/plantoncloud-inc/graphton/releases) page.

