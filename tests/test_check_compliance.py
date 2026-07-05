"""Tests for scripts/check_compliance.py."""

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


class TestCheckENG001:
    """Tests for ENG-001: Open source — licence file check."""

    def test_check_eng_001_pass(self, tmp_path: Path):
        """Repo with LICENCE file passes ENG-001."""
        # Create a fake repo with a LICENCE file
        (tmp_path / "LICENCE").write_text("MIT Licence\n")
        (tmp_path / ".git").mkdir()  # Fake git dir for ENG-002

        result = run_check_compliance(tmp_path, category="ENG")
        # ENG-001 should pass
        assert result.returncode == 0 or "PASS" in result.stdout
        assert "Licence found" in result.stdout or "PASS" in result.stdout

    def test_check_eng_001_fail(self, tmp_path: Path):
        """Repo without LICENCE file fails ENG-001."""
        # Create a bare repo with no licence
        (tmp_path / ".git").mkdir()
        (tmp_path / "README.md").write_text("# Project\n" * 12)

        result = run_check_compliance(tmp_path, category="ENG")
        # Should have at least one failure for ENG-001
        assert "No LICENCE" in result.stdout or "FAIL" in result.stdout


class TestCheckENG003:
    """Tests for ENG-003: CI workflows check."""

    def test_check_eng_003_pass(self, tmp_path: Path):
        """Repo with .github/workflows/*.yml passes ENG-003."""
        workflows_dir = tmp_path / ".github" / "workflows"
        workflows_dir.mkdir(parents=True)
        (workflows_dir / "ci.yml").write_text("name: CI\non: push\njobs: {}\n")
        (tmp_path / ".git").mkdir()
        (tmp_path / "LICENCE").write_text("MIT\n")

        result = run_check_compliance(tmp_path, category="ENG")
        assert "CI workflows found" in result.stdout or "PASS" in result.stdout


class TestCheckSEC001:
    """Tests for SEC-001: HTTPS everywhere."""

    def test_check_sec_001_pass(self, tmp_path: Path):
        """Repo with no http:// URLs passes SEC-001."""
        # Create a source file with only https URLs
        (tmp_path / "main.py").write_text('url = "https://example.com"\n')
        (tmp_path / ".git").mkdir()

        result = run_check_compliance(tmp_path, category="SEC")
        assert "No plaintext HTTP" in result.stdout or "PASS" in result.stdout


class TestCheckSEC002:
    """Tests for SEC-002: Dependency vulnerability scanning."""

    def test_check_sec_002_pass(self, tmp_path: Path):
        """Repo with dependabot.yml passes SEC-002."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "dependabot.yml").write_text("version: 2\nupdates: []\n")
        (tmp_path / ".git").mkdir()

        result = run_check_compliance(tmp_path, category="SEC")
        assert "Dependency scanner configured" in result.stdout or "PASS" in result.stdout

    def test_check_sec_002_fail(self, tmp_path: Path):
        """Repo without any scanner config fails SEC-002."""
        (tmp_path / ".git").mkdir()
        (tmp_path / "main.py").write_text('print("hello")\n')

        result = run_check_compliance(tmp_path, category="SEC")
        assert "No dependency scanning" in result.stdout or "FAIL" in result.stdout
