# Modules

Standards are organised into **modules** — pluggable rule packs that can be mixed and matched. An organisation picks the modules that apply to their stack.

## Available modules

| Module | Description | Standards | Also checked in IDE |
|--------|-------------|-----------|---------------------|
| [core](core/) | Cross-cutting UK Gov engineering standards | 33 | SEC-001, SEC-003 |
| [python](python/) | Python + Django + Flask | 8 | PY-001, PY-003, PY-004, PY-005, PY-006, PY-008 |
| [java](java/) | Java + Spring Boot | 6 | JV-002, JV-003, JV-006 |
| [typescript](typescript/) | TypeScript + React + Node | 6 | TS-001, TS-002, TS-004 |
| [org-example](org-example/) | Example showing how an org adds custom rules | 2 | ORG-001, ORG-002 |

**Total: 55 standards** across 5 modules.

## Using modules

### CLI

```bash
# List available modules
python scripts/query_standards.py --list-modules

# Query core only (default)
python scripts/query_standards.py --conformance MUST

# Query a specific module
python scripts/query_standards.py --module python

# Query all modules
python scripts/query_standards.py --module all
```

### VS Code extension

The extension auto-discovers `modules/*/rules.json` and applies rules based on file type. Toggle modules in settings:

```json
{
  "ukGovStandards.modules.core": true,
  "ukGovStandards.modules.python": true,
  "ukGovStandards.modules.java": false,
  "ukGovStandards.modules.typescript": true
}
```

### CI/CD compliance checker

The checker reads all modules by default. To restrict to specific modules in a consuming repo, create `.standards-config.yaml`:

```yaml
modules:
  - core
  - python
  - /path/to/your-org-module
```

## Creating your own module

A module is a directory with this structure:

```
my-module/
├── module.yaml             # metadata (name, description, version)
├── standards-index.yaml    # standard entries (same format as core)
├── standards/              # one .md file per standard
│   ├── MYMOD-001.md
│   └── MYMOD-002.md
└── rules.json              # (optional) VS Code extension line-level checks
```

### module.yaml

```yaml
name: my-module
description: What these standards cover
version: 0.1.0
author: Your Team
applies_to:
  platform: python    # or "any" for cross-cutting
```

### standards-index.yaml

Same format as the core index. Each entry needs: `id`, `title`, `conformance`, `enforcement`, `applies_to`, `category`, `source`, `tags`.

### standards/*.md

Same format as core standards: YAML frontmatter + Standard + Rationale + What good looks like + Enforcement + Source traceability.

See [docs/sources.md](../docs/sources.md) for the traceability format, synthesis methodology, and list of approved source frameworks.

### rules.json (optional)

For the VS Code extension — defines regex-based line-level checks:

```json
{
  "module": "my-module",
  "rules": [
    {
      "id": "MYMOD-001",
      "pattern": "regex to match violations",
      "excludePattern": "regex for lines to skip (e.g. comments)",
      "filePattern": "**/*.py",
      "excludeFilePattern": "**/test_*",
      "severity": "warning",
      "message": "MYMOD-001: Human-readable explanation of what's wrong."
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Standard ID this rule checks |
| `pattern` | Yes | Regex to match violations (per line) |
| `excludePattern` | No | Lines matching this are skipped (e.g. comments) |
| `filePattern` | Yes | Glob for which files this rule applies to |
| `excludeFilePattern` | No | Glob for files to exclude (e.g. tests) |
| `severity` | Yes | `error`, `warning`, or `information` |
| `message` | Yes | Shown to the engineer in the squiggly tooltip |

## ID naming convention

Use a short prefix unique to your module:

| Prefix | Module |
|--------|--------|
| ENG, SEC, ARC, OPS, DAT, ACC, EMG | core |
| PY | python |
| JV | java |
| TS | typescript |
| ORG | org-example |
| MYMOD | your custom module |

## Related docs

- [Main README](../README.md) — architecture overview and quick start
- [VS Code extension](../vscode-extension/README.md) — how the extension loads rules from modules
- [Sources](../docs/sources.md) — traceability format and approved source frameworks
- [Usage by role](../docs/usage-by-role.md) — how different roles use the standards
