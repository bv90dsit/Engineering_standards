"""Core query logic for the engineering standards library."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"
INDEX_PATH = REPO_ROOT / "standards-index.yaml"
STANDARDS_DIR = REPO_ROOT / "standards"


def _discover_modules() -> list[Path]:
    """Find all module directories that contain a standards-index.yaml."""
    if not MODULES_DIR.is_dir():
        return []
    return sorted(
        p.parent for p in MODULES_DIR.glob("*/standards-index.yaml")
    )


def _load_module_index(module_path: Path) -> list[dict]:
    """Load standards from a single module's index, tagging each with the module name."""
    index_file = module_path / "standards-index.yaml"
    try:
        with open(index_file) as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(
            f"Warning: Module index not found: {index_file}",
            file=sys.stderr,
        )
        return []
    except yaml.YAMLError as e:
        print(
            f"Warning: Failed to parse module index {index_file}: {e}",
            file=sys.stderr,
        )
        return []
    if data is None:
        return []
    standards = data.get("standards", [])
    module_name = module_path.name
    for s in standards:
        s["_module"] = module_name
    return standards


def load_index(module: Optional[str] = None) -> list[dict]:
    """Load standards from modules.

    Args:
        module: Filter to a specific module name, "all" for everything,
                or None for "core" only (backwards compatible).
    """
    modules = _discover_modules()

    if modules:
        if module == "all":
            standards = []
            for m in modules:
                standards.extend(_load_module_index(m))
            return standards
        elif module:
            matching = [m for m in modules if m.name == module]
            if not matching:
                raise ValueError(f"Module '{module}' not found. Available: {[m.name for m in modules]}")
            return _load_module_index(matching[0])
        else:
            core = [m for m in modules if m.name == "core"]
            if core:
                return _load_module_index(core[0])

    # Fallback: no modules directory, use root-level index (backwards compatible)
    if INDEX_PATH.exists():
        try:
            with open(INDEX_PATH) as f:
                data = yaml.safe_load(f)
        except FileNotFoundError:
            print(
                f"Warning: Standards index not found: {INDEX_PATH}",
                file=sys.stderr,
            )
            return []
        except yaml.YAMLError as e:
            print(
                f"Warning: Failed to parse standards index {INDEX_PATH}: {e}",
                file=sys.stderr,
            )
            return []
        if data is None:
            return []
        standards = data.get("standards", [])
        for s in standards:
            s["_module"] = "core"
        return standards

    return []


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
    module: Optional[str] = None,
) -> list[dict]:
    """Filter standards by context. All parameters are optional.

    Args:
        module: "core" (default), a specific module name, or "all".
    """
    standards = load_index(module=module)
    return [
        s
        for s in standards
        if _matches_context(s, role, platform, data_class, category, tag, enforcement, conformance)
    ]


def get_standard(standard_id: str) -> str:
    """Return the full markdown content of a single standard file.

    Searches across all modules for the standard ID.
    """
    # Search in modules first
    modules = _discover_modules()
    for m in modules:
        file_path = m / "standards" / f"{standard_id}.md"
        if file_path.exists():
            return file_path.read_text()

    # Fallback to root-level standards
    file_path = STANDARDS_DIR / f"{standard_id}.md"
    if file_path.exists():
        return file_path.read_text()

    searched_locations = [m.name for m in modules]
    if STANDARDS_DIR.is_dir():
        searched_locations.append(f"root ({STANDARDS_DIR})")
    raise FileNotFoundError(
        f"Standard file not found for ID: {standard_id}. "
        f"Searched modules: {searched_locations or ['(none — no modules directory found)']}"
    )


def list_modules() -> list[dict]:
    """Return metadata for all available modules."""
    modules = _discover_modules()
    result = []
    for m in modules:
        meta_file = m / "module.yaml"
        if meta_file.exists():
            try:
                with open(meta_file) as f:
                    meta = yaml.safe_load(f)
            except (yaml.YAMLError, OSError) as e:
                print(
                    f"Warning: Skipping module '{m.name}' — failed to load {meta_file}: {e}",
                    file=sys.stderr,
                )
                continue
            if meta is None:
                continue
            meta["path"] = str(m)
            result.append(meta)
    return result


def list_categories(module: Optional[str] = None) -> list[str]:
    """Return sorted unique categories from the index."""
    standards = load_index(module=module or "all")
    return sorted({s.get("category", "") for s in standards if s.get("category")})


def list_tags(module: Optional[str] = None) -> list[str]:
    """Return sorted unique tags from the index."""
    standards = load_index(module=module or "all")
    tags: set[str] = set()
    for s in standards:
        for t in s.get("tags", []):
            tags.add(t)
    return sorted(tags)


def to_json(standards: list[dict]) -> str:
    """Serialize a list of standard dicts to a JSON string."""
    return json.dumps(standards, indent=2, default=str)
