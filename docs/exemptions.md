# Exemptions and Waivers

## When to request an exemption

MUST standards are non-negotiable by default. However, there are legitimate reasons a service may not be able to comply:

- Legacy system constraints (cannot be modified within the migration timeline)
- Third-party dependency that prevents compliance
- Conflicting regulatory requirement
- Temporary non-compliance during a phased migration

## How to document an exemption

Create an Architecture Decision Record (ADR) in your service's repo:

```markdown
# ADR-XXX: Exemption from [STANDARD-ID]

## Status: Accepted

## Context
[Why this service cannot comply with this specific standard]

## Decision
[What we are doing instead, and why it's an acceptable alternative]

## Compensating controls
[What mitigations are in place to manage the risk]

## Review date
[When this exemption will be reassessed — maximum 6 months]

## Approved by
[Name and role of the person accepting the risk]
```

## Rules

- Exemptions MUST be documented in an ADR (not verbal, not Slack, not email)
- Exemptions MUST have an expiry/review date (maximum 6 months)
- Exemptions MUST describe compensating controls
- Exemptions MUST be approved by a named individual who accepts the risk
- Exemptions are NOT blanket — they apply to one service, one standard, one reason
- The compliance checker will still report the standard as failed — the ADR is the evidence that the failure is known and accepted

## What is NOT an exemption

- "We didn't have time" — plan it into the next sprint
- "We don't agree with the standard" — propose a change via PR, don't bypass it
- "Nobody told us" — the onboarding tool and compliance checker surface everything

## Linking exemptions to standards

Reference the exemption in your compliance check output. When the checker reports a failure, the ADR is your evidence at service assessment that the gap is managed, not ignored.
