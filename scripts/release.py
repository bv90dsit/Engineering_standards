#!/usr/bin/env python3
"""Create a new release of the engineering standards.

Usage:
    python scripts/release.py --version v1.0.0
    python scripts/release.py --version v1.1.0 --dry-run
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=REPO_ROOT, check=check, capture_output=capture, text=True)


def validate_version(version: str) -> None:
    if not re.match(r"^v\d+\.\d+\.\d+$", version):
        print(f"ERROR: Version must be in format vX.Y.Z, got '{version}'")
        sys.exit(1)


def check_clean_tree() -> None:
    result = run(["git", "status", "--porcelain"], capture=True)
    if result.stdout.strip():
        print("ERROR: Working tree is not clean. Commit or stash changes first.")
        print(result.stdout)
        sys.exit(1)


def check_tag_exists(version: str) -> bool:
    result = run(["git", "tag", "-l", version], capture=True)
    return version in result.stdout


def run_validation() -> None:
    print("Running validation...")
    result = run(["python3", "scripts/validate_standards.py"], check=False, capture=True)
    if result.returncode != 0:
        print("ERROR: Validation failed. Fix errors before releasing.")
        print(result.stdout)
        sys.exit(1)
    print(result.stdout.strip().split("\n")[-1])


def count_standards() -> dict:
    import yaml
    modules_dir = REPO_ROOT / "modules"
    counts = {}
    total = 0
    for module_path in sorted(modules_dir.iterdir()):
        index_file = module_path / "standards-index.yaml"
        if not index_file.exists():
            continue
        with open(index_file) as f:
            data = yaml.safe_load(f)
        count = len(data.get("standards", []))
        counts[module_path.name] = count
        total += count
    counts["_total"] = total
    return counts


def create_tag(version: str, dry_run: bool) -> None:
    counts = count_standards()
    message = f"Release {version} — {counts['_total']} standards across {len(counts) - 1} modules"

    if dry_run:
        print(f"\n[DRY RUN] Would create tag: {version}")
        print(f"[DRY RUN] Message: {message}")
        return

    run(["git", "tag", "-a", version, "-m", message])
    print(f"\n✓ Created tag: {version}")
    print(f"  Message: {message}")


def push_tag(version: str, dry_run: bool) -> None:
    if dry_run:
        print(f"[DRY RUN] Would push tag {version} to origin")
        return

    run(["git", "push", "origin", version])
    print(f"✓ Pushed tag {version} to origin")


def create_release(version: str, dry_run: bool) -> None:
    counts = count_standards()
    notes = f"""## {version}

**{counts['_total']} standards** across {len(counts) - 1} modules.

| Module | Standards |
|--------|-----------|
"""
    for name, count in sorted(counts.items()):
        if name.startswith("_"):
            continue
        notes += f"| {name} | {count} |\n"

    notes += f"\nSee [CHANGELOG.md](CHANGELOG.md) for full details."

    if dry_run:
        print(f"[DRY RUN] Would create GitHub release {version}")
        print(notes)
        return

    # Build vsix
    vscode_dir = REPO_ROOT / "vscode-extension"
    print("Building VS Code extension...")
    run(["npm", "run", "compile"], check=True, capture=True)
    vsix_name = f"uk-gov-engineering-standards-{version.lstrip('v')}.vsix"
    run(["npx", "vsce", "package", "--out", vsix_name], check=True, capture=True)

    vsix_path = vscode_dir / vsix_name

    # Create release
    cmd = [
        "gh", "release", "create", version,
        "--title", f"{version} — {counts['_total']} standards",
        "--notes", notes,
    ]
    if vsix_path.exists():
        cmd.append(str(vsix_path))

    run(cmd)
    print(f"✓ Created GitHub release: {version}")


def main():
    parser = argparse.ArgumentParser(description="Create a new standards release")
    parser.add_argument("--version", required=True, help="Version tag (e.g. v1.0.0)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without doing it")
    args = parser.parse_args()

    validate_version(args.version)

    if not args.dry_run:
        check_clean_tree()

    if check_tag_exists(args.version):
        print(f"ERROR: Tag {args.version} already exists")
        sys.exit(1)

    run_validation()

    print(f"\nCreating release {args.version}...")
    create_tag(args.version, args.dry_run)
    push_tag(args.version, args.dry_run)
    create_release(args.version, args.dry_run)

    if not args.dry_run:
        print(f"\n{'='*50}")
        print(f"  Release {args.version} complete!")
        print(f"  https://github.com/bv90dsit/Engineering_standards/releases/tag/{args.version}")
        print(f"{'='*50}")


if __name__ == "__main__":
    main()
