#!/usr/bin/env python3
"""MCP Server for UK Government Engineering Standards.

Exposes the standards library as MCP tools so AI coding agents
can query applicable standards and check code against them.

Usage:
    python mcp-server/server.py

Configure in Claude Code's settings.json or any MCP client:
    {
        "mcpServers": {
            "uk-gov-standards": {
                "command": "python",
                "args": ["mcp-server/server.py"],
                "cwd": "/path/to/engineering_standards"
            }
        }
    }
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Add repo root to path so standards_lib is importable
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

from standards_lib.query import (
    query_standards,
    get_standard,
    load_index,
    list_modules,
    list_categories,
    list_tags,
    to_json,
)

import yaml

server = Server("uk-gov-standards")

# --- Load rules for check_file ---

MODULES_DIR = REPO_ROOT / "modules"


def _load_all_rules() -> list[dict]:
    """Load all rules.json from all modules."""
    rules = []
    for module_path in sorted(MODULES_DIR.iterdir()):
        rules_file = module_path / "rules.json"
        if rules_file.exists():
            try:
                with open(rules_file) as f:
                    data = json.load(f)
                rules.extend(data.get("rules", []))
            except (json.JSONDecodeError, OSError):
                pass
    return rules


ALL_RULES = _load_all_rules()


def _matches_glob(filepath: str, pattern: str) -> bool:
    """Simple glob matching for file patterns."""
    regex = pattern.replace(".", r"\.").replace("**", "{{GLOB}}").replace("*", "[^/]*").replace("{{GLOB}}", ".*").replace("?", "[^/]")
    if "{" in regex:
        regex = re.sub(r"\{([^}]+)\}", lambda m: "(?:" + "|".join(re.escape(a).replace(r"\.", ".") for a in m.group(1).split(",")) + ")", regex)
    return bool(re.match(f"^{regex}$", filepath))


# --- MCP Tools ---


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_standards",
            description="Query UK Gov engineering standards by context. Returns matching standards as JSON.",
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "description": "Role filter (e.g. engineer, architect)"},
                    "platform": {"type": "string", "description": "Platform filter (e.g. python, java, typescript)"},
                    "conformance": {"type": "string", "enum": ["MUST", "SHOULD", "COULD"], "description": "Conformance level filter"},
                    "category": {"type": "string", "description": "Category filter (e.g. SEC, ENG, OPS)"},
                    "tag": {"type": "string", "description": "Tag filter (e.g. security, ai, logging)"},
                    "enforcement": {"type": "string", "enum": ["automated", "peer-review", "periodic-audit", "ways-of-working"], "description": "Enforcement mechanism filter"},
                    "module": {"type": "string", "description": "Module filter (core, python, java, typescript, all)"},
                },
                "required": [],
            },
        ),
        Tool(
            name="get_standard",
            description="Get the full content of a specific standard by ID. Returns the markdown with all guidance.",
            inputSchema={
                "type": "object",
                "properties": {
                    "standard_id": {"type": "string", "description": "Standard ID (e.g. SEC-001, PY-003, JV-002)"},
                },
                "required": ["standard_id"],
            },
        ),
        Tool(
            name="check_file",
            description="Check a file's content against applicable standards rules. Returns any violations found.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "The filename (e.g. app.py, Service.java, index.ts)"},
                    "content": {"type": "string", "description": "The file content to check"},
                },
                "required": ["filename", "content"],
            },
        ),
        Tool(
            name="list_modules",
            description="List all available standards modules with their descriptions and standard counts.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "query_standards":
        results = query_standards(
            role=arguments.get("role"),
            platform=arguments.get("platform"),
            conformance=arguments.get("conformance"),
            category=arguments.get("category"),
            tag=arguments.get("tag"),
            enforcement=arguments.get("enforcement"),
            module=arguments.get("module"),
        )
        summary = f"Found {len(results)} standard(s).\n\n"
        for s in results:
            summary += f"- **{s['id']}** [{s['conformance']}] {s['title']}\n"
        return [TextContent(type="text", text=summary)]

    elif name == "get_standard":
        standard_id = arguments["standard_id"]
        try:
            content = get_standard(standard_id)
            return [TextContent(type="text", text=content)]
        except FileNotFoundError as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    elif name == "check_file":
        filename = arguments["filename"]
        content = arguments["content"]
        violations = _check_content(filename, content)
        if not violations:
            return [TextContent(type="text", text=f"✓ No violations found in {filename}")]
        result = f"Found {len(violations)} violation(s) in {filename}:\n\n"
        for v in violations:
            result += f"- **Line {v['line']}** [{v['rule_id']}]: {v['message']}\n"
        return [TextContent(type="text", text=result)]

    elif name == "list_modules":
        modules = list_modules()
        result = "Available modules:\n\n"
        for m in modules:
            standards = load_index(module=m["name"])
            result += f"- **{m['name']}** — {m.get('description', '')} ({len(standards)} standards)\n"
        return [TextContent(type="text", text=result)]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


def _check_content(filename: str, content: str) -> list[dict]:
    """Run all applicable rules against file content."""
    violations = []
    lines = content.split("\n")

    for rule in ALL_RULES:
        if not _matches_glob(filename, rule["filePattern"]):
            continue
        if rule.get("excludeFilePattern") and _matches_glob(filename, rule["excludeFilePattern"]):
            continue

        pattern = re.compile(rule["pattern"], re.IGNORECASE)
        exclude_pattern = re.compile(rule["excludePattern"]) if rule.get("excludePattern") else None

        for i, line in enumerate(lines, 1):
            if exclude_pattern and exclude_pattern.match(line):
                continue
            if pattern.search(line):
                violations.append({
                    "line": i,
                    "rule_id": rule["id"],
                    "message": rule["message"],
                    "severity": rule["severity"],
                })

    return violations


# --- MCP Resources ---


@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = [
        Resource(
            uri="standards://index",
            name="Standards Index",
            description="Full index of all standards across all modules",
            mimeType="application/json",
        ),
    ]
    # Add individual standards as resources
    standards = load_index(module="all")
    for s in standards:
        resources.append(Resource(
            uri=f"standards://{s['id']}",
            name=f"{s['id']}: {s['title']}",
            description=f"[{s['conformance']}] {s['title']}",
            mimeType="text/markdown",
        ))
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "standards://index":
        standards = load_index(module="all")
        return to_json(standards)

    # standards://SEC-001 -> SEC-001
    standard_id = uri.replace("standards://", "")
    try:
        return get_standard(standard_id)
    except FileNotFoundError:
        return f"Standard not found: {standard_id}"


# --- Main ---


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
