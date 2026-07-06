---
name: impact
description: Show what standards, graph nodes, and pages are affected when a source or standard changes
---

# Impact Analysis

When a source framework or standard changes, show everything that's affected across the repo.

## Usage

The user provides either:
- A **source name** (e.g. "NCSC Secure by Design", "DORA") — show all standards that trace to it
- A **standard ID** (e.g. "SEC-001") — show what sources back it and what would break if it changed

## Steps for source impact

1. Grep all `modules/*/standards/*.md` files for the source name in their `## Source traceability` tables.

2. List all affected standards with their:
   - ID and title
   - Conformance level
   - Whether this source is the **sole Tier 1 backing** (critical — removing it could invalidate a MUST)

3. Check `docs/sources-graph.md` — show the graph node ID and current linkage count.

4. Check `docs/sources.md` — show where this source appears in the documentation.

5. Flag risks:
   - Standards where this is the only Tier 1 source (MUST standards need Tier 1)
   - Standards that would have NO source traceability if this source were removed

## Steps for standard impact

1. Read the standard file and list all its sources from the traceability table.

2. Show which other standards share the same sources (siblings/related standards).

3. Check if it appears in:
   - `docs/sources-graph.md` (graph data)
   - `docs/index.md` (main page listing)
   - Any `index.yaml` files

4. Show enforcement mechanism — what CI checks would need updating if the standard changed.

## Output format

Present as a clear summary with sections for: affected standards, graph impact, documentation impact, and risk flags.
