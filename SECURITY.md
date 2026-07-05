# Security Policy

## What this repository contains

This repo contains engineering standards (markdown files), Python scripts (query/validation tooling), and a VS Code extension (TypeScript). It does **not** contain:
- Services that handle user data
- Credentials or secrets
- Network-facing applications (except the MCP server which runs locally)

## Supported versions

| Version | Supported |
|---------|-----------|
| v1.0.0 (latest) | ✅ Yes |
| main (unreleased) | Best-effort |
| < v1.0.0 | ❌ No |

## Reporting a vulnerability

If you discover a security issue in this repository:

1. **Do NOT open a public issue**
2. Email: bharathtvadhoola@gmail.com
3. Include: description, steps to reproduce, affected versions
4. Expected response: within 5 working days

We will acknowledge receipt, assess severity, and coordinate disclosure.

## What we scan

| Check | Tool | When |
|-------|------|------|
| Python SAST | bandit | Every PR (CI — Code pipeline) |
| Python lint | ruff | Every PR |
| Dependency vulnerabilities (Python) | Dependabot | Weekly scan + PR alerts |
| Dependency vulnerabilities (npm) | npm audit + Dependabot | Weekly scan + PR alerts |
| TypeScript type safety | tsc --strict | Every PR |
| Secrets in code | detect-secrets (pre-commit) | Every commit (local) |
| Trusted sources | validate_standards.py | Every PR touching modules/ |

## Permissions and trust model

### VS Code extension

The extension requires **no special permissions**. It:
- ✅ Reads files in your workspace (to run regex checks)
- ✅ Reads the `modules/` directory (to load rules)
- ❌ Does NOT access the network
- ❌ Does NOT read files outside your workspace
- ❌ Does NOT execute arbitrary code
- ❌ Does NOT send telemetry

The extension is open source — inspect `vscode-extension/src/` to verify.

### GitHub Action (compliance checker)

When you use the reusable workflow, it:
- ✅ Checks out YOUR repo (read-only)
- ✅ Checks out THIS repo (read-only, to get the standards)
- ✅ Runs a Python script that greps files and checks config existence
- ❌ Does NOT push to your repo
- ❌ Does NOT access secrets
- ❌ Does NOT make network calls
- ❌ Does NOT modify any files

Pin to a tagged version (`@v1.0.0`) — never `@main` — so you control exactly what code runs.

### MCP server

The MCP server:
- ✅ Runs locally on your machine (stdio transport)
- ✅ Reads standards files from disk
- ✅ Runs regex checks against content passed to it
- ❌ Does NOT access the network
- ❌ Does NOT write files
- ❌ Does NOT execute code beyond regex matching

### Python scripts (query, validate, check_compliance)

All scripts:
- ✅ Read YAML/markdown files
- ✅ Run `grep` and `git` subprocesses (read-only)
- ❌ Do NOT modify files in the target repo (check_compliance only reads)
- ❌ Do NOT access the network
- ❌ Do NOT use `shell=True` in subprocess calls

## Supply chain integrity

- All dependencies are pinned in `requirements.txt` and `package-lock.json`
- Dependabot alerts are enabled for both Python and npm
- `.vsix` releases are built from tagged commits — verify by checking the release's commit SHA
- Pre-commit hooks scan for secrets before they reach the repo

## Verifying a release

```bash
# Check the .vsix was built from the tagged commit
gh release view v1.0.0 --json tagName,targetCommitish
git log --oneline v1.0.0 -1

# Verify the .vsix contents (it's a zip file)
unzip -l uk-gov-engineering-standards-1.0.0.vsix
```
