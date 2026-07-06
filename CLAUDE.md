# Engineering Standards — Claude Code Configuration

## Project structure

- `modules/*/standards/*.md` — source-of-truth standard files (core, python, java, typescript, org)
- `modules/*/index.yaml` — module indexes listing all standards with metadata
- `docs/` — Jekyll GitHub Pages site (source: `./docs` in CI)
- `docs/_standards/` — generated at build time by `scripts/build_site.py` (do NOT edit directly)
- `docs/sources-graph.md` — D3 force graph with source→standard linkages
- `scripts/` — build, validation, and scaffolding tools
- `scripts/trusted_sources.yaml` — allowed domains for source traceability

## Key conventions

- Standards use RFC 2119 conformance levels: MUST, SHOULD, COULD
- Every standard traces to at least one published framework in its `## Source traceability` table
- MUST standards require at least one Tier 1 source
- The `source` frontmatter field is kebab-case (e.g. `technology-code-of-practice`)
- The graph data in `sources-graph.md` must stay in sync with actual traceability tables — use `/rebuild-graph` after changes

## Skills

- `/new-standard` — scaffold a new standard with guided prompts
- `/rebuild-graph` — regenerate sources graph from traceability tables
- `/preflight` — validate + build check before pushing
- `/impact` — show what's affected by a source or standard change
- `/add-source` — add a new source framework with trust criteria gate
