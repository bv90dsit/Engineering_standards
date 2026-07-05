# Test Strategy

See also: [Main README](../README.md) | [CONTRIBUTING.md](../CONTRIBUTING.md)

## Overview

| Suite | Framework | Files | Tests | What it covers |
|-------|-----------|-------|-------|----------------|
| Python unit tests | pytest | `tests/` | 29 | Query library, validation, compliance checker, scaffold |
| VS Code extension tests | mocha | `vscode-extension/src/test/suite/` | 20 | Glob matching, rule pattern matching |
| Standards validation | Custom (`validate_standards.py`) | — | — | Format, traceability, trusted sources, orphans |
| **Total** | | | **49** | |

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

## VS Code extension tests (`vscode-extension/src/test/suite/`)

### glob.test.ts (12 tests) — Glob matching

The glob logic is extracted into `src/glob.ts` (pure function, no VS Code dependency) so it can be tested directly with mocha — no electron runner needed.

| Test | What it proves | Why it matters |
|------|---------------|----------------|
| `* matches filename` | `*.py` matches `file.py` | Basic pattern matching works |
| `* does not match path separators` | `*.py` doesn't match `src/file.py` | Prevents overly broad matches |
| `** matches any depth` | `**/*.tsx` matches at any nesting | Deep paths get checked |
| `** with directory prefix` | `src/**/*.ts` only matches under src/ | Module-scoped rules don't leak |
| `brace expansion {a,b}` | `*.{ts,tsx}` matches both extensions | Multi-extension patterns from rules.json work |
| `brace expansion in path` | Works with `**` together | Real-world patterns like `**/*.{py,js,ts}` |
| `? matches single character` | `file?.py` matches `file1.py` not `file12.py` | Single-char wildcards work |
| `dots are escaped` | `*.py` doesn't match `filexpy` | Dot is literal, not regex `.` |
| `exclude patterns` | `**/*.test.*` matches test files | Exclusion patterns correctly identify test files |
| `real-world patterns` | Patterns from actual rules.json files | Integration check against the rules we ship |
| `test file exclusion` | `**/test_*` matches pytest files | Python test exclusions work |
| `tsconfig pattern` | `**/tsconfig*.json` matches variants | TS-001 check fires on the right files |

### rulePatterns.test.ts (8 tests) — Rule regex patterns

Tests the actual regex patterns from `modules/*/rules.json` to verify they match what they should and don't false-positive:

| Test | What it proves | Why it matters |
|------|---------------|----------------|
| `SEC-001: http:// URLs` | Matches `http://example.com`, skips `http://localhost` | Core check — no false positives on dev URLs |
| `SEC-003: passwords` | Matches `password = "long_secret"`, skips short/env-based | Doesn't flag every use of the word "password" |
| `SEC-003: AWS keys` | Matches `AKIA` + 16 chars pattern | Catches real AWS key format |
| `PY-001: print()` | Matches `print(`, skips `fingerprint` | Word boundary prevents false match on "print" substring |
| `PY-004: wildcard imports` | Matches `from x import *` | Catches the anti-pattern |
| `JV-002: System.out` | Matches println/print on out/err | Java logging check works |
| `TS-002: any type` | Matches `: any` annotation | TypeScript type safety check works |
| `exclude patterns` | Comment lines skipped | Rules don't fire inside comments |

## What's NOT unit tested (and why)

| Component | Why | How it's verified instead |
|-----------|-----|--------------------------|
| `onboarding.py` | Print formatter — if query library works, output is correct | Manual review |
| `release.py` | Does git operations | `--dry-run` flag |
| Individual standard content | Not code — it's prose | `validate_standards.py` checks structure |
| GitHub Actions workflows | Require GitHub runner | Triggered by test PRs |

## Running tests

```bash
# Python tests (29 tests, ~3s)
pytest                           # all tests
pytest tests/test_query.py       # just the query library
pytest -k "test_check_eng_001"   # one specific test

# VS Code extension tests (20 tests, <1s)
cd vscode-extension
npm test                         # runs mocha on compiled output

# Both from repo root
pytest && (cd vscode-extension && npm test)
```

## Adding tests

When adding a new feature:
- New query filter? → add a test in `test_query.py`
- New compliance check? → add pass/fail tests in `test_check_compliance.py`
- New validation rule? → add a test in `test_validate.py`
- New VS Code rule engine feature? → add a test in `vscode-extension/src/test/`
