# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version                  | Supported          |
| ------------------------ | ------------------ |
| latest (basecamp branch) | :white_check_mark: |
| < 1.0                    | :x:                |

## Reporting a Vulnerability

The DigitalChild project takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### 🔒 Please Do NOT

- ❌ Open a public GitHub issue for security vulnerabilities
- ❌ Post about the vulnerability publicly before we've had a chance to address it
- ❌ Exploit the vulnerability beyond what is necessary to demonstrate it

### ✅ Please DO

**1. Report Privately**

Email security concerns to: **[YOUR-EMAIL@DOMAIN.COM]**

<!-- TODO: Add your actual security contact email -->

**2. Include in Your Report:**

- **Description:** Clear description of the vulnerability
- **Impact:** What could an attacker do? What data is at risk?
- **Steps to Reproduce:** Detailed steps to reproduce the issue
- **Proof of Concept:** Code or commands demonstrating the vulnerability (if possible)
- **Suggested Fix:** If you have ideas for how to fix it
- **Your Contact Info:** So we can follow up with questions

**Example Report:**

```
Subject: [SECURITY] Path Traversal in File Upload

Description: The file upload functionality in processor X doesn't validate
file paths, allowing directory traversal attacks.

Impact: An attacker could read arbitrary files from the server, potentially
accessing sensitive data like API keys or scraped documents.

Steps to Reproduce:
1. Call processor.upload('../../../etc/passwd')
2. File is written outside intended directory
3. Contents can be read

Proof of Concept:
[Code snippet]

Suggested Fix: Validate and sanitize file paths using os.path.normpath()
and ensure they stay within the intended directory.
```

### 📧 Response Timeline

- **Within 48 hours:** We'll acknowledge receipt of your report
- **Within 7 days:** We'll provide an initial assessment and expected timeline
- **Within 30 days:** We'll aim to release a fix (complex issues may take longer)

We'll keep you informed throughout the process.

### 🎉 After the Fix

Once the vulnerability is fixed:

- We'll credit you in the fix announcement (unless you prefer to remain anonymous)
- We'll publish a security advisory on GitHub
- We'll update affected documentation

## 🛡️ Security Best Practices

If you're deploying or using this project, follow these security practices:

### For Users

1. **Keep Updated:** Always use the latest version from the `basecamp` branch
1. **Review Dependencies:** Regularly update dependencies (`pip install --upgrade -r requirements.txt`)
1. **Validate Input:** Don't trust user-provided URLs, file paths, or data
1. **Check Logs:** Monitor logs for suspicious activity
1. **Secure Credentials:** Never commit API keys or credentials to the repository

### For Developers

1. **Input Validation:** Always validate and sanitize user input

1. **Use Validators:** Use the `processors/validators.py` module for:

   - URL validation (blocks malicious patterns)
   - Path validation (prevents traversal attacks)
   - File validation (checks size, extension)

1. **Avoid Eval:** Never use `eval()` or `exec()` on untrusted input

1. **SQL Injection:** Use parameterized queries (we don't use SQL, but good practice)

1. **Dependencies:** Regularly check for vulnerable dependencies:

   ```bash
   pip install safety
   safety check
   ```

### For Scrapers

When adding new scrapers:

- ✅ Validate all URLs before requests
- ✅ Set timeouts on all HTTP requests
- ✅ Limit file sizes when downloading
- ✅ Validate file types after download
- ✅ Handle errors gracefully (don't expose stack traces)
- ✅ Respect robots.txt and rate limits
- ❌ Don't scrape without permission
- ❌ Don't follow untrusted redirects blindly

### Data Security

This project handles sensitive human rights data:

1. **Access Control:** Limit who can access scraped documents
1. **Transmission:** Use HTTPS for all data transfers
1. **Storage:** Be mindful of where data is stored (especially cloud services)
1. **Deletion:** Follow data retention policies
1. **Privacy:** See [docs/DATA_GOVERNANCE.md](docs/DATA_GOVERNANCE.md) for detailed policies

## 🔍 Known Security Considerations

### Current Security Features

✅ **Input Validation:**

- URL validation with malicious pattern blocking (`validators.py`)
- Path traversal protection (`validators.py`)
- File size limits (configurable, default 100MB)
- Extension whitelisting

✅ **Dependency Management:**

- Requirements pinned in `requirements.txt`
- Pre-commit hooks for code quality

✅ **Code Quality:**

- Automated testing (124 tests)
- Linting with flake8
- Type checking encouraged

### Areas for Improvement

⚠️ **Authentication:** No authentication system (not needed for current use case)
⚠️ **Rate Limiting:** Basic timeout, but no sophisticated rate limiting
⚠️ **Secrets Management:** Use environment variables for any API keys
⚠️ **Logging:** Ensure no sensitive data in logs

## 🚨 Security Incidents

If we discover a security incident:

1. We'll notify affected users immediately
1. We'll publish a post-mortem
1. We'll implement measures to prevent recurrence

## 📚 Security Resources

- **OWASP Top 10:** <https://owasp.org/www-project-top-ten/>
- **CWE:** <https://cwe.mitre.org/>
- **Python Security:** <https://python.readthedocs.io/en/stable/library/security_warnings.html>

## 🙏 Thank You

We appreciate security researchers and users who help keep this project secure. Responsible disclosure benefits everyone in the human rights research community.

______________________________________________________________________

**Last updated:** January 2026

**TODO:** Update the security contact email address above!
