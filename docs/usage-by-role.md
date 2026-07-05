# Usage by Role

How different roles interact with the engineering standards. See also:
- [Main README](../README.md) — quick start and architecture overview
- [Modules](../modules/README.md) — how to add language or org-specific standards
- [Sources](sources.md) — where standards come from and how they're synthesised
- [VS Code extension](../vscode-extension/README.md) — instant feedback in your editor

## Engineer

### Adopt the standards

Add one workflow file to your service repo. The standards are pulled at runtime:

```yaml
# .github/workflows/standards.yml
jobs:
  compliance:
    uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1.1.0
    with:
      role: engineer
      platform: python   # or java, node, etc.
```

Every PR now checks compliance automatically.

### See what applies and how to comply

```bash
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards && pip install pyyaml
python scripts/onboarding.py --role engineer --platform python
```

### Check locally before pushing

```bash
python scripts/check_compliance.py --repo-path /path/to/your-service
```

### What the automated checks look for

| Check | What to do to pass |
|-------|-------------------|
| ENG-001 | Add a `LICENCE` file (MIT or OGL v3) |
| ENG-003 | Have a CI workflow in `.github/workflows/` |
| SEC-001 | No `http://` URLs in source code |
| SEC-002 | Add `.github/dependabot.yml` or equivalent |
| SEC-003 | Add secret scanning (detect-secrets or GitHub secret scanning) |
| ENG-004 | Have a `README.md` with more than 10 lines |

---

## Tech Lead

### Set up CI enforcement + get the standard list for your team

```bash
# JSON output for dashboards, wikis, or team onboarding docs
python scripts/query_standards.py --role engineer --platform python --json

# What blocks PRs vs what needs team agreement
python scripts/query_standards.py --enforcement automated --conformance MUST
python scripts/query_standards.py --enforcement ways-of-working
```

---

## Delivery Manager

### Assessment evidence checklist

```bash
python scripts/query_standards.py --conformance MUST --enforcement periodic-audit
```

Each standard file has a "What good looks like" section — use as evidence criteria.

### Compliance report for a service

```bash
python scripts/check_compliance.py --repo-path /path/to/service --output markdown
```

Paste into your assessment deck. "Manual review" items are what assessors will ask about.

---

## Security Lead

```bash
python scripts/query_standards.py --category SEC
```

| Automated (CI) | Periodic audit (you review) |
|---------------|----------------------------|
| SEC-001 HTTPS everywhere | SEC-005 OAuth2/OIDC auth |
| SEC-002 Dependency scanning | SEC-007 Annual pen test |
| SEC-003 No secrets in code | |
| SEC-004 Input validation (SAST) | |
| SEC-006 Container scanning | |

---

## Head of Engineering

```bash
# Tooling investment vs coaching investment
python scripts/query_standards.py --enforcement automated
python scripts/query_standards.py --enforcement ways-of-working

# Audit a specific service
python scripts/check_compliance.py --repo-path ../service-x --output markdown
```

---

## Machine consumer (CI/CD, dashboards)

```python
from standards_lib import query_standards

standards = query_standards(
    conformance="MUST",
    enforcement="automated",
    platform="python"
)
```

Or use the reusable GitHub Action — it checks out the standards repo at runtime, runs the compliance script, and writes the report to the step summary.
