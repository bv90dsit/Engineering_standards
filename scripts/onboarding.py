#!/usr/bin/env python3
"""Onboarding script — shows relevant standards for a given role and platform.

Usage:
    python scripts/onboarding.py --role engineer --platform python
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

# Ensure the package is importable when running the script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from standards_lib.query import query_standards, STANDARDS_DIR


def format_enforcement(enforcement: list) -> str:
    """Format enforcement list into a readable string."""
    return ", ".join(enforcement)


def print_grouped_standards(standards: list[dict], header: str) -> None:
    """Print standards grouped by category under a header."""
    if not standards:
        return

    grouped: dict[str, list[dict]] = defaultdict(list)
    for s in standards:
        grouped[s.get("category", "OTHER")].append(s)

    print(f"\n{'=' * 60}")
    print(f"  {header}")
    print(f"{'=' * 60}")

    for category in sorted(grouped.keys()):
        print(f"\n  [{category}]")
        print(f"  {'-' * 40}")
        for s in grouped[category]:
            std_id = s["id"]
            title = s["title"]
            enforcement = format_enforcement(s.get("enforcement", []))
            file_path = STANDARDS_DIR / f"{std_id}.md"
            print(f"    {std_id}: {title}")
            print(f"      Enforcement: {enforcement}")
            print(f"      Read more: {file_path}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Onboarding guide — lists standards relevant to your role and platform"
    )
    parser.add_argument("--role", required=True, help="Your role, e.g. engineer, architect, lead")
    parser.add_argument("--platform", required=True, help="Your platform, e.g. python, java, node, any")
    args = parser.parse_args()

    results = query_standards(role=args.role, platform=args.platform)

    if not results:
        print(f"No standards found for role={args.role}, platform={args.platform}.")
        sys.exit(0)

    # Welcome message
    print()
    print("*" * 60)
    print(f"  Welcome to the Engineering Standards Onboarding!")
    print(f"  Role: {args.role} | Platform: {args.platform}")
    print("*" * 60)
    print()
    print(f"  There are {len(results)} standard(s) that apply to your context.")
    print(f"  Below they are grouped by conformance level and category.")

    # Separate by conformance
    must_standards = [s for s in results if s.get("conformance") == "MUST"]
    should_standards = [s for s in results if s.get("conformance") == "SHOULD"]
    could_standards = [s for s in results if s.get("conformance") == "COULD"]

    print_grouped_standards(must_standards, "MUST — You are required to comply with these")
    print_grouped_standards(should_standards, "SHOULD — Strongly recommended")
    print_grouped_standards(could_standards, "COULD — Optional, but encouraged")

    print(f"\n{'=' * 60}")
    print("  For full details on any standard, open the linked file.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
