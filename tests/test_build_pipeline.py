#!/usr/bin/env python3
"""End-to-end test for the build pipeline.

Tests: validate standards → build_site.py → check output is valid.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
DOCS_DIR = REPO_ROOT / "docs"
STANDARDS_OUTPUT = DOCS_DIR / "_standards"


@pytest.fixture(autouse=True)
def clean_output():
    """Remove generated _standards before and after each test."""
    import shutil

    if STANDARDS_OUTPUT.exists():
        shutil.rmtree(STANDARDS_OUTPUT)
    yield
    if STANDARDS_OUTPUT.exists():
        shutil.rmtree(STANDARDS_OUTPUT)


def run_script(script_name: str) -> subprocess.CompletedProcess:
    """Run a script from the scripts/ directory and return the result."""
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


class TestBuildSite:
    """Tests that build_site.py correctly generates docs/_standards/ from module sources."""

    def test_build_site_creates_standards(self):
        """build_site.py exits 0 and creates the _standards/ output directory."""
        result = run_script("build_site.py")
        assert result.returncode == 0, f"Build failed:\n{result.stdout}\n{result.stderr}"
        assert STANDARDS_OUTPUT.exists(), "_standards directory not created"

    def test_build_site_copies_all_standards(self):
        """Every standard in modules/ produces a corresponding file in _standards/."""
        run_script("build_site.py")

        source_count = len(list(REPO_ROOT.glob("modules/*/standards/*.md")))
        output_count = len(list(STANDARDS_OUTPUT.glob("*.md")))
        assert output_count == source_count, (
            f"Expected {source_count} standards, got {output_count}"
        )

    def test_built_standards_have_required_frontmatter(self):
        """Each built file has layout: standard and render_with_liquid: false."""
        run_script("build_site.py")

        import re

        for filepath in STANDARDS_OUTPUT.glob("*.md"):
            content = filepath.read_text(encoding="utf-8")
            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            assert match, f"{filepath.name} missing frontmatter"
            fm = match.group(1)
            assert "layout: standard" in fm, f"{filepath.name} missing layout"
            assert "render_with_liquid: false" in fm, f"{filepath.name} missing render_with_liquid"

    def test_built_standards_wrapped_in_raw(self):
        """Each built file body is wrapped in raw/endraw to prevent Liquid parsing."""
        run_script("build_site.py")

        for filepath in STANDARDS_OUTPUT.glob("*.md"):
            content = filepath.read_text(encoding="utf-8")
            body_start = content.index("---", 3) + 3
            body = content[body_start:].strip()
            assert body.startswith("{% raw %}"), f"{filepath.name} body not wrapped in raw"
            assert body.endswith("{% endraw %}"), f"{filepath.name} body not closed with endraw"


class TestGraphSync:
    """Tests that the sources graph data stays in sync with source traceability tables."""

    def test_graph_data_matches_traceability(self):
        """check_graph_sync.py finds no drift between graph and standard files."""
        result = run_script("check_graph_sync.py")
        assert result.returncode == 0, f"Graph out of sync:\n{result.stdout}"


class TestSkillGeneration:
    """Tests that build_skill.py generates a valid coding skill file."""

    def test_skill_generates_without_error(self):
        """build_skill.py exits 0."""
        result = run_script("build_skill.py")
        assert result.returncode == 0, f"Skill build failed:\n{result.stdout}\n{result.stderr}"

    def test_skill_output_exists(self):
        """The generated skill file exists at .claude/skills/uk-gov-standards.md."""
        run_script("build_skill.py")
        skill_path = REPO_ROOT / ".claude" / "skills" / "uk-gov-standards.md"
        assert skill_path.exists(), "Skill file not generated"
