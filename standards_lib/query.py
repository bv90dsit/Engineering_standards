"""Core query logic for the engineering standards library."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import yaml

INDEX_PATH = Path(__file__).resolve().parent.parent / "standards-index.yaml"
STANDARDS_DIR = Path(__file__).resolve().parent.parent / "standards"


def load_index() -> list[dict]:
    """Load and return the list of standard dicts from the index YAML."""
    with open(INDEX_PATH) as f:
        data = yaml.safe_load(f)
    return data["standards"]


def _matches_context(
    standard: dict,
    role: str | None,
    platform: str | None,
    data_class: str | None,
    category: str | None,
    tag: str | None,
    enforcement: str | None,
    conformance: str | None,
) -> bool:
    """Return True if standard matches all provided filter criteria."""
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

    if enforcement:
        std_enforcement = standard.get("enforcement", [])
        if enforcement not in std_enforcement:
            return False

    if conformance and standard.get("conformance") != conformance:
        return False

    return True


def query_standards(
    role: Optional[str] = None,
    platform: Optional[str] = None,
    data_class: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    enforcement: Optional[str] = None,
    conformance: Optional[str] = None,
) -> list[dict]:
    """Filter standards by context. All parameters are optional."""
    standards = load_index()
    return [
        s
        for s in standards
        if _matches_context(s, role, platform, data_class, category, tag, enforcement, conformance)
    ]


def get_standard(standard_id: str) -> str:
    """Return the full markdown content of a single standard file."""
    file_path = STANDARDS_DIR / f"{standard_id}.md"
    if not file_path.exists():
        raise FileNotFoundError(f"Standard file not found: {file_path}")
    return file_path.read_text()


def list_categories() -> list[str]:
    """Return sorted unique categories from the index."""
    standards = load_index()
    return sorted({s.get("category", "") for s in standards if s.get("category")})


def list_tags() -> list[str]:
    """Return sorted unique tags from the index."""
    standards = load_index()
    tags: set[str] = set()
    for s in standards:
        for t in s.get("tags", []):
            tags.add(t)
    return sorted(tags)


def to_json(standards: list[dict]) -> str:
    """Serialize a list of standard dicts to a JSON string."""
    return json.dumps(standards, indent=2, default=str)
