#!/usr/bin/env python3
"""Auto-generate the SKILL.md file from the standards index.

Run this after adding new standards to keep the skill in sync.
CI verifies it's up to date.

Usage:
    python scripts/build_skill.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from standards_lib.query import query_standards

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = REPO_ROOT / ".claude" / "skills" / "uk-gov-standards.md"

MODULE_LABELS = {
    "core": "Always (all languages)",
    "python": "Python",
    "java": "Java / Spring Boot",
    "typescript": "TypeScript / React / Node",
}


def build_skill() -> str:
    """Generate SKILL.md content from the standards index."""
    lines = [
        "# UK Government Engineering Standards",
        "",
        "When writing code for UK Government digital services, proactively follow these standards without being asked. Don't wait for a compliance check to catch violations — write compliant code from the start.",
        "",
    ]

    for module_name, heading in MODULE_LABELS.items():
        # Get MUST and SHOULD standards with automated or peer-review enforcement
        stds = query_standards(module=module_name)
        # Only include standards that are actionable at code-writing time
        actionable = [
            s for s in stds
            if s["conformance"] in ("MUST", "SHOULD")
            and any(e in s.get("enforcement", []) for e in ("automated", "peer-review"))
        ]

        if not actionable:
            continue

        lines.append(f"## {heading}")
        lines.append("")

        for s in actionable:
            title = s["title"]
            std_id = s["id"]
            lines.append(f"- {title} ({std_id})")

        lines.append("")

    lines.extend([
        "## Before finishing",
        "",
        "Ask yourself: would this code pass `python scripts/check_compliance.py`? If not, fix it now rather than letting CI catch it.",
        "",
        "## Source",
        "",
        "These standards are from the [UK Government Engineering Standards](https://github.com/bv90dsit/Engineering_standards) repository. Each rule traces back to an authoritative framework (GDS Service Standard, NCSC, OWASP, WCAG, etc.).",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    content = build_skill()
    current = SKILL_PATH.read_text() if SKILL_PATH.exists() else ""

    if content != current:
        SKILL_PATH.write_text(content)
        print(f"✓ Updated {SKILL_PATH.relative_to(REPO_ROOT)}")
    else:
        print("Skill is up to date.")


if __name__ == "__main__":
    main()
