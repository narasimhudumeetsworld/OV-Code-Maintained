# Secret Management Guide

This guide covers best practices for managing secrets in AI-generated and human-written code.

## Core Principles

1. **Never commit secrets to version control**
2. **Use environment variables or secret managers**
3. **Rotate secrets regularly**
4. **Apply principle of least privilege**
5. **Audit secret access**

## What Are Secrets?

Secrets include:
- API keys
- Database passwords
- Encryption keys
- OAuth tokens
- Private keys
- Connection strings

## Storage Options

### 1. Environment Variables (Development)

```bash
# .env file (NEVER commit this)
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
```

```python
# Python usage
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
```

### 2. Secret Managers (Production)

Recommended services:
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager
- HashiCorp Vault

```python
# AWS Secrets Manager example
import boto3
import json

def get_secret(secret_name: str) -> dict:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

# Usage
db_credentials = get_secret("prod/database")
```

## .gitignore Configuration

Always include these patterns:

```gitignore
# Environment files
.env
.env.local
.env.*.local

# Secret files
secrets.yaml
secrets.json
*.pem
*.key

# IDE settings that might contain secrets
.idea/
.vscode/

# AWS credentials
.aws/credentials

# Google credentials
gcloud/
service-account.json
```

## Secret Detection

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### CI/CD Scanning

```yaml
# GitHub Actions
- name: Scan for secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
```

## Code Examples

### Good Practices

```python
# Good: Load from environment
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

# Good: Use secret manager
from secret_manager import get_secret

db_password = get_secret("database_password")
```

### Bad Practices

```python
# BAD: Hardcoded secrets
API_KEY = "sk-12345abcdef"  # NEVER DO THIS

# BAD: Secrets in source code
DATABASE_URL = "postgresql://user:password123@localhost/db"

# BAD: Committing .env files
# (should be in .gitignore)
```

## Secret Rotation

### Rotation Policy

| Secret Type | Rotation Frequency |
|-------------|-------------------|
| API Keys | Every 90 days |
| Database Passwords | Every 90 days |
| Encryption Keys | Every 365 days |
| Session Secrets | Every 30 days |

### Rotation Process

1. Generate new secret
2. Update secret in secret manager
3. Deploy application with new secret
4. Verify functionality
5. Revoke old secret
6. Audit and document

## Audit and Monitoring

### What to Monitor

- Secret access attempts
- Failed authentication
- Unusual access patterns
- Secret modifications

### Logging

```python
# Log secret access (without logging the secret itself)
logger.info(f"Secret accessed: {secret_name} by {user_id}")

# Never log actual secret values
# BAD: logger.info(f"Using API key: {api_key}")
```

## Emergency Response

If a secret is compromised:

1. **Immediately rotate** the compromised secret
2. **Review access logs** for unauthorized use
3. **Notify affected parties** if necessary
4. **Document the incident**
5. **Implement additional controls** to prevent recurrence

## Checklist

Before deploying:

- [ ] No secrets in source code
- [ ] All secrets in environment variables or secret manager
- [ ] .gitignore includes secret file patterns
- [ ] Pre-commit hooks detect secrets
- [ ] CI/CD scans for secrets
- [ ] Rotation policy documented
- [ ] Access logging enabled
