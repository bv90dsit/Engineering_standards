#!/usr/bin/env python3
"""Analyse the impact of a change and show what else needs attention.

Usage:
    python scripts/impact_analysis.py --changed modules/core/standards/SEC-010.md
    python scripts/impact_analysis.py --changed modules/python/rules.json
    python scripts/impact_analysis.py --changed standards_lib/query.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


def analyse_standard_change(file_path: Path) -> None:
    """Analyse impact of a new or changed standard .md file."""
    std_id = file_path.stem
    module_name = file_path.parent.parent.name

    print(f"\n{'='*60}")
    print(f"  Impact analysis: {std_id} ({module_name} module)")
    print(f"{'='*60}")

    # Check if it's a new standard (not in index) or a change to existing
    index_file = file_path.parent.parent / "standards-index.yaml"
    is_new = True
    if index_file.exists():
        with open(index_file) as f:
            data = yaml.safe_load(f)
        existing_ids = [s.get("id") for s in data.get("standards", [])]
        is_new = std_id not in existing_ids

    if is_new:
        print(f"\n  Status: NEW standard")
    else:
        print(f"\n  Status: CHANGED existing standard")

    # Automatic (no action needed)
    print(f"\n  AUTOMATIC (handled by runtime/CI):")
    print(f"  ✓ standards_lib picks it up from index at runtime")
    print(f"  ✓ query_standards.py / onboarding.py will include it")
    print(f"  ✓ suggest_standards.py will recommend it for matching repos")
    print(f"  ✓ check_compliance.py reports 'manual review' (unless automated check exists)")
    print(f"  ✓ GitHub Action consumers get it on next PR to their repo")
    print(f"  ✓ MCP server exposes it via query_standards / get_standard")

    # Needs action
    print(f"\n  NEEDS ACTION:")

    if is_new:
        # Check if index entry exists
        if std_id not in (existing_ids if not is_new else []):
            print(f"  ⚠ {index_file.relative_to(REPO_ROOT)} — add index entry (or use scaffold command)")

        print(f"  ⚠ Run: python scripts/update_counts.py (updates README counts + version refs)")
        print(f"  ⚠ Run: python scripts/build_skill.py (updates Claude Code skill with new standard)")

        # Check module README
        module_readme = file_path.parent.parent / "README.md"
        if module_readme.exists():
            print(f"  ⚠ {module_readme.relative_to(REPO_ROOT)} — add row to standards table")

        # About page stats
        print(f"  ⚠ docs/about.md — stats card total may be stale")

        # Sources graph
        print(f"  ⚠ docs/sources-graph.md — if this standard connects to a source not already in the graph data, update the JavaScript arrays")

    # VS Code extension check
    rules_file = file_path.parent.parent / "rules.json"
    has_rule = False
    if rules_file.exists():
        import json
        with open(rules_file) as f:
            rules_data = json.load(f)
        has_rule = any(r.get("id", "").startswith(std_id) for r in rules_data.get("rules", []))

    if has_rule:
        print(f"  ✓ VS Code extension has a rule for {std_id}")
    else:
        category = std_id.split("-")[0]
        automatable_categories = {"SEC", "ENG", "PY", "JV", "TS", "ORG"}
        if category in automatable_categories:
            print(f"  ? VS Code extension — no rules.json entry for {std_id}. Can this be detected by regex? (scaffold command will ask)")
        else:
            print(f"  ○ VS Code extension — {category} standards typically aren't line-checkable (skip)")

    # Changelog
    print(f"  ⚠ CHANGELOG.md — document in next release notes")

    # Review (semantic - human needed)
    print(f"\n  REVIEW (human judgement):")

    # Check sources
    if file_path.exists():
        content = file_path.read_text()
        if "TODO" in content:
            print(f"  ! Standard has TODOs — fill in before merging")

        # Check if any URL in traceability points to a new domain
        trusted_file = REPO_ROOT / "scripts" / "trusted_sources.yaml"
        if trusted_file.exists():
            with open(trusted_file) as f:
                trusted = yaml.safe_load(f)
            domains = set(trusted.get("trusted_domains", []))

            import re
            # Only match URLs in the source traceability table (lines starting with |)
            traceability_urls = re.findall(r'\|\s*https?://([a-zA-Z0-9.-]+)', content)
            new_domains = [u for u in traceability_urls if not any(u == d or u.endswith("." + d) for d in domains)]
            if new_domains:
                print(f"  ! New source domain(s) detected — add to trusted_sources.yaml:")
                for d in set(new_domains):
                    print(f"      - {d}")
            else:
                print(f"  ✓ All source URLs are from trusted domains")

    print(f"  ? Does this standard contradict or overlap with any existing standard?")
    print(f"  ? Is the enforcement mechanism realistic for the teams who'll adopt it?")


def analyse_rules_change(file_path: Path) -> None:
    """Analyse impact of a rules.json change."""
    module_name = file_path.parent.name

    print(f"\n{'='*60}")
    print(f"  Impact analysis: rules.json ({module_name} module)")
    print(f"{'='*60}")

    print(f"\n  AUTOMATIC:")
    print(f"  ✓ VS Code extension picks up new rules at activation")
    print(f"  ✓ Build VS Code Extension workflow triggers on merge → .vsix rebuilt")

    print(f"\n  NEEDS ACTION:")
    print(f"  ⚠ modules/README.md — update 'Also checked in IDE' column if new rule added")
    print(f"  ⚠ vscode-extension/README.md — update the rules table for {module_name}")

    print(f"\n  REVIEW:")
    print(f"  ? Is the regex pattern tested? (check vscode-extension/src/test/suite/rulePatterns.test.ts)")
    print(f"  ? Does the pattern have false positives? (test against real code)")


def analyse_code_change(file_path: Path) -> None:
    """Analyse impact of a Python/TS source code change."""
    rel = file_path.relative_to(REPO_ROOT)

    print(f"\n{'='*60}")
    print(f"  Impact analysis: {rel}")
    print(f"{'='*60}")

    print(f"\n  NEEDS ACTION:")
    print(f"  ⚠ Add/update tests covering the change")
    print(f"  ⚠ Run: pytest (Python) or npm test (TypeScript)")

    # Identify what imports this file
    if str(rel).startswith("standards_lib/"):
        print(f"\n  FIRST-ORDER IMPACT (directly imports standards_lib):")
        print(f"    → scripts/query_standards.py")
        print(f"    → scripts/onboarding.py")
        print(f"    → scripts/suggest_standards.py")
        print(f"    → scripts/check_compliance.py")
        print(f"    → scripts/new_standard.py")
        print(f"    → mcp-server/server.py")
        print(f"    → tests/test_query.py")
        print(f"\n  SECOND-ORDER IMPACT (consumers of the above):")
        print(f"    → .github/workflows/compliance.yml (uses check_compliance.py)")
        print(f"    → .github/workflows/ci-code.yml (runs pytest)")
        print(f"    → All repos using the reusable GitHub Action")
    elif "vscode-extension" in str(rel):
        print(f"\n  FIRST-ORDER IMPACT:")
        print(f"    → VS Code extension behaviour changes")
        print(f"    → .github/workflows/build-extension.yml triggers rebuild")
        print(f"\n  SECOND-ORDER IMPACT:")
        print(f"    → All engineers using the extension get new behaviour on next download")
    elif str(rel).startswith("scripts/"):
        script_name = file_path.name
        print(f"\n  FIRST-ORDER IMPACT:")
        if script_name == "validate_standards.py":
            print(f"    → .github/workflows/ci-standards.yml (runs this script)")
            print(f"    → All PRs touching modules/ are affected")
        elif script_name == "update_counts.py":
            print(f"    → README.md and modules/README.md counts")
            print(f"    → .github/workflows/ci-standards.yml (verifies counts)")
        elif script_name == "check_compliance.py":
            print(f"    → .github/workflows/compliance.yml (reusable action)")
            print(f"    → All consuming repos' CI")
        elif script_name == "new_standard.py":
            print(f"    → Contributor workflow (scaffold command)")
            print(f"    → .github/workflows/generate-standard-from-issue.yml")
        else:
            print(f"    → Check who calls this script")

    print(f"\n  REVIEW:")
    print(f"  ? Does this break backwards compatibility?")
    print(f"  ? Are there consuming repos that might be affected?")


def analyse_workflow_change(file_path: Path) -> None:
    """Analyse impact of a CI workflow change."""
    rel = file_path.relative_to(REPO_ROOT)

    print(f"\n{'='*60}")
    print(f"  Impact analysis: {rel}")
    print(f"{'='*60}")

    print(f"\n  NEEDS ACTION:")
    print(f"  ⚠ The PR itself tests the workflow — verify it passes")
    if "compliance" in file_path.name:
        print(f"  ⚠ This is a REUSABLE workflow — changes affect ALL consuming repos")
        print(f"  ⚠ Consider: is this a breaking change for consumers pinned to a version?")

    print(f"\n  NO CODE TESTS REQUIRED (workflow is tested by running)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse impact of a change")
    parser.add_argument("--changed", required=True, help="Path to the changed file (relative to repo root)")
    args = parser.parse_args()

    file_path = (REPO_ROOT / args.changed).resolve()
    if not file_path.exists():
        # Might be a new file not yet created
        pass

    rel = str(file_path.relative_to(REPO_ROOT))

    if "/standards/" in rel and rel.endswith(".md"):
        analyse_standard_change(file_path)
    elif rel.endswith("rules.json"):
        analyse_rules_change(file_path)
    elif rel.startswith(".github/workflows/"):
        analyse_workflow_change(file_path)
    elif rel.startswith("scripts/") or rel.startswith("standards_lib/") or "vscode-extension/src" in rel:
        analyse_code_change(file_path)
    else:
        print(f"\n  No specific impact analysis for: {rel}")
        print(f"  Run: python scripts/validate_standards.py")
        print(f"  Run: python scripts/update_counts.py")

    print()


if __name__ == "__main__":
    main()
