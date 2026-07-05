# Test Strategy

See also: [Main README](../README.md) | [CONTRIBUTING.md](../CONTRIBUTING.md)

## Overview

| Suite | Framework | Files | Tests | What it covers |
|-------|-----------|-------|-------|----------------|
| Python unit tests | pytest | `tests/` | 29 | Query library, validation, compliance checker, scaffold |
| VS Code extension tests | @vscode/test-electron | `vscode-extension/src/test/` | TBD | Rule engine, glob matching, diagnostics |
| Standards validation | Custom (`validate_standards.py`) | — | — | Format, traceability, trusted sources, orphans |

## Python tests (`tests/`)

### test_query.py (14 tests) — Query library

The query library (`standards_lib/`) powers every consumer. These tests verify:

| Area | What's tested | Why |
|------|--------------|-----|
| Loading | Index loads from modules, falls back to root | A broken loader crashes every tool |
| Module isolation | `module="python"` returns only python standards | Wrong results mislead teams about what applies |
| Filtering | conformance, category, tag, enforcement, combined | The onboarding tool, CLI, and CI all depend on accurate filtering |
| Error handling | Bad module name raises ValueError, missing ID raises FileNotFoundError | Clear errors vs silent wrong behaviour |
| Serialisation | `to_json()` produces valid JSON | Machine consumers need parseable output |

### test_validate.py (5 tests) — CI validation gate

These test the script that prevents broken standards from merging:

| Test | Why it exists |
|------|--------------|
| Passes on current repo | Regression — ensures we haven't broken our own standards |
| Catches missing frontmatter | Contributors get told what's wrong immediately |
| Catches orphans | Prevents "standard in index but file doesn't exist" |
| Catches untrusted source | The trusted sources gate actually works |
| Catches TODOs | Half-finished standards can't ship |

### test_check_compliance.py (6 tests) — Compliance checker

These test the tool that runs in consuming repos' CI:

| Test | Why it exists |
|------|--------------|
| ENG-001 pass/fail | Licence detection works both ways (no false positives, no misses) |
| ENG-003 pass | CI workflow detection works |
| SEC-001 pass | Doesn't flag clean code |
| SEC-002 pass/fail | Dependency scanner detection works both ways |

### test_new_standard.py (2 tests) — Scaffold command

| Test | Why it exists |
|------|--------------|
| Creates file + index | The "one command" promise works end-to-end |
| Duplicate ID fails | Prevents accidental overwrite |

## VS Code extension tests (`vscode-extension/src/test/`)

Tests the rule engine and glob matching logic that runs in the editor:

| Area | What's tested | Why |
|------|--------------|-----|
| Glob matching | `*`, `**`, `?`, `{a,b}`, character classes | A broken glob means rules fire on wrong files or miss violations |
| Rule loading | Valid rules.json parsed, invalid skipped with warning | Silent load failures mean no checks run |
| Rule execution | Patterns match expected lines, excludes work | False positives annoy engineers; false negatives miss violations |

## What's NOT unit tested (and why)

| Component | Why | How it's verified instead |
|-----------|-----|--------------------------|
| `onboarding.py` | Print formatter — if query library works, output is correct | Manual review |
| `release.py` | Does git operations | `--dry-run` flag |
| Individual standard content | Not code — it's prose | `validate_standards.py` checks structure |
| GitHub Actions workflows | Require GitHub runner | Triggered by test PRs |

## Running tests

```bash
# Python tests
pytest                           # all 29 tests
pytest tests/test_query.py       # just the query library
pytest -k "test_check_eng_001"   # one specific test

# VS Code extension tests
cd vscode-extension
npm test
```

## Adding tests

When adding a new feature:
- New query filter? → add a test in `test_query.py`
- New compliance check? → add pass/fail tests in `test_check_compliance.py`
- New validation rule? → add a test in `test_validate.py`
- New VS Code rule engine feature? → add a test in `vscode-extension/src/test/`
