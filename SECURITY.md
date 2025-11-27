# Security Policy

## Supported Versions

The following versions of Graphton are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

We recommend always using the latest version.

## Reporting a Vulnerability

We take the security of Graphton seriously. If you've discovered a security vulnerability, please help us protect our users by reporting it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security vulnerabilities by emailing:

**security@planton.cloud**

Include in your report:

1. **Description**: Clear description of the vulnerability
2. **Impact**: What an attacker could do with this vulnerability
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Proof of Concept**: Code or steps demonstrating the vulnerability (if applicable)
5. **Suggested Fix**: If you have ideas on how to fix it (optional)
6. **Your Contact Info**: So we can follow up with you

### What to Expect

1. **Acknowledgment**: We'll acknowledge your report within 48 hours
2. **Updates**: We'll keep you informed as we investigate and work on a fix
3. **Disclosure**: We'll work with you on responsible disclosure timing
4. **Credit**: We'll credit you in the security advisory (if you wish)

### Security Update Process

1. **Triage**: We'll assess the severity and impact
2. **Fix**: We'll develop and test a fix
3. **Release**: We'll release a security patch
4. **Advisory**: We'll publish a security advisory
5. **Notification**: We'll notify users of the vulnerability and fix

## Security Best Practices

When using Graphton:

### 1. API Key Management

**DO**:
- Store API keys in environment variables or secure secret managers
- Use different keys for development and production
- Rotate keys regularly
- Restrict key permissions to minimum required

**DON'T**:
- Hardcode API keys in code
- Commit keys to version control
- Share keys via insecure channels
- Use production keys in development

```python
# ✅ Good: Use environment variables
import os
user_token = os.getenv("PLANTON_API_KEY")

# ❌ Bad: Hardcoded key
user_token = "pk_live_123456789"  # Never do this!
```

### 2. User Token Handling

**DO**:
- Pass user tokens via config at runtime
- Validate token format before use
- Use HTTPS for MCP server connections
- Implement token expiration

**DON'T**:
- Store tokens in code or logs
- Share tokens across users
- Use HTTP for production MCP servers

```python
# ✅ Good: Per-user token via config
result = agent.invoke(
    {"messages": [...]},
    config={"configurable": {"_user_token": user_token}}
)

# ❌ Bad: Global token
os.environ["USER_TOKEN"] = token  # Affects all users
```

### 3. Input Validation

**DO**:
- Validate all user inputs
- Sanitize data before passing to agents
- Use Pydantic models for validation
- Implement rate limiting

**DON'T**:
- Trust user input blindly
- Pass raw user data to system commands
- Allow arbitrary code execution

### 4. Dependency Management

**DO**:
- Keep Graphton and dependencies updated
- Review dependency security advisories
- Use virtual environments
- Pin dependency versions in production

**DON'T**:
- Use outdated versions with known vulnerabilities
- Install from untrusted sources

```bash
# Check for security updates
pip list --outdated

# Update to latest secure version
pip install --upgrade git+https://github.com/plantoncloud-inc/graphton.git@latest
```

### 5. MCP Server Security

**DO**:
- Use HTTPS for production MCP servers
- Verify MCP server certificates
- Implement authentication for your MCP servers
- Monitor MCP server access logs

**DON'T**:
- Use HTTP in production
- Disable SSL verification
- Expose MCP servers without authentication

```python
# ✅ Good: HTTPS MCP server
mcp_servers = {
    "my-server": {
        "url": "https://mcp.example.com/",  # HTTPS
        "auth_from_context": True,
    }
}

# ⚠️ Warning: HTTP only for localhost development
mcp_servers = {
    "local-dev": {
        "url": "http://localhost:8000/",  # OK for local dev
        "auth_from_context": False,
    }
}
```

### 6. Production Deployment

**DO**:
- Use secure environment variable management
- Implement proper access controls
- Monitor for suspicious activity
- Keep logs secure and private
- Use secure network configurations

**DON'T**:
- Expose internal services publicly
- Log sensitive information
- Skip authentication in production

## Known Security Considerations

### 1. LangGraph Agent Execution

Agents use LLMs which may produce unexpected outputs. Always:
- Validate agent responses before acting on them
- Implement timeouts and recursion limits
- Monitor agent behavior in production
- Review agent actions that affect critical systems

### 2. MCP Tool Access

MCP tools have access to your infrastructure. Ensure:
- Users are properly authenticated
- Tools have appropriate permissions
- Actions are logged and auditable
- Critical operations require confirmation

### 3. Prompt Injection

LLM agents can be susceptible to prompt injection:
- Validate and sanitize user inputs
- Use system prompts that discourage harmful behavior
- Implement output validation
- Monitor for unusual agent behavior

## Security-Related Dependencies

Graphton depends on:

- **LangChain**: For LLM interactions
- **LangGraph**: For agent orchestration
- **Pydantic**: For data validation
- **langchain-mcp-adapters**: For MCP integration

We monitor these dependencies for security updates and update Graphton accordingly.

## Vulnerability Disclosure Policy

We believe in responsible vulnerability disclosure:

1. **Report vulnerabilities privately** to security@planton.cloud
2. **Give us reasonable time** to fix the issue (typically 90 days)
3. **Coordinate disclosure timing** with us
4. **Do not exploit** vulnerabilities in production systems

We commit to:

1. **Respond promptly** to security reports
2. **Keep reporters informed** of our progress
3. **Credit reporters** in security advisories (with permission)
4. **Release patches** as quickly as possible

## Security Updates

Security updates are released as:

- **Patch versions** (e.g., 0.1.1) for non-breaking security fixes
- **Security advisories** published on GitHub
- **Notifications** via GitHub watch/star
- **Announcements** in release notes and discussions

Subscribe to security updates:

1. Watch this repository on GitHub
2. Follow release notes
3. Check [GitHub Security Advisories](https://github.com/plantoncloud-inc/graphton/security/advisories)

## Contact

- **Security issues**: security@planton.cloud
- **General questions**: [GitHub Discussions](https://github.com/plantoncloud-inc/graphton/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/plantoncloud-inc/graphton/issues)

## Attribution

We appreciate security researchers who help keep Graphton safe. Thank you to:

- (Security researchers will be listed here as vulnerabilities are responsibly disclosed)

---

**Last Updated**: November 27, 2025

