#!/usr/bin/env python3
"""Build script for GitHub Pages site.

Copies all standards from modules/*/standards/*.md into docs/_standards/
with the appropriate frontmatter additions (layout and module fields).
"""

import os
import re
import shutil
from pathlib import Path


def extract_frontmatter(content: str) -> tuple[str, str]:
    """Extract YAML frontmatter and body from a markdown file.

    Returns:
        Tuple of (frontmatter_text, body_text). Frontmatter does NOT include
        the --- delimiters.
    """
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def add_frontmatter_fields(frontmatter: str, fields: dict[str, str]) -> str:
    """Add fields to YAML frontmatter text if not already present."""
    for key, value in fields.items():
        # Check if field already exists
        if not re.search(rf"^{key}:", frontmatter, re.MULTILINE):
            frontmatter += f"\n{key}: {value}"
    return frontmatter


def main():
    # Resolve paths relative to this script's location
    repo_root = Path(__file__).resolve().parent.parent
    standards_output = repo_root / "docs" / "_standards"
    modules_dir = repo_root / "modules"

    # Clean output directory
    if standards_output.exists():
        shutil.rmtree(standards_output)
    standards_output.mkdir(parents=True, exist_ok=True)

    # Find all standard files
    standard_files = sorted(modules_dir.glob("*/standards/*.md"))

    count = 0
    for filepath in standard_files:
        # Determine module name from path: modules/<module_name>/standards/file.md
        module_name = filepath.parent.parent.name

        content = filepath.read_text(encoding="utf-8")
        frontmatter, body = extract_frontmatter(content)

        if not frontmatter:
            print(f"  Skipping {filepath.name} (no frontmatter)")
            continue

        # Extract the standard ID from frontmatter for use as standard_id
        # (Jekyll overrides page.id for collection documents)
        id_match = re.search(r"^id:\s*(.+)$", frontmatter, re.MULTILINE)
        standard_id = id_match.group(1).strip() if id_match else filepath.stem

        # Add layout, module, standard_id, and disable Liquid parsing
        # (standards contain {{ }} in code examples which Jekyll misinterprets)
        frontmatter = add_frontmatter_fields(frontmatter, {
            "layout": "standard",
            "module": module_name,
            "standard_id": standard_id,
            "render_with_liquid": "false",
        })

        # Wrap body in {% raw %} to prevent Jekyll Liquid parsing
        # (standards contain {{ }} in code examples)
        body = "{% raw %}\n" + body + "\n{% endraw %}"

        # Write to output
        output_file = standards_output / filepath.name
        output_content = f"---\n{frontmatter}\n---\n{body}"
        output_file.write_text(output_content, encoding="utf-8")
        count += 1

    print(f"Copied {count} standards to {standards_output}")


if __name__ == "__main__":
    main()
