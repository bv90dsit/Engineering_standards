# UK Government Engineering Standards

Machine-readable, context-aware engineering standards for UK Government digital services. 69 standards across 5 modules, queryable by role, platform, and enforcement type.

> **Status: MVP / Draft** — not yet adopted by teams. Being developed in the open for feedback.
>
> **Browse the standards:** https://bv90dsit.github.io/Engineering_standards/about/

```
Layer 0 — Source frameworks (GDS, NCSC, DORA, OWASP, WCAG, etc.)
    ↓ synthesised into
Layer 1 — Individual standard files (one .md per standard, with frontmatter)
    ↓ catalogued in
Layer 2 — standards-index.yaml (lightweight, always loaded)
    ↓ filtered by
Layer 3 — query_standards(context) → returns only what applies
    ↓ served to
Layer 4 — Consumers (CI/CD, VS Code extension, onboarding, MCP server)
```

## Quick start

### Auto mode

```bash
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards && pip install pyyaml

python scripts/suggest_standards.py --repo-path /path/to/your-service
```

Detects your stack and lists applicable standards grouped by MUST/SHOULD/COULD.

### Manual mode

```bash
python scripts/onboarding.py --role engineer --platform python
```

Specify your role and platform explicitly. See [usage by role](docs/usage-by-role.md) for detailed workflows.

### Adopt in your service

**1. VS Code extension** — inline warnings as you type ([details](vscode-extension/README.md)):
```bash
code --install-extension uk-gov-engineering-standards-1.1.0.vsix
```

**2. CI check** — compliance on every PR:
```yaml
# .github/workflows/standards.yml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1.1.0
    with:
      role: engineer
      platform: python   # or java, typescript, any
```

**3. Claude Code skill** — Claude follows standards proactively when writing code:
```bash
# Copy the skill into your project
cp -r skills/uk-gov-standards /path/to/your-project/.claude/skills/
```

**4. MCP server** — AI agents query standards and check code in real time ([details](mcp-server/README.md)):
```json
{"mcpServers": {"uk-gov-standards": {"command": "python", "args": ["mcp-server/server.py"]}}}
```

## Modules

| Module | Standards | Focus |
|--------|-----------|-------|
| [core](modules/core/) | 41 | Security, ops, architecture, data, accessibility, AI |
| [python](modules/python/) | 10 | Python + Django + Flask |
| [java](modules/java/) | 8 | Java + Spring Boot |
| [typescript](modules/typescript/) | 8 | TypeScript + React + Node |
| [org-example](modules/org-example/) | 2 | Demonstrates custom org rules |

See [modules/README.md](modules/README.md) for how to create your own.

## Conformance and enforcement

| Conformance | Meaning |
|-------------|---------|
| **MUST** | Non-negotiable. Exceptions require an [exemption](docs/exemptions.md). |
| **SHOULD** | Expected unless justified. |
| **COULD** | Recommended. |

| Enforcement | When |
|-------------|------|
| **automated** | As you type (IDE) + every PR (CI/CD) |
| **peer-review** | During code review |
| **periodic-audit** | Service assessment / quarterly |
| **ways-of-working** | Team charter / runbooks |

## Documentation

| Document | What it covers |
|----------|---------------|
| [docs/usage-by-role.md](docs/usage-by-role.md) | Workflows per role (engineer, tech lead, security, delivery) |
| [docs/sources.md](docs/sources.md) | Source frameworks, synthesis methodology |
| [docs/versioning.md](docs/versioning.md) | Version policy, pinning, migration windows |
| [docs/testing.md](docs/testing.md) | Test strategy (49 tests) |
| [docs/exemptions.md](docs/exemptions.md) | Waiver process for MUST standards |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add a standard |
| [SECURITY.md](SECURITY.md) | Trust model, permissions, vulnerability reporting |
| [CHANGELOG.md](CHANGELOG.md) | Release history |

## Development

```bash
pip install -e ".[dev]"
pytest                                # 29 Python tests
cd vscode-extension && npm test       # 20 TypeScript tests
python scripts/validate_standards.py  # validate all standards
```

## Governance

All changes require a PR. CI must pass. 1 maintainer approval required.

| Control | Status |
|---------|--------|
| PR + CI + approval | ✅ Enforced |
| Force pushes | ❌ Blocked |
| Trusted sources gate | ✅ [allowlist](scripts/trusted_sources.yaml) |
| Versioned releases | ✅ [v1.1.0](https://github.com/bv90dsit/Engineering_standards/releases/tag/v1.1.0) |

See [docs/versioning.md](docs/versioning.md) for release policy.
