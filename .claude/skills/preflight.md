---
name: preflight
description: Validate standards, build the site, and catch errors before pushing to main
---

# Preflight Check

Run the full validation and build pipeline locally to catch errors before they hit CI.

## Steps

1. **Validate standards** — run `python scripts/validate_standards.py`
   - Checks frontmatter fields are present and valid
   - Checks conformance values are MUST/SHOULD/COULD
   - Checks source URLs are from trusted domains
   - Checks index.yaml entries match standard files
   - Report any errors clearly

2. **Build site** — run `python scripts/build_site.py`
   - Generates `docs/_standards/` from module sources
   - Confirms all standards are copied successfully
   - Report the count

3. **Check for Liquid syntax issues** — grep for `{{`, `{%` in `docs/_standards/*.md` that are NOT wrapped in `{% raw %}` blocks. The build script should handle this but flag any that slip through.

4. **Summary** — report pass/fail for each step. If all pass, it's safe to push. If any fail, explain what needs fixing.

## Notes

- Requires Python 3 with `pyyaml` installed (`pip install pyyaml`)
- Does NOT require Jekyll locally — the CI handles the actual Jekyll build
- Run from the repo root directory
