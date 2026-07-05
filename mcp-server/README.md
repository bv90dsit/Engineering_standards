# MCP Server — UK Government Engineering Standards

Exposes the standards library to AI coding agents via the [Model Context Protocol](https://modelcontextprotocol.io/). Any MCP-compatible client (Claude Code, Cursor, custom agents) can query standards and check code in real time.

## What it provides

### Tools

| Tool | What it does |
|------|-------------|
| `query_standards` | Filter standards by role, platform, conformance, category, tag, enforcement, module |
| `get_standard` | Get full markdown content of a specific standard (e.g. SEC-001) |
| `check_file` | Check file content against applicable rules — returns line-level violations |
| `list_modules` | List available modules with descriptions and counts |

### Resources

| Resource | What it provides |
|----------|-----------------|
| `standards://index` | Full JSON index of all 55 standards |
| `standards://{ID}` | Individual standard as markdown (e.g. `standards://SEC-003`) |

## Setup

### Install dependency

```bash
pip install mcp
```

### Configure in Claude Code

Add to your Claude Code settings (`.claude/settings.json` or project-level):

```json
{
  "mcpServers": {
    "uk-gov-standards": {
      "command": "python",
      "args": ["mcp-server/server.py"],
      "cwd": "/path/to/engineering_standards"
    }
  }
}
```

### Configure in other MCP clients

Any client that supports stdio transport can connect:

```json
{
  "command": "python",
  "args": ["/path/to/engineering_standards/mcp-server/server.py"]
}
```

## How an AI agent uses it

1. Agent starts coding a Python Django service
2. Calls `query_standards(platform="python", conformance="MUST")` → gets 28+ applicable standards
3. Before generating code, the agent knows: no print(), use parameterised queries, don't hardcode secrets, enable CSRF
4. After writing code, calls `check_file(filename="views.py", content="...")` → gets line-level violations
5. Agent fixes violations before presenting code to the user

## Example interactions

```
Agent → query_standards(category="SEC", conformance="MUST")
Server → "Found 5 standard(s):
  - SEC-001 [MUST] HTTPS everywhere
  - SEC-002 [MUST] Dependency vulnerability scanning
  - SEC-003 [MUST] No secrets in source code
  - SEC-004 [MUST] Input validation and output encoding
  - SEC-005 [MUST] Authentication via standards"

Agent → check_file(filename="app.py", content="password = \"hunter2\"\n...")
Server → "Found 1 violation(s):
  - Line 1 [SEC-003-password]: Possible hardcoded password. Use environment variables."

Agent → get_standard(standard_id="SEC-003")
Server → [full markdown with Quick reference showing .pre-commit-config.yaml etc.]
```

## Related docs

- [Main README](../README.md) — architecture overview
- [standards_lib/README.md](../standards_lib/README.md) — Python API (what the MCP server wraps)
- [Modules](../modules/README.md) — how rules are organised
