# OWASP Security Checklist

This checklist covers the OWASP Top 10 security risks that all code must address.

## A01:2021 - Broken Access Control

### Requirements
- [ ] Implement proper authentication for all endpoints
- [ ] Validate authorization for every request
- [ ] Use principle of least privilege
- [ ] Deny access by default
- [ ] Log access control failures

### Code Examples

```python
# Good: Check authorization
@require_permission("users:read")
async def get_user(user_id: str, current_user: User):
    if not current_user.can_access(user_id):
        raise AuthorizationError("Cannot access this user")
    return await user_service.get(user_id)

# Bad: No authorization check
async def get_user(user_id: str):
    return await user_service.get(user_id)
```

## A02:2021 - Cryptographic Failures

### Requirements
- [ ] Use strong encryption algorithms (AES-256, RSA-2048+)
- [ ] Hash passwords with bcrypt/argon2
- [ ] Use TLS for data in transit
- [ ] Don't hardcode encryption keys
- [ ] Rotate secrets regularly

### Code Examples

```python
# Good: Use bcrypt for passwords
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

## A03:2021 - Injection

### Requirements
- [ ] Use parameterized queries
- [ ] Validate and sanitize all input
- [ ] Use ORM instead of raw SQL
- [ ] Escape special characters
- [ ] Whitelist allowed inputs where possible

### Code Examples

```python
# Good: Parameterized query
query = "SELECT * FROM users WHERE id = :id"
result = db.execute(query, {"id": user_id})

# Bad: String interpolation (SQL injection risk)
query = f"SELECT * FROM users WHERE id = {user_id}"
result = db.execute(query)
```

## A04:2021 - Insecure Design

### Requirements
- [ ] Threat model during design phase
- [ ] Use secure design patterns
- [ ] Implement defense in depth
- [ ] Follow secure development lifecycle
- [ ] Review design for security

## A05:2021 - Security Misconfiguration

### Requirements
- [ ] Remove default credentials
- [ ] Disable unnecessary features
- [ ] Configure security headers
- [ ] Keep software updated
- [ ] Use secure defaults

### Security Headers

```python
# Required security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}
```

## A06:2021 - Vulnerable Components

### Requirements
- [ ] Inventory all dependencies
- [ ] Monitor for vulnerabilities
- [ ] Update dependencies regularly
- [ ] Remove unused dependencies
- [ ] Use only trusted sources

### Commands

```bash
# Check for vulnerabilities
pip-audit
npm audit

# Update dependencies
pip install --upgrade -r requirements.txt
npm update
```

## A07:2021 - Authentication Failures

### Requirements
- [ ] Implement multi-factor authentication
- [ ] Use secure session management
- [ ] Implement account lockout
- [ ] Use secure password policies
- [ ] Protect against brute force

### Password Policy

```python
PASSWORD_REQUIREMENTS = {
    "min_length": 8,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_digit": True,
    "require_special": True,
    "max_age_days": 90,
}
```

## A08:2021 - Software and Data Integrity Failures

### Requirements
- [ ] Verify digital signatures
- [ ] Use integrity checks for updates
- [ ] Secure CI/CD pipeline
- [ ] Review third-party code
- [ ] Use signed commits

## A09:2021 - Security Logging and Monitoring

### Requirements
- [ ] Log security events
- [ ] Monitor for anomalies
- [ ] Set up alerts
- [ ] Retain logs appropriately
- [ ] Protect log integrity

### What to Log

```python
# Security events to log
SECURITY_EVENTS = [
    "login_success",
    "login_failure",
    "password_change",
    "permission_denied",
    "token_expired",
    "suspicious_activity",
]
```

## A10:2021 - Server-Side Request Forgery (SSRF)

### Requirements
- [ ] Validate and sanitize URLs
- [ ] Use allowlists for external calls
- [ ] Disable unnecessary URL schemes
- [ ] Don't return raw responses
- [ ] Implement network segmentation

### Code Examples

```python
# Good: Whitelist allowed domains
ALLOWED_DOMAINS = ["api.example.com", "cdn.example.com"]

def fetch_url(url: str) -> bytes:
    parsed = urlparse(url)
    if parsed.netloc not in ALLOWED_DOMAINS:
        raise SecurityError("Domain not allowed")
    return requests.get(url).content
```

## Review Checklist

Before deploying code, verify:

- [ ] All input is validated
- [ ] Authentication is implemented
- [ ] Authorization checks are in place
- [ ] Sensitive data is encrypted
- [ ] Secrets are not hardcoded
- [ ] Dependencies are up to date
- [ ] Security headers are configured
- [ ] Logging is implemented
- [ ] Error messages don't leak info
