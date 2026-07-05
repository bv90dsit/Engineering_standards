#!/usr/bin/env python3
"""Validate all standards have correct format, matching index entries, and no orphans."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"
TRUSTED_SOURCES_FILE = Path(__file__).resolve().parent / "trusted_sources.yaml"

REQUIRED_FRONTMATTER = {"id", "title", "conformance", "category", "applies_to", "source", "tags", "last_reviewed"}
REQUIRED_INDEX_FIELDS = {"id", "title", "conformance", "enforcement", "applies_to", "category", "source", "tags"}
REQUIRED_RULES_FIELDS = {"id", "pattern", "filePattern", "severity", "message"}
VALID_CONFORMANCE = {"MUST", "SHOULD", "COULD"}
VALID_ENFORCEMENT = {"automated", "peer-review", "periodic-audit", "ways-of-working"}
VALID_SEVERITY = {"error", "warning", "information"}


def load_trusted_domains() -> set[str]:
    if not TRUSTED_SOURCES_FILE.exists():
        return set()
    with open(TRUSTED_SOURCES_FILE) as f:
        data = yaml.safe_load(f)
    return set(data.get("trusted_domains", []))

errors: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def validate_frontmatter(file_path: Path, content: str) -> dict | None:
    if not content.startswith("---"):
        error(f"{file_path}: Missing YAML frontmatter (must start with ---)")
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        error(f"{file_path}: Invalid frontmatter (missing closing ---)")
        return None

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        error(f"{file_path}: Invalid YAML in frontmatter: {e}")
        return None

    if not isinstance(fm, dict):
        error(f"{file_path}: Frontmatter is not a dict")
        return None

    missing = REQUIRED_FRONTMATTER - set(fm.keys())
    if missing:
        error(f"{file_path}: Missing frontmatter fields: {', '.join(sorted(missing))}")

    if fm.get("conformance") not in VALID_CONFORMANCE:
        error(f"{file_path}: Invalid conformance '{fm.get('conformance')}' (must be MUST/SHOULD/COULD)")

    return fm


def validate_body(file_path: Path, content: str, trusted_domains: set[str]) -> None:
    if "## Enforcement" not in content:
        error(f"{file_path}: Missing '## Enforcement' section")

    if "## Source traceability" not in content:
        error(f"{file_path}: Missing '## Source traceability' section")

    if "| Framework | Reference | URL | What it says |" not in content:
        error(f"{file_path}: Source traceability table not in 4-column format (Framework | Reference | URL | What it says)")
        return

    # Extract source traceability rows and validate
    in_table = False
    header_seen = False
    for line in content.split("\n"):
        if "| Framework | Reference | URL | What it says |" in line:
            in_table = True
            header_seen = True
            continue
        if in_table and line.startswith("|--"):
            continue
        if in_table and line.startswith("|"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) < 4:
                error(f"{file_path}: Source traceability row has fewer than 4 columns")
                continue

            framework, reference, url, what_it_says = cols[0], cols[1], cols[2], cols[3]

            # Completeness: no TODOs or blanks
            if "TODO" in framework or not framework:
                error(f"{file_path}: Source traceability has TODO/blank in Framework column")
            if "TODO" in reference or not reference:
                error(f"{file_path}: Source traceability has TODO/blank in Reference column")
            if "TODO" in url:
                error(f"{file_path}: Source traceability has TODO in URL column")
            if "TODO" in what_it_says or not what_it_says:
                error(f"{file_path}: Source traceability has TODO/blank in 'What it says' column")

            # Trusted sources: validate URL domain
            if url and url != "—" and url.startswith("http"):
                domain = url.split("//")[1].split("/")[0].split(":")[0]
                if not any(domain == d or domain.endswith("." + d) for d in trusted_domains):
                    error(f"{file_path}: URL domain '{domain}' is not in trusted_sources.yaml. Add it if it's an authoritative source.")
        elif in_table and header_seen:
            break  # end of table


def validate_index(module_path: Path) -> set[str]:
    index_file = module_path / "standards-index.yaml"
    if not index_file.exists():
        error(f"{module_path.name}: Missing standards-index.yaml")
        return set()

    try:
        with open(index_file) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        error(f"{index_file}: Invalid YAML: {e}")
        return set()

    standards = data.get("standards", [])
    if not isinstance(standards, list):
        error(f"{index_file}: 'standards' must be a list")
        return set()

    ids = set()
    for i, entry in enumerate(standards):
        if not isinstance(entry, dict):
            error(f"{index_file}: Entry {i} is not a dict")
            continue

        missing = REQUIRED_INDEX_FIELDS - set(entry.keys())
        if missing:
            error(f"{index_file}: Entry '{entry.get('id', f'#{i}')}' missing fields: {', '.join(sorted(missing))}")

        std_id = entry.get("id", "")
        ids.add(std_id)

        if entry.get("conformance") not in VALID_CONFORMANCE:
            error(f"{index_file}: '{std_id}' invalid conformance '{entry.get('conformance')}'")

        enforcement = entry.get("enforcement", [])
        if not isinstance(enforcement, list):
            error(f"{index_file}: '{std_id}' enforcement must be a list")
        else:
            for e in enforcement:
                if e not in VALID_ENFORCEMENT:
                    error(f"{index_file}: '{std_id}' invalid enforcement '{e}'")

    return ids


def validate_rules_json(module_path: Path) -> None:
    rules_file = module_path / "rules.json"
    if not rules_file.exists():
        return

    try:
        with open(rules_file) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        error(f"{rules_file}: Invalid JSON: {e}")
        return

    rules = data.get("rules", [])
    if not isinstance(rules, list):
        error(f"{rules_file}: 'rules' must be a list")
        return

    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            error(f"{rules_file}: Rule {i} is not a dict")
            continue

        missing = REQUIRED_RULES_FIELDS - set(rule.keys())
        if missing:
            error(f"{rules_file}: Rule '{rule.get('id', f'#{i}')}' missing fields: {', '.join(sorted(missing))}")

        if rule.get("severity") not in VALID_SEVERITY:
            error(f"{rules_file}: Rule '{rule.get('id', f'#{i}')}' invalid severity '{rule.get('severity')}'")


def validate_module(module_path: Path, trusted_domains: set[str]) -> None:
    module_name = module_path.name

    # Validate module.yaml exists
    module_yaml = module_path / "module.yaml"
    if not module_yaml.exists():
        error(f"{module_name}: Missing module.yaml")

    # Validate index and get IDs
    index_ids = validate_index(module_path)

    # Validate each standard file
    standards_dir = module_path / "standards"
    if not standards_dir.is_dir():
        error(f"{module_name}: Missing standards/ directory")
        return

    file_ids = set()
    for md_file in sorted(standards_dir.glob("*.md")):
        content = md_file.read_text()
        fm = validate_frontmatter(md_file, content)
        if fm:
            file_ids.add(fm.get("id", ""))
        validate_body(md_file, content, trusted_domains)

    # Check for orphans (in index but no file)
    index_only = index_ids - file_ids
    if index_only:
        error(f"{module_name}: In index but no .md file: {', '.join(sorted(index_only))}")

    # Check for orphans (file exists but not in index)
    file_only = file_ids - index_ids
    if file_only:
        error(f"{module_name}: .md file exists but not in index: {', '.join(sorted(file_only))}")

    # Validate rules.json
    validate_rules_json(module_path)


def main() -> int:
    if not MODULES_DIR.is_dir():
        print("ERROR: modules/ directory not found")
        return 1

    modules = sorted(p for p in MODULES_DIR.iterdir() if p.is_dir() and (p / "standards-index.yaml").exists())
    trusted_domains = load_trusted_domains()

    print(f"Validating {len(modules)} modules ({len(trusted_domains)} trusted source domains loaded)...")

    for module_path in modules:
        validate_module(module_path, trusted_domains)

    if errors:
        print(f"\n{'='*60}")
        print(f"VALIDATION FAILED — {len(errors)} error(s):")
        print(f"{'='*60}\n")
        for err in errors:
            print(f"  ✗ {err}")
        print()
        return 1
    else:
        total = sum(
            len(list((m / "standards").glob("*.md")))
            for m in modules if (m / "standards").is_dir()
        )
        print(f"\n✓ All {total} standards across {len(modules)} modules validated successfully.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
