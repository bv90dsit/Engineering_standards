# UK Government Engineering Standards

A machine-readable, context-aware set of engineering standards for UK Government digital services.

## Architecture

![UK Government Engineering Standards — How It Works](docs/architecture.png)

Five layers from raw source material to the engineer at their desk:

### Layer status

| Layer | Component | Status | What exists |
|-------|-----------|--------|-------------|
| **0 — Source frameworks** | External published standards | ✅ Complete | Referenced in every standard's traceability table |
| **1 — Standard files** | `standards/*.md` | ✅ Complete (33) | 7 categories: ENG, SEC, ARC, OPS, DAT, ACC, EMG |
| **2 — Index file** | `standards-index.yaml` | ✅ Complete | All 33 entries with conformance, enforcement, applies_to, tags |
| **3 — Query interface** | `standards_lib/` | ✅ Built | Importable Python library + CLI with JSON output, enforcement filter |
| **4 — Consumers** | Tools calling the query layer | 🔶 Partial | See below |

### Layer 4 consumers — built vs planned

| Consumer | Status | Description |
|----------|--------|-------------|
| **CI/CD compliance checker** | ✅ Built | `scripts/check_compliance.py` — automated checks for all 33 standards |
| **Reusable GitHub Action** | ✅ Built | `.github/workflows/compliance.yml` — any repo can call it |
| **Onboarding tool** | ✅ Built | `scripts/onboarding.py` — "you just joined, here's what applies" |
| **Human reader** | ✅ Built | Browse on GitHub, README explains everything |
| **Compliance dashboard** | 🔲 Planned | Web view: all services × all standards = pass/fail matrix |
| **IDE plugin** | 🔲 Planned | Inline warnings (hardcoded secret, HTTP URL, missing tests) |
| **Slack/Teams bot** | 🔲 Planned | Query standards from chat ("what are the SEC standards for my Python service?") |

## Quick start

```bash
# Onboarding — "I just joined, what applies to me?"
python scripts/onboarding.py --role engineer --platform python

# Query all MUST standards
python scripts/query_standards.py --conformance MUST

# Query security standards only
python scripts/query_standards.py --category SEC

# Query what applies to a Python engineer
python scripts/query_standards.py --role engineer --platform python

# Query only standards enforced via CI/CD
python scripts/query_standards.py --enforcement automated

# Output as JSON (for programmatic consumers)
python scripts/query_standards.py --category SEC --json

# Check a repo's compliance
python scripts/check_compliance.py --repo-path /path/to/repo --role engineer

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

## Governance and contribution

> **Status: MVP / Draft.** This standards set is not yet adopted by any teams. It is being developed in the open for feedback and iteration.

### Current approval process (lightweight)

This is an early-stage project. The approval process is intentionally minimal to allow rapid iteration:

- **No PR approval required** — direct pushes to `main` are allowed for the sole maintainer
- **Force pushes blocked** — history is protected to maintain an audit trail
- **Branch deletions blocked** — prevents accidental loss

### When teams start adopting (planned)

Once this moves beyond MVP and teams begin referencing these standards, governance will tighten:

| Setting | Current (MVP) | Future (adopted) |
|---------|---------------|-------------------|
| PR required | No | Yes |
| Approvals needed | 0 | 2 |
| CI checks must pass | No | Yes (YAML lint, index consistency) |
| CODEOWNERS | None | Category owners (SEC → security team, etc.) |
| Dismiss stale reviews | No | Yes |
| Conversation resolution | No | Yes |
| Change communication | None | Changelog + notify consuming teams |

### Proposing a change

Even during MVP, the intent is:

1. Open an issue describing the change and why
2. Create a branch and PR (even if self-merging)
3. Give it 24 hours for async comment before merging

This creates a paper trail for when the governance review happens later.
