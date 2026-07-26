# Security Policy

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:               |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please:

1. **DO NOT** disclose it publicly
2. **Email** us at [aldanehutchinson5@gmail.com]
3. **Include** as much detail as possible:
   - Type of vulnerability
   - Affected version(s)
   - Steps to reproduce
   - Potential impact

## Response Process

1. **Initial Response** - Within 24 hours
2. **Investigation** - We'll confirm the vulnerability
3. **Patch Development** - We'll work on a fix
4. **Coordinated Disclosure** - We'll publicly disclose after a fix is available

## Security Best Practices

When using Tite:

- Always use the latest version
- Review generated project files before committing
- Never commit secrets or credentials to version control
- Use `.env` for environment variables (Tite creates this for you)

## Security Features in Tite

- `.gitignore` is auto-generated to exclude sensitive files
- `.env.example` is provided for environment variables
- Virtual environment isolation
- No external code execution during setup

---

Thank you for helping keep Tite secure! 🔒