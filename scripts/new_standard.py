#!/usr/bin/env python3
"""Scaffold a new engineering standard with minimal input.

Usage:
    python scripts/new_standard.py --id PY-009 --module python \
        --title "Use virtual environments" --conformance SHOULD
"""

from __future__ import annotations

import argparse
import datetime
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"

# Mapping from ID prefix to default category
PREFIX_TO_CATEGORY = {
    "PY": "ENG",
    "TS": "ENG",
    "JAVA": "ENG",
    "ENG": "ENG",
    "SEC": "SEC",
    "OPS": "OPS",
    "ARC": "ARC",
    "DAT": "DAT",
    "ACC": "ACC",
    "EMG": "EMG",
    "ORG": "ENG",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a new engineering standard."
    )
    parser.add_argument(
        "--id", required=True, help="Standard ID, e.g. PY-009, SEC-008, ORG-003"
    )
    parser.add_argument(
        "--module",
        required=True,
        help="Module name (must exist under modules/)",
    )
    parser.add_argument("--title", required=True, help="Standard title")
    parser.add_argument(
        "--conformance",
        required=True,
        choices=["MUST", "SHOULD", "COULD"],
        help="Conformance level: MUST, SHOULD, or COULD",
    )
    parser.add_argument(
        "--category",
        default=None,
        help="Category (defaults to inferring from ID prefix)",
    )
    parser.add_argument(
        "--enforcement",
        default="peer-review",
        help="Comma-separated enforcement mechanisms (default: peer-review)",
    )
    parser.add_argument(
        "--platform",
        default=None,
        help="Platform (defaults to module's applies_to.platform from module.yaml, or 'any')",
    )
    parser.add_argument(
        "--tags", default=None, help="Comma-separated tags"
    )
    return parser.parse_args()


def infer_category(standard_id: str) -> str:
    """Infer category from the ID prefix."""
    prefix = standard_id.split("-")[0]
    return PREFIX_TO_CATEGORY.get(prefix, "ENG")


def get_module_platform(module_path: Path) -> str:
    """Read the platform from module.yaml, defaulting to 'any'."""
    module_yaml = module_path / "module.yaml"
    if not module_yaml.exists():
        return "any"
    with open(module_yaml) as f:
        data = yaml.safe_load(f)
    applies_to = data.get("applies_to", {})
    if applies_to and isinstance(applies_to, dict):
        return applies_to.get("platform", "any") or "any"
    return "any"


def id_exists_in_index(index_path: Path, standard_id: str) -> bool:
    """Check if the ID already exists in the module's standards-index.yaml."""
    if not index_path.exists():
        return False
    with open(index_path) as f:
        data = yaml.safe_load(f)
    standards = data.get("standards", []) if data else []
    return any(s.get("id") == standard_id for s in standards)


def generate_standard_md(
    standard_id: str,
    title: str,
    conformance: str,
    category: str,
    platform: str,
    source: str,
    tags: list[str],
    today: str,
) -> str:
    """Generate the markdown content for the new standard."""
    tags_str = ", ".join(tags)
    return f"""---
id: {standard_id}
title: {title}
conformance: {conformance}
category: {category}
applies_to:
  role: any
  platform: {platform}
source: {source}
tags: [{tags_str}]
last_reviewed: {today}
---

# {standard_id}: {title}

## Standard

TODO: Write a clear statement of what {conformance} be done.

## Rationale

TODO: Why this matters (2-4 bullet points).

## What good looks like

TODO: Concrete examples of compliance.

## Enforcement

| Mechanism | What is checked | When |
|-----------|----------------|------|
| **TODO** | TODO | TODO |

**Primary enforcement: TODO.**

## Source traceability

| Framework | Reference | URL | What it says |
|-----------|-----------|-----|--------------|
| TODO | TODO | TODO | "TODO" |
"""


def append_to_index(
    index_path: Path,
    standard_id: str,
    title: str,
    conformance: str,
    enforcement: list[str],
    platform: str,
    category: str,
    source: str,
    tags: list[str],
) -> None:
    """Append the new standard entry to the standards-index.yaml."""
    # Read the existing file content to append in the same format
    content = index_path.read_text() if index_path.exists() else "standards:\n"

    # Ensure file ends with a newline before we add
    if not content.endswith("\n"):
        content += "\n"

    # Build the new entry
    enforcement_str = "[" + ", ".join(enforcement) + "]"
    tags_str = "[" + ", ".join(tags) + "]"

    entry = f"""
  - id: {standard_id}
    title: {title}
    conformance: {conformance}
    enforcement: {enforcement_str}
    applies_to:
      role: any
      platform: {platform}
    category: {category}
    source: {source}
    tags: {tags_str}
"""

    index_path.write_text(content + entry)


def run_update_counts() -> bool:
    """Run scripts/update_counts.py to update README counts."""
    update_script = REPO_ROOT / "scripts" / "update_counts.py"
    if not update_script.exists():
        return False
    result = subprocess.run(
        [sys.executable, str(update_script)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return result.returncode == 0


def prompt_for_vscode_rule(standard_id: str, module_path: Path) -> bool:
    """Ask whether to add a VS Code rule and collect the pattern."""
    print()
    print("─" * 50)
    print("  VS Code Extension Rule")
    print("─" * 50)
    print()
    print("  Can this standard be detected by a regex pattern")
    print("  on a single line of code?")
    print()
    print("  Examples that CAN:  http:// URLs, print(), hardcoded secrets")
    print("  Examples that CAN'T: architecture decisions, SLOs, team process")
    print()

    answer = input("  Add a VS Code rule? (y/n): ").strip().lower()
    if answer != "y":
        return False

    print()
    file_pattern = input("  File pattern (e.g. **/*.py, **/*.{ts,tsx}): ").strip()
    if not file_pattern:
        file_pattern = "**/*"

    pattern = input("  Regex pattern to match violations: ").strip()
    if not pattern:
        print("  Skipped — no pattern provided.")
        return False

    severity = input("  Severity (error/warning/information) [warning]: ").strip()
    if severity not in ("error", "warning", "information"):
        severity = "warning"

    message = input(f"  Message shown to engineer [{standard_id}: ...]: ").strip()
    if not message:
        message = f"{standard_id}: Violation detected. See the standard for guidance."

    exclude_pattern = input("  Exclude pattern for comments (leave blank for default ^\\s*(#|//|\\*)): ").strip()
    if not exclude_pattern:
        exclude_pattern = "^\\s*(#|//|\\*)"

    exclude_file = input("  Exclude file pattern (e.g. **/test_*, leave blank for none): ").strip()

    # Build the rule
    import json as json_mod
    rule = {
        "id": standard_id,
        "pattern": pattern,
        "excludePattern": exclude_pattern,
        "filePattern": file_pattern,
        "severity": severity,
        "message": message,
    }
    if exclude_file:
        rule["excludeFilePattern"] = exclude_file

    # Append to rules.json
    rules_file = module_path / "rules.json"
    if rules_file.exists():
        with open(rules_file) as f:
            data = json_mod.load(f)
    else:
        data = {"module": module_path.name, "rules": []}

    data["rules"].append(rule)

    with open(rules_file, "w") as f:
        json_mod.dump(data, f, indent=2)

    print(f"  ✓ Added rule to {rules_file.relative_to(REPO_ROOT)}")
    return True


def main() -> int:
    args = parse_args()

    # Validate module exists
    module_path = MODULES_DIR / args.module
    if not module_path.is_dir():
        print(f"Error: Module '{args.module}' does not exist under modules/")
        print(f"Available modules: {', '.join(p.name for p in sorted(MODULES_DIR.iterdir()) if p.is_dir())}")
        return 1

    # Validate ID doesn't already exist
    index_path = module_path / "standards-index.yaml"
    if id_exists_in_index(index_path, args.id):
        print(f"Error: ID '{args.id}' already exists in {index_path.relative_to(REPO_ROOT)}")
        return 1

    # Resolve defaults
    category = args.category if args.category else infer_category(args.id)
    platform = args.platform if args.platform else get_module_platform(module_path)
    enforcement = [e.strip() for e in args.enforcement.split(",")]
    today = datetime.date.today().isoformat()

    # Resolve tags
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",")]
    else:
        tags = [platform, "TODO-add-tags"]

    source = "TODO-add-source"

    # Ensure standards directory exists
    standards_dir = module_path / "standards"
    standards_dir.mkdir(exist_ok=True)

    # Generate the .md file
    md_path = standards_dir / f"{args.id}.md"
    if md_path.exists():
        print(f"Error: File already exists: {md_path.relative_to(REPO_ROOT)}")
        return 1

    md_content = generate_standard_md(
        standard_id=args.id,
        title=args.title,
        conformance=args.conformance,
        category=category,
        platform=platform,
        source=source,
        tags=tags,
        today=today,
    )
    md_path.write_text(md_content)

    # Append to index
    append_to_index(
        index_path=index_path,
        standard_id=args.id,
        title=args.title,
        conformance=args.conformance,
        enforcement=enforcement,
        platform=platform,
        category=category,
        source=source,
        tags=tags,
    )

    # Add row to module README
    module_readme = module_path / "README.md"
    if module_readme.exists():
        readme_content = module_readme.read_text()
        # Find the table and append a row before the "How to use" section
        enforcement_str = ", ".join(enforcement)
        new_row = f"| {args.id} | {args.title} | {args.conformance} | {enforcement_str} | TODO |\n"
        # Insert before the last row or "How to use" heading
        if "## How to use" in readme_content:
            readme_content = readme_content.replace(
                "\n## How to use",
                f"{new_row}\n## How to use"
            )
            module_readme.write_text(readme_content)
            print(f"✓ Added row to {module_readme.relative_to(REPO_ROOT)}")

    # Run update_counts.py
    counts_updated = run_update_counts()

    # Print summary
    rel_md = md_path.relative_to(REPO_ROOT)
    rel_index = index_path.relative_to(REPO_ROOT)

    print(f"✓ Created {rel_md}")
    print(f"✓ Added to {rel_index}")
    if counts_updated:
        print("✓ Updated counts in README.md")
    else:
        print("! Could not update counts (run scripts/update_counts.py manually)")

    # Ask about VS Code rule
    rule_added = prompt_for_vscode_rule(args.id, module_path)

    print(f"\nNext steps:")
    print(f"  1. Fill in the TODO sections in {rel_md}")
    if not rule_added:
        print(f"  2. (Optional) Add a rules.json entry for VS Code line-level checking")
    print(f"  {'2' if rule_added else '3'}. Run: python scripts/validate_standards.py")
    print(f"  {'3' if rule_added else '4'}. Open a PR")
    if rule_added:
        print(f"\n  Note: When your PR merges, the VS Code extension rebuilds automatically.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
