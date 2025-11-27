---
name: Bug Report
about: Report a bug to help us improve Graphton
title: "[BUG] "
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of the bug.

## Steps to Reproduce

1. Install Graphton version '...'
2. Run code '...'
3. See error

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Error Message

```
Paste full error message and stack trace here
```

## Minimal Reproducible Example

```python
from graphton import create_deep_agent

# Minimal code that reproduces the bug
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
)

result = agent.invoke({"messages": [...]})
# Bug occurs here
```

## Environment

- **Graphton Version**: [e.g., v0.1.0, main branch]
- **Python Version**: [e.g., 3.11.5]
- **Operating System**: [e.g., macOS 14.0, Ubuntu 22.04, Windows 11]
- **LangGraph Version**: [e.g., 1.0.0]
- **LangChain Version**: [e.g., 1.0.0]

Get versions:
```bash
pip show graphton
python --version
```

## Additional Context

- Is this blocking your work?
- Does it work with a different model/configuration?
- Any relevant logs or debugging information?
- Screenshots (if applicable)

## Checklist

- [ ] I've searched existing issues to ensure this isn't a duplicate
- [ ] I've included a minimal reproducible example
- [ ] I've included the full error message and stack trace
- [ ] I've tested with the latest version of Graphton
- [ ] I've included my environment details

