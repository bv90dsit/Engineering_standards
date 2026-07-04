# UK Government Engineering Standards

A machine-readable, context-aware set of engineering standards for UK Government digital services.

## Architecture

```
Layer 0 — Source frameworks (GDS Service Standard, NCSC, DORA, OWASP, etc.)
    ↓ synthesised into
Layer 1 — Individual standard files (one .md per standard, with frontmatter tags)
    ↓ catalogued in
Layer 2 — standards-index.yaml (lightweight index, always loaded)
    ↓ filtered by
Layer 3 — query_standards(context) → returns only what applies
    ↓ served to
Layer 4 — Consumers (CI/CD, onboarding, compliance checks, IDE plugins, humans)
```

## Quick start

```bash
# Query all MUST standards
python scripts/query_standards.py --conformance MUST

# Query security standards only
python scripts/query_standards.py --category SEC

# Query what applies to a Python engineer
python scripts/query_standards.py --role engineer --platform python

# Query AI-related standards
python scripts/query_standards.py --tag ai
```

## Adding a new standard

1. Create `standards/{ID}.md` with YAML frontmatter (see existing files for format)
2. Add a row to `standards-index.yaml`
3. That's it. No consumer changes needed.

## Standard ID scheme

| Prefix | Category |
|--------|----------|
| ENG | Engineering practice |
| SEC | Security |
| ARC | Architecture |
| OPS | Operations & reliability |
| EMG | Emerging technology (AI, etc.) |
| DAT | Data |
| ACC | Accessibility |

## Conformance levels (RFC 2119)

| Level | Meaning |
|-------|---------|
| MUST | Non-negotiable. Exceptions require a documented ADR. |
| SHOULD | Expected unless there is a justified reason to deviate. |
| COULD | Recommended good practice. |

## Source traceability

Every standard traces back to at least one published framework:

- [Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice) (UK Gov, 13 points)
- [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard) (UK Gov, 14 points)
- [NCSC Secure by Design](https://www.ncsc.gov.uk/collection/developers-collection) (DSIT/NCSC)
- [DORA Metrics](https://dora.dev/) (Google, 4+1 metrics)
- [OWASP Top 10 / ASVS](https://owasp.org/www-project-application-security-verification-standard/) (Industry, security)
- ISO 27001, NIST, 12-Factor, WCAG, and others as referenced
