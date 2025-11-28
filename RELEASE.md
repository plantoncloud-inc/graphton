# Release Guide

Step-by-step guide for creating releases of Graphton.

## Table of Contents

- [Release Process Overview](#release-process-overview)
- [Pre-Release Checklist](#pre-release-checklist)
- [Creating a Release](#creating-a-release)
- [Post-Release Tasks](#post-release-tasks)
- [Version Numbering](#version-numbering)
- [Hotfix Releases](#hotfix-releases)

## Release Process Overview

Graphton uses **semantic versioning** (MAJOR.MINOR.PATCH) and follows a **tag-based release workflow**:

1. **Pre-Release**: Verify all changes, update documentation, run tests
2. **Release**: Create git tag, push to GitHub, create GitHub release
3. **Post-Release**: Verify installation, update dependent projects, announce

## Pre-Release Checklist

### 1. Code Quality

- [ ] All tests passing locally
  ```bash
  make test
  ```

- [ ] Linter passes
  ```bash
  make lint
  ```

- [ ] Type checker passes
  ```bash
  make typecheck
  ```

- [ ] All checks pass
  ```bash
  make build
  ```

- [ ] CI/CD pipeline is green
  - Check GitHub Actions: https://github.com/plantoncloud-inc/graphton/actions

### 2. Documentation

- [ ] README.md is up to date
  - Features list reflects current functionality
  - Installation instructions are correct
  - Examples work as shown

- [ ] CHANGELOG.md is updated
  - All changes since last release are documented
  - Version number is set
  - Release date is set
  - Links are updated

- [ ] API documentation is current
  - docs/API.md reflects actual API
  - docs/CONFIGURATION.md is complete
  - All examples work

- [ ] Examples are working
  - Run all examples to verify
  - Update examples/README.md if needed

### 3. Version Numbering

- [ ] Decide on version number (see [Version Numbering](#version-numbering))

- [ ] Update `pyproject.toml`:
  ```toml
  [tool.poetry]
  version = "0.1.0"  # Update this
  ```

- [ ] Update `src/graphton/__init__.py`:
  ```python
  __version__ = "0.1.0"  # Update this
  ```

- [ ] Update CHANGELOG.md:
  ```markdown
  ## [0.1.0] - 2025-11-28  # Set date
  ```

- [ ] Commit version changes:
  ```bash
  git add pyproject.toml src/graphton/__init__.py CHANGELOG.md
  git commit -m "chore: bump version to 0.1.0"
  git push origin main
  ```

### 4. Final Testing

- [ ] Install from main branch
  ```bash
  pip install git+https://github.com/plantoncloud-inc/graphton.git@main
  ```

- [ ] Run examples
  ```bash
  python examples/simple_agent.py
  python examples/static_mcp_agent.py
  python examples/mcp_agent.py
  ```

- [ ] Verify in fresh environment
  ```bash
  python -m venv test_env
  source test_env/bin/activate
  pip install git+https://github.com/plantoncloud-inc/graphton.git@main
  python -c "from graphton import create_deep_agent; print('✅ Import successful')"
  deactivate
  rm -rf test_env
  ```

## Creating a Release

### Step 1: Create Git Tag

```bash
# Fetch latest changes
git checkout main
git pull origin main

# Create annotated tag
git tag -a v0.1.0 -m "Release v0.1.0"

# Verify tag
git tag -l "v0.1.0"
git show v0.1.0
```

### Step 2: Push Tag to GitHub

```bash
# Push tag to origin
git push origin v0.1.0

# Verify tag on GitHub
open https://github.com/plantoncloud-inc/graphton/tags
```

### Step 3: Create GitHub Release

#### Option A: Using gh CLI (Recommended)

```bash
# Install gh CLI if needed
# macOS: brew install gh
# Other: https://cli.github.com/

# Authenticate
gh auth login

# Create release from CHANGELOG
gh release create v0.1.0 \
  --title "v0.1.0" \
  --notes "$(cat <<'EOF'
# Graphton v0.1.0

First stable release of Graphton - a declarative agent creation framework for LangGraph.

## What's New

- **Declarative Agent Creation**: Create production-ready agents in 3-10 lines instead of 100+
- **Universal MCP Authentication**: Support for any MCP server with static and dynamic authentication
- **Type-Safe Configuration**: Pydantic validation with helpful error messages
- **Full Documentation**: Comprehensive guides for installation, migration, troubleshooting, and API

## Installation

```bash
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

## Quick Start

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

See [README.md](https://github.com/plantoncloud-inc/graphton#readme) for more details.

## Full Changelog

See [CHANGELOG.md](https://github.com/plantoncloud-inc/graphton/blob/v0.1.0/CHANGELOG.md) for complete list of changes.

## Breaking Changes

None (initial release).

## Contributors

Thanks to all contributors who made this release possible!

EOF
)"
```

#### Option B: Using GitHub Web Interface

1. Go to: https://github.com/plantoncloud-inc/graphton/releases/new
2. Select tag: `v0.1.0`
3. Set title: `v0.1.0`
4. Add release notes (see template above)
5. Click "Publish release"

### Step 4: Verify Release

```bash
# Verify release exists
gh release view v0.1.0

# Or visit GitHub
open https://github.com/plantoncloud-inc/graphton/releases/tag/v0.1.0
```

## Post-Release Tasks

### 1. Verify Installation

Test installation from the release tag:

```bash
# Create test environment
python -m venv release_test
source release_test/bin/activate

# Install from release tag
pip install git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0

# Verify version
python -c "import graphton; print(f'Graphton {graphton.__version__}')"

# Test basic functionality
python -c "
from graphton import create_deep_agent
agent = create_deep_agent(
    model='claude-sonnet-4.5',
    system_prompt='Test agent'
)
print('✅ Release verification successful')
"

# Cleanup
deactivate
rm -rf release_test
```

### 2. Update Dependent Projects

If any projects depend on Graphton (e.g., graph-fleet), update them:

```toml
# pyproject.toml in dependent project
[tool.poetry.dependencies]
graphton = {git = "https://github.com/plantoncloud-inc/graphton.git", tag = "v0.1.0"}
```

```bash
# Update dependencies
poetry lock
poetry install

# Test dependent project
make test
```

### 3. Announce Release

#### Internal Announcement

- [ ] Notify team on Slack/Discord
- [ ] Update internal documentation
- [ ] Schedule demo/walkthrough if needed

#### External Announcement (when ready for public)

- [ ] Post on GitHub Discussions
- [ ] Tweet about release (if applicable)
- [ ] Update any external documentation
- [ ] Post to relevant communities (Reddit, HN, etc.)

### 4. Monitor for Issues

- [ ] Watch GitHub issues for bug reports
- [ ] Monitor discussions for questions
- [ ] Be ready for hotfix if critical issues found

## Version Numbering

Graphton follows [Semantic Versioning](https://semver.org/):

### Format: MAJOR.MINOR.PATCH

**MAJOR** (X.0.0): Breaking changes
- API changes that break backward compatibility
- Removal of deprecated features
- Fundamental architecture changes

**MINOR** (0.X.0): New features (backward compatible)
- New functionality added
- New parameters (with defaults)
- Performance improvements
- Deprecation notices (features still work)

**PATCH** (0.0.X): Bug fixes (backward compatible)
- Bug fixes
- Documentation updates
- Security fixes (non-breaking)
- Internal refactoring

### Examples

**0.1.0 → 0.2.0** (Minor):
- Add support for new model provider
- Add new optional parameter to `create_deep_agent()`
- Add new template functions

**0.2.0 → 0.2.1** (Patch):
- Fix bug in template substitution
- Update documentation
- Fix type hints

**0.2.1 → 1.0.0** (Major):
- Remove deprecated features
- Change required parameters
- Rename core functions

### Pre-1.0 Versioning

Before 1.0.0, we're more flexible:
- 0.1.0: Initial release
- 0.2.0: New features
- 0.3.0: More features
- 1.0.0: Production-ready, stable API

## Hotfix Releases

For critical bugs in production:

### Process

1. **Identify Issue**
   - Security vulnerability
   - Critical bug affecting all users
   - Data loss or corruption issue

2. **Create Hotfix Branch**
   ```bash
   git checkout -b hotfix/0.1.1 v0.1.0
   ```

3. **Fix Issue**
   ```bash
   # Make fix
   git add .
   git commit -m "fix: critical bug description"
   ```

4. **Test Thoroughly**
   ```bash
   make build
   # Run affected examples
   ```

5. **Update Version**
   ```bash
   # Update pyproject.toml: 0.1.0 → 0.1.1
   # Update src/graphton/__init__.py: 0.1.0 → 0.1.1
   # Update CHANGELOG.md
   git add pyproject.toml src/graphton/__init__.py CHANGELOG.md
   git commit -m "chore: bump version to 0.1.1"
   ```

6. **Merge to Main**
   ```bash
   git checkout main
   git merge hotfix/0.1.1
   git push origin main
   ```

7. **Create Release**
   ```bash
   git tag -a v0.1.1 -m "Release v0.1.1 (hotfix)"
   git push origin v0.1.1
   gh release create v0.1.1 --title "v0.1.1 (hotfix)" --notes "Critical bug fix..."
   ```

8. **Notify Users**
   - Post on GitHub Discussions
   - Update dependent projects immediately
   - Send notifications if appropriate

## Release Checklist Template

Copy this for each release:

```markdown
# Release v0.X.Y Checklist

## Pre-Release
- [ ] All tests passing
- [ ] Linter passes
- [ ] Type checker passes
- [ ] CI/CD green
- [ ] README.md updated
- [ ] CHANGELOG.md updated
- [ ] Version updated (pyproject.toml, __init__.py)
- [ ] Version committed and pushed
- [ ] Fresh install test passed

## Release
- [ ] Git tag created: `git tag -a v0.X.Y -m "Release v0.X.Y"`
- [ ] Tag pushed: `git push origin v0.X.Y`
- [ ] GitHub release created
- [ ] Release notes published

## Post-Release
- [ ] Installation verified from tag
- [ ] Examples tested with released version
- [ ] Dependent projects updated (if any)
- [ ] Team notified
- [ ] GitHub Issues/Discussions monitored

## Date: YYYY-MM-DD
## Released by: [Your Name]
```

## Troubleshooting

### Tag Already Exists

```bash
# Delete local tag
git tag -d v0.1.0

# Delete remote tag
git push origin :refs/tags/v0.1.0

# Recreate tag
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

### Wrong Version Number

If version was wrong after tag:

```bash
# Delete tag (see above)
# Fix version in files
# Commit fix
# Recreate tag
```

### Release Creation Failed

```bash
# Delete release (if created)
gh release delete v0.1.0

# Recreate
gh release create v0.1.0 --title "v0.1.0" --notes "..."
```

## Questions?

- Open a discussion: https://github.com/plantoncloud-inc/graphton/discussions
- Contact maintainers: security@planton.ai
- Review past releases: https://github.com/plantoncloud-inc/graphton/releases

## Related Documents

- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [README.md](README.md) - Project overview
