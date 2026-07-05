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

## Two ways to contribute

### Option A: CLI scaffold (for engineers)

One command generates everything:

```bash
python scripts/new_standard.py --id PY-009 --module python \
  --title "Use virtual environments" --conformance SHOULD
```

This creates the `.md` template, adds the index entry, and updates README counts. You just fill in the TODOs and open a PR.

Optional arguments: `--category`, `--enforcement`, `--platform`, `--tags`.

### Option B: GitHub Issue form (for anyone)

1. Go to **Issues → New Issue → "Propose a new standard"**
2. Fill in the form (title, conformance, rationale, sources)
3. Submit — a bot creates a PR with scaffolded files automatically
4. A maintainer fills in the detail and merges

Use this path if you're proposing a standard but not writing the implementation yourself (e.g. a security lead, delivery manager, or architect).

---

## Manual steps (if not using the scaffold)

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

When your PR merges, the **Build VS Code Extension** workflow automatically rebuilds the `.vsix` and uploads it to the latest release. No manual packaging needed.

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

All changes go through PRs — direct pushes to `main` are blocked.

## What CI checks on your PR

Two pipelines run based on what your PR touches:

### Standards changes (`modules/**`)

| Check | What it does | Common failure |
|-------|-------------|----------------|
| Format validation | Frontmatter has all required fields, index matches files | Missing `last_reviewed` or `enforcement` field |
| Trusted sources | Every URL in source traceability matches [trusted_sources.yaml](scripts/trusted_sources.yaml) | Citing a domain not in the allowlist |
| Traceability completeness | No TODOs or blanks in the 4-column table | Left a placeholder unfilled |
| Counts up to date | README numbers match actual standard count | Forgot to run `update_counts.py` |

### Code changes (`scripts/`, `standards_lib/`, `vscode-extension/`)

| Check | What it does | Common failure |
|-------|-------------|----------------|
| Lint (ruff) | Python code style and errors | Unused import, line too long |
| Security (bandit) | Python SAST scan | Hardcoded password, insecure function |
| Type check (tsc) | TypeScript compiles cleanly | Type error in extension code |
| npm audit | Known vulnerabilities in JS dependencies | Outdated dependency with CVE |

**Both must pass and 1 maintainer must approve before merge.**

### Adding a new trusted source

If your standard cites a source from a domain not in `scripts/trusted_sources.yaml`, add the domain to that file in the same PR. The domain addition itself gets reviewed — this is intentional; it prevents arbitrary websites being cited as authority.

## Local development setup

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests (29 tests covering query, validation, compliance, scaffold)
pytest

# Lint
ruff check scripts/ standards_lib/

# Pre-commit hooks (validates standards on every commit to modules/)
pip install pre-commit && pre-commit install
```

## Checklist

- [ ] Standard file created with all sections
- [ ] Index entry added with all required fields
- [ ] Source traceability uses 4-column format with URLs from [trusted sources](scripts/trusted_sources.yaml)
- [ ] `python scripts/validate_standards.py` passes locally
- [ ] `python scripts/update_counts.py` run and changes committed
- [ ] `pytest` passes (if you changed code in `scripts/` or `standards_lib/`)
- [ ] (Optional) `rules.json` entry for VS Code extension
- [ ] PR opened — CI runs automatically
