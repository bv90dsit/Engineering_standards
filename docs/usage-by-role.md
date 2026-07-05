# Usage by Role

How different users interact with the engineering standards.

## Engineer (day-to-day coding)

```bash
# Day 1: "I just joined, what do I need to know?"
python scripts/onboarding.py --role engineer --platform python

# Before raising a PR: "Will this pass?"
python scripts/check_compliance.py --repo-path .
```

Sees 33 standards grouped by MUST/SHOULD/COULD, with enforcement types so they know what's automated vs what's on them. Fixes issues before review rather than getting bounced.

## Tech Lead (setting up a new service)

```bash
# "What standards apply to my new Python service?"
python scripts/query_standards.py --role engineer --platform python --json
```

Gets the full list in JSON to wire into their CI pipeline:

```yaml
# .github/workflows/ci.yml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
    with:
      role: engineer
      platform: python
```

Every PR now runs the compliance check automatically.

## Delivery Manager / Service Owner (at assessment)

```bash
# "Show me what's MUST and how we prove it"
python scripts/query_standards.py --conformance MUST --enforcement periodic-audit
```

Gets the list of things assessors will ask about. Each standard file has a "What good looks like" section to use as evidence criteria.

## Security Lead

```bash
# "What's the security baseline?"
python scripts/query_standards.py --category SEC
```

7 standards with clear enforcement. Knows which are automated (SEC-002, SEC-003, SEC-006) vs which need pen test evidence (SEC-007) or architecture review (SEC-005).

## Head of Engineering / Principal Technologist

```bash
# "What's enforceable via pipeline vs what relies on culture?"
python scripts/query_standards.py --enforcement automated
python scripts/query_standards.py --enforcement ways-of-working

# "How compliant is service X?"
python scripts/check_compliance.py --repo-path ../service-x --output markdown
```

Sees the split: automated standards vs those that depend on team culture. That's where to focus tooling investment vs coaching.

## New contractor / Supplier

Lands on the GitHub repo → reads the README → sees the diagram → runs the onboarding command. Within 10 minutes they know what's mandatory, how each standard is enforced, and where to find detail.

## CI/CD pipeline (machine consumer)

```python
from standards_lib import query_standards, to_json

standards = query_standards(
    conformance="MUST",
    enforcement="automated",
    platform="python"
)
```

Returns structured data — no parsing needed.
