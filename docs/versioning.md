# Versioning Policy

## How versions work

Standards are released as tagged versions (e.g. `v1.0.0`). Teams pin to a version and upgrade on their own schedule.

### Semantic versioning for standards

| Change type | Version bump | Teams must act? | Migration window |
|-------------|:---:|:---:|:---:|
| New MUST standard added | **Major** (v2.0.0) | Yes — new requirement | 12 weeks |
| Breaking change to existing MUST | **Major** | Yes — may need code/process changes | 12 weeks |
| New SHOULD/COULD standard | **Minor** (v1.1.0) | No — advisory only | — |
| New module added | **Minor** | No — opt-in | — |
| Non-breaking refinement to existing standard | **Minor** | No — wording clearer, same intent | — |
| Typo, URL fix, documentation | **Patch** (v1.0.1) | No — zero compliance impact | — |

### Migration windows

When a major version is released:
1. Release notes document exactly what changed and what teams need to do
2. Teams have **12 weeks** to migrate from the previous major version
3. The previous version remains valid during the window
4. After the window, the old version is deprecated (still functional, but new assessments use the new version)

## How teams pin to a version

### GitHub Action

```yaml
# Pin to a specific version
uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1.0.0

# Track latest minor/patch within a major (get refinements automatically)
uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1
```

### VS Code extension

Each release includes a `.vsix` tagged to the version. Teams install the version they've assessed against.

### CLI tools

```bash
# Clone a specific version
git clone --branch v1.0.0 https://github.com/bv90dsit/Engineering_standards.git
```

## How compliance is stated

Teams reference the version they comply with:

> "This service complies with UK Gov Engineering Standards **v1.0.0** (assessed 2026-07-05)"

Assessors verify against the version stated, not `main`.

## Release process

One command does everything:

```bash
python scripts/release.py --version v1.1.0
```

### What the script does (in order)

| Step | Action | What happens |
|------|--------|--------------|
| 1 | Validate | Runs `validate_standards.py` — fails if any standard is broken |
| 2 | Tag | Creates annotated git tag `v1.1.0` |
| 3 | Push tag | Pushes tag to origin |
| 4 | GitHub Release | Creates release with changelog + `.vsix` attached |
| 5 | Update references | Runs `update_counts.py` which changes all `@v1.0.0` → `@v1.1.0` in docs/scripts |
| 6 | Commit + push | Commits the reference updates and pushes to main |
| 7 | Reminder | Prints list of docs to manually review for semantic staleness |

After the script completes, the release is fully self-contained:
- Tag exists
- GitHub Release exists with artefacts
- All docs/scripts reference the new version
- No manual follow-up needed (except the doc review reminder)

### Dry run

Preview what would happen without making any changes:

```bash
python scripts/release.py --version v1.1.0 --dry-run
```

### How version references stay in sync

`scripts/update_counts.py` (called by the release script and by CI) finds every `@vX.Y.Z` reference in these files and updates them to the latest git tag:

- `README.md`
- `docs/usage-by-role.md`
- `.github/workflows/compliance.yml`
- `scripts/onboarding.py`

If a contributor opens a PR after a release without running this script, CI fails with: "version references are stale."

### Workflow

```
PRs merged to main (standards or code changes)
    ↓
Maintainer decides it's time to release
    ↓
python scripts/release.py --version v1.1.0
    ↓
├── validates → tags → pushes → creates GitHub Release
├── updates all @vX.Y.Z refs → commits → pushes
└── prints doc review reminder
    ↓
Done. Teams can pin to @v1.1.0.
```

See also: [CHANGELOG.md](../CHANGELOG.md)
