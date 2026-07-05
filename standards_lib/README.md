# standards_lib — Python API

Importable library for querying UK Gov engineering standards programmatically.

## Install

```bash
pip install .  # from repo root
```

Or add to your requirements:
```
git+https://github.com/bv90dsit/Engineering_standards.git
```

## Usage

```python
from standards_lib import query_standards, load_index, get_standard, list_modules, list_categories, list_tags, to_json

# Query with filters
results = query_standards(
    role="engineer",
    platform="python",
    conformance="MUST",
    enforcement="automated",
    category="SEC",
    tag="security",
    module="all",  # or "core", "python", etc.
)

# Get full markdown content of a standard
content = get_standard("SEC-001")

# List available modules
modules = list_modules()  # returns [{name, description, version, ...}]

# Get all categories or tags
categories = list_categories()  # ["ACC", "ARC", "DAT", ...]
tags = list_tags()  # ["accessibility", "ai", ...]

# Serialize to JSON
json_str = to_json(results)
```

## Functions

| Function | Parameters | Returns |
|----------|-----------|---------|
| `query_standards()` | `role`, `platform`, `data_class`, `category`, `tag`, `enforcement`, `conformance`, `module` (all optional) | `list[dict]` |
| `load_index(module=None)` | `module`: "core" (default), specific name, or "all" | `list[dict]` |
| `get_standard(standard_id)` | Standard ID (e.g. "SEC-001") | `str` (markdown content) |
| `list_modules()` | — | `list[dict]` (module metadata) |
| `list_categories(module=None)` | Optional module filter | `list[str]` |
| `list_tags(module=None)` | Optional module filter | `list[str]` |
| `to_json(standards)` | List of standard dicts | `str` (JSON) |

## Error handling

- `query_standards(module="nonexistent")` raises `ValueError` with available module names
- `get_standard("FAKE-999")` raises `FileNotFoundError`
- Malformed YAML in a module prints a warning to stderr and skips that module (doesn't crash)
