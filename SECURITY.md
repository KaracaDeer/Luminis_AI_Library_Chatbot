# Security Policy

## 🛡️ Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| 0.9.x   | :x:                |
| < 0.9   | :x:                |

## 🚨 Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability within Luminis.AI, please report it responsibly.

### 📧 How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via:

- **Email**: [security@luminis-ai.com](mailto:security@luminis-ai.com)
- **LinkedIn**: [Fatma Karaca Erdogan](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378/)
- **GitHub Security Advisories**: Use the "Report a vulnerability" button on our repository

### 📋 Information to Include

When reporting a vulnerability, please include:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** assessment
4. **Suggested fix** (if any)
5. **Your contact information** for follow-up

### ⏱️ Response Timeline

- **Initial Response**: Within 24 hours
- **Status Update**: Within 72 hours
- **Resolution**: Within 30 days (depending on complexity)

## 🔒 Security Measures

### Authentication & Authorization

- **JWT Tokens**: Secure token-based authentication with configurable expiration
- **OAuth 2.0**: Integration with Google, GitHub, and Microsoft for secure social login
- **Password Security**: Bcrypt hashing with salt rounds
- **Session Management**: Secure session handling with automatic cleanup

### Data Protection

- **API Key Security**: OpenAI API keys are stored securely and never exposed to frontend
- **Database Security**: SQLite with parameterized queries to prevent SQL injection
- **Environment Variables**: Sensitive data stored in environment variables
- **HTTPS**: All production communications encrypted with TLS

### Input Validation

- **Request Validation**: Pydantic models for all API endpoints
- **SQL Injection Prevention**: Parameterized queries throughout
- **XSS Protection**: Input sanitization and output encoding
- **File Upload Security**: Restricted file types and size limits

### Infrastructure Security

- **Docker Security**: Minimal base images and non-root user execution
- **Network Security**: Firewall rules and network isolation
- **Dependency Scanning**: Regular updates and vulnerability scanning
- **Secrets Management**: Secure handling of API keys and credentials

## 🔧 Security Configuration

### Environment Variables

```bash
# JWT Security
JWT_SECRET_KEY=your_very_strong_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# API Security
OPENAI_API_KEY=your_openai_api_key_here
API_RATE_LIMIT=100  # requests per minute

# Database Security
DATABASE_URL=sqlite:///./luminis_library.db
CHROMA_PERSIST_DIRECTORY=./chroma_db

# CORS Security
CORS_ORIGINS=["http://localhost:5173", "https://yourdomain.com"]
CORS_METHODS=["GET", "POST", "PUT", "DELETE"]
CORS_HEADERS=["*"]
```

### Security Headers

The application implements the following security headers:

```python
# Security Headers
"X-Content-Type-Options": "nosniff"
"X-Frame-Options": "DENY"
"X-XSS-Protection": "1; mode=block"
"Strict-Transport-Security": "max-age=31536000; includeSubDomains"
"Content-Security-Policy": "default-src 'self'"
"Referrer-Policy": "strict-origin-when-cross-origin"
```

## 🔍 Security Audit Checklist

### Code Review Process

- [ ] Input validation on all endpoints
- [ ] Authentication checks for protected routes
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Rate limiting implementation
- [ ] Error handling without information disclosure

### Dependency Management

- [ ] Regular dependency updates
- [ ] Vulnerability scanning with `safety` or `pip-audit`
- [ ] License compliance checking
- [ ] Minimal dependency footprint

### Infrastructure Security

- [ ] Docker image scanning
- [ ] Network security configuration
- [ ] SSL/TLS certificate management
- [ ] Backup and recovery procedures
- [ ] Monitoring and logging

## 🛠️ Security Tools

### Development Tools

```bash
# Python Security Scanning
pip install safety bandit semgrep
safety check
bandit -r src/
semgrep --config=auto src/

# Node.js Security Scanning
npm audit
npm install -g snyk
snyk test

# Docker Security
docker run --rm -v $(pwd):/src securecodewarrior/docker-security-scan
```

### CI/CD Security

```yaml
# GitHub Actions Security Workflow
- name: Security Scan
  run: |
    pip install safety bandit
    safety check
    bandit -r src/

- name: Dependency Check
  run: |
    npm audit --audit-level moderate
    pip install pip-audit
    pip-audit
```

## 📚 Security Best Practices

### For Developers

1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive data
3. **Validate all inputs** before processing
4. **Implement proper error handling** without information disclosure
5. **Keep dependencies updated** regularly
6. **Use HTTPS** in production
7. **Implement rate limiting** to prevent abuse
8. **Log security events** for monitoring

### For Users

1. **Keep your API keys secure** and never share them
2. **Use strong passwords** for local accounts
3. **Enable 2FA** when available
4. **Regularly update** your local installation
5. **Report suspicious activity** immediately

## 🚨 Incident Response

### Security Incident Process

1. **Detection**: Monitor logs and alerts
2. **Assessment**: Evaluate the scope and impact
3. **Containment**: Isolate affected systems
4. **Investigation**: Determine root cause
5. **Recovery**: Restore services securely
6. **Post-Incident**: Document lessons learned

### Contact Information

- **Security Team**: [security@luminis-ai.com](mailto:security@luminis-ai.com)
- **Project Maintainer**: [Fatma Karaca Erdogan](https://www.linkedin.com/in/fatma-karaca-erdogan-32201a378/)
- **Emergency Contact**: fatmakaracaerdogan@gmail.com

## 📖 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [React Security](https://react.dev/learn/keeping-components-pure)
- [OpenAI API Security](https://platform.openai.com/docs/guides/safety-best-practices)

## 📄 License

This security policy is part of the Luminis.AI project and is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Last Updated**: December 2024
**Version**: 1.0.0
**Maintainer**: Fatma Karaca Erdogan
