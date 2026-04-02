---
name: security-best-practices
description: Implement security best practices for Python applications and API integrations. Use when securing API keys, preventing injection attacks, handling secrets, or implementing rate limiting. Handles OWASP Top 10, secrets management, input validation, and dependency security.
metadata:
  tags: security, API-keys, secrets, OWASP, input-validation, rate-limiting
  platforms: Claude, ChatGPT, Gemini
---


# Security Best Practices

## When to use this skill
- **New project**: consider security from the start
- **API integration**: securing LLM API keys and external service calls
- **Data handling**: protecting company data and user queries
- **Dependency audit**: checking for vulnerable packages

## Instructions

### Step 1: Manage secrets

**.env (never commit)**:
```bash
# LLM API Keys
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-4
```

```python
# Read from environment variables
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")
```

### Step 2: Input validation

```python
# Validate user queries before processing
def validate_query(query: str) -> str:
    """Validate and sanitize user query input."""
    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    query = query.strip()
    if len(query) == 0:
        raise ValueError("Query cannot be empty")
    if len(query) > 1000:
        raise ValueError("Query too long (max 1000 characters)")
    return query
```

### Step 3: API rate limiting and error handling

```python
import time
from functools import wraps

def rate_limit(max_calls: int, period: float):
    """Rate limit decorator for API calls."""
    calls = []
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if now - c < period]
            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                time.sleep(sleep_time)
            calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Step 4: Dependency security

```bash
# Check for known vulnerabilities
pip audit

# Pin dependencies
pip freeze > requirements.txt

# Use safety check
pip install safety
safety check
```

## Constraints

### Required rules (MUST)
1. **Secrets via environment**: manage via .env and environment variables; never hardcode
2. **Input validation**: validate all user queries and data inputs
3. **API key rotation**: support key rotation without code changes
4. **Dependency pinning**: pin all dependency versions in requirements.txt
5. **.gitignore**: ensure .env, __pycache__, *.pyc, data/ are ignored

### Prohibited items (MUST NOT)
1. **No hardcoded API keys**: code injection risk
2. **No committing secrets**: never commit .env files
3. **No eval() on user input**: code injection risk
4. **No unpinned dependencies**: reproducibility risk

## OWASP Top 10 checklist (adapted for ML pipelines)

```markdown
- [ ] A01: Broken Access Control - API key management, data access
- [ ] A02: Cryptographic Failures - HTTPS for API calls, encrypted secrets
- [ ] A03: Injection - Input validation on queries, no string interpolation in prompts
- [ ] A04: Insecure Design - Rate limiting, cost controls on LLM calls
- [ ] A05: Security Misconfiguration - Default configs reviewed, debug mode off
- [ ] A06: Vulnerable Components - pip audit, dependency updates
- [ ] A07: Authentication Failures - Secure API key handling
- [ ] A08: Data Integrity Failures - Validate LLM responses, handle malformed data
- [ ] A09: Logging Failures - Log API errors, track costs, monitor usage
- [ ] A10: SSRF - Validate any URLs from company data before fetching
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)
