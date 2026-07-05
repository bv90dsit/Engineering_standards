#!/usr/bin/env python3
"""Auto-update standard counts and version references in README files.

Run this after adding/removing standards or cutting a new release.
CI will fail if counts or versions are stale.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"
README = REPO_ROOT / "README.md"
MODULES_README = MODULES_DIR / "README.md"

VERSION_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "usage-by-role.md",
    REPO_ROOT / ".github" / "workflows" / "compliance.yml",
    REPO_ROOT / "scripts" / "onboarding.py",
    REPO_ROOT / "vscode-extension" / "README.md",
]


def load_all_standards() -> dict[str, list[dict]]:
    """Load standards per module."""
    result = {}
    for module_path in sorted(MODULES_DIR.iterdir()):
        index_file = module_path / "standards-index.yaml"
        if not index_file.exists():
            continue
        with open(index_file) as f:
            data = yaml.safe_load(f)
        result[module_path.name] = data.get("standards", [])
    return result


def count_conformance(all_standards: list[dict]) -> dict[str, int]:
    counts = {"MUST": 0, "SHOULD": 0, "COULD": 0}
    for s in all_standards:
        level = s.get("conformance", "")
        if level in counts:
            counts[level] += 1
    return counts


def update_main_readme(modules: dict[str, list[dict]]) -> bool:
    all_standards = [s for standards in modules.values() for s in standards]
    total = len(all_standards)
    conformance = count_conformance(all_standards)

    content = README.read_text()
    original = content

    # Update opening line count
    content = re.sub(
        r'\d+ standards across \d+ modules',
        f'{total} standards across {len(modules)} modules',
        content
    )

    # Update conformance counts
    content = re.sub(
        r'\*\*MUST\*\* \(\d+\)',
        f'**MUST** ({conformance["MUST"]})',
        content
    )
    content = re.sub(
        r'\*\*SHOULD\*\* \(\d+\)',
        f'**SHOULD** ({conformance["SHOULD"]})',
        content
    )
    content = re.sub(
        r'\*\*COULD\*\* \(\d+\)',
        f'**COULD** ({conformance["COULD"]})',
        content
    )

    # Update module table counts
    module_descriptions = {
        "core": "Cross-cutting UK Gov (security, ops, architecture, data, accessibility, AI)",
        "python": "Python + Django + Flask",
        "java": "Java + Spring Boot",
        "typescript": "TypeScript + React + Node",
        "org-example": "Demonstrates how an org adds custom rules",
    }

    for name, standards in modules.items():
        desc = module_descriptions.get(name, "")
        old_pattern = rf'\| \[{name}\]\(modules/{name}/\) \| \d+ \|'
        new_value = f'| [{name}](modules/{name}/) | {len(standards)} |'
        content = re.sub(old_pattern, new_value, content)

    # Update total in "What's in the box" table
    content = re.sub(
        r'\| \d+ standards',
        f'| {total} standards',
        content
    )

    if content != original:
        README.write_text(content)
        return True
    return False


def update_modules_readme(modules: dict[str, list[dict]]) -> bool:
    content = MODULES_README.read_text()
    original = content

    # Update total
    total = sum(len(s) for s in modules.values())
    content = re.sub(
        r'\*\*Total: \d+ standards\*\*',
        f'**Total: {total} standards**',
        content
    )

    # Update per-module counts in the table
    for name, standards in modules.items():
        old_pattern = rf'(\| \[{name}\]\({name}/\) \| [^|]+ \| )\d+( \|)'
        new_value = rf'\g<1>{len(standards)}\2'
        content = re.sub(old_pattern, new_value, content)

    if content != original:
        MODULES_README.write_text(content)
        return True
    return False


def get_latest_version() -> str | None:
    """Get the latest git tag (assumes semver tags like v1.0.0)."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def update_version_references(version: str) -> list[str]:
    """Update all @vX.Y.Z and vsix filename version references."""
    at_pattern = re.compile(r"@v\d+\.\d+\.\d+")
    vsix_pattern = re.compile(r"uk-gov-engineering-standards-\d+\.\d+\.\d+\.vsix")
    bare_version = version.lstrip("v")
    changed_files = []

    for file_path in VERSION_FILES:
        if not file_path.exists():
            continue
        content = file_path.read_text()
        updated = at_pattern.sub(f"@{version}", content)
        updated = vsix_pattern.sub(f"uk-gov-engineering-standards-{bare_version}.vsix", updated)
        if updated != content:
            file_path.write_text(updated)
            changed_files.append(str(file_path.relative_to(REPO_ROOT)))

    return changed_files


def main() -> int:
    modules = load_all_standards()
    total = sum(len(s) for s in modules.values())

    print(f"Found {total} standards across {len(modules)} modules:")
    for name, standards in modules.items():
        print(f"  {name}: {len(standards)}")

    changed_main = update_main_readme(modules)
    changed_modules = update_modules_readme(modules)

    # Update version references
    latest_version = get_latest_version()
    changed_version_files: list[str] = []
    if latest_version:
        changed_version_files = update_version_references(latest_version)
        if changed_version_files:
            print(f"\nVersion references updated to {latest_version} in: {', '.join(changed_version_files)}")
    else:
        print("\nNo git tags found — skipping version reference update.")

    all_changed = []
    if changed_main:
        all_changed.append("README.md")
    if changed_modules:
        all_changed.append("modules/README.md")
    all_changed.extend(changed_version_files)

    if all_changed:
        print(f"\nUpdated: {', '.join(set(all_changed))}")
        print("Commit these changes.")
    else:
        print("\nAll counts and versions are up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
