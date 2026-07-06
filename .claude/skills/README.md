# Claude Code Skills

These are slash commands available when working in this repo with [Claude Code](https://claude.ai/code). Type the command name in the Claude Code prompt to invoke it.

## Available skills

| Command | What it does |
|---------|--------------|
| `/new-standard` | Scaffold a new standard with guided prompts for ID, conformance, sources, and validation |
| `/rebuild-graph` | Regenerate the D3 sources graph from actual source traceability tables |
| `/preflight` | Run validation and build checks before pushing — catches CI failures locally |
| `/impact` | Show what standards, graph nodes, and pages are affected by a change |
| `/add-source` | Add a new source framework with trust criteria gate |

## How skills work

Each `.md` file in this directory defines a skill. When invoked, Claude follows the steps described in the file — asking questions, reading/writing files, and running scripts as needed.

Skills are project-specific. They only appear when Claude Code is running in this repository.

## Adding a new skill

Create a new `.md` file in this directory with frontmatter:

```markdown
---
name: skill-name
description: One-line description shown in skill listings
---

# Skill Title

Instructions for Claude to follow when this skill is invoked.
```
