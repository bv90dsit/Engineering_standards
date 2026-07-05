# UK Government Engineering Standards

Machine-readable, context-aware engineering standards for UK Government digital services. 55 standards across 5 modules, queryable by role, platform, and enforcement type.

> **Status: MVP / Draft** — not yet adopted by teams. Being developed in the open for feedback.

```
Layer 0 — Source frameworks (GDS, NCSC, DORA, OWASP, WCAG, etc.)
    ↓ synthesised into
Layer 1 — Individual standard files (one .md per standard, with frontmatter)
    ↓ catalogued in
Layer 2 — standards-index.yaml (lightweight, always loaded)
    ↓ filtered by
Layer 3 — query_standards(context) → returns only what applies
    ↓ served to
Layer 4 — Consumers (CI/CD, VS Code extension, onboarding, compliance checker)
```

See the [full architecture diagram](docs/architecture.png) for the visual version.

## Quick start

### 1. Install the VS Code extension (instant feedback)

Download the `.vsix` from the [latest release](https://github.com/bv90dsit/Engineering_standards/releases/latest), then:

```bash
code --install-extension uk-gov-engineering-standards-0.1.0.vsix
```

You'll get inline warnings as you type — `http://` URLs, hardcoded secrets, missing LICENCE/CI/README. See the [extension docs](vscode-extension/README.md) for full details.

### 2. Add the CI check to your service (2 minutes)

Add `.github/workflows/standards.yml` to your repo:

```yaml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1.0.0
    with:
      role: engineer
      platform: python   # or java, node, any
```

Every PR now checks compliance automatically.

### 3. See what applies to you

```bash
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards
pip install pyyaml

python scripts/onboarding.py --role engineer --platform python
```

This tells you which standards apply, how each is enforced, and what to do to comply. See [usage by role](docs/usage-by-role.md) for detailed workflows per role.

## What's in the box

| Layer | What | Status |
|-------|------|--------|
| Source frameworks | GDS, NCSC, DORA, OWASP, WCAG, etc. ([full list](docs/sources.md)) | ✅ Referenced |
| 55 standards | Across 5 modules ([browse modules](modules/README.md)) | ✅ Complete |
| Index | `standards-index.yaml` per module — lightweight, always loaded | ✅ Complete |
| Query library | `standards_lib/` — importable Python package + CLI | ✅ Built |
| CI/CD checker | `scripts/check_compliance.py` — automated + manual flags | ✅ Built |
| Reusable GitHub Action | `.github/workflows/compliance.yml` | ✅ Built |
| Onboarding tool | `scripts/onboarding.py` | ✅ Built |
| VS Code extension | [`vscode-extension/`](vscode-extension/README.md) — inline warnings as you type | ✅ Built |
| Test suite | `tests/` — 29 pytest tests covering query, validation, compliance, scaffold | ✅ Built |
| Compliance dashboard | Web view: services × standards matrix | 🔲 Planned |

## Modules

Standards are organised into pluggable modules. See [modules/README.md](modules/README.md) for how to create your own.

| Module | Standards | Focus |
|--------|-----------|-------|
| [core](modules/core/) | 33 | Cross-cutting UK Gov (security, ops, architecture, data, accessibility, AI) |
| [python](modules/python/) | 8 | Python + Django + Flask |
| [java](modules/java/) | 6 | Java + Spring Boot |
| [typescript](modules/typescript/) | 6 | TypeScript + React + Node |
| [org-example](modules/org-example/) | 2 | Demonstrates how an org adds custom rules |

```bash
python scripts/query_standards.py --list-modules
python scripts/query_standards.py --module python
python scripts/query_standards.py --module all
```

## Adding a new standard

**Quickest path** — one command scaffolds everything:

```bash
python scripts/new_standard.py --id PY-009 --module python \
  --title "Use virtual environments" --conformance SHOULD
```

**Non-technical contributors** — use the [GitHub Issue form](https://github.com/bv90dsit/Engineering_standards/issues/new?template=new-standard.yml) and a bot creates the PR.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, and [modules/README.md](modules/README.md) for the module structure.

## Categories

| Prefix | Category | Count |
|--------|----------|-------|
| ENG | Engineering practice | 6 |
| SEC | Security | 7 |
| ARC | Architecture | 5 |
| OPS | Operations & reliability | 5 |
| DAT | Data | 4 |
| ACC | Accessibility | 2 |
| EMG | Emerging technology (AI) | 4 |
| PY | Python / Django / Flask | 8 |
| JV | Java / Spring Boot | 6 |
| TS | TypeScript / React / Node | 6 |

## Conformance and enforcement

Each standard has a **conformance level** (how mandatory) and an **enforcement mechanism** (how it's checked):

| Conformance | Meaning |
|-------------|---------|
| **MUST** (28) | Non-negotiable. Exceptions require a documented ADR. |
| **SHOULD** (26) | Expected unless there is a justified reason to deviate. |
| **COULD** (1) | Recommended good practice. |

| Enforcement | When | Example standards |
|-------------|------|-------------------|
| **automated** | As you type (IDE) + every PR (CI/CD) | ENG-001, SEC-002, SEC-003, PY-001, JV-002, TS-001 |
| **peer-review** | During code review | SEC-004, ARC-004, EMG-001, PY-002, JV-004 |
| **periodic-audit** | Service assessment / quarterly | SEC-005, SEC-007, OPS-001, DAT-001 |
| **ways-of-working** | Team charter / runbooks | OPS-003, ENG-005, ENG-006 |

Standards marked `automated` are checked in two places — the VS Code extension (instant, as you type) and the CI pipeline (on every PR). Not all automated standards have IDE rules; those that do are listed in [modules/README.md](modules/README.md).

Standards can have multiple enforcement types. The compliance checker automates what it can and flags the rest for manual review.

## Source frameworks

Every standard traces back to at least one published framework. Key sources include:

- [Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice) — UK Gov
- [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard) — UK Gov
- [NCSC Secure by Design](https://www.ncsc.gov.uk/collection/developers-collection) — DSIT/NCSC
- [DORA Metrics](https://dora.dev/) — Google
- [OWASP Top 10 / ASVS](https://owasp.org/www-project-application-security-verification-standard/) — Industry
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — W3C

See [docs/sources.md](docs/sources.md) for the full list, synthesis methodology, and worked example.

## Documentation

| Document | What it covers |
|----------|---------------|
| [docs/usage-by-role.md](docs/usage-by-role.md) | Workflows for engineers, tech leads, delivery managers, security leads |
| [docs/sources.md](docs/sources.md) | All source frameworks, how standards are synthesised, traceability template |
| [modules/README.md](modules/README.md) | How to create and use modules |
| [vscode-extension/README.md](vscode-extension/README.md) | VS Code extension install and configuration |
| [docs/versioning.md](docs/versioning.md) | Version policy, pinning, migration windows |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [docs/testing.md](docs/testing.md) | Test strategy, what's covered, how to add tests |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add a standard (CLI scaffold, Issue form, CI checks) |

## Development

```bash
# Install (with dev tools)
pip install -e ".[dev]"    # or: pip install -r requirements-dev.txt

# Run tests
pytest

# Lint
ruff check scripts/ standards_lib/

# Validate all standards
python scripts/validate_standards.py

# Pre-commit hooks (optional, runs on every commit)
pip install pre-commit && pre-commit install
```

## Governance

**All changes require a PR.** Direct pushes to `main` are blocked.

### CI pipelines (run automatically on PRs)

| Pipeline | Triggers on | What it checks |
|----------|-------------|----------------|
| **CI — Standards** | `modules/**` | Format validation, trusted sources, source traceability completeness, README counts |
| **CI — Code** | `scripts/`, `standards_lib/`, `vscode-extension/` | Lint (ruff), security scan (bandit), type check (tsc), npm audit |

Both must pass before merge. A PR touching both standards and code triggers both pipelines.

### Merge requirements

| Control | Status |
|---------|--------|
| PR required | ✅ Enforced |
| CI must pass | ✅ Enforced |
| 1 maintainer approval | ✅ Required |
| Force pushes | ❌ Blocked |
| Branch deletions | ❌ Blocked |
| Conversations resolved | ✅ Required |

### Trusted sources

Source traceability URLs are validated against an [allowlist](scripts/trusted_sources.yaml). Adding a new source domain requires updating this file — which itself goes through PR review.

### Versioning

Standards are released as tagged versions. Teams pin to a version and upgrade on their own schedule.

```yaml
# Pin to a specific version
uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1.0.0
```

| Version bump | What changed | Teams must act? |
|:---:|-------------|:---:|
| **Major** (v2.0.0) | New MUST standard or breaking change | Yes (12-week window) |
| **Minor** (v1.1.0) | New SHOULD/COULD, new module, refinements | No |
| **Patch** (v1.0.1) | Typos, URL fixes, docs | No |

See [docs/versioning.md](docs/versioning.md) for the full policy and [CHANGELOG.md](CHANGELOG.md) for release history.

### Future

| Setting | Status |
|---------|--------|
| CODEOWNERS per category | Planned |
| 2 approvals | When more maintainers join |
