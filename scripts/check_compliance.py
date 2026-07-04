#!/usr/bin/env python3
"""Check a repository's compliance against applicable UK Gov engineering standards.

Usage:
    python check_compliance.py --repo-path /path/to/repo
    python check_compliance.py --repo-path . --role engineer --platform python
    python check_compliance.py --repo-path . --output markdown
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import yaml

INDEX_PATH = Path(__file__).resolve().parent.parent / "standards-index.yaml"

PASS = "\033[92m✓ PASS\033[0m"
FAIL = "\033[91m✗ FAIL\033[0m"
SKIP = "\033[93m○ MANUAL\033[0m"

PASS_MD = "✅ PASS"
FAIL_MD = "❌ FAIL"
SKIP_MD = "⚠️ MANUAL"


def load_index() -> list[dict]:
    with open(INDEX_PATH) as f:
        data = yaml.safe_load(f)
    return data["standards"]


def filter_standards(standards, role=None, platform=None, category=None):
    results = []
    for s in standards:
        applies = s.get("applies_to", {})
        if role:
            std_role = applies.get("role", "any")
            if std_role != "any" and role not in std_role.split(","):
                continue
        if platform:
            std_platform = applies.get("platform", "any")
            if std_platform != "any" and platform not in std_platform.split(","):
                continue
        if category and s.get("category") != category:
            continue
        results.append(s)
    return results


def check_eng_001(repo: Path) -> tuple[str, str]:
    """Open source: check if repo has a licence file."""
    licence_files = list(repo.glob("LICEN[CS]E*")) + list(repo.glob("licen[cs]e*"))
    if licence_files:
        return "pass", f"Licence found: {licence_files[0].name}"
    return "fail", "No LICENCE or LICENSE file found in repository root"


def check_eng_002(repo: Path) -> tuple[str, str]:
    """Version control: check .git exists and has branch protection indicators."""
    if not (repo / ".git").is_dir():
        return "fail", "Not a git repository"
    result = subprocess.run(
        ["git", "-C", str(repo), "remote", "-v"],
        capture_output=True, text=True
    )
    if "origin" in result.stdout:
        return "pass", "Git repo with remote origin configured"
    return "pass", "Git repo (no remote configured — local only)"


def check_eng_003(repo: Path) -> tuple[str, str]:
    """CI: check for workflow files."""
    workflows_dir = repo / ".github" / "workflows"
    if workflows_dir.is_dir() and any(workflows_dir.glob("*.yml")) or any(workflows_dir.glob("*.yaml")):
        files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        return "pass", f"CI workflows found: {', '.join(f.name for f in files[:3])}"
    if (repo / ".gitlab-ci.yml").exists():
        return "pass", "GitLab CI configuration found"
    if (repo / "Jenkinsfile").exists():
        return "pass", "Jenkinsfile found"
    return "fail", "No CI configuration found (.github/workflows/, .gitlab-ci.yml, or Jenkinsfile)"


def check_sec_001(repo: Path) -> tuple[str, str]:
    """HTTPS: grep for http:// URLs in source code (excluding tests and docs)."""
    try:
        result = subprocess.run(
            ["grep", "-r", "--include=*.py", "--include=*.js", "--include=*.ts",
             "--include=*.go", "--include=*.java", "--include=*.rb",
             "--exclude-dir=scripts", "--exclude-dir=test*",
             "--exclude-dir=node_modules", "--exclude-dir=venv",
             "-l", "http://", str(repo)],
            capture_output=True, text=True
        )
        files = [f for f in result.stdout.strip().split("\n") if f and "test" not in f.lower()]
        if files:
            return "fail", f"HTTP URLs found in: {', '.join(Path(f).name for f in files[:3])}"
    except FileNotFoundError:
        return "skip", "grep not available"
    return "pass", "No plaintext HTTP URLs found in source code"


def check_sec_002(repo: Path) -> tuple[str, str]:
    """Dependency scanning: check for scanner configuration."""
    checks = [
        repo / ".github" / "dependabot.yml",
        repo / ".github" / "dependabot.yaml",
        repo / ".snyk",
        repo / ".trivyignore",
        repo / "renovate.json",
        repo / ".renovaterc",
    ]
    for check in checks:
        if check.exists():
            return "pass", f"Dependency scanner configured: {check.name}"
    return "fail", "No dependency scanning configuration found (dependabot.yml, .snyk, renovate.json, etc.)"


def check_arc_001(repo: Path) -> tuple[str, str]:
    """Cloud-first: check for IaC files."""
    iac_patterns = [
        ("terraform", list(repo.rglob("*.tf"))),
        ("CloudFormation", list(repo.rglob("*template*.yaml")) + list(repo.rglob("*template*.json"))),
        ("Pulumi", [repo / "Pulumi.yaml"]),
        ("Dockerfile", list(repo.rglob("Dockerfile*"))),
    ]
    found = [(name, files) for name, files in iac_patterns if any(f.exists() if hasattr(f, 'exists') else True for f in files) and files]
    if found:
        names = [name for name, _ in found]
        return "pass", f"Infrastructure-as-code found: {', '.join(names)}"
    return "skip", "No IaC files detected — manual review required"


def check_arc_002(repo: Path) -> tuple[str, str]:
    """12-factor: check for env-based config patterns."""
    env_example = repo / ".env.example"
    docker_compose = repo / "docker-compose.yml"
    if env_example.exists() or docker_compose.exists():
        return "pass", "Environment-based configuration pattern detected"
    return "skip", "Cannot determine 12-factor compliance automatically — manual review required"


def check_ops_001(repo: Path) -> tuple[str, str]:
    """Monitoring: check for monitoring/alerting configuration."""
    indicators = [
        repo / "monitoring",
        repo / "alerts",
        repo / "grafana",
        repo / "prometheus.yml",
        repo / "datadog.yaml",
    ]
    for indicator in indicators:
        if indicator.exists():
            return "pass", f"Monitoring configuration found: {indicator.name}"
    return "skip", "No monitoring configuration detected — manual review required"


def check_ops_002(repo: Path) -> tuple[str, str]:
    """Deployment frequency: cannot be automated from repo alone."""
    return "skip", "Deployment frequency requires runtime metrics — manual review required"


def check_emg_001(repo: Path) -> tuple[str, str]:
    """AI code review: check PR review is required (inferred from branch protection)."""
    if (repo / ".git").is_dir():
        return "skip", "AI code review policy requires branch protection check via GitHub API — manual review"
    return "skip", "Not a git repository — cannot check"


CHECKS = {
    "ENG-001": check_eng_001,
    "ENG-002": check_eng_002,
    "ENG-003": check_eng_003,
    "SEC-001": check_sec_001,
    "SEC-002": check_sec_002,
    "ARC-001": check_arc_001,
    "ARC-002": check_arc_002,
    "OPS-001": check_ops_001,
    "OPS-002": check_ops_002,
    "EMG-001": check_emg_001,
}


def run_checks(repo: Path, standards: list[dict], output_format: str = "terminal") -> int:
    results = []
    for s in standards:
        std_id = s["id"]
        check_fn = CHECKS.get(std_id)
        if check_fn:
            status, detail = check_fn(repo)
        else:
            status, detail = "skip", "No automated check available"
        results.append((s, status, detail))

    if output_format == "markdown":
        print_markdown(results)
    else:
        print_terminal(results)

    failures = [(s, d) for s, st, d in results if st == "fail" and s["conformance"] == "MUST"]
    return 1 if failures else 0


def print_terminal(results):
    print(f"\n{'='*70}")
    print("UK Government Engineering Standards — Compliance Report")
    print(f"{'='*70}\n")

    for s, status, detail in results:
        if status == "pass":
            icon = PASS
        elif status == "fail":
            icon = FAIL
        else:
            icon = SKIP
        conformance = f"[{s['conformance']}]"
        print(f"  {icon}  {s['id']} {conformance:<8} {s['title']}")
        print(f"         {detail}\n")

    passes = sum(1 for _, st, _ in results if st == "pass")
    fails = sum(1 for _, st, _ in results if st == "fail")
    skips = sum(1 for _, st, _ in results if st == "skip")
    must_fails = sum(1 for s, st, _ in results if st == "fail" and s["conformance"] == "MUST")

    print(f"{'─'*70}")
    print(f"  Results: {passes} passed, {fails} failed, {skips} manual review")
    if must_fails:
        print(f"  ⚠️  {must_fails} MUST-level failure(s) — action required")
    else:
        print(f"  All MUST-level standards satisfied (or require manual review)")
    print()


def print_markdown(results):
    print("## UK Government Engineering Standards — Compliance Report\n")
    print("| Status | ID | Level | Standard | Detail |")
    print("|--------|-----|-------|----------|--------|")

    for s, status, detail in results:
        if status == "pass":
            icon = PASS_MD
        elif status == "fail":
            icon = FAIL_MD
        else:
            icon = SKIP_MD
        print(f"| {icon} | {s['id']} | {s['conformance']} | {s['title']} | {detail} |")

    passes = sum(1 for _, st, _ in results if st == "pass")
    fails = sum(1 for _, st, _ in results if st == "fail")
    skips = sum(1 for _, st, _ in results if st == "skip")
    must_fails = sum(1 for s, st, _ in results if st == "fail" and s["conformance"] == "MUST")

    print(f"\n**Results:** {passes} passed, {fails} failed, {skips} manual review")
    if must_fails:
        print(f"\n**⚠️ {must_fails} MUST-level failure(s) — action required**")


def main():
    parser = argparse.ArgumentParser(description="Check repository compliance against UK Gov engineering standards")
    parser.add_argument("--repo-path", required=True, help="Path to the repository to check")
    parser.add_argument("--role", help="e.g. engineer, architect, lead")
    parser.add_argument("--platform", help="e.g. python, java, node")
    parser.add_argument("--category", help="e.g. ENG, SEC, ARC, OPS, EMG")
    parser.add_argument("--output", choices=["terminal", "markdown"], default="terminal")
    args = parser.parse_args()

    repo = Path(args.repo_path).resolve()
    if not repo.is_dir():
        print(f"Error: {repo} is not a directory", file=sys.stderr)
        sys.exit(1)

    standards = load_index()
    standards = filter_standards(standards, role=args.role, platform=args.platform, category=args.category)

    if not standards:
        print("No standards match the given context.")
        sys.exit(0)

    exit_code = run_checks(repo, standards, output_format=args.output)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
