#!/usr/bin/env python3
"""Auto-update standard counts in README files.

Run this after adding/removing standards. CI will fail if counts are stale.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"
README = REPO_ROOT / "README.md"
MODULES_README = MODULES_DIR / "README.md"


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


def main() -> int:
    modules = load_all_standards()
    total = sum(len(s) for s in modules.values())

    print(f"Found {total} standards across {len(modules)} modules:")
    for name, standards in modules.items():
        print(f"  {name}: {len(standards)}")

    changed_main = update_main_readme(modules)
    changed_modules = update_modules_readme(modules)

    if changed_main or changed_modules:
        files = []
        if changed_main:
            files.append("README.md")
        if changed_modules:
            files.append("modules/README.md")
        print(f"\nUpdated: {', '.join(files)}")
        print("Commit these changes.")
        return 0
    else:
        print("\nAll counts are up to date.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
