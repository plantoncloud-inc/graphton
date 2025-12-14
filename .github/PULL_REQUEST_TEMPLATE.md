# Pull Request

## Summary

Brief description of what this PR does (1-2 sentences).

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test updates
- [ ] CI/CD updates
- [ ] Dependency updates

## Related Issues

Fixes #(issue number)
Closes #(issue number)
Related to #(issue number)

## Changes Made

Detailed list of changes:

- Change 1: Description
- Change 2: Description
- Change 3: Description

## Code Changes

**Files Modified:**
- `src/graphton/core/agent.py`: Description of changes
- `src/graphton/core/config.py`: Description of changes
- ...

**New Files Added:**
- `src/graphton/utils/new_module.py`: Description
- ...

**Files Removed:**
- `src/graphton/deprecated.py`: Reason for removal
- ...

## Examples

**Before:**

```python
# Code showing old behavior
```

**After:**

```python
# Code showing new behavior
```

## Breaking Changes

**Is this a breaking change?**
- [ ] Yes
- [ ] No

**If yes, describe the breaking changes and migration path:**

1. What breaks:
2. How to migrate:
3. Deprecation notices added:

## Testing

### Test Coverage

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing locally (`make test`)
- [ ] Code coverage maintained/improved

**Test Results:**

```bash
# Paste test output here
```

### Manual Testing

Describe manual testing performed:

1. Test scenario 1:
   - Steps taken
   - Expected result
   - Actual result

2. Test scenario 2:
   - Steps taken
   - Expected result
   - Actual result

### Tested Environments

- [ ] Python 3.11
- [ ] Python 3.12
- [ ] macOS
- [ ] Linux
- [ ] Windows

## Code Quality

- [ ] Linter passes (`make lint`)
- [ ] Type checker passes (`make typecheck`)
- [ ] All checks pass (`make build`)
- [ ] Code follows project style guidelines
- [ ] Functions have docstrings (Google style)
- [ ] Type hints added for new code

## Documentation

- [ ] README.md updated (if needed)
- [ ] API documentation updated (`docs/API.md`)
- [ ] Configuration guide updated (`docs/CONFIGURATION.md`)
- [ ] Examples updated/added
- [ ] CHANGELOG.md updated
- [ ] Docstrings added/updated
- [ ] Comments added for complex logic

## Backward Compatibility

- [ ] This change is backward compatible
- [ ] Deprecation warnings added for deprecated features
- [ ] Migration guide provided for breaking changes
- [ ] Version number updated appropriately

## Performance Impact

**Does this change affect performance?**
- [ ] Yes - improves performance
- [ ] Yes - degrades performance
- [ ] No - no performance impact
- [ ] Unknown

**If yes, provide benchmarks:**

```
Before: X ms
After: Y ms
Improvement: Z%
```

## Security Considerations

- [ ] No security implications
- [ ] Security implications reviewed
- [ ] Input validation added
- [ ] Authentication/authorization checks added
- [ ] Sensitive data handling reviewed
- [ ] Dependencies reviewed for vulnerabilities

## Deployment Considerations

- [ ] No special deployment steps needed
- [ ] Special deployment steps required (describe below)
- [ ] Database migrations needed
- [ ] Configuration changes needed
- [ ] Dependencies updated

**Special deployment instructions:**

1. Step 1
2. Step 2

## Screenshots/Recordings

If applicable, add screenshots or recordings to help explain your changes.

## Additional Context

Any other information that reviewers should know.

## Checklist

Before submitting, ensure:

### Code
- [ ] Code follows project coding standards
- [ ] No commented-out code or debug statements
- [ ] No hardcoded secrets or sensitive data
- [ ] Imports are organized and minimal
- [ ] No unnecessary dependencies added

### Testing
- [ ] All existing tests still pass
- [ ] New tests cover the changes
- [ ] Edge cases are tested
- [ ] Error cases are tested

### Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has explanatory comments
- [ ] Examples are provided for new features
- [ ] CHANGELOG.md is updated

### Review
- [ ] Self-reviewed my own code
- [ ] Checked for potential side effects
- [ ] Verified no breaking changes (or documented them)
- [ ] Commits are logical and well-described
- [ ] PR description is clear and complete

## Reviewer Notes

Anything specific you want reviewers to focus on?

- Focus area 1
- Focus area 2
- Specific concerns or questions

## Post-Merge Tasks

Tasks to complete after merging:

- [ ] Update dependent projects
- [ ] Announce changes (if significant)
- [ ] Monitor for issues
- [ ] Update external documentation

---

**Thank you for contributing to Graphton!** 🚀

For questions, see [CONTRIBUTING.md](https://github.com/plantoncloud/graphton/blob/main/CONTRIBUTING.md) or ask in [Discussions](https://github.com/plantoncloud/graphton/discussions).
