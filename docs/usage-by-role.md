# Usage by Role

How different users interact with the engineering standards.

## Engineer (day-to-day coding)

### Day 1: Adopt the standards in your service

You don't install anything into your repo. You add one workflow file that pulls the standards at check time:

```yaml
# Add to YOUR repo: .github/workflows/standards.yml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
    with:
      role: engineer
      platform: python   # or java, node, etc.
```

That's it. Every PR now checks your repo against the applicable standards.

### Day 1: See what applies to you

```bash
# Clone the standards repo (read-only — you don't commit here)
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards
pip install pyyaml

# See your personalised onboarding
python scripts/onboarding.py --role engineer --platform python
```

This shows you:
- Which standards block your PR (automated checks)
- What reviewers will look for (peer-review standards)
- What you'll need at service assessment (periodic-audit standards)
- What to agree as a team (ways-of-working standards)

### Before raising a PR

```bash
# Run the compliance check against your service repo
python scripts/check_compliance.py --repo-path /path/to/your-service
```

Fix any failures before pushing. The same check runs in CI, so catching it locally saves a round-trip.

### What the automated checks actually look for

| Check | What to do to pass |
|-------|-------------------|
| ENG-001 | Add a `LICENCE` file (MIT or OGL v3) to your repo root |
| ENG-003 | Have at least one CI workflow in `.github/workflows/` |
| SEC-001 | No `http://` URLs in source code (use `https://`) |
| SEC-002 | Add `.github/dependabot.yml` or configure Snyk/Renovate |
| SEC-003 | Add secret scanning (detect-secrets in pre-commit, or enable GitHub secret scanning) |
| ENG-004 | Have a `README.md` with more than 10 lines |

---

## Tech Lead (setting up a new service)

### Wire standards into CI from the start

```yaml
# .github/workflows/standards.yml in your new service repo
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
    with:
      role: engineer
      platform: python
```

### Get the full list for your platform as JSON

```bash
python scripts/query_standards.py --role engineer --platform python --json
```

Use this to feed into dashboards, wikis, or onboarding docs specific to your team.

### Check what's automated vs what needs team process

```bash
# These will block PRs:
python scripts/query_standards.py --enforcement automated --conformance MUST

# These need team agreements:
python scripts/query_standards.py --enforcement ways-of-working
```

---

## Delivery Manager / Service Owner (at assessment)

### Get your assessment evidence checklist

```bash
# "What will assessors ask about?"
python scripts/query_standards.py --conformance MUST --enforcement periodic-audit
```

Each standard file has a **"What good looks like"** section — use that as your evidence criteria.

### Generate a compliance report for your service

```bash
python scripts/check_compliance.py --repo-path /path/to/service --output markdown
```

Paste the markdown output into your assessment deck. Standards flagged as "manual review" are the ones you need to provide evidence for.

---

## Security Lead

### See the full security baseline

```bash
python scripts/query_standards.py --category SEC
```

7 standards. The enforcement column tells you which you can verify automatically vs which need pen test evidence or architecture review:

| Automated (CI catches it) | Periodic audit (you review it) |
|--------------------------|-------------------------------|
| SEC-001 HTTPS everywhere | SEC-005 OAuth2/OIDC auth |
| SEC-002 Dependency scanning | SEC-007 Annual pen test |
| SEC-003 No secrets in code | |
| SEC-004 Input validation (SAST) | |
| SEC-006 Container scanning | |

---

## Head of Engineering / Principal Technologist

### Understand the tooling vs culture split

```bash
# What can be enforced by machines:
python scripts/query_standards.py --enforcement automated

# What relies on team culture:
python scripts/query_standards.py --enforcement ways-of-working
```

This tells you where to invest in **tooling** (automated) vs **coaching and community of practice** (ways-of-working).

### Audit a specific service

```bash
python scripts/check_compliance.py --repo-path ../service-x --output markdown
```

### See cross-cutting standards (apply everywhere)

```bash
python scripts/query_standards.py --conformance MUST --json | python -m json.tool
```

---

## New contractor / Supplier

1. Land on the [GitHub repo](https://github.com/bv90dsit/Engineering_standards)
2. Read the README — the diagram explains the architecture in 15 seconds
3. Clone and run onboarding:

```bash
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards
pip install pyyaml
python scripts/onboarding.py --role engineer --platform python
```

Within 10 minutes you know what's mandatory, how each standard is enforced, and what to add to your repo.

---

## CI/CD pipeline (machine consumer)

### Import as a Python library

```python
from standards_lib import query_standards, to_json

# Get only automated MUST standards for this platform
standards = query_standards(
    conformance="MUST",
    enforcement="automated",
    platform="python"
)

# Returns structured data — no parsing needed
for s in standards:
    print(f"{s['id']}: {s['title']}")
```

### Use the reusable GitHub Action

```yaml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@main
    with:
      role: engineer
      platform: python
```

The action checks out both the target repo and the standards repo, runs the compliance script, and writes the report to the GitHub Actions step summary.
