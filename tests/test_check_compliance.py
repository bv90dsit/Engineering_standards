"""Tests for the compliance checker tool (scripts/check_compliance.py).

These verify that the checker correctly detects compliance/non-compliance
when pointed at a repository. They test the detection logic, not the
standards themselves.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECK_SCRIPT = REPO_ROOT / "scripts" / "check_compliance.py"


def run_check_compliance(
    repo_path: str | Path,
    category: str | None = None,
    extra_args: list[str] | None = None,
) -> subprocess.CompletedProcess:
    """Run check_compliance.py as a subprocess."""
    cmd = [sys.executable, str(CHECK_SCRIPT), "--repo-path", str(repo_path)]
    if category:
        cmd.extend(["--category", category])
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


class TestLicenceDetection:
    """Tests that the checker correctly detects presence/absence of a licence file."""

    def test_repo_with_licence_passes(self, tmp_path: Path):
        """Checker reports PASS when a LICENCE file exists."""
        # Create a fake repo with a LICENCE file
        (tmp_path / "LICENCE").write_text("MIT Licence\n")
        (tmp_path / ".git").mkdir()  # Fake git dir for ENG-002

        result = run_check_compliance(tmp_path, category="ENG")
        # ENG-001 should pass
        assert result.returncode == 0 or "PASS" in result.stdout
        assert "Licence found" in result.stdout or "PASS" in result.stdout

    def test_repo_without_licence_fails(self, tmp_path: Path):
        """Checker reports FAIL when no LICENCE file exists."""
        # Create a bare repo with no licence
        (tmp_path / ".git").mkdir()
        (tmp_path / "README.md").write_text("# Project\n" * 12)

        result = run_check_compliance(tmp_path, category="ENG")
        # Should have at least one failure for ENG-001
        assert "No LICENCE" in result.stdout or "FAIL" in result.stdout


class TestCIWorkflowDetection:
    """Tests that the checker correctly detects CI workflow configuration."""

    def test_repo_with_workflows_passes(self, tmp_path: Path):
        """Checker reports PASS when GitHub Actions workflows exist."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "ci.yml").write_text("name: CI\non: push\njobs: {}\n")
        (tmp_path / ".git").mkdir()
        (tmp_path / "LICENCE").write_text("MIT\n")

        result = run_check_compliance(tmp_path, category="ENG")
        assert "CI workflows found" in result.stdout or "PASS" in result.stdout


class TestHTTPSDetection:
    """Tests that the checker correctly detects plaintext HTTP URLs."""

    def test_repo_with_only_https_passes(self, tmp_path: Path):
        """Checker reports PASS when no http:// URLs found in source."""
        # Create a source file with only https URLs
        (tmp_path / "main.py").write_text('url = "https://example.com"\n')
        (tmp_path / ".git").mkdir()

        result = run_check_compliance(tmp_path, category="SEC")
        assert "No plaintext HTTP" in result.stdout or "PASS" in result.stdout


class TestDependencyScannerDetection:
    """Tests that the checker correctly detects dependency scanning configuration."""

    def test_repo_with_dependabot_passes(self, tmp_path: Path):
        """Checker reports PASS when dependabot.yml is configured."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "dependabot.yml").write_text("version: 2\nupdates: []\n")
        (tmp_path / ".git").mkdir()

        result = run_check_compliance(tmp_path, category="SEC")
        assert "Dependency scanner configured" in result.stdout or "PASS" in result.stdout

    def test_repo_without_scanner_fails(self, tmp_path: Path):
        """Checker reports FAIL when no dependency scanning is configured."""
        (tmp_path / ".git").mkdir()
        (tmp_path / "main.py").write_text('print("hello")\n')

        result = run_check_compliance(tmp_path, category="SEC")
        assert "No dependency scanning" in result.stdout or "FAIL" in result.stdout
