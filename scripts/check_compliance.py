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


def check_sec_003(repo: Path) -> tuple[str, str]:
    """No secrets in source code: check for secret scanning config and common patterns."""
    # Check for secret scanning configuration
    has_config = False
    pre_commit = repo / ".pre-commit-config.yaml"
    if pre_commit.exists():
        content = pre_commit.read_text()
        if "detect-secrets" in content or "git-secrets" in content:
            has_config = True
    if (repo / ".github" / "secret-scanning.yml").exists():
        has_config = True

    # Grep for common secret patterns in source code
    secret_patterns = [
        r"password\s*=\s*['\"]",
        r"api_key\s*=\s*['\"]",
        r"secret\s*=\s*['\"]",
    ]
    violations = []
    for pattern in secret_patterns:
        try:
            result = subprocess.run(
                ["grep", "-r", "-l", "-E", "--include=*.py", "--include=*.js",
                 "--include=*.ts", "--include=*.go", "--include=*.java",
                 "--include=*.rb", "--include=*.yaml", "--include=*.yml",
                 "--include=*.json", "--include=*.cfg", "--include=*.ini",
                 "--exclude-dir=node_modules", "--exclude-dir=venv",
                 "--exclude-dir=.git", "--exclude-dir=test*",
                 "--exclude=*.example", "--exclude=*.test.*",
                 pattern, str(repo)],
                capture_output=True, text=True
            )
            files = [f for f in result.stdout.strip().split("\n")
                     if f and "test" not in f.lower() and ".example" not in f.lower()]
            violations.extend(files)
        except FileNotFoundError:
            pass

    if violations:
        unique = list(set(violations))
        return "fail", f"Potential secrets found in: {', '.join(Path(f).name for f in unique[:3])}"
    if has_config:
        return "pass", "Secret scanning configured and no common secret patterns found"
    return "fail", "No secret scanning config found (.pre-commit-config.yaml with detect-secrets/git-secrets, or .github/secret-scanning.yml)"


def check_sec_004(repo: Path) -> tuple[str, str]:
    """Input validation: check for SAST config (CodeQL or Semgrep)."""
    # Check for semgrep config files
    if (repo / "semgrep.yml").exists() or (repo / ".semgrep.yml").exists():
        return "pass", "Semgrep configuration found"

    # Check workflow files for codeql or semgrep
    workflows_dir = repo / ".github" / "workflows"
    if workflows_dir.is_dir():
        for wf in list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml")):
            try:
                content = wf.read_text().lower()
                if "codeql" in content:
                    return "pass", f"CodeQL SAST found in {wf.name}"
                if "semgrep" in content:
                    return "pass", f"Semgrep SAST found in {wf.name}"
            except OSError:
                continue

    return "fail", "No SAST configuration found (CodeQL or Semgrep in CI workflows, or semgrep.yml)"


def check_sec_005(repo: Path) -> tuple[str, str]:
    """Authentication via standards (OAuth2/OIDC) — manual review required."""
    return "skip", "Authentication standards require architectural review — manual review required"


def check_sec_006(repo: Path) -> tuple[str, str]:
    """Container image scanning: check Dockerfile exists and scan step in CI."""
    dockerfiles = list(repo.rglob("Dockerfile*"))
    if not dockerfiles:
        return "skip", "No Dockerfile found — not applicable"

    # Check CI workflows for container scanning
    workflows_dir = repo / ".github" / "workflows"
    if workflows_dir.is_dir():
        for wf in list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml")):
            try:
                content = wf.read_text().lower()
                if "trivy" in content or "snyk container" in content:
                    return "pass", f"Container scanning found in {wf.name}"
            except OSError:
                continue

    # Also check for .gitlab-ci.yml
    gitlab_ci = repo / ".gitlab-ci.yml"
    if gitlab_ci.exists():
        try:
            content = gitlab_ci.read_text().lower()
            if "trivy" in content or "snyk container" in content:
                return "pass", "Container scanning found in .gitlab-ci.yml"
        except OSError:
            pass

    return "fail", "Dockerfile exists but no container image scanning (Trivy/Snyk) found in CI workflows"


def check_sec_007(repo: Path) -> tuple[str, str]:
    """Annual penetration testing — manual review required."""
    return "skip", "Penetration testing schedule requires periodic audit — manual review required"


def check_arc_003(repo: Path) -> tuple[str, str]:
    """API standards: check for OpenAPI/Swagger spec file."""
    spec_names = ["openapi.yaml", "openapi.json", "openapi.yml",
                  "swagger.yaml", "swagger.json", "swagger.yml"]
    for name in spec_names:
        matches = list(repo.rglob(name))
        if matches:
            rel = matches[0].relative_to(repo)
            return "pass", f"OpenAPI spec found: {rel}"

    # Check if this is even an API project — look for indicators
    indicators = (
        list(repo.rglob("*controller*")) +
        list(repo.rglob("*routes*")) +
        list(repo.rglob("*api*"))
    )
    if not indicators:
        return "skip", "No API indicators found — not applicable"

    return "fail", "API indicators found but no OpenAPI/Swagger spec file (openapi.yaml/json, swagger.yaml/json)"


def check_arc_004(repo: Path) -> tuple[str, str]:
    """ADRs: check for ADR directory with at least one .md file."""
    adr_dirs = [
        repo / "docs" / "adr",
        repo / "adr",
        repo / "doc" / "architecture" / "decisions",
    ]
    for adr_dir in adr_dirs:
        if adr_dir.is_dir():
            md_files = list(adr_dir.glob("*.md"))
            if md_files:
                return "pass", f"ADR directory found ({adr_dir.relative_to(repo)}) with {len(md_files)} record(s)"
    return "fail", "No ADR directory found (docs/adr/, adr/, or doc/architecture/decisions/) with .md files"


def check_arc_005(repo: Path) -> tuple[str, str]:
    """Resilience patterns — manual review required."""
    return "skip", "Resilience pattern review (retry, circuit-breaker, timeouts) — manual review required"


def check_dat_001(repo: Path) -> tuple[str, str]:
    """Data classified and labelled — manual review required."""
    return "skip", "Data classification and labelling requires periodic audit — manual review required"


def check_dat_002(repo: Path) -> tuple[str, str]:
    """Personal data has a retention policy — manual review required."""
    return "skip", "Data retention policy requires periodic audit — manual review required"


def check_dat_003(repo: Path) -> tuple[str, str]:
    """Backups tested with restore drill — manual review required."""
    return "skip", "Backup restore drills require periodic audit — manual review required"


def check_dat_004(repo: Path) -> tuple[str, str]:
    """Open data published where possible — manual review required."""
    return "skip", "Open data publication requires periodic audit — manual review required"


def check_ops_003(repo: Path) -> tuple[str, str]:
    """Incident management process with post-mortems — manual review required."""
    return "skip", "Incident management process requires ways-of-working review — manual review required"


def check_ops_004(repo: Path) -> tuple[str, str]:
    """Disaster recovery plan tested annually — manual review required."""
    return "skip", "Disaster recovery plan testing requires periodic audit — manual review required"


def check_ops_005(repo: Path) -> tuple[str, str]:
    """Change failure rate tracked (DORA) — manual review required."""
    return "skip", "Change failure rate tracking requires runtime metrics — manual review required"


def check_acc_001(repo: Path) -> tuple[str, str]:
    """WCAG 2.2 AA: check for accessibility testing config."""
    # Check if this is a web project
    package_json = repo / "package.json"
    html_files = list(repo.rglob("*.html"))
    if not package_json.exists() and not html_files:
        return "skip", "No package.json or HTML files — not a web project, skipping"

    # Check for pa11y
    if (repo / ".pa11yci").exists() or (repo / ".pa11yci.json").exists():
        return "pass", "pa11y accessibility testing configured (.pa11yci)"

    # Check package.json for pa11y or axe
    if package_json.exists():
        try:
            content = package_json.read_text().lower()
            if "pa11y" in content:
                return "pass", "pa11y found in package.json"
            if "axe" in content:
                return "pass", "axe accessibility testing found in package.json"
        except OSError:
            pass

    # Check for accessibility test files
    a11y_tests = (
        list(repo.rglob("*accessibility*test*")) +
        list(repo.rglob("*a11y*test*")) +
        list(repo.rglob("*a11y*.spec.*"))
    )
    if a11y_tests:
        return "pass", f"Accessibility test files found: {a11y_tests[0].name}"

    return "fail", "Web project detected but no accessibility testing config (pa11y, axe in package.json, or a11y test files)"


def check_acc_002(repo: Path) -> tuple[str, str]:
    """Progressive enhancement — manual review required."""
    return "skip", "Progressive enhancement requires peer review — manual review required"


def check_eng_004(repo: Path) -> tuple[str, str]:
    """Documentation: check README.md exists and is non-empty (>10 lines)."""
    readme_candidates = list(repo.glob("README*")) + list(repo.glob("readme*"))
    if not readme_candidates:
        return "fail", "No README file found in repository root"
    readme = readme_candidates[0]
    try:
        lines = readme.read_text().strip().splitlines()
        if len(lines) > 10:
            return "pass", f"README found ({readme.name}) with {len(lines)} lines"
        return "fail", f"README found ({readme.name}) but only {len(lines)} lines — should be more than 10"
    except OSError:
        return "fail", f"README found ({readme.name}) but could not be read"


def check_eng_005(repo: Path) -> tuple[str, str]:
    """Technical debt tracked and prioritised — manual review required."""
    return "skip", "Technical debt tracking requires ways-of-working review — manual review required"


def check_eng_006(repo: Path) -> tuple[str, str]:
    """Pair/mob programming for complex work — manual review required."""
    return "skip", "Pair/mob programming practices require ways-of-working review — manual review required"


def check_emg_002(repo: Path) -> tuple[str, str]:
    """AI systems have a transparency statement — manual review required."""
    return "skip", "AI transparency statement requires periodic audit — manual review required"


def check_emg_003(repo: Path) -> tuple[str, str]:
    """AI outputs validated before user-facing use — manual review required."""
    return "skip", "AI output validation requires peer review and testing verification — manual review required"


def check_emg_004(repo: Path) -> tuple[str, str]:
    """AI training data checked for bias and IP compliance — manual review required."""
    return "skip", "AI training data review requires periodic audit — manual review required"


CHECKS = {
    "ENG-001": check_eng_001,
    "ENG-002": check_eng_002,
    "ENG-003": check_eng_003,
    "ENG-004": check_eng_004,
    "ENG-005": check_eng_005,
    "ENG-006": check_eng_006,
    "SEC-001": check_sec_001,
    "SEC-002": check_sec_002,
    "SEC-003": check_sec_003,
    "SEC-004": check_sec_004,
    "SEC-005": check_sec_005,
    "SEC-006": check_sec_006,
    "SEC-007": check_sec_007,
    "ARC-001": check_arc_001,
    "ARC-002": check_arc_002,
    "ARC-003": check_arc_003,
    "ARC-004": check_arc_004,
    "ARC-005": check_arc_005,
    "DAT-001": check_dat_001,
    "DAT-002": check_dat_002,
    "DAT-003": check_dat_003,
    "DAT-004": check_dat_004,
    "OPS-001": check_ops_001,
    "OPS-002": check_ops_002,
    "OPS-003": check_ops_003,
    "OPS-004": check_ops_004,
    "OPS-005": check_ops_005,
    "ACC-001": check_acc_001,
    "ACC-002": check_acc_002,
    "EMG-001": check_emg_001,
    "EMG-002": check_emg_002,
    "EMG-003": check_emg_003,
    "EMG-004": check_emg_004,
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
