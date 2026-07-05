"""Tests for scripts/validate_standards.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate_standards.py"


def run_validate(cwd: str | Path | None = None, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    """Run validate_standards.py as a subprocess."""
    import os

    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else str(REPO_ROOT),
        env=env,
    )


class TestValidateStandards:
    """Tests for the validate_standards.py script."""

    def test_validate_passes_on_current_repo(self):
        """Running against the real repo passes without errors."""
        result = run_validate()
        assert result.returncode == 0, f"Validation failed:\n{result.stdout}\n{result.stderr}"
        assert "validated successfully" in result.stdout

    def test_validate_catches_missing_frontmatter(self, tmp_path: Path):
        """A standard file without proper frontmatter is caught."""
        # Create a minimal module structure with a bad standard file
        module_dir = tmp_path / "modules" / "bad-module"
        module_dir.mkdir(parents=True)

        # module.yaml
        (module_dir / "module.yaml").write_text(
            yaml.dump({"name": "bad-module", "description": "test", "version": "0.1.0"})
        )

        # standards-index.yaml with one entry
        index_data = {
            "standards": [
                {
                    "id": "BAD-001",
                    "title": "Bad standard",
                    "conformance": "MUST",
                    "enforcement": ["automated"],
                    "applies_to": {"role": "any", "platform": "any"},
                    "category": "ENG",
                    "source": "test",
                    "tags": ["test"],
                }
            ]
        }
        (module_dir / "standards-index.yaml").write_text(yaml.dump(index_data))

        # Standard file WITHOUT frontmatter (no ---)
        standards_dir = module_dir / "standards"
        standards_dir.mkdir()
        (standards_dir / "BAD-001.md").write_text("# BAD-001\n\nNo frontmatter here.\n")

        # We need to temporarily make the script look at our tmp modules directory.
        # The script uses REPO_ROOT / "modules", so we create a wrapper that patches MODULES_DIR.
        wrapper_script = tmp_path / "run_validate.py"
        wrapper_script.write_text(f"""\
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / 'scripts')!r})

# Patch the module-level variables before importing main
import validate_standards
validate_standards.MODULES_DIR = Path({str(tmp_path / 'modules')!r})
validate_standards.errors = []

# Run validation
exit_code = validate_standards.main()
sys.exit(exit_code)
""")

        result = subprocess.run(
            [sys.executable, str(wrapper_script)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
        assert "Missing YAML frontmatter" in result.stdout or "VALIDATION FAILED" in result.stdout

    def test_validate_catches_orphan_in_index(self, tmp_path: Path):
        """An index entry with no corresponding .md file is caught."""
        module_dir = tmp_path / "modules" / "orphan-module"
        module_dir.mkdir(parents=True)

        (module_dir / "module.yaml").write_text(
            yaml.dump({"name": "orphan-module", "description": "test", "version": "0.1.0"})
        )

        # Index references ORPHAN-001, but no .md file exists
        index_data = {
            "standards": [
                {
                    "id": "ORPHAN-001",
                    "title": "Orphan standard",
                    "conformance": "MUST",
                    "enforcement": ["automated"],
                    "applies_to": {"role": "any", "platform": "any"},
                    "category": "ENG",
                    "source": "test",
                    "tags": ["test"],
                }
            ]
        }
        (module_dir / "standards-index.yaml").write_text(yaml.dump(index_data))

        # Create standards directory but no .md file
        (module_dir / "standards").mkdir()

        wrapper_script = tmp_path / "run_validate.py"
        wrapper_script.write_text(f"""\
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / 'scripts')!r})

import validate_standards
validate_standards.MODULES_DIR = Path({str(tmp_path / 'modules')!r})
validate_standards.errors = []

exit_code = validate_standards.main()
sys.exit(exit_code)
""")

        result = subprocess.run(
            [sys.executable, str(wrapper_script)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
        assert "no .md file" in result.stdout or "ORPHAN-001" in result.stdout

    def test_validate_catches_untrusted_source(self, tmp_path: Path):
        """A URL from a non-trusted domain is caught."""
        module_dir = tmp_path / "modules" / "untrusted-module"
        module_dir.mkdir(parents=True)

        (module_dir / "module.yaml").write_text(
            yaml.dump({"name": "untrusted-module", "description": "test", "version": "0.1.0"})
        )

        index_data = {
            "standards": [
                {
                    "id": "UNTRUST-001",
                    "title": "Untrusted standard",
                    "conformance": "MUST",
                    "enforcement": ["automated"],
                    "applies_to": {"role": "any", "platform": "any"},
                    "category": "ENG",
                    "source": "test",
                    "tags": ["test"],
                }
            ]
        }
        (module_dir / "standards-index.yaml").write_text(yaml.dump(index_data))

        standards_dir = module_dir / "standards"
        standards_dir.mkdir()

        # Standard with URL from untrusted domain
        standard_md = """\
---
id: UNTRUST-001
title: Untrusted standard
conformance: MUST
category: ENG
applies_to:
  role: any
  platform: any
source: test
tags: [test]
last_reviewed: 2024-01-01
---

# UNTRUST-001: Untrusted standard

## Standard

All tests MUST pass.

## Rationale

- Testing ensures quality.

## What good looks like

- Tests pass in CI.

## Enforcement

| Mechanism | What is checked | When |
|-----------|----------------|------|
| **CI** | Tests pass | On every PR |

**Primary enforcement: automated.**

## Source traceability

| Framework | Reference | URL | What it says |
|-----------|-----------|-----|--------------|
| Random Blog | Some Post | https://untrusted-blog-xyz.com/post | "Do this" |
"""
        (standards_dir / "UNTRUST-001.md").write_text(standard_md)

        # Also copy the trusted_sources.yaml for the script to find
        import shutil

        trusted_src = REPO_ROOT / "scripts" / "trusted_sources.yaml"
        # The script resolves TRUSTED_SOURCES_FILE from its own location,
        # so we patch it in the wrapper
        wrapper_script = tmp_path / "run_validate.py"
        wrapper_script.write_text(f"""\
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / 'scripts')!r})

import validate_standards
validate_standards.MODULES_DIR = Path({str(tmp_path / 'modules')!r})
validate_standards.errors = []
# Keep the real trusted_sources.yaml path (already set correctly relative to script)

exit_code = validate_standards.main()
sys.exit(exit_code)
""")

        result = subprocess.run(
            [sys.executable, str(wrapper_script)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
        assert "not in trusted_sources" in result.stdout or "untrusted" in result.stdout.lower()

    def test_validate_catches_todo_in_traceability(self, tmp_path: Path):
        """A TODO left in the traceability table is caught."""
        module_dir = tmp_path / "modules" / "todo-module"
        module_dir.mkdir(parents=True)

        (module_dir / "module.yaml").write_text(
            yaml.dump({"name": "todo-module", "description": "test", "version": "0.1.0"})
        )

        index_data = {
            "standards": [
                {
                    "id": "TODO-001",
                    "title": "Todo standard",
                    "conformance": "MUST",
                    "enforcement": ["automated"],
                    "applies_to": {"role": "any", "platform": "any"},
                    "category": "ENG",
                    "source": "test",
                    "tags": ["test"],
                }
            ]
        }
        (module_dir / "standards-index.yaml").write_text(yaml.dump(index_data))

        standards_dir = module_dir / "standards"
        standards_dir.mkdir()

        # Standard with TODO in traceability table
        standard_md = """\
---
id: TODO-001
title: Todo standard
conformance: MUST
category: ENG
applies_to:
  role: any
  platform: any
source: test
tags: [test]
last_reviewed: 2024-01-01
---

# TODO-001: Todo standard

## Standard

All tests MUST pass.

## Rationale

- Testing ensures quality.

## What good looks like

- Tests pass in CI.

## Enforcement

| Mechanism | What is checked | When |
|-----------|----------------|------|
| **CI** | Tests pass | On every PR |

**Primary enforcement: automated.**

## Source traceability

| Framework | Reference | URL | What it says |
|-----------|-----------|-----|--------------|
| TODO | TODO | TODO | "TODO" |
"""
        (standards_dir / "TODO-001.md").write_text(standard_md)

        wrapper_script = tmp_path / "run_validate.py"
        wrapper_script.write_text(f"""\
import sys
from pathlib import Path
sys.path.insert(0, {str(REPO_ROOT / 'scripts')!r})

import validate_standards
validate_standards.MODULES_DIR = Path({str(tmp_path / 'modules')!r})
validate_standards.errors = []

exit_code = validate_standards.main()
sys.exit(exit_code)
""")

        result = subprocess.run(
            [sys.executable, str(wrapper_script)],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
        assert "TODO" in result.stdout
