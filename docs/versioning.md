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

1. Changes accumulate on `main` via PRs
2. When ready to release, a maintainer runs `python scripts/release.py --version v1.1.0`
3. Script validates all standards, generates release notes, creates a git tag
4. GitHub Release is created with the changelog and `.vsix` attached
5. Teams are notified (major versions only — via changelog and any configured webhooks)

See also: [CHANGELOG.md](../CHANGELOG.md)
