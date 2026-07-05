# Modules

Standards are organised into **modules** — pluggable rule packs that can be mixed and matched.

## Available modules

| Module | Description | Standards |
|--------|-------------|-----------|
| `core` | Cross-cutting UK Gov engineering standards | 33 |
| `python` | Python-specific standards | 4 |
| `org-example` | Example showing how an organisation adds custom rules | 2 |

## Using modules

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

Same format as core standards: YAML frontmatter + Standard + Rationale + What good looks like + Enforcement + Source traceability. See [docs/sources.md](../docs/sources.md) for the traceability format, synthesis methodology, and list of approved source frameworks.

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

## Adding your module to a consuming repo

Create `.standards-config.yaml` in the consuming service's root:

```yaml
modules:
  - core
  - python
  - /path/to/your-org-module
```

The compliance checker reads this file and applies only the listed modules.

## ID naming convention

Use a short prefix unique to your module:

| Prefix | Module |
|--------|--------|
| ENG, SEC, ARC, OPS, DAT, ACC, EMG | core |
| PY | python |
| TS | typescript (future) |
| JV | java (future) |
| ORG | org-example |
| MYMOD | your custom module |
