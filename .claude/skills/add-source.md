---
name: add-source
description: Add a new source framework with trust criteria gate, update trusted_sources.yaml and graph
---

# Add Source Framework

Add a new authoritative or established source to the standards framework, with a trust criteria gate.

## Steps

1. **Gather information** — ask the user for:
   - Source name (e.g. "CIS Benchmarks")
   - Publisher / organisation
   - URL (primary domain)
   - Proposed tier (1 = Authoritative, 2 = Established)

2. **Trust criteria gate** — ask the four questions. All four should be "yes" for Tier 1; at least questions 1 and 2 for Tier 2:

   | # | Question | Required for |
   |---|----------|:---:|
   | 1 | **Would a GDS service assessor accept this as evidence?** If you'd be embarrassed citing it in a service assessment, it doesn't belong. | Tier 1 & 2 |
   | 2 | **Is it a primary source?** Not a blog post about a primary source. We cite the standard itself, not someone's explanation of it. | Tier 1 & 2 |
   | 3 | **Is it recognised by the UK Gov digital community?** Referenced in GDS guidance, NCSC recommendations, or cross-government architecture. | Tier 1 |
   | 4 | **Has it been stable for 3+ years?** A source that might disappear next year isn't a foundation for a standard. | Tier 1 |

   If the source fails the gate:
   - Suggest it belongs in "What good looks like" sections (implementation guidance) rather than source traceability
   - Ask if the user wants to proceed anyway (they may have context you don't)

3. **Update `scripts/trusted_sources.yaml`** — add the domain under the appropriate tier section with a rationale comment explaining why it qualifies.

4. **Update `docs/sources-graph.md`** — add a new node to the appropriate tier array in the JavaScript `data` object:
   ```js
   { id: "short-id", label: "Display\nName", url: "https://...", standards: [] }
   ```
   The standards array starts empty — it gets populated when standards reference this source.

5. **Ask about existing standards** — "Do any existing standards already reference this source in their traceability tables?" If yes, add those IDs to the graph node's standards array.

6. **Update `docs/sources.md`** — add the source to the appropriate section (UK Government, International Standards Bodies, or Industry Research & Practice) with its URL and any standards derived.

7. **Report** — summarise what was added and remind the user to run `/rebuild-graph` after linking standards to this source.

## Important

- The domain added to `trusted_sources.yaml` should be the bare domain (e.g. `cisecurity.org` not `https://www.cisecurity.org/benchmark/docker`)
- Tier 1 sources can be the sole authority for a MUST standard
- Tier 2 sources should be paired with a Tier 1 source for MUST standards
- Sources that fail the trust criteria belong in implementation guidance, not traceability
