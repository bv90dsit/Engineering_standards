# Contributing a Standard

## How propagation works

Adding a standard = one `.md` file + one index row. Everything else picks it up automatically because consumers read the index at runtime.

| Consumer | How it discovers your new standard | When |
|----------|-----------------------------------|------|
| `standards_lib` (query library) | Reads `standards-index.yaml` at runtime | Next function call |
| `query_standards.py` / `onboarding.py` | Call the library | Next run |
| `check_compliance.py` | Loads index → no automated check exists → reports "manual review required" | Next run |
| VS Code extension | Reads `rules.json` at activation | Next VS Code restart (if you added a rule) |
| GitHub Action (consuming repos) | Checks out this repo at runtime → gets latest | Next PR in the consuming repo |
| README counts | `update_counts.py` regenerates from the index | You run it before PR; CI verifies |

**You do NOT need to:**
- Modify any Python code in `standards_lib/`
- Update the compliance checker source
- Rebuild the VS Code extension
- Manually edit README counts (the script does it)

The only things that require manual work beyond the standard file + index entry:
- **VS Code line-level check** — add a `rules.json` entry (only if the standard is detectable by regex)
- **New source framework** — add to `docs/sources.md` (only if citing a framework not already listed)

## Steps to add a new standard

### 1. Choose your module

| If the standard is... | Add it to |
|----------------------|-----------|
| Cross-cutting (any language/platform) | `modules/core/` |
| Python/Django/Flask specific | `modules/python/` |
| Java/Spring Boot specific | `modules/java/` |
| TypeScript/React/Node specific | `modules/typescript/` |
| Your org's custom rule | Your own module (see [modules/README.md](modules/README.md)) |

### 2. Create the standard file

Create `modules/{module}/standards/{ID}.md`:

```markdown
---
id: SEC-008
title: Your standard title
conformance: MUST
category: SEC
applies_to:
  role: any
  platform: any
source: the-source-framework
tags: [relevant, tags, here]
last_reviewed: 2026-07-05
---

# SEC-008: Your standard title

## Standard

What MUST/SHOULD/COULD be done. One clear statement.

## Rationale

Why this matters (2-4 bullet points).

## What good looks like

Concrete examples of compliance.

## Enforcement

| Mechanism | What is checked | When |
|-----------|----------------|------|
| **Automated (CI/CD)** | ... | Every PR |

**Primary enforcement: ...**

## Source traceability

| Framework | Reference | URL | What it says |
|-----------|-----------|-----|--------------|
| Source 1 | Clause X | https://... | "Quote or paraphrase" |
```

### 3. Add the index entry

Add to `modules/{module}/standards-index.yaml`:

```yaml
  - id: SEC-008
    title: Your standard title
    conformance: MUST
    enforcement: [automated]
    applies_to:
      role: any
      platform: any
    category: SEC
    source: the-source-framework
    tags: [relevant, tags, here]
```

### 4. (Optional) Add a VS Code rule

If the standard can be detected by a regex pattern on a single line, add to `modules/{module}/rules.json`:

```json
{
  "id": "SEC-008",
  "pattern": "regex to match violations",
  "excludePattern": "^\\s*(#|//)",
  "filePattern": "**/*.py",
  "excludeFilePattern": "**/test_*",
  "severity": "error",
  "message": "SEC-008: Explanation of what's wrong and what to do instead."
}
```

### 5. Update counts

```bash
python scripts/update_counts.py
```

This updates the hardcoded counts in README.md and modules/README.md.

### 6. Validate

```bash
python scripts/validate_standards.py
```

This checks your standard has:
- Valid YAML frontmatter with all required fields
- A matching index entry (no orphans either way)
- Source traceability in the 4-column format
- An Enforcement section

### 7. Open a PR

CI runs both validation and count checks automatically. If either fails, fix and push again.

## Checklist

- [ ] Standard file created with all sections
- [ ] Index entry added with all required fields
- [ ] Source traceability uses 4-column format with URLs
- [ ] `python scripts/validate_standards.py` passes
- [ ] `python scripts/update_counts.py` run and changes committed
- [ ] (Optional) `rules.json` entry for VS Code extension
