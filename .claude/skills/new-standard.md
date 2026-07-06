---
name: new-standard
description: Scaffold a new engineering standard with guided prompts for ID, conformance, sources, and validation
---

# New Standard

Scaffold a new engineering standard in the correct module directory with all required sections.

## Steps

1. Ask the user for:
   - **Standard ID** (e.g. SEC-010, PY-011) — check it doesn't already exist in `modules/*/standards/`
   - **Title** — short, imperative description
   - **Conformance level** — MUST, SHOULD, or COULD
   - **Module** — which module directory (core, python, java, typescript, org)
   - **Source frameworks** — which authoritative sources back this standard (minimum one Tier 1 for MUST)
   - **Brief description** of what the standard requires

2. Determine the category from the ID prefix (ENG, SEC, OPS, ARC, DAT, ACC, EMG, PY, JV, TS, ORG).

3. Create the standard file at `modules/{module}/standards/{ID}.md` with this structure:
   - Frontmatter: id, title, conformance, category, applies_to, source, tags, last_reviewed
   - `## Standard` — the requirement statement
   - `## Rationale` — why this matters
   - `## What good looks like` — concrete implementation examples
   - `## What bad looks like` — anti-patterns
   - `## Enforcement` — table with mechanism, what is checked, when
   - `## Source traceability` — table with Framework, Reference, URL, What it says

4. Run validation: `python scripts/validate_standards.py` to check the file is well-formed.

5. Check if the standard's sources already exist in the graph data in `docs/sources-graph.md`. If not, note that `/rebuild-graph` should be run after.

## Important

- MUST standards require at least one Tier 1 source (check `scripts/trusted_sources.yaml`)
- The `last_reviewed` date should be today's date
- The `source` frontmatter field is the kebab-case source name (e.g. `technology-code-of-practice`)
- Tags should be lowercase, hyphenated
- Check `modules/{module}/index.yaml` exists and add the standard entry there too
