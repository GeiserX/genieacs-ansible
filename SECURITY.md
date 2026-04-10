# Security Policy

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please use GitHub's private vulnerability reporting:

1. Go to https://github.com/GeiserX/genieacs-ansible/security/advisories
2. Click "Report a vulnerability"
3. Fill out the form with details

We will respond within **48 hours** and work with you to understand and address the issue.

### What to Include

- Type of issue (e.g., credential exposure, privilege escalation, insecure defaults)
- Full paths of affected source files
- Step-by-step instructions to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact assessment and potential attack scenarios

### Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

Only the latest version receives security updates. We recommend always running the latest version.

## Security Best Practices for Users

1. **Never commit secrets** - Use Ansible Vault for sensitive variables
2. **Use strong passwords** - For all GenieACS and database credentials
3. **Restrict network access** - Limit GenieACS ports to trusted networks
4. **Keep updated** - Run the latest version of both this role and GenieACS
5. **Review variables** - Audit all configuration variables before deployment

## Contact

For security questions that aren't vulnerabilities, contact: security@geiser.cloud
