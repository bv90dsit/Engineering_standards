# Source Frameworks

Every standard traces back to at least one published framework. This page lists all sources referenced across the standards, grouped by authority.

## UK Government

| Source | Publisher | Standards derived |
|--------|-----------|-------------------|
| [Technology Code of Practice](https://www.gov.uk/guidance/the-technology-code-of-practice) | CDDO | ENG-001, ENG-002, ARC-001, DAT-004, ENG-005, EMG-001 |
| [GOV.UK Service Standard](https://www.gov.uk/service-manual/service-standard) | GDS | ENG-003, OPS-001, OPS-002, ACC-002, ARC-004, ARC-005, ENG-004, ENG-006, OPS-003 |
| [NCSC Secure by Design](https://www.ncsc.gov.uk/collection/developers-collection) | NCSC / DSIT | SEC-001, SEC-003, SEC-005, SEC-006, SEC-007, DAT-003, OPS-004 |
| [Government Security Classifications](https://www.gov.uk/government/publications/government-security-classifications) | Cabinet Office | DAT-001 |
| [UK GDPR / Data Protection Act 2018](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/) | ICO | DAT-002 |
| [Public Sector Bodies Accessibility Regulations 2018](https://www.legislation.gov.uk/uksi/2018/952) | UK Parliament | ACC-001 |
| [GDS API Technical and Data Standards](https://www.gov.uk/guidance/gds-api-technical-and-data-standards) | GDS | ARC-003 |
| [CDDO Generative AI Framework](https://www.gov.uk/government/publications/generative-ai-framework-for-hmg) | CDDO | EMG-002, EMG-003, EMG-004 |

## International Standards Bodies

| Source | Publisher | Standards derived |
|--------|-----------|-------------------|
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | OWASP Foundation | SEC-002, SEC-004, PY-003, PY-005, JV-003 |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | OWASP Foundation | SEC-001, SEC-004, SEC-005 |
| [ISO 27001](https://www.iso.org/standard/27001) | ISO | DAT-003 |
| [ISO 22301](https://www.iso.org/standard/75106.html) | ISO | OPS-004 |
| [NIST SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) | NIST | SEC-002 |
| [NIST SP 800-63](https://pages.nist.gov/800-63-3/) | NIST | SEC-005 |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | W3C | ACC-001 |

## Industry Research & Practice

| Source | Publisher | Standards derived |
|--------|-----------|-------------------|
| [DORA Metrics / State of DevOps](https://dora.dev/) | Google / DORA team | OPS-002, OPS-005 |
| [Accelerate](https://itrevolution.com/product/accelerate/) | Forsgren, Humble, Kim | OPS-002, OPS-005 |
| [12-Factor App](https://12factor.net/) | Heroku / Adam Wiggins | ARC-002, TS-006 |
| [Google SRE Book](https://sre.google/sre-book/table-of-contents/) | Google | OPS-001, OPS-003 |

## Language & Framework Documentation

| Source | Standards derived |
|--------|-------------------|
| [Python logging HOWTO](https://docs.python.org/3/howto/logging.html) | PY-001 |
| [PEP 484 — Type Hints](https://peps.python.org/pep-0484/) | PY-002 |
| [PEP 8 — Style Guide](https://peps.python.org/pep-0008/) | PY-004 |
| [Django Security Docs](https://docs.djangoproject.com/en/stable/topics/security/) | PY-005, PY-008 |
| [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/) | PY-008 |
| [Flask Configuration Handling](https://flask.palletsprojects.com/en/stable/config/) | PY-006 |
| [Spring Framework — Constructor Injection](https://docs.spring.io/spring-framework/reference/core/beans/dependencies.html) | JV-001 |
| [Spring Security Reference](https://docs.spring.io/spring-security/reference/) | JV-005 |
| [SLF4J Manual](https://www.slf4j.org/manual.html) | JV-006 |
| [TypeScript Handbook — strict](https://www.typescriptlang.org/tsconfig#strict) | TS-001 |
| [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) | TS-005 |

## How standards are synthesised from multiple sources

Most standards trace to more than one source. When multiple frameworks cover the same concern, we synthesise them — not by picking one, but by combining their strengths.

### Principles

1. **The standard statement uses the tightest common ground** — the requirement all sources agree on
2. **"What good looks like" pulls specifics from the most detailed source** — concrete implementation guidance
3. **We never contradict a source** — if sources disagree on strictness, we take the stricter position and note the difference
4. **We never invent requirements beyond what sources say** — enforcement and tooling are our value-add, not the requirement itself
5. **The source traceability table cites the specific clause** — not just the framework name

### Worked example: SEC-001 (HTTPS everywhere)

Three sources inform this standard:

| Source | Specific reference | What it says |
|--------|-------------------|--------------|
| NCSC Secure by Design | Transport Layer Security | "Use TLS 1.2 or above for all connections. Enable HSTS." |
| OWASP ASVS | V9.1.1 | "Verify that TLS is used for all client connectivity, not just limited to sensitive endpoints." |
| GDS Service Standard | Point 9: Create a secure service | "Protect users' privacy... evaluate what data the service collects, stores and provides." |

**How they were combined:**

| Part of the standard | Where it came from |
|---------------------|-------------------|
| "All services MUST use HTTPS for every connection, with no HTTP fallback" | Tightest common ground — all three require it |
| "TLS 1.2 is the minimum; TLS 1.3 SHOULD be preferred" | NCSC (most specific on protocol version) |
| "HSTS headers with a minimum max-age of 1 year" | NCSC (specific technical requirement) |
| "No mixed content warnings" | OWASP (verification criterion) |
| "Certificate renewal is automated" | Our operational guidance — not in any source, but derived from "What good looks like" for maintaining TLS |

**What was NOT included:**

- GDS Point 9 is broader than just HTTPS — we didn't expand the standard to cover all of Point 9
- OWASP V9 has sub-requirements about cipher suites — we kept SEC-001 focused on the core requirement and would create SEC-008 if cipher suite guidance were needed
- None of the sources specify *enforcement mechanism* — that's our addition (automated grep for `http://` + periodic audit for TLS config)

### Template for traceability

When writing a new standard that draws from multiple sources:

```markdown
## Source traceability

| Framework | Reference | URL | What it says |
|-----------|-----------|-----|--------------|
| [Source 1] | Clause/section number | https://... | Direct quote or paraphrase of what this source requires |
| [Source 2] | Clause/section number | https://... | What this source adds beyond Source 1 |
| [Source 3] | Clause/section number | https://... | Additional context or authority |
```

Every row must have:
- **Framework** — the publishing body or document name
- **Reference** — the specific clause, section, or point number
- **URL** — direct link to the source (use `—` if internal/unpublished)
- **What it says** — a short quote or paraphrase of the specific requirement; shows *why* this source is listed, not just that it exists
