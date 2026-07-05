#!/usr/bin/env python3
"""Query the engineering standards index by context.

Usage:
    python query_standards.py --role engineer --platform python --data-class OFFICIAL
    python query_standards.py --category SEC
    python query_standards.py --tag ai
    python query_standards.py --enforcement automated
    python query_standards.py --role engineer --json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the package is importable when running the script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from standards_lib.query import query_standards, list_modules, to_json


def main():
    parser = argparse.ArgumentParser(description="Query UK Gov engineering standards by context")
    parser.add_argument("--role", help="e.g. engineer, architect, lead")
    parser.add_argument("--platform", help="e.g. python, java, node, any")
    parser.add_argument("--data-class", help="e.g. OFFICIAL, OFFICIAL-SENSITIVE, SECRET")
    parser.add_argument("--category", help="e.g. ENG, SEC, ARC, OPS, EMG")
    parser.add_argument("--tag", help="filter by tag")
    parser.add_argument("--enforcement", help="filter by enforcement type: automated, peer-review, periodic-audit, ways-of-working")
    parser.add_argument("--conformance", help="filter by conformance level: MUST, SHOULD, COULD")
    parser.add_argument("--module", help="module to query: core (default), python, org-example, or 'all'")
    parser.add_argument("--list-modules", action="store_true", help="list available modules and exit")
    parser.add_argument("--json", action="store_true", dest="json_output", help="output results as JSON")
    args = parser.parse_args()

    if args.list_modules:
        for m in list_modules():
            print(f"  {m['name']:<15} {m.get('description', '')}")
        sys.exit(0)

    results = query_standards(
        role=args.role,
        platform=args.platform,
        data_class=args.data_class,
        category=args.category,
        tag=args.tag,
        enforcement=args.enforcement,
        conformance=args.conformance,
        module=args.module,
    )

    if not results:
        print("No standards match the given context.")
        sys.exit(0)

    if args.json_output:
        print(to_json(results))
    else:
        print(f"{'ID':<10} {'Conformance':<12} {'Title'}")
        print("-" * 60)
        for s in results:
            print(f"{s['id']:<10} {s['conformance']:<12} {s['title']}")
        print(f"\n{len(results)} standard(s) matched.")


if __name__ == "__main__":
    main()
