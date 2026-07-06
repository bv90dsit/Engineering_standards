# Claude Code Integration

This repo has two types of Claude Code skill, serving different audiences.

## 1. Coding skill — `uk-gov-standards.md`

**Audience:** Any developer using Claude Code to write code for UK Gov services.

**What it does:** Makes Claude proactively write standards-compliant code without being asked. When installed, Claude follows all MUST/SHOULD standards (security, accessibility, architecture, language-specific) from the start.

**Install in another project:**
```bash
mkdir -p .claude/skills
curl -sL https://raw.githubusercontent.com/bv90dsit/Engineering_standards/main/.claude/skills/uk-gov-standards.md \
  -o .claude/skills/uk-gov-standards.md
```

**How it stays current:** Generated automatically by `scripts/build_skill.py` from the standards index. Run that script after adding or changing standards — CI verifies it's up to date.

---

## 2. Repo developer skills — `.claude/skills/`

**Audience:** Developers maintaining this standards repo using Claude Code.

**What they do:** Slash commands for repo development tasks. Type the command in a Claude Code session while in this repo.

| Command | What it does |
|---------|--------------|
| `/new-standard` | Scaffold a new standard with guided prompts for ID, conformance, sources, and validation |
| `/rebuild-graph` | Regenerate the D3 sources graph from actual source traceability tables |
| `/preflight` | Run validation and build checks before pushing — catches CI failures locally |
| `/impact` | Show what standards, graph nodes, and pages are affected by a change |
| `/add-source` | Add a new source framework with trust criteria gate |

**How they work:** Each `.md` file in this directory defines a skill. When invoked, Claude follows the steps described in the file — asking questions, reading/writing files, and running scripts as needed. These only appear when Claude Code is running in this repository.

---

## Adding a new maintainer skill

Create a `.md` file in this directory:

```markdown
---
name: skill-name
description: One-line description shown in skill listings
---

# Skill Title

Steps for Claude to follow when invoked.
```

## Updating the coding skill

After adding or modifying standards:

```bash
python scripts/build_skill.py
```

This regenerates `.claude/skills/uk-gov-standards.md` from the current index.
