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

## Enforcement mechanisms

Every standard specifies *how* compliance is verified — not just what the standard says.

| Mechanism | What it means | When it runs | Examples |
|-----------|---------------|--------------|----------|
| **automated** | Checked by CI/CD pipeline — file exists, pattern match, config present | Every PR | Licence file exists, CI workflow present, no secrets in code |
| **peer-review** | Checked by a human during code review | Every PR | Input validation, ADR written, AI code critically reviewed |
| **periodic-audit** | Checked at service assessment or quarterly review | Alpha/beta/live assessments, quarterly | Pen test evidence, DORA metrics, SLOs defined, DR tested |
| **ways-of-working** | Team practice documented in charter/runbooks | Ongoing | Incident process, tech debt allocation, pairing norms |

Standards can have multiple enforcement mechanisms. For example, SEC-001 (HTTPS) is both **automated** (grep for `http://` in CI) and **periodic-audit** (TLS configuration verified at security review).

### Compliance checker

Run the automated checks against any repository:

```bash
# Check a repo against all applicable standards
python scripts/check_compliance.py --repo-path /path/to/repo --role engineer

# Output as markdown (for GitHub Actions summaries)
python scripts/check_compliance.py --repo-path . --output markdown

# Use as a reusable GitHub Action in another repo
# .github/workflows/compliance.yml:
#   uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
#   with:
#     role: engineer
#     platform: python
```

Standards enforced via `periodic-audit` or `ways-of-working` are reported as "manual review required" — the pipeline flags them for human attention rather than attempting to automate a judgement call.

## Source traceability

Every standard traces back to at least one published framework:

- [Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice) (UK Gov, 13 points)
- [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard) (UK Gov, 14 points)
- [NCSC Secure by Design](https://www.ncsc.gov.uk/collection/developers-collection) (DSIT/NCSC)
- [DORA Metrics](https://dora.dev/) (Google, 4+1 metrics)
- [OWASP Top 10 / ASVS](https://owasp.org/www-project-application-security-verification-standard/) (Industry, security)
- ISO 27001, NIST, 12-Factor, WCAG, and others as referenced
