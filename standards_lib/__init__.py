"""standards_lib — importable library for querying UK Gov engineering standards."""

from __future__ import annotations

from standards_lib.query import (
    get_standard,
    list_categories,
    list_tags,
    load_index,
    query_standards,
    to_json,
)

__all__ = [
    "load_index",
    "query_standards",
    "get_standard",
    "list_categories",
    "list_tags",
    "to_json",
]
