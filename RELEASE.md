# Release Guide for Graphton v0.1.0

This document provides step-by-step instructions for creating the v0.1.0 release.

## Pre-Release Checklist

- [x] All Phase 5 tasks completed
- [x] Documentation created and polished:
  - [x] README.md
  - [x] docs/INSTALLATION.md
  - [x] docs/MIGRATION.md
  - [x] docs/TROUBLESHOOTING.md
  - [x] docs/API.md
  - [x] docs/CONFIGURATION.md
  - [x] examples/README.md
  - [x] CONTRIBUTING.md
  - [x] SECURITY.md
  - [x] CHANGELOG.md
- [x] GitHub repository files created:
  - [x] .github/ISSUE_TEMPLATE/bug_report.md
  - [x] .github/ISSUE_TEMPLATE/feature_request.md
  - [x] .github/ISSUE_TEMPLATE/question.md
  - [x] .github/PULL_REQUEST_TEMPLATE.md
- [x] Examples working:
  - [x] examples/simple_agent.py
  - [x] examples/mcp_agent.py
- [x] Version set to 0.1.0:
  - [x] pyproject.toml
  - [x] src/graphton/__init__.py

## Release Steps

### 1. Final Verification

Run all checks to ensure everything is working:

```bash
# Navigate to graphton repository
cd /Users/suresh/scm/github.com/plantoncloud-inc/graphton

# Run all checks
make build

# Expected output:
# ✅ Linting passes
# ✅ Type checking passes
# ✅ All tests pass
```

If any checks fail, fix issues before proceeding.

### 2. Commit All Phase 5 Changes

```bash
# Check status
git status

# Add all Phase 5 files
git add .

# Commit
git commit -m "docs: complete Phase 5 - documentation and open source release

- Updated README with GitHub installation instructions
- Created comprehensive documentation (INSTALLATION, MIGRATION, TROUBLESHOOTING)
- Enhanced CONTRIBUTING.md with development workflows
- Added GitHub issue templates and PR template
- Created SECURITY.md and CHANGELOG.md
- Documented all examples with examples/README.md
- Updated API docs with MCP integration details
- Marked Phase 5 as complete in roadmap

Phase 5 is now complete. Graphton is ready for v0.1.0 release."

# Push to main
git push origin main
```

### 3. Create Git Tag

```bash
# Create annotated tag
git tag -a v0.1.0 -m "Release v0.1.0 - Initial Public Release

Graphton v0.1.0 includes:
- Declarative agent creation (Phase 1-2)
- MCP integration with zero boilerplate (Phase 3)
- Configuration validation with Pydantic (Phase 4)
- Comprehensive documentation and examples (Phase 5)

Install: pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

See CHANGELOG.md for full release notes."

# Verify tag was created
git tag -l -n9 v0.1.0

# Push tag to GitHub
git push origin v0.1.0
```

### 4. Create GitHub Release

1. **Go to GitHub Releases page**:
   - Navigate to: https://github.com/plantoncloud-inc/graphton/releases
   - Click "Draft a new release"

2. **Configure the release**:
   - **Choose a tag**: Select `v0.1.0` (just created)
   - **Release title**: `v0.1.0 - Initial Public Release`
   - **Pre-release**: ✅ Check this box (mark as pre-release since it's v0.x.x)

3. **Release description** (copy from CHANGELOG.md):

```markdown
# Graphton v0.1.0 - Initial Public Release

**Declarative agent creation for LangGraph - eliminate boilerplate, build agents in minutes**

## Highlights

Graphton reduces agent creation from 100+ lines of boilerplate to ~10 lines of declarative configuration:

- ✅ **Rapid Development**: Create agents in minutes, not hours
- ✅ **Zero Boilerplate**: No manual tool wrappers or middleware
- ✅ **MCP Integration**: First-class Model Context Protocol support
- ✅ **Type-Safe**: Full Pydantic validation with clear error messages
- ✅ **Production-Ready**: Battle-tested patterns from graph-fleet

## Installation

```bash
# Install v0.1.0
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Or with Poetry
poetry add git+https://github.com/plantoncloud-inc/graphton.git#v0.1.0
```

## Quick Example

```python
from graphton import create_deep_agent

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="You are a helpful assistant.",
    
    # MCP tools with zero boilerplate
    mcp_servers={
        "planton-cloud": {
            "url": "https://mcp.planton.ai/",
        }
    },
    mcp_tools={
        "planton-cloud": ["list_organizations", "create_cloud_resource"]
    }
)

# Invoke with per-user authentication
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"_user_token": token}}
)
```

## What's Included

### Phase 1-2: Core Agent Factory
- Model name parsing with friendly aliases (Anthropic, OpenAI)
- Automatic model instantiation
- Parameter overrides (temperature, max_tokens, recursion_limit)

### Phase 3: MCP Integration
- MCP server configuration (Cursor-compatible format)
- Automatic tool wrapper generation (zero boilerplate)
- Per-user authentication support
- Works in local and LangGraph Cloud deployments

### Phase 4: Configuration Validation
- Pydantic models with comprehensive validation
- Clear error messages with actionable suggestions
- Type hints throughout (mypy clean)

### Phase 5: Documentation & Examples
- Comprehensive guides: [Installation](docs/INSTALLATION.md), [Migration](docs/MIGRATION.md), [Troubleshooting](docs/TROUBLESHOOTING.md)
- Complete [API documentation](docs/API.md) and [Configuration reference](docs/CONFIGURATION.md)
- Working examples: [simple_agent.py](examples/simple_agent.py), [mcp_agent.py](examples/mcp_agent.py)
- Enhanced [CONTRIBUTING guide](CONTRIBUTING.md)
- Security policy and issue templates

## Documentation

- **README**: [README.md](README.md)
- **Installation**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **API Reference**: [docs/API.md](docs/API.md)
- **Configuration**: [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- **Migration Guide**: [docs/MIGRATION.md](docs/MIGRATION.md)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Examples**: [examples/](examples/)

## Requirements

- Python 3.11+
- LangGraph >= 1.0.0
- LangChain >= 1.0.0
- See [pyproject.toml](pyproject.toml) for full dependency list

## Breaking Changes

None (initial release)

## Known Issues

- Currently only supports `streamable_http` MCP transport
- Model string validation happens at runtime (not compile time)

## Contributors

- [@sureshattaluri](https://github.com/sureshattaluri) - Core development
- Planton Cloud Engineering Team - Testing and feedback

## What's Next

**Phase 6**: graph-fleet migration and production validation
- Migrate existing graph-fleet agents to Graphton
- Real-world production testing
- Performance optimizations

**Future releases** will add:
- Additional MCP transports (stdio, SSE)
- React Agent support
- Enhanced tooling and CLI
- PyPI distribution (when external adoption grows)

## Feedback

We'd love to hear from you:
- 🐛 **Bug reports**: [Open an issue](https://github.com/plantoncloud-inc/graphton/issues)
- 💡 **Feature requests**: [Open an issue](https://github.com/plantoncloud-inc/graphton/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)

---

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)
```

4. **Publish the release**:
   - Click "Publish release"

### 5. Verify Installation

Test installation from the released tag:

```bash
# Create fresh test environment
cd /tmp
python -m venv test-graphton-v0.1.0
source test-graphton-v0.1.0/bin/activate

# Install from v0.1.0 tag
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Verify version
python -c "from graphton import __version__; print(f'Graphton version: {__version__}')"
# Expected: Graphton version: 0.1.0

# Verify import works
python -c "from graphton import create_deep_agent; print('✅ Import successful')"

# Test with example (requires API key)
export ANTHROPIC_API_KEY="your-key"
cd /Users/suresh/scm/github.com/plantoncloud-inc/graphton
python examples/simple_agent.py

# Expected: Examples run successfully

# Cleanup
deactivate
rm -rf test-graphton-v0.1.0
```

### 6. Update graph-fleet to Use v0.1.0

Once release is verified, update graph-fleet to use the released version:

```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet

# Update dependency
# In pyproject.toml or requirements.txt:
# graphton @ git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Or with Poetry:
poetry add git+https://github.com/plantoncloud-inc/graphton.git#v0.1.0

# Test graph-fleet agents with new version
make test

# Commit and push
git commit -am "deps: upgrade to graphton v0.1.0"
git push origin main
```

### 7. Announcement (Optional)

Consider announcing the release:

1. **GitHub Discussions**:
   - Create a post in Announcements category
   - Link to release notes
   - Highlight key features

2. **Internal Communication**:
   - Share with Planton Cloud team
   - Update project documentation

3. **Social Media** (if desired):
   - Twitter/LinkedIn post
   - Dev.to article
   - Show before/after code comparison

## Post-Release

### Repository Settings

Configure GitHub repository (if not already done):

1. **About section**:
   - Description: "Declarative agent creation for LangGraph - eliminate boilerplate, build agents in minutes"
   - Website: Link to README or docs
   - Topics: `langgraph`, `langchain`, `agents`, `mcp`, `ai`, `python`, `deep-agents`

2. **Features**:
   - ✅ Issues
   - ✅ Discussions
   - ✅ Projects (optional)

3. **Branches**:
   - Default branch: `main`
   - Branch protection (optional):
     - Require PR reviews before merging
     - Require status checks to pass

### Monitor and Support

After release:

1. **Watch for issues**:
   - Monitor GitHub issues
   - Respond to questions in Discussions
   - Fix critical bugs promptly

2. **Gather feedback**:
   - Track what features users request
   - Note common pain points
   - Identify documentation gaps

3. **Plan improvements**:
   - Use feedback for Phase 6
   - Prioritize v0.2.0 features
   - Update roadmap

## Troubleshooting Release

### Problem: Tag already exists

```bash
# Delete local tag
git tag -d v0.1.0

# Delete remote tag
git push origin :refs/tags/v0.1.0

# Recreate tag
git tag -a v0.1.0 -m "..."
git push origin v0.1.0
```

### Problem: Need to update release

- Edit the GitHub release (can update description any time)
- For code changes, create v0.1.1 instead

### Problem: Installation fails

- Check tag exists: https://github.com/plantoncloud-inc/graphton/tags
- Verify URL format is correct
- Test in clean environment

## Release Checklist

- [ ] All Phase 5 tasks completed
- [ ] `make build` passes (lint, typecheck, test)
- [ ] All documentation reviewed and polished
- [ ] Version set to 0.1.0 in pyproject.toml and __init__.py
- [ ] CHANGELOG.md updated
- [ ] Phase 5 changes committed and pushed to main
- [ ] Git tag v0.1.0 created and pushed
- [ ] GitHub release created and published
- [ ] Installation verified from v0.1.0 tag
- [ ] graph-fleet updated to use v0.1.0
- [ ] Repository settings configured
- [ ] Announcement posted (if doing public announcement)

## Success Criteria

Release is successful when:

- ✅ v0.1.0 tag exists on GitHub
- ✅ GitHub release is published
- ✅ Installation works: `pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0`
- ✅ Examples run successfully
- ✅ graph-fleet uses v0.1.0
- ✅ No critical issues reported in first 48 hours

---

**Congratulations on releasing Graphton v0.1.0!** 🎉

Next up: Phase 6 - graph-fleet migration and production validation.

