# UK Gov Engineering Standards — VS Code Extension

Real-time compliance checking against UK Government engineering standards, directly in your editor.

## What it does

Gives you inline warnings and errors as you type — catching standards violations at the moment of creation, before you even commit.

| Check | What it flags | Severity |
|-------|--------------|----------|
| **SEC-001** | `http://` URLs (should be `https://`) | Warning (yellow squiggly) |
| **SEC-003** | Hardcoded secrets (passwords, API keys, tokens) | Error (red squiggly) |
| **ENG-001** | No LICENCE file in workspace | Information |
| **SEC-002** | No dependency scanning config | Information |
| **ENG-003** | No CI workflow | Information |
| **ENG-004** | No README or README too short | Information |

Hovering any diagnostic shows the standard ID — click it to read the full standard.

## Install

```bash
cd vscode-extension
npm install
npm run compile
```

Then in VS Code: `Ctrl+Shift+P` → "Extensions: Install from VSIX" → select the `.vsix` file.

Or for development: open this folder in VS Code, press `F5` to launch the Extension Development Host.

## Settings

All checks are on by default. Disable individually in VS Code settings:

```json
{
  "ukGovStandards.enable": true,
  "ukGovStandards.checks.sec001": true,
  "ukGovStandards.checks.sec003": true,
  "ukGovStandards.checks.eng001": true,
  "ukGovStandards.checks.sec002": true,
  "ukGovStandards.checks.eng003": true,
  "ukGovStandards.checks.eng004": true
}
```

## How it fits the standards architecture

This is a **Layer 4 consumer** — it calls the same logic as the CI pipeline but runs it at the point of code creation:

```
CI/CD pipeline   →  catches problems after push (10+ min feedback)
Local CLI check  →  catches problems before commit (2 min feedback)
VS Code extension →  catches problems as you type (instant feedback)
```

All three enforce the same standards. The extension covers only the subset that makes sense at the line level.
