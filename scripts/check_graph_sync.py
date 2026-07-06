#!/usr/bin/env python3
"""Check that sources-graph.md data matches actual source traceability tables.

Exits 0 if in sync, 1 if drift detected. Used in CI to prevent graph staleness.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"
GRAPH_FILE = REPO_ROOT / "docs" / "sources-graph.md"

SOURCE_MAP = {
    "Technology Code of Practice": "tcop",
    "GDS Service Standard": "gds",
    "GDS Service Manual": "gds",
    "GDS Progressive Enhancement": "gds",
    "GDS": "gds",
    "GDS API Standards": "gds",
    "NCSC Secure by Design": "ncsc",
    "NCSC Secure Development": "ncsc",
    "NCSC Cloud Security": "ncsc",
    "NCSC Cloud Security Principles": "ncsc",
    "NCSC": "ncsc",
    "OWASP Top 10": "owasp",
    "OWASP ASVS": "owasp",
    "OWASP API Security": "owasp",
    "OWASP": "owasp",
    "WCAG 2.2": "wcag",
    "NIST SP 800-53": "nist",
    "NIST SP 800-63": "nist",
    "NIST SP 800-190": "nist",
    "ISO 27001": "nist",
    "ISO 22301": "nist",
    "UK GDPR": "ukgdpr",
    "ICO": "ukgdpr",
    "Public Sector Bodies Accessibility Regulations 2018": "accessibility",
    "CDDO Generative AI Framework": "cddo-ai",
    "CDDO": "cddo-ai",
    "Government Security Classifications": "gsc",
    "Cabinet Office SPF": "gsc",
    "Cabinet Office": "gsc",
    "IETF": "ietf",
    "Government Cloud First policy": "tcop",
    "DORA Metrics": "dora",
    "DORA State of DevOps": "dora",
    "DORA": "dora",
    "12-Factor App": "12factor",
    "Google SRE Book": "sre",
    "Google Engineering": "sre",
    "AWS Well-Architected": "aws-wa",
    "Accelerate": "accelerate",
    "OpenAPI Initiative": "openapi",
    "Spring Framework": "spring",
    "Spring Framework docs": "spring",
    "Spring Data JPA": "spring",
    "Spring Security": "spring",
    "Spring docs": "spring",
    "Python docs": "python-docs",
    "PEP 484": "python-docs",
    "PEP 8": "python-docs",
    "PEP 428": "python-docs",
    "Django docs": "django",
    "Django": "django",
    "TypeScript Handbook": "typescript",
    "TypeScript docs": "typescript",
    "React docs": "react",
    "React": "react",
    "MDN": "mdn",
}


def extract_traceability() -> dict[str, set[str]]:
    """Scan all standards and build node_id -> set of standard IDs."""
    node_standards: dict[str, set[str]] = defaultdict(set)

    for filepath in sorted(MODULES_DIR.glob("*/standards/*.md")):
        content = filepath.read_text(encoding="utf-8")

        id_match = re.search(r"^id:\s*(.+)$", content, re.MULTILINE)
        if not id_match:
            continue
        std_id = id_match.group(1).strip()

        trace_match = re.search(r"## Source traceability\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        if not trace_match:
            continue

        table_text = trace_match.group(1)
        for row in table_text.strip().split("\n"):
            if not row.startswith("|") or row.startswith("|---") or row.startswith("| Framework"):
                continue
            cols = [c.strip() for c in row.split("|")]
            if len(cols) < 3:
                continue
            framework = cols[1]
            node_id = SOURCE_MAP.get(framework)
            if node_id:
                node_standards[node_id].add(std_id)

    return node_standards


def extract_graph_data() -> dict[str, set[str]]:
    """Parse the JavaScript data from sources-graph.md."""
    content = GRAPH_FILE.read_text(encoding="utf-8")

    node_standards: dict[str, set[str]] = {}

    pattern = re.compile(
        r'\{\s*id:\s*"([^"]+)".*?standards:\s*\[([^\]]*)\]',
        re.DOTALL,
    )

    for match in pattern.finditer(content):
        node_id = match.group(1)
        standards_str = match.group(2)
        standards = set(re.findall(r'"([^"]+)"', standards_str))
        node_standards[node_id] = standards

    return node_standards


def main() -> int:
    expected = extract_traceability()
    actual = extract_graph_data()

    all_nodes = sorted(set(expected.keys()) | set(actual.keys()))
    drift_found = False

    for node_id in all_nodes:
        exp = expected.get(node_id, set())
        act = actual.get(node_id, set())

        missing = sorted(exp - act)
        extra = sorted(act - exp)

        if missing:
            print(f"  {node_id}: missing from graph: {missing}")
            drift_found = True
        if extra:
            print(f"  {node_id}: in graph but not in traceability: {extra}")
            drift_found = True

    if drift_found:
        print("\n✗ Graph data is out of sync with source traceability tables.")
        print("  Run /rebuild-graph or manually update docs/sources-graph.md")
        return 1
    else:
        print("✓ Graph data matches source traceability tables.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
