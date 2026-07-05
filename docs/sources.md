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

## How sources are used

Each standard's `.md` file has a **Source traceability** section that links to the specific clause, point, or recommendation within the source framework. This ensures:

- Every standard has authority behind it (not opinion)
- Assessors can verify alignment with the originating framework
- If a source framework updates, affected standards can be identified and reviewed
