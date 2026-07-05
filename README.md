# UK Government Engineering Standards

Machine-readable, context-aware engineering standards for UK Government digital services. 33 standards across 7 categories, queryable by role, platform, and enforcement type.

> **Status: MVP / Draft** — not yet adopted by teams. Being developed in the open for feedback.

![UK Government Engineering Standards — How It Works](docs/architecture.png)

## Quick start

### Add standards checking to your service (2 minutes)

Add this file to your service repo at `.github/workflows/standards.yml`:

```yaml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
    with:
      role: engineer
      platform: python   # or java, node, any
```

Every PR now checks compliance automatically. That's the whole integration.

### Explore the standards locally

```bash
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards
pip install pyyaml

# See what applies to you and how to comply
python scripts/onboarding.py --role engineer --platform python

# Check a repo's compliance
python scripts/check_compliance.py --repo-path /path/to/your-service

# Query standards
python scripts/query_standards.py --conformance MUST
python scripts/query_standards.py --category SEC --json
python scripts/query_standards.py --enforcement automated
```

See [docs/usage-by-role.md](docs/usage-by-role.md) for detailed workflows per role.

## What's in the box

| Layer | What | Status |
|-------|------|--------|
| Source frameworks | GDS Service Standard, NCSC, DORA, OWASP, WCAG, etc. | ✅ Referenced |
| 33 standard files | `standards/*.md` — one per standard with frontmatter | ✅ Complete |
| Index | `standards-index.yaml` — lightweight, always loaded | ✅ Complete |
| Query library | `standards_lib/` — importable Python package + CLI | ✅ Built |
| CI/CD checker | `scripts/check_compliance.py` — automated + manual flags | ✅ Built |
| Reusable GitHub Action | `.github/workflows/compliance.yml` | ✅ Built |
| Onboarding tool | `scripts/onboarding.py` | ✅ Built |
| Compliance dashboard | Web view: services × standards matrix | 🔲 Planned |
| VS Code extension | `vscode-extension/` — inline warnings as you type | ✅ Built |

## Who uses this and how

| Role | Primary tool | What they get |
|------|-------------|---------------|
| Engineer | `onboarding.py`, `check_compliance.py` | Know what applies, fix before PR |
| Tech Lead | GitHub Action, `--json` output | Automated enforcement on every PR |
| Delivery Manager | `--conformance MUST --enforcement periodic-audit` | Assessment evidence checklist |
| Security Lead | `--category SEC` | Security baseline with clear enforcement split |
| Head of Engineering | `--enforcement automated` vs `ways-of-working` | Where to invest in tooling vs coaching |
| Contractor | README + onboarding | Up to speed in 10 minutes |
| Pipeline (machine) | `from standards_lib import query_standards` | Structured data, no parsing |

See [docs/usage-by-role.md](docs/usage-by-role.md) for full examples per role.

## Adding a new standard

1. Create `standards/{ID}.md` with YAML frontmatter
2. Add one row to `standards-index.yaml`
3. Done. No consumer changes needed.

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

## Conformance and enforcement

Each standard has a **conformance level** (how mandatory) and an **enforcement mechanism** (how it's checked):

| Conformance | Meaning |
|-------------|---------|
| **MUST** (18) | Non-negotiable. Exceptions require a documented ADR. |
| **SHOULD** (14) | Expected unless there is a justified reason to deviate. |
| **COULD** (1) | Recommended good practice. |

| Enforcement | When | Example standards |
|-------------|------|-------------------|
| **automated** | Every PR via CI/CD | ENG-001, ENG-003, SEC-002, SEC-003 |
| **peer-review** | During code review | SEC-004, ARC-004, EMG-001 |
| **periodic-audit** | Service assessment / quarterly | SEC-005, SEC-007, OPS-001, DAT-001 |
| **ways-of-working** | Team charter / runbooks | OPS-003, ENG-005, ENG-006 |

Standards can have multiple enforcement types. The compliance checker automates what it can and flags the rest for manual review.

## Using the compliance checker

```bash
# Terminal output
python scripts/check_compliance.py --repo-path . --role engineer

# Markdown (for GitHub Actions step summary)
python scripts/check_compliance.py --repo-path . --output markdown
```

As a reusable GitHub Action in another repo:

```yaml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
    with:
      role: engineer
      platform: python
```

## Source frameworks

Every standard traces back to at least one published framework:

- [Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice) — UK Gov
- [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard) — UK Gov
- [NCSC Secure by Design](https://www.ncsc.gov.uk/collection/developers-collection) — DSIT/NCSC
- [DORA Metrics](https://dora.dev/) — Google
- [OWASP Top 10 / ASVS](https://owasp.org/www-project-application-security-verification-standard/) — Industry
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — W3C
- [UK GDPR](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/) — ICO
- ISO 27001, NIST, 12-Factor, and others as referenced per standard

## Governance

**Current (MVP):** Direct pushes to `main` allowed. Force pushes and branch deletions blocked.

**When teams adopt:**

| Setting | Now | Future |
|---------|-----|--------|
| PR required | No | Yes |
| Approvals | 0 | 2 |
| CI checks | No | YAML lint + index consistency |
| CODEOWNERS | None | Per-category owners |

Even during MVP: open an issue, create a PR (even if self-merging), give 24 hours for async comment.
