---
name: Bug report
about: Create a report to help us improve Graphton
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## To Reproduce

Steps to reproduce the behavior:

1. Install Graphton: `pip install git+https://github.com/plantoncloud-inc/graphton.git@vX.Y.Z`
2. Create agent with: '...'
3. Invoke with: '...'
4. See error

**Minimal Code Example:**

```python
from graphton import create_deep_agent

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "..."}]
})
```

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

**Error Message:**

```
Paste complete error message and traceback here
```

## Environment

**Python Version:**
```bash
python --version
```

**Graphton Version:**
```python
import graphton
print(graphton.__version__)
```

**Dependencies:**
```bash
pip list | grep -E "(graphton|langgraph|langchain|deepagents)"
```

**Operating System:**
- [ ] macOS
- [ ] Linux
- [ ] Windows
- [ ] Other: ___________

**Installation Method:**
- [ ] pip
- [ ] Poetry
- [ ] From source

## Additional Context

Add any other context about the problem here:

- Configuration files (redact sensitive info)
- Relevant logs
- Screenshots (if applicable)
- Related issues

## Checklist

Before submitting, please check:

- [ ] I have searched existing issues for duplicates
- [ ] I have provided a minimal reproducible example
- [ ] I have included the complete error message
- [ ] I have specified my environment details
- [ ] I have checked the [Troubleshooting Guide](https://github.com/plantoncloud-inc/graphton/blob/main/docs/TROUBLESHOOTING.md)
