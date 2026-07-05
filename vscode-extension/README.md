# UK Gov Engineering Standards — VS Code Extension

Real-time compliance checking against UK Government engineering standards, directly in your editor.

## What it does

Gives you inline warnings and errors as you type — catching standards violations at the moment of creation, before you even commit.

The extension loads rules from [modules](../modules/README.md). Checks activate based on the file you're editing:

### Core (all languages)

| Check | What it flags | Severity |
|-------|--------------|----------|
| **SEC-001** | `http://` URLs (should be `https://`) | Warning |
| **SEC-003** | Hardcoded secrets (passwords, API keys, tokens, AWS keys) | Error |
| **ENG-001** | No LICENCE file in workspace | Info |
| **SEC-002** | No dependency scanning config | Info |
| **ENG-003** | No CI workflow | Info |
| **ENG-004** | No README or README too short | Info |

### Python (`.py` files)

| Check | What it flags | Severity |
|-------|--------------|----------|
| **PY-001** | `print()` in production code | Warning |
| **PY-003** | Raw SQL string construction (f-strings or concatenation) | Error |
| **PY-004** | `from x import *` | Warning |
| **PY-005** | `@csrf_exempt` or CSRF middleware disabled | Error |
| **PY-006** | Hardcoded `SECRET_KEY` | Error |
| **PY-008** | `DEBUG = True` in settings | Error |

### Java (`.java` files)

| Check | What it flags | Severity |
|-------|--------------|----------|
| **JV-002** | `System.out.println` / `System.err` | Warning |
| **JV-003** | SQL string concatenation | Error |
| **JV-006** | `import java.util.logging` or `import org.apache.log4j` | Warning |

### TypeScript (`.ts` / `.tsx` files)

| Check | What it flags | Severity |
|-------|--------------|----------|
| **TS-001** | `"strict": false` in tsconfig.json | Error |
| **TS-002** | `: any` type annotation | Warning |
| **TS-004** | `console.log` / `console.error` etc. | Warning |

Hovering any diagnostic shows the standard ID — click it to read the full standard.

## Install

### For engineers (one command)

Download the `.vsix` from the [latest release](https://github.com/bv90dsit/Engineering_standards/releases/latest), then:

```bash
code --install-extension uk-gov-engineering-standards-0.1.0.vsix
```

Or in VS Code: `Ctrl+Shift+P` → "Extensions: Install from VSIX" → select the downloaded file.

That's it. Restart VS Code and the extension is active in every workspace.

### For teams using dev containers

Add to your `.devcontainer/devcontainer.json`:

```json
{
  "customizations": {
    "vscode": {
      "extensions": ["uk-gov-engineering.uk-gov-engineering-standards"]
    }
  }
}
```

### For contributors (development mode)

```bash
cd vscode-extension
npm install
npm run compile
```

Then press `F5` in VS Code to launch the Extension Development Host. A `.vscode/launch.json` and `tasks.json` are included — `F5` automatically compiles in watch mode and launches the extension.

Warnings and errors from rule loading appear in the **Output** panel under "UK Gov Standards".

## Settings

### Enable/disable modules

Each module can be toggled independently:

```json
{
  "ukGovStandards.enable": true,
  "ukGovStandards.modules.core": true,
  "ukGovStandards.modules.python": true,
  "ukGovStandards.modules.java": true,
  "ukGovStandards.modules.typescript": true
}
```

A Java team can disable Python and TypeScript rules. A frontend team can disable Java.

### Add your organisation's rules

Point to external modules with `additionalModules`:

```json
{
  "ukGovStandards.additionalModules": [
    "/path/to/my-org-standards/modules/org-rules"
  ]
}
```

The path must contain a `rules.json` in the same format as the built-in modules. See [modules/README.md](../modules/README.md) for the format.

### Workspace-level checks (fallback)

If no `modules/` directory is found (standalone install without the full repo), the extension falls back to hardcoded SEC-001 and SEC-003 checks:

```json
{
  "ukGovStandards.checks.sec001": true,
  "ukGovStandards.checks.sec003": true,
  "ukGovStandards.checks.eng001": true,
  "ukGovStandards.checks.sec002": true,
  "ukGovStandards.checks.eng003": true,
  "ukGovStandards.checks.eng004": true
}
```

## How it fits the standards architecture

This is a **Layer 4 consumer** — it loads `rules.json` from each module and applies them at the point of code creation:

```
CI/CD pipeline   →  catches problems after push (10+ min feedback)
Local CLI check  →  catches problems before commit (2 min feedback)
VS Code extension →  catches problems as you type (instant feedback)
```

All three enforce the same standards from the same modules. The extension covers the subset that can be detected at the line level via regex.

## Related docs

- [Main README](../README.md) — overview of the full standards architecture
- [Modules](../modules/README.md) — how to create modules and add custom rules
- [Sources](../docs/sources.md) — where the standards come from
- [Usage by role](../docs/usage-by-role.md) — how different roles interact with the standards
