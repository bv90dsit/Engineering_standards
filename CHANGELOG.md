# Changelog

All notable changes to the UK Government Engineering Standards are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/). Versioning follows [Semantic Versioning](https://semver.org/) adapted for standards:

- **Major** (v2.0.0) — new MUST standards added, or breaking changes to existing MUST standards (teams must take action)
- **Minor** (v1.1.0) — new SHOULD/COULD standards, new modules, non-breaking refinements to existing standards
- **Patch** (v1.0.1) — typos, clarification of wording, URL fixes, documentation updates (no compliance impact)

---

## [v1.1.0] — 2026-07-05

### Added

**14 new standards (55 → 69):**
- SEC-008: API rate limiting
- SEC-009: CORS explicitly configured
- OPS-006: Structured logging with correlation IDs
- OPS-007: Support model and on-call defined
- ARC-006: No single points of failure
- ACC-003: Content written in plain English
- DAT-005: Audit trail for data changes
- ENG-007: Code review turnaround within 24h
- PY-009: Pin dependencies with lock file
- PY-010: Use pathlib for file operations
- JV-007: Use records for DTOs
- JV-008: Structured logging in JSON
- TS-007: ESLint with strict ruleset
- TS-008: No @ts-ignore without justification

**Tooling:**
- MCP server for AI coding agents (`mcp-server/`)
- Repo scanner (`scripts/suggest_standards.py`) — auto-detects stack
- SBOM generation in release script (CycloneDX format)
- Tests in CI (pytest + mocha run on every PR)
- GitHub Pages site live
- VS Code extension rule: SEC-009 CORS wildcard detection

**Documentation:**
- Module-level READMEs with "why it exists" and enforcement column
- Exemption/waiver process (`docs/exemptions.md`)
- SECURITY.md with trust model and permissions
- Test strategy (`docs/testing.md`)

### Fixed
- OPS-001: Invalid Prometheus 30-day rate query → recording rules
- TS-006: Zod boolean coercion footgun → custom transform
- GitHub Pages Liquid parsing errors

### Changed
- All 69 standards now have Quick reference sections with copy-paste code/config
- Trusted sources: removed Tier 3 (library docs), kept Tier 1 + Tier 2 only
- Architecture diagram consistent across README and website

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
