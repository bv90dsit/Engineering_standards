#!/usr/bin/env python3
"""Onboarding script — shows relevant standards and how to adopt them.

Usage:
    python scripts/onboarding.py --role engineer --platform python
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from standards_lib.query import query_standards

REPO_URL = "https://github.com/bv90dsit/Engineering_standards"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Onboarding guide — what standards apply and how to adopt them"
    )
    parser.add_argument("--role", required=True, help="Your role, e.g. engineer, architect, lead")
    parser.add_argument("--platform", required=True, help="Your platform, e.g. python, java, node, any")
    args = parser.parse_args()

    results = query_standards(role=args.role, platform=args.platform)

    if not results:
        print(f"No standards found for role={args.role}, platform={args.platform}.")
        sys.exit(0)

    must = [s for s in results if s.get("conformance") == "MUST"]
    should = [s for s in results if s.get("conformance") == "SHOULD"]
    could = [s for s in results if s.get("conformance") == "COULD"]

    automated = [s for s in must if "automated" in s.get("enforcement", [])]
    peer_review = [s for s in must if "peer-review" in s.get("enforcement", [])]
    audit = [s for s in must if "periodic-audit" in s.get("enforcement", []) and "automated" not in s.get("enforcement", [])]
    culture = [s for s in must if "ways-of-working" in s.get("enforcement", []) and "automated" not in s.get("enforcement", [])]

    print()
    print("=" * 66)
    print("  UK Government Engineering Standards — Onboarding")
    print(f"  Role: {args.role} | Platform: {args.platform}")
    print("=" * 66)
    print()
    print(f"  {len(results)} standards apply to you: {len(must)} MUST, {len(should)} SHOULD, {len(could)} COULD")
    print()
    print("─" * 66)
    print("  HOW TO ADOPT THESE STANDARDS IN YOUR SERVICE")
    print("─" * 66)
    print()
    print("  Step 1: Add the compliance check to your CI pipeline")
    print()
    print("    Add this to .github/workflows/ci.yml in YOUR repo:")
    print()
    print("    jobs:")
    print("      standards:")
    print(f"        uses: {REPO_URL.split('github.com/')[1]}/.github/workflows/compliance.yml@main")
    print("        with:")
    print(f"          role: {args.role}")
    print(f"          platform: {args.platform}")
    print()
    print("  Step 2: Fix the automated checks (these block your PR)")
    print()

    if automated:
        for s in automated:
            print(f"    [{s['id']}] {s['title']}")
            print(f"        → {_action_hint(s['id'])}")
            print()
    else:
        print("    (none — all MUST standards require manual verification)")
        print()

    print("  Step 3: Be aware of these during code review")
    print()
    if peer_review:
        for s in peer_review:
            print(f"    [{s['id']}] {s['title']}")
        print()
    else:
        print("    (none)")
        print()

    print("  Step 4: Prepare evidence for service assessment")
    print()
    if audit:
        for s in audit:
            print(f"    [{s['id']}] {s['title']}")
        print()
    else:
        print("    (none)")
        print()

    print("  Step 5: Agree these as team practices")
    print()
    if culture:
        for s in culture:
            print(f"    [{s['id']}] {s['title']}")
        print()
    else:
        print("    (none)")
        print()

    print("─" * 66)
    print("  FULL STANDARDS LIST")
    print("─" * 66)
    print()
    print(f"  {'ID':<10} {'Level':<8} {'Title':<45} {'Read'}")
    print(f"  {'─'*10} {'─'*7} {'─'*45} {'─'*30}")

    for s in results:
        url = f"{REPO_URL}/blob/main/standards/{s['id']}.md"
        print(f"  {s['id']:<10} {s['conformance']:<8} {s['title']:<45} {url}")

    print()
    print("─" * 66)
    print(f"  Browse all standards: {REPO_URL}")
    print(f"  Run compliance check: python scripts/check_compliance.py --repo-path .")
    print("─" * 66)
    print()


def _action_hint(std_id: str) -> str:
    """Quick hint on what to do to pass this check."""
    hints = {
        "ENG-001": "Add a LICENCE file (MIT or OGL v3) to your repo root",
        "ENG-002": "Ensure you have a git remote and branch protection enabled",
        "ENG-003": "Add a CI workflow in .github/workflows/ with automated tests",
        "SEC-001": "Replace any http:// URLs with https:// in source code",
        "SEC-002": "Add .github/dependabot.yml or configure Snyk/Renovate",
        "SEC-003": "Add secret scanning (detect-secrets in pre-commit, or GitHub secret scanning)",
        "SEC-004": "Add SAST tool (CodeQL or Semgrep) to your CI workflow",
        "EMG-003": "Add validation tests for any AI-generated output pipelines",
    }
    return hints.get(std_id, "See the standard file for guidance")


if __name__ == "__main__":
    main()
