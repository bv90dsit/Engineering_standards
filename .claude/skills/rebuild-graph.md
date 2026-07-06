---
name: rebuild-graph
description: Regenerate the sources graph data from actual source traceability tables in all standards
---

# Rebuild Sources Graph

Scan all standard files and rebuild the D3 force graph data in `docs/sources-graph.md` to match the actual source traceability tables.

## Steps

1. Scan all `modules/*/standards/*.md` files and extract the `## Source traceability` table from each. For each standard, collect the framework names listed in the first column.

2. Map each framework name to its graph node ID using this mapping:
   - **Tier 1**: Technology Code of Practice → `tcop`, GDS Service Standard/Manual/API Standards → `gds`, NCSC (any variant) → `ncsc`, OWASP (any variant) → `owasp`, WCAG → `wcag`, NIST/ISO → `nist`, UK GDPR/ICO → `ukgdpr`, Accessibility Regs → `accessibility`, CDDO (any variant) → `cddo-ai`, Government Security Classifications/Cabinet Office → `gsc`, IETF → `ietf`
   - **Tier 2**: DORA (any variant) → `dora`, 12-Factor App → `12factor`, Google SRE/Engineering → `sre`, AWS Well-Architected → `aws-wa`, Accelerate → `accelerate`, OpenAPI → `openapi`, Spring (any variant) → `spring`, Python docs/PEP → `python-docs`, Django → `django`, TypeScript → `typescript`, React → `react`, MDN → `mdn`

3. Build the standards array for each node (sorted alphabetically).

4. Replace the `const data = { tier1: [...], tier2: [...] };` block in `docs/sources-graph.md` with the regenerated data. Preserve the node labels, URLs, and structure — only update the `standards` arrays.

5. Also update the `## Source → Standards reference` table below the graph to match.

6. Report a summary: how many linkages changed, any new standards not connected to any graph node (these may need a new node or source mapping).

## When to run

- After creating a new standard (`/new-standard`)
- After editing a standard's source traceability table
- After adding a new source (`/add-source`)
- Periodically as a consistency check
