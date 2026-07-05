# Contributing

## Add a standard (one command)

```bash
python scripts/new_standard.py --id PY-011 --module python \
  --title "Your standard title" --conformance SHOULD
```

The scaffold handles everything:
- ✅ Creates the `.md` file with template
- ✅ Adds the index entry
- ✅ Adds row to module README
- ✅ Updates counts in all READMEs
- ✅ Asks about VS Code rule and adds it if yes

All you do after: **fill in the TODOs and open a PR.**

**Non-technical?** Use the [GitHub Issue form](https://github.com/bv90dsit/Engineering_standards/issues/new?template=new-standard.yml) — a bot creates the PR for you.

## Who does what

### Contributor (before opening PR)

| Task | Automated? | How |
|------|:---:|------|
| Create `.md` + index + module README row + counts | ✅ | Scaffold command does it |
| VS Code rule (if applicable) | ✅ | Scaffold asks and adds it |
| Fill in TODOs in the standard | ❌ | You write the content |
| CHANGELOG entry | ❌ | Note what you added (for next release) |
| Update sources graph (if new source framework) | ❌ | Edit `docs/sources-graph.md` JS arrays |
| Write tests (if code change) | ❌ | Add test in `tests/` or `vscode-extension/src/test/` |

### Reviewer (seeing the PR)

The **Impact Analysis** bot comments on every PR with a checklist. Reviewer verifies:

| Check | What to look for |
|-------|-----------------|
| ⚠ items done? | Counts updated, README rows added, index entry present |
| TODOs filled? | No placeholders left in the standard |
| Sources trusted? | URLs from domains in `trusted_sources.yaml` |
| Contradictions? | Does this overlap or conflict with an existing standard? |
| Enforcement realistic? | Can teams actually check this the way it claims? |
| Tests included? (code changes) | New function → new test |

### What's fully automatic (nobody does anything)

| What | When |
|------|------|
| All consumers discover the new standard | Immediately on merge (runtime) |
| VS Code extension rebuilds with new rules | On merge (CI workflow) |
| Version references update | At release (release script) |
| Impact analysis comment posted | On PR open (CI workflow) |

## VS Code rule (the scaffold asks)

The scaffold asks: "Can this be detected by regex on a single line?"

- **Yes:** `http://` URLs, `print()`, secrets, `@ts-ignore` → it collects the pattern and adds to `rules.json`
- **No:** architecture decisions, SLOs, team process → skip, enforcement is peer-review or audit

After merge, CI rebuilds the `.vsix` automatically.

## Testing requirements

| Change type | Tests required? | Where |
|-------------|:---:|-------|
| Standard + index entry | No | CI validates format |
| `rules.json` entry | No | Reviewed; engine is tested |
| New/changed Python function | **Yes** | `tests/test_*.py` |
| New/changed TypeScript logic | **Yes** | `vscode-extension/src/test/suite/*.test.ts` |
| CI workflow | No | PR itself tests it |

**Rule:** if you add or modify a function, add a test. CI warns (not blocks) if code changes without test changes.

## What CI checks

**Standards changes** (`modules/**`):
- Format validation (frontmatter, index match, enforcement section)
- Trusted sources (URLs must be in [trusted_sources.yaml](scripts/trusted_sources.yaml))
- No TODOs in source traceability
- README counts current

**Code changes** (`scripts/`, `standards_lib/`, `vscode-extension/`):
- Lint (ruff) + security (bandit)
- Unit tests (pytest + mocha)
- TypeScript compiles
- npm audit

Both must pass. 1 maintainer approval required.

## Local setup

```bash
pip install -e ".[dev]"
pytest                              # 29 Python tests
cd vscode-extension && npm test     # 20 TypeScript tests
ruff check scripts/ standards_lib/  # lint
python scripts/validate_standards.py  # validate standards
```

## Checklist

- [ ] `.md` file + index entry created (or use the scaffold command)
- [ ] Source traceability: 4-column format, URLs from [trusted sources](scripts/trusted_sources.yaml)
- [ ] `python scripts/validate_standards.py` passes
- [ ] `python scripts/update_counts.py` run and committed
- [ ] Tests added (if code changed)
- [ ] PR opened
