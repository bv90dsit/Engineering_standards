---
layout: default
title: About
permalink: /about/
---

# About UK Government Engineering Standards

This repository provides **machine-readable, context-aware engineering standards** for UK Government digital services. Standards are written in Markdown with structured YAML frontmatter, making them parseable by tooling (linters, IDE extensions, CI pipelines) while remaining human-readable.

## Architecture

Five layers from raw source material to the engineer at their desk:

```
Layer 0 — Source frameworks (GDS, NCSC, DORA, OWASP, WCAG, etc.)
    ↓ synthesised into
Layer 1 — Individual standard files (one .md per standard, with frontmatter)
    ↓ catalogued in
Layer 2 — standards-index.yaml (lightweight, always loaded)
    ↓ filtered by
Layer 3 — query_standards(context) → returns only what applies
    ↓ served to
Layer 4 — Consumers (CI/CD, VS Code extension, onboarding, MCP server)
```

- **Layer 0 -- Source frameworks:** Published authoritative standards (GDS Service Standard, NCSC, OWASP, WCAG, etc.) that provide the authority behind each standard.
- **Layer 1 -- Standard files:** One `.md` file per standard with YAML frontmatter. Organised into modules: core (cross-cutting), python, java, typescript, org-specific.
- **Layer 2 -- Index:** `standards-index.yaml` per module — lightweight, always loaded. The single source of truth for filtering and discovery.
- **Layer 3 -- Query interface:** `standards_lib/` Python library that filters by role, platform, conformance, enforcement, category, tag, and module.
- **Layer 4 -- Consumers:** Every tool that needs standards calls the query interface. CI/CD pipeline, VS Code extension, onboarding tool, compliance checker, MCP server, this website.

## Adopting These Standards

1. **Fork or clone** the [GitHub repository](https://github.com/bv90dsit/Engineering_standards)
2. **Choose your modules** -- start with `core`, add language modules as needed
3. **Customise at Layer 5** -- add your organisation's overrides
4. **Integrate tooling** -- use the VS Code extension, CI workflows, and Python library
5. **Contribute back** -- open PRs for improvements that benefit everyone

## Quick Start

```bash
git clone https://github.com/bv90dsit/Engineering_standards.git
cd Engineering_standards
pip install -r requirements.txt
python scripts/query_standards.py --category SEC --conformance MUST
```

## Links

- [GitHub Repository](https://github.com/bv90dsit/Engineering_standards)
- [Contributing Guide](https://github.com/bv90dsit/Engineering_standards/blob/main/CONTRIBUTING.md)
- [Changelog](https://github.com/bv90dsit/Engineering_standards/blob/main/CHANGELOG.md)
