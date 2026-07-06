"""Tests for scripts/new_standard.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
NEW_STANDARD_SCRIPT = REPO_ROOT / "scripts" / "new_standard.py"


def run_new_standard(
    tmp_repo: Path,
    standard_id: str,
    module: str,
    title: str,
    conformance: str = "SHOULD",
    extra_args: list[str] | None = None,
) -> subprocess.CompletedProcess:
    """Run new_standard.py in a temporary repo-like directory."""
    # We create a wrapper that patches REPO_ROOT and MODULES_DIR
    wrapper_script = tmp_repo / "_run_new_standard.py"
    wrapper_script.write_text(f"""\
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / 'scripts')!r})

# Patch module-level constants before importing the module's functions
import new_standard
new_standard.REPO_ROOT = Path({str(tmp_repo)!r})
new_standard.MODULES_DIR = Path({str(tmp_repo / 'modules')!r})

# Now run via parse_args + main, but we need to set sys.argv
sys.argv = [
    "new_standard.py",
    "--id", {standard_id!r},
    "--module", {module!r},
    "--title", {title!r},
    "--conformance", {conformance!r},
]
extra = {extra_args!r}
if extra:
    sys.argv.extend(extra)

exit_code = new_standard.main()
sys.exit(exit_code)
""")

    return subprocess.run(
        [sys.executable, str(wrapper_script)],
        capture_output=True,
        text=True,
        cwd=str(tmp_repo),
        input="n\n",
    )


class TestNewStandard:
    """Tests for the new_standard.py scaffold script."""

    def test_scaffold_creates_file_and_index(self, tmp_path: Path):
        """Running scaffold creates the .md file and adds an index entry."""
        # Set up a temporary module directory
        module_dir = tmp_path / "modules" / "python"
        module_dir.mkdir(parents=True)
        (module_dir / "module.yaml").write_text(
            yaml.dump({
                "name": "python",
                "description": "Python standards",
                "version": "0.1.0",
                "applies_to": {"role": "any", "platform": "python"},
            })
        )
        # Existing (empty) index
        (module_dir / "standards-index.yaml").write_text("standards: []\n")
        # Standards directory (may or may not exist yet)
        (module_dir / "standards").mkdir()

        result = run_new_standard(
            tmp_repo=tmp_path,
            standard_id="PY-099",
            module="python",
            title="Test scaffold standard",
            conformance="SHOULD",
        )

        assert result.returncode == 0, f"Failed:\n{result.stdout}\n{result.stderr}"

        # Verify the .md file was created
        md_file = module_dir / "standards" / "PY-099.md"
        assert md_file.exists(), "Standard .md file was not created"
        content = md_file.read_text()
        assert "PY-099" in content
        assert "Test scaffold standard" in content

        # Verify the index was updated
        index_content = (module_dir / "standards-index.yaml").read_text()
        assert "PY-099" in index_content
        assert "Test scaffold standard" in index_content

    def test_scaffold_duplicate_id_fails(self, tmp_path: Path):
        """Running twice with same ID fails on the second attempt."""
        module_dir = tmp_path / "modules" / "python"
        module_dir.mkdir(parents=True)
        (module_dir / "module.yaml").write_text(
            yaml.dump({
                "name": "python",
                "description": "Python standards",
                "version": "0.1.0",
                "applies_to": {"role": "any", "platform": "python"},
            })
        )
        # Seed the index with a pre-existing entry so the YAML is valid block-style.
        # The script's append_to_index uses raw text concatenation, so it needs
        # block-format YAML (not flow-style []).
        index_content = """\
standards:
  - id: PY-100
    title: First standard
    conformance: MUST
    enforcement: [peer-review]
    applies_to:
      role: any
      platform: python
    category: ENG
    source: TODO-add-source
    tags: [python, TODO-add-tags]
"""
        (module_dir / "standards-index.yaml").write_text(index_content)
        (module_dir / "standards").mkdir()
        # Also create the .md file so the script's file-exists check triggers
        (module_dir / "standards" / "PY-100.md").write_text("---\nid: PY-100\n---\n# PY-100\n")

        # Running with same ID should fail because it already exists in the index
        result2 = run_new_standard(
            tmp_repo=tmp_path,
            standard_id="PY-100",
            module="python",
            title="Duplicate standard",
            conformance="MUST",
        )
        assert result2.returncode == 1
        assert "already exists" in result2.stdout
