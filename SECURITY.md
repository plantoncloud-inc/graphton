# Security Policy

## Supported Versions

Currently supported versions for security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Graphton seriously. If you believe you have found a security vulnerability, please report it to us responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please email security details to:

**Email:** security@planton.ai

**Include in your report:**
1. Description of the vulnerability
2. Steps to reproduce the issue
3. Potential impact of the vulnerability
4. Suggested fix (if you have one)
5. Your contact information for follow-up

### What to Expect

- **Acknowledgment:** Within 48 hours of your report
- **Initial Assessment:** Within 5 business days
- **Status Updates:** Regular updates on progress
- **Resolution:** We aim to resolve confirmed vulnerabilities within 30 days

### Security Update Process

1. We will investigate and validate the report
2. We will develop and test a fix
3. We will release a security patch
4. We will credit the reporter (unless they wish to remain anonymous)
5. We will publish a security advisory

## Security Best Practices

### API Key Management

#### DO ✅

```python
# Use environment variables
import os
from graphton import create_deep_agent

agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
)

# API key is loaded from environment by LangChain
# ANTHROPIC_API_KEY=... python script.py
```

```python
# Use secrets management
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

os.environ['ANTHROPIC_API_KEY'] = get_secret('anthropic-key')
```

```python
# Use .env files (not committed to git)
from dotenv import load_dotenv
load_dotenv()  # Loads from .env file

# .gitignore should include:
# .env
# .env.local
```

#### DON'T ❌

```python
# NEVER hardcode API keys
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
)
os.environ['ANTHROPIC_API_KEY'] = "sk-ant-hardcoded-key"  # DON'T DO THIS!
```

```python
# NEVER commit API keys to git
# Bad: config.py
ANTHROPIC_API_KEY = "sk-ant-..."  # DON'T DO THIS!
```

```python
# NEVER log API keys
import logging
logging.info(f"Using key: {os.getenv('ANTHROPIC_API_KEY')}")  # DON'T DO THIS!
```

### MCP Authentication Security

#### Dynamic Authentication (Recommended for Multi-Tenant)

```python
# ✅ Good: Per-user tokens
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={
        "api": {
            "url": "https://api.example.com",
            "headers": {
                "Authorization": "Bearer {{USER_TOKEN}}"  # Template variable
            }
        }
    },
    mcp_tools={"api": ["list_resources"]},
)

# Each user gets their own token
result = agent.invoke(
    {"messages": [...]},
    config={
        "configurable": {
            "USER_TOKEN": get_user_token(user_id)  # Per-user
        }
    }
)
```

#### Static Authentication (Use with Caution)

```python
# ⚠️ Use only when appropriate
# (shared credentials, internal services, etc.)
agent = create_deep_agent(
    model="claude-sonnet-4.5",
    system_prompt="...",
    mcp_servers={
        "api": {
            "url": "https://api.example.com",
            "headers": {
                "X-API-Key": os.getenv("API_KEY")  # From environment, not hardcoded
            }
        }
    },
    mcp_tools={"api": ["list_resources"]},
)
```

### Input Validation

#### Validate User Input

```python
# ✅ Good: Validate and sanitize input
def safe_invoke(agent, user_input):
    # Validate input length
    if len(user_input) > 10000:
        raise ValueError("Input too long")
    
    # Sanitize input
    user_input = user_input.strip()
    
    # Check for obvious injection attempts
    if any(pattern in user_input for pattern in ["{{", "}}", "${"]):
        raise ValueError("Invalid input pattern")
    
    return agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
```

#### Prevent Template Injection

```python
# ✅ Good: Don't allow user input in templates
mcp_servers = {
    "api": {
        "url": "https://api.example.com",
        "headers": {
            "Authorization": f"Bearer {{USER_TOKEN}}"  # Fixed template
        }
    }
}

# ❌ Bad: User input in template
user_server_url = request.get("server_url")  # DON'T DO THIS!
mcp_servers = {
    "api": {
        "url": user_server_url,  # DANGEROUS!
    }
}
```

### Rate Limiting

```python
# ✅ Good: Implement rate limiting
from functools import wraps
from time import time

def rate_limit(max_calls, period):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time()
            # Remove old calls
            calls[:] = [call for call in calls if call > now - period]
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=10, period=60)  # 10 calls per minute
def invoke_agent(agent, message):
    return agent.invoke({"messages": [{"role": "user", "content": message}]})
```

### Error Handling

```python
# ✅ Good: Don't leak sensitive info in errors
try:
    result = agent.invoke(
        {"messages": [...]},
        config={
            "configurable": {
                "USER_TOKEN": user_token
            }
        }
    )
except Exception as e:
    # Log full error internally
    logger.error(f"Agent invocation failed: {str(e)}", exc_info=True)
    
    # Return generic error to user
    return {"error": "An error occurred processing your request"}

# ❌ Bad: Exposing internal details
except Exception as e:
    return {"error": str(e)}  # May contain tokens, URLs, etc.
```

### Dependency Security

#### Keep Dependencies Updated

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Or with Poetry
poetry show --outdated
```

```bash
# Update dependencies regularly
pip install --upgrade git+https://github.com/plantoncloud-inc/graphton.git

# Or with Poetry
poetry update graphton
```

#### Pin Dependencies in Production

```toml
# pyproject.toml
[tool.poetry.dependencies]
graphton = {git = "https://github.com/plantoncloud-inc/graphton.git", tag = "v0.1.0"}
```

```
# requirements.txt
git+https://github.com/plantoncloud-inc/graphton.git@v0.1.0
```

### Network Security

#### Use HTTPS

```python
# ✅ Good: HTTPS URLs
mcp_servers = {
    "api": {
        "url": "https://api.example.com",  # HTTPS
    }
}

# ❌ Bad: HTTP URLs (unless local dev)
mcp_servers = {
    "api": {
        "url": "http://api.example.com",  # Insecure!
    }
}
```

#### Verify SSL Certificates

```python
# Default behavior is to verify SSL
# Only disable for local development

# ⚠️ Development only
import os
if os.getenv("ENV") == "development":
    # Disable SSL verification (dev only!)
    pass
```

### Deployment Security

#### Use Secrets Management

```yaml
# Kubernetes: Use secrets
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
type: Opaque
data:
  ANTHROPIC_API_KEY: <base64-encoded-key>
  PLANTON_API_KEY: <base64-encoded-key>
```

```yaml
# Reference in deployment
env:
  - name: ANTHROPIC_API_KEY
    valueFrom:
      secretKeyRef:
        name: api-keys
        key: ANTHROPIC_API_KEY
```

#### Restrict Network Access

```yaml
# Kubernetes: Network policies
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: graphton-agent
spec:
  podSelector:
    matchLabels:
      app: graphton-agent
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: allowed-namespace
  - to:
    - podSelector:
        matchLabels:
          app: allowed-service
  - to:
    # Allow external MCP servers
    ports:
    - port: 443
      protocol: TCP
```

#### Use Least Privilege

```python
# ✅ Good: Load only necessary tools
mcp_tools = {
    "planton-cloud": [
        "list_organizations",  # Only what's needed
    ]
}

# ❌ Bad: Loading all tools
mcp_tools = {
    "planton-cloud": [
        "list_organizations",
        "create_cloud_resource",  # Not needed? Don't load!
        "delete_cloud_resource",  # Dangerous if not needed
        # ... many more tools
    ]
}
```

### Logging and Monitoring

#### Log Security Events

```python
import logging

logger = logging.getLogger(__name__)

# Log security-relevant events
logger.info(f"Agent invoked by user {user_id}")
logger.warning(f"Rate limit exceeded for user {user_id}")
logger.error(f"Authentication failed for user {user_id}")

# DON'T log sensitive data
# logger.info(f"Token: {user_token}")  # DON'T DO THIS!
```

#### Monitor for Anomalies

```python
# Monitor usage patterns
def monitor_usage(user_id, action):
    # Track API calls per user
    # Alert on unusual patterns
    # Block suspicious activity
    pass
```

## Security Considerations by Feature

### Template Variables

**Security Model:**
- Template variables are substituted at runtime
- No arbitrary code execution
- Simple string replacement only

**Risks:**
- User input should never be used directly as template values without validation
- Template syntax itself should not be exposed to users

**Mitigations:**
- Validate all input
- Use fixed template patterns
- Don't allow user-defined templates

### MCP Tool Loading

**Security Model:**
- Tools are loaded from configured MCP servers only
- Tool names must be explicitly listed
- No arbitrary tool loading

**Risks:**
- MCP server compromise could provide malicious tools
- Tool invocation with malicious parameters

**Mitigations:**
- Only connect to trusted MCP servers
- Use HTTPS for all connections
- Validate tool parameters
- Implement rate limiting

### Agent Execution

**Security Model:**
- Agent runs within LangGraph framework constraints
- Recursion limit prevents infinite loops
- Tools are sandboxed by MCP protocol

**Risks:**
- Excessive API usage (cost)
- Long-running operations
- Resource exhaustion

**Mitigations:**
- Set appropriate recursion limits
- Implement timeouts
- Monitor resource usage
- Rate limit invocations

## Compliance

### GDPR Considerations

If handling EU user data:

1. **Data Minimization:** Only collect necessary data
2. **Purpose Limitation:** Use data only for stated purposes
3. **Storage Limitation:** Delete data when no longer needed
4. **Right to Erasure:** Provide mechanism to delete user data
5. **Data Portability:** Allow users to export their data

### SOC 2 Considerations

For SOC 2 compliance:

1. **Access Controls:** Implement role-based access
2. **Audit Logging:** Log all security-relevant events
3. **Encryption:** Encrypt data in transit and at rest
4. **Incident Response:** Have a security incident response plan
5. **Vendor Management:** Assess security of dependencies

## Security Checklist

Before deploying to production:

- [ ] API keys stored securely (not hardcoded)
- [ ] Environment variables or secrets management used
- [ ] Input validation implemented
- [ ] Rate limiting configured
- [ ] Error messages don't leak sensitive info
- [ ] HTTPS used for all external connections
- [ ] Dependencies pinned to specific versions
- [ ] Security scanning tools integrated (safety, bandit)
- [ ] Logging configured (without sensitive data)
- [ ] Monitoring and alerting set up
- [ ] Backup and recovery procedures documented
- [ ] Security review completed
- [ ] Penetration testing performed (if applicable)

## Resources

- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **LangChain Security:** https://python.langchain.com/docs/security
- **MCP Security:** Consult MCP server documentation

## Contact

For security concerns or questions:

- **Email:** security@planton.ai
- **GitHub Security Advisories:** https://github.com/plantoncloud-inc/graphton/security/advisories

## Updates

This security policy is reviewed quarterly and updated as needed. Last updated: November 2025.
