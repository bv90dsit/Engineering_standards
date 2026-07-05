# Python Standards

Standards for Python services including Django and Flask. Apply these alongside core.

## Standards

| ID | Standard | Level | Enforcement | Why it exists |
|----|----------|-------|-------------|---------------|
| PY-001 | Use the logging module instead of print() | SHOULD | automated | print() can't be filtered, routed, or levelled in production |
| PY-002 | Add type hints to function signatures | SHOULD | peer-review | Without types, IDE support breaks and bugs hide until runtime |
| PY-003 | Use parameterised queries | MUST | automated | SQL injection via f-strings is the #1 Python web vulnerability |
| PY-004 | Avoid wildcard imports | SHOULD | automated | Wildcard imports make it impossible to trace where names come from |
| PY-005 | Never disable CSRF protection in Django | MUST | automated | Django has CSRF built in; disabling it is always wrong |
| PY-006 | Load secrets from environment variables | MUST | automated | Hardcoded secrets get committed; Flask makes this especially easy |
| PY-007 | Prefer ORM queries over raw SQL | SHOULD | peer-review, automated | Raw SQL bypasses ORM protections |
| PY-008 | Disable DEBUG mode in production | MUST | automated | DEBUG=True exposes stack traces, queries, and settings to attackers |
| PY-009 | Pin all dependency versions | MUST | automated | Unpinned deps = unreproducible builds + supply chain attacks |
| PY-010 | Use pathlib for file path manipulation | SHOULD | peer-review | os.path is error-prone; pathlib is cross-platform and readable |

## How to use

Query all Python standards:

```bash
python scripts/query_standards.py --module python
```

Filter by conformance level:

```bash
python scripts/query_standards.py --module python --conformance MUST
```
