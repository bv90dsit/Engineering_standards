---
layout: default
title: About
permalink: /about/
---

# About UK Government Engineering Standards

This repository provides **machine-readable, context-aware engineering standards** for UK Government digital services. Standards are written in Markdown with structured YAML frontmatter, making them parseable by tooling (linters, IDE extensions, CI pipelines) while remaining human-readable.

## Five-Layer Architecture

```
+-------------------------------------------------------+
|  Layer 5: ORGANISATION OVERRIDES                      |
|  (org-specific customisations and additions)          |
+-------------------------------------------------------+
|  Layer 4: LANGUAGE / PLATFORM MODULES                 |
|  (Python, Java, TypeScript, etc.)                     |
+-------------------------------------------------------+
|  Layer 3: CORE STANDARDS                              |
|  (universal engineering standards)                    |
+-------------------------------------------------------+
|  Layer 2: STANDARDS LIBRARY (standards_lib)           |
|  (Python tooling: validation, queries, compliance)    |
+-------------------------------------------------------+
|  Layer 1: SCHEMA & INDEX                              |
|  (standards-index.yaml, frontmatter schema)           |
+-------------------------------------------------------+
```

- **Layer 1 -- Schema & Index:** The `standards-index.yaml` file and frontmatter schema define the structure every standard must follow.
- **Layer 2 -- Standards Library:** Python tooling (`standards_lib/`) for validating, querying, and checking compliance against standards.
- **Layer 3 -- Core Standards:** Universal engineering standards (`modules/core/`) that apply regardless of language or platform.
- **Layer 4 -- Language Modules:** Platform-specific standards (`modules/python/`, `modules/java/`, `modules/typescript/`) that extend the core.
- **Layer 5 -- Organisation Overrides:** Customisations for specific organisations (`modules/org-example/`) that can tighten or extend any layer below.

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
