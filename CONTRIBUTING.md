# Contributing

## Add a standard (one command)

```bash
python scripts/new_standard.py --id PY-011 --module python \
  --title "Your standard title" --conformance SHOULD
```

This creates the `.md` file, adds the index entry, updates counts, and asks whether to add a VS Code rule. Fill in the TODOs and open a PR.

**Non-technical?** Use the [GitHub Issue form](https://github.com/bv90dsit/Engineering_standards/issues/new?template=new-standard.yml) — a bot creates the PR for you.

## What happens automatically

| What | How | When |
|------|-----|------|
| All consumers discover the new standard | Read index at runtime | Immediately on merge |
| README counts update | `update_counts.py` (you run it; CI verifies) | Before PR |
| VS Code extension rebuilds | CI workflow on rules.json change | On merge |
| Version references stay current | `update_counts.py` updates @vX.Y.Z | At release |

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
