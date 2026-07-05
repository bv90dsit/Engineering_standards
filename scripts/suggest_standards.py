#!/usr/bin/env python3
"""Scan a repository and suggest which standards apply based on its technology stack.

Usage:
    python scripts/suggest_standards.py --repo-path /path/to/service
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from standards_lib.query import query_standards, list_modules


def detect_stack(repo: Path) -> dict:
    """Detect the technology stack from repo contents."""
    stack = {
        "languages": [],
        "frameworks": [],
        "has_docker": False,
        "has_ci": False,
    }

    # Python
    py_signals = list(repo.rglob("*.py"))
    if py_signals or (repo / "requirements.txt").exists() or (repo / "pyproject.toml").exists():
        stack["languages"].append("python")

        # Django
        reqs = ""
        for req_file in [repo / "requirements.txt", repo / "Pipfile"]:
            if req_file.exists():
                reqs += req_file.read_text().lower()
        pyproject = repo / "pyproject.toml"
        if pyproject.exists():
            reqs += pyproject.read_text().lower()

        if "django" in reqs or (repo / "manage.py").exists():
            stack["frameworks"].append("django")
        if "flask" in reqs:
            stack["frameworks"].append("flask")

    # Java
    if (repo / "pom.xml").exists() or (repo / "build.gradle").exists() or (repo / "build.gradle.kts").exists():
        stack["languages"].append("java")
        pom = repo / "pom.xml"
        gradle = repo / "build.gradle"
        build_content = ""
        if pom.exists():
            build_content = pom.read_text().lower()
        elif gradle.exists():
            build_content = gradle.read_text().lower()
        if "spring-boot" in build_content or "springframework" in build_content:
            stack["frameworks"].append("spring-boot")

    # TypeScript / JavaScript
    if (repo / "tsconfig.json").exists() or list(repo.rglob("*.ts")) or list(repo.rglob("*.tsx")):
        stack["languages"].append("typescript")
        pkg = repo / "package.json"
        if pkg.exists():
            pkg_content = pkg.read_text().lower()
            if "react" in pkg_content:
                stack["frameworks"].append("react")
            if "express" in pkg_content or "fastify" in pkg_content or "koa" in pkg_content:
                stack["frameworks"].append("node")
    elif (repo / "package.json").exists():
        stack["languages"].append("javascript")

    # Docker
    if list(repo.rglob("Dockerfile*")) or (repo / "docker-compose.yml").exists():
        stack["has_docker"] = True

    # CI
    workflows = repo / ".github" / "workflows"
    if (workflows.is_dir() and list(workflows.glob("*.yml"))) or (repo / ".gitlab-ci.yml").exists():
        stack["has_ci"] = True

    return stack


def suggest(repo: Path) -> None:
    """Detect stack and suggest applicable standards."""
    stack = detect_stack(repo)

    # Determine which modules apply
    modules = ["core"]
    if "python" in stack["languages"]:
        modules.append("python")
    if "java" in stack["languages"]:
        modules.append("java")
    if "typescript" in stack["languages"] or "javascript" in stack["languages"]:
        modules.append("typescript")

    # Print detection results
    print()
    print("=" * 60)
    print("  Standards Suggestion — Repository Scan")
    print("=" * 60)
    print()
    print(f"  Repository: {repo}")
    print()
    print(f"  Detected languages:  {', '.join(stack['languages']) or 'none'}")
    print(f"  Detected frameworks: {', '.join(stack['frameworks']) or 'none'}")
    print(f"  Has Docker:          {'yes' if stack['has_docker'] else 'no'}")
    print(f"  Has CI:              {'yes' if stack['has_ci'] else 'no'}")
    print()
    print(f"  Recommended modules: {', '.join(modules)}")
    print()

    # Query applicable standards
    all_standards = []
    for mod in modules:
        all_standards.extend(query_standards(module=mod))

    must = [s for s in all_standards if s["conformance"] == "MUST"]
    should = [s for s in all_standards if s["conformance"] == "SHOULD"]
    could = [s for s in all_standards if s["conformance"] == "COULD"]

    print("─" * 60)
    print(f"  {len(all_standards)} standards apply ({len(must)} MUST, {len(should)} SHOULD, {len(could)} COULD)")
    print("─" * 60)

    # Print MUST
    print()
    print("  MUST — you are required to comply with these:")
    print()
    for s in must:
        enforcement = ", ".join(s.get("enforcement", []))
        print(f"    {s['id']:<10} {s['title']}")
        print(f"             enforcement: {enforcement}")
    print()

    # Print SHOULD
    print("  SHOULD — strongly recommended:")
    print()
    for s in should:
        print(f"    {s['id']:<10} {s['title']}")
    print()

    # Print COULD
    if could:
        print("  COULD — optional, encouraged:")
        print()
        for s in could:
            print(f"    {s['id']:<10} {s['title']}")
        print()

    # Adoption hint
    print("─" * 60)
    platform = stack["languages"][0] if stack["languages"] else "any"
    print(f"  To adopt, add to your repo: .github/workflows/standards.yml")
    print()
    print(f"    jobs:")
    print(f"      compliance:")
    print(f"        uses: bv90dsit/Engineering_standards/.github/workflows/compliance.yml@v1.0.0")
    print(f"        with:")
    print(f"          role: engineer")
    print(f"          platform: {platform}")
    print("─" * 60)
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a repo and suggest applicable engineering standards")
    parser.add_argument("--repo-path", required=True, help="Path to the repository to scan")
    args = parser.parse_args()

    repo = Path(args.repo_path).resolve()
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    suggest(repo)


if __name__ == "__main__":
    main()
