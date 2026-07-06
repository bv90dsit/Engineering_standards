# Test Strategy

See also: [Main README](../README.md) | [CONTRIBUTING.md](../CONTRIBUTING.md)

## Overview

| Suite | Framework | Files | What it covers |
|-------|-----------|-------|----------------|
| Python unit tests | pytest | `tests/` | Query library, validation, compliance checker, scaffold |
| Build pipeline tests | pytest | `tests/test_build_pipeline.py` | End-to-end: build → graph sync → skill |
| VS Code extension tests | mocha | `vscode-extension/src/test/suite/` | Glob matching, rule pattern matching |
| Standards validation | Custom (`validate_standards.py`) | — | Format, traceability, trusted sources, orphans |
| Graph sync check | Custom (`check_graph_sync.py`) | — | Graph data matches source traceability |

## Python tests (`tests/`)

### test_query.py — Query library

The query library (`standards_lib/`) powers every consumer. These tests verify:

| Area | What's tested | Why |
|------|--------------|-----|
| Loading | Index loads from modules, falls back to root | A broken loader crashes every tool |
| Module isolation | `module="python"` returns only python standards | Wrong results mislead teams about what applies |
| Filtering | conformance, category, tag, enforcement, combined | The onboarding tool, CLI, and CI all depend on accurate filtering |
| Error handling | Bad module name raises ValueError, missing ID raises FileNotFoundError | Clear errors vs silent wrong behaviour |
| Serialisation | `to_json()` produces valid JSON | Machine consumers need parseable output |

### test_validate.py — CI validation gate

These test the script that prevents broken standards from merging:

| Test | Why it exists |
|------|--------------|
| Passes on current repo | Regression — ensures we haven't broken our own standards |
| Catches missing frontmatter | Contributors get told what's wrong immediately |
| Catches orphans | Prevents "standard in index but file doesn't exist" |
| Catches untrusted source | The trusted sources gate actually works |
| Catches TODOs | Half-finished standards can't ship |

### test_check_compliance.py — Compliance checker detection logic

These test the compliance checker tool (`scripts/check_compliance.py`) that other teams run against their repos. They verify the checker's detection logic — not the standards themselves.

| Test class | What it verifies |
|------------|-----------------|
| `TestLicenceDetection` | Correctly identifies repos with/without a LICENCE file |
| `TestCIWorkflowDetection` | Correctly identifies repos with GitHub Actions workflows |
| `TestHTTPSDetection` | Correctly identifies repos free of plaintext HTTP URLs |
| `TestDependencyScannerDetection` | Correctly identifies repos with/without dependency scanning |

### test_new_standard.py — Scaffold command

| Test | Why it exists |
|------|--------------|
| Creates file + index | The "one command" promise works end-to-end |
| Duplicate ID fails | Prevents accidental overwrite |

## VS Code extension tests (`vscode-extension/src/test/suite/`)

### glob.test.ts — Glob matching

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

### rulePatterns.test.ts — Rule regex patterns

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

### test_build_pipeline.py — End-to-end build

Tests the full pipeline that CI and Pages deploy rely on:

| Test | What it proves | Why it matters |
|------|---------------|----------------|
| `validate_standards_passes` | All standards pass validation | Broken standards can't reach the site |
| `build_site_creates_standards` | `_standards/` directory is created | Pages has content to deploy |
| `build_site_copies_all_standards` | Output count matches source count | No standards silently dropped |
| `built_standards_have_required_frontmatter` | layout + render_with_liquid present | Jekyll renders them correctly |
| `built_standards_wrapped_in_raw` | Body wrapped in raw/endraw | Liquid syntax in code examples doesn't break the build |
| `graph_data_matches_traceability` | Graph nodes match actual sources | The visual graph is truthful |
| `skill_generates_without_error` | build_skill.py exits 0 | Skill generation isn't broken |
| `skill_output_exists` | .claude/skills/uk-gov-standards.md created | The file developers install actually exists |

---

## CI Pipelines

### What CI tests (automated on every PR)

| Workflow | Triggers on | What it checks |
|----------|------------|----------------|
| `ci-standards.yml` | modules/**, docs/sources-graph.md, scripts/ | Standard format validation, README counts, skill freshness, graph sync |
| `ci-code.yml` | scripts/**, tests/**, standards_lib/** | Python tests (pytest), linting |
| `compliance.yml` | PR to main | Compliance check against the standards themselves |
| `impact-analysis.yml` | modules/** | Reports which standards/pages are affected by the change |
| `pages.yml` | push to main | Build site + deploy to GitHub Pages |

### What CI does NOT test

| Gap | Why | Risk | Mitigation |
|-----|-----|------|------------|
| Jekyll HTML output | No Jekyll in CI unit tests; only the Pages workflow does a full build | Broken layouts or links | Pages workflow fails on build errors; visual check after deploy |
| Browser rendering | No visual regression testing | CSS/JS bugs on the live site | Manual check after significant page changes |
| MCP server integration | Requires a running Claude session | MCP tool calls could break | Unit tests for query library cover the data layer |
| VS Code extension in real editor | Mocha tests run without VS Code host | Extension activation or UI bugs | Manual testing + marketplace reviews |
| Cross-browser compatibility | No browser matrix | Layout issues on Safari/Firefox | GOV.UK design system is well-tested across browsers |
| Performance / load | No lighthouse or load tests | Slow pages | Static site with minimal JS; low risk |

---

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
pytest                           # all tests
pytest tests/test_query.py       # just the query library
pytest -k "test_repo_with_licence"  # one specific test

# VS Code extension tests
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
