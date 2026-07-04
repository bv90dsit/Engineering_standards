#!/usr/bin/env python3
"""Query the engineering standards index by context.

Usage:
    python query_standards.py --role engineer --platform python --data-class OFFICIAL
    python query_standards.py --category SEC
    python query_standards.py --tag ai
"""

import argparse
import sys
from pathlib import Path

import yaml


INDEX_PATH = Path(__file__).resolve().parent.parent / "standards-index.yaml"


def load_index() -> list[dict]:
    with open(INDEX_PATH) as f:
        data = yaml.safe_load(f)
    return data["standards"]


def matches_context(standard: dict, role: str | None, platform: str | None,
                    data_class: str | None, category: str | None, tag: str | None) -> bool:
    applies = standard.get("applies_to", {})

    if role:
        std_role = applies.get("role", "any")
        if std_role != "any" and role not in std_role.split(","):
            return False

    if platform:
        std_platform = applies.get("platform", "any")
        if std_platform != "any" and platform not in std_platform.split(","):
            return False

    if category and standard.get("category") != category:
        return False

    if tag and tag not in standard.get("tags", []):
        return False

    return True


def query_standards(role=None, platform=None, data_class=None, category=None, tag=None) -> list[dict]:
    standards = load_index()
    return [s for s in standards if matches_context(s, role, platform, data_class, category, tag)]


def main():
    parser = argparse.ArgumentParser(description="Query UK Gov engineering standards by context")
    parser.add_argument("--role", help="e.g. engineer, architect, lead")
    parser.add_argument("--platform", help="e.g. python, java, node, any")
    parser.add_argument("--data-class", help="e.g. OFFICIAL, OFFICIAL-SENSITIVE, SECRET")
    parser.add_argument("--category", help="e.g. ENG, SEC, ARC, OPS, EMG")
    parser.add_argument("--tag", help="filter by tag")
    parser.add_argument("--conformance", help="filter by conformance level: MUST, SHOULD, COULD")
    args = parser.parse_args()

    results = query_standards(
        role=args.role,
        platform=args.platform,
        data_class=args.data_class,
        category=args.category,
        tag=args.tag,
    )

    if args.conformance:
        results = [r for r in results if r.get("conformance") == args.conformance]

    if not results:
        print("No standards match the given context.")
        sys.exit(0)

    print(f"{'ID':<10} {'Conformance':<12} {'Title'}")
    print("-" * 60)
    for s in results:
        print(f"{s['id']:<10} {s['conformance']:<12} {s['title']}")

    print(f"\n{len(results)} standard(s) matched.")


if __name__ == "__main__":
    main()
