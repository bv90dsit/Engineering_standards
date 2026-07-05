"""Shared fixtures for the engineering standards test suite."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


@pytest.fixture
def repo_root() -> Path:
    """Return the root path of this repository."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def tmp_module(tmp_path: Path) -> Path:
    """Create a temporary module directory with a minimal valid standard for testing.

    Returns the path to the temporary module directory.
    """
    module_dir = tmp_path / "modules" / "test-module"
    module_dir.mkdir(parents=True)

    # module.yaml
    module_yaml = {
        "name": "test-module",
        "description": "Temporary test module",
        "version": "0.1.0",
        "author": "Test",
        "applies_to": {"role": "any", "platform": "python"},
    }
    (module_dir / "module.yaml").write_text(yaml.dump(module_yaml))

    # standards-index.yaml
    index_data = {
        "standards": [
            {
                "id": "TEST-001",
                "title": "Test standard",
                "conformance": "MUST",
                "enforcement": ["automated"],
                "applies_to": {"role": "any", "platform": "python"},
                "category": "ENG",
                "source": "test-source",
                "tags": ["testing", "automation"],
            }
        ]
    }
    (module_dir / "standards-index.yaml").write_text(yaml.dump(index_data))

    # standards/TEST-001.md
    standards_dir = module_dir / "standards"
    standards_dir.mkdir()
    standard_md = """\
---
id: TEST-001
title: Test standard
conformance: MUST
category: ENG
applies_to:
  role: any
  platform: python
source: test-source
tags: [testing, automation]
last_reviewed: 2024-01-01
---

# TEST-001: Test standard

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
| GDS | Service Standard | https://gov.uk/service-standard | "Test your service" |
"""
    (standards_dir / "TEST-001.md").write_text(standard_md)

    # rules.json (minimal)
    rules_json = {
        "rules": [
            {
                "id": "TEST-001",
                "pattern": "# TODO",
                "filePattern": "**/*.py",
                "severity": "warning",
                "message": "TODO found in code",
            }
        ]
    }
    import json

    (module_dir / "rules.json").write_text(json.dumps(rules_json, indent=2))

    return module_dir
