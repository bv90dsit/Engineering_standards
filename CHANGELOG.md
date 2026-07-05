# Changelog

All notable changes to the UK Government Engineering Standards are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [Semantic Versioning](https://semver.org/) adapted for standards:

- **Major** (v2.0.0) — new MUST standards added, or breaking changes to existing MUST standards (teams must take action)
- **Minor** (v1.1.0) — new SHOULD/COULD standards, new modules, non-breaking refinements to existing standards
- **Patch** (v1.0.1) — typos, clarification of wording, URL fixes, documentation updates (no compliance impact)

---

## [v1.0.0] — 2026-07-05

### Initial release

**55 standards** across 5 modules:

| Module | Standards |
|--------|-----------|
| core | 33 (ENG ×6, SEC ×7, ARC ×5, OPS ×5, DAT ×4, ACC ×2, EMG ×4) |
| python | 8 (PY-001 to PY-008) |
| java | 6 (JV-001 to JV-006) |
| typescript | 6 (TS-001 to TS-006) |
| org-example | 2 (ORG-001 to ORG-002) |

### Tooling included

- Query library (`standards_lib/`) with CLI and JSON output
- Compliance checker (`scripts/check_compliance.py`) — automated + manual review
- Reusable GitHub Action (`.github/workflows/compliance.yml`)
- Onboarding tool (`scripts/onboarding.py`)
- VS Code extension with modular rule engine
- CLI scaffold for new standards (`scripts/new_standard.py`)
- GitHub Issue template for non-technical contributors
- CI validation pipeline (standards + code, two-track)
- Trusted sources allowlist with tier system

### Conformance summary

- 28 MUST
- 26 SHOULD
- 1 COULD

### Source frameworks

30 trusted source domains across Tier 1 (authoritative) and Tier 2 (established).
