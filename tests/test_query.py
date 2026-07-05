"""Tests for standards_lib/query.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure standards_lib is importable from repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from standards_lib.query import (
    get_standard,
    list_categories,
    list_modules,
    list_tags,
    load_index,
    query_standards,
    to_json,
)


class TestLoadIndex:
    """Tests for the load_index function."""

    def test_load_index_returns_list(self):
        """Basic loading works and returns a list."""
        result = load_index()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_load_index_core_default(self):
        """No module arg returns core only."""
        result = load_index()
        # All entries should be tagged as 'core' module
        modules_in_result = {s.get("_module") for s in result}
        assert modules_in_result == {"core"}

    def test_load_index_specific_module(self):
        """module='python' returns only python standards."""
        result = load_index(module="python")
        assert isinstance(result, list)
        assert len(result) > 0
        modules_in_result = {s.get("_module") for s in result}
        assert modules_in_result == {"python"}

    def test_load_index_all(self):
        """module='all' returns everything from all modules."""
        result = load_index(module="all")
        assert isinstance(result, list)
        assert len(result) > 0
        # Should have more than just core
        modules_in_result = {s.get("_module") for s in result}
        assert "core" in modules_in_result
        assert len(modules_in_result) > 1

    def test_load_index_invalid_module_raises(self):
        """Bad module name raises ValueError."""
        with pytest.raises(ValueError, match="not found"):
            load_index(module="nonexistent-module-xyz")


class TestQueryFilters:
    """Tests for the query_standards filtering."""

    def test_query_filter_by_conformance(self):
        """MUST filter works — all returned items have conformance=MUST."""
        result = query_standards(conformance="MUST", module="core")
        assert len(result) > 0
        for s in result:
            assert s["conformance"] == "MUST"

    def test_query_filter_by_category(self):
        """SEC filter works — all returned items have category=SEC."""
        result = query_standards(category="SEC", module="core")
        assert len(result) > 0
        for s in result:
            assert s["category"] == "SEC"

    def test_query_filter_by_tag(self):
        """Filtering by tag returns only matching standards."""
        result = query_standards(tag="ci", module="core")
        assert len(result) > 0
        for s in result:
            assert "ci" in s["tags"]

    def test_query_filter_by_enforcement(self):
        """Automated filter works — all returned items have 'automated' in enforcement."""
        result = query_standards(enforcement="automated", module="core")
        assert len(result) > 0
        for s in result:
            assert "automated" in s["enforcement"]

    def test_query_filter_combined(self):
        """Multiple filters at once narrows results correctly."""
        result = query_standards(
            conformance="MUST", category="SEC", module="core"
        )
        assert len(result) > 0
        for s in result:
            assert s["conformance"] == "MUST"
            assert s["category"] == "SEC"


class TestGetStandard:
    """Tests for the get_standard function."""

    def test_get_standard_returns_content(self):
        """Reads a .md file and returns its content."""
        content = get_standard("ENG-001")
        assert isinstance(content, str)
        assert "ENG-001" in content
        assert "---" in content  # has frontmatter

    def test_get_standard_not_found_raises(self):
        """Missing ID raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="not found"):
            get_standard("NONEXISTENT-999")


class TestListFunctions:
    """Tests for list_modules, list_categories, list_tags."""

    def test_list_modules(self):
        """Returns all module metadata as a list of dicts."""
        result = list_modules()
        assert isinstance(result, list)
        assert len(result) > 0
        # Each entry should have at least a name
        for m in result:
            assert "name" in m
            assert "path" in m

    def test_list_categories(self):
        """Returns sorted unique categories."""
        result = list_categories()
        assert isinstance(result, list)
        assert len(result) > 0
        # Should be sorted
        assert result == sorted(result)
        # Should contain known categories
        assert "ENG" in result
        assert "SEC" in result

    def test_list_tags(self):
        """Returns sorted unique tags."""
        result = list_tags()
        assert isinstance(result, list)
        assert len(result) > 0
        # Should be sorted
        assert result == sorted(result)


class TestToJson:
    """Tests for the to_json serialization."""

    def test_to_json(self):
        """Serializes to valid JSON."""
        standards = load_index()
        json_str = to_json(standards)
        assert isinstance(json_str, str)
        # Should be valid JSON
        parsed = json.loads(json_str)
        assert isinstance(parsed, list)
        assert len(parsed) == len(standards)
