# UK Government Engineering Standards

When writing code for UK Government digital services, proactively follow these standards without being asked. Don't wait for a compliance check to catch violations — write compliant code from the start.

## Always (all languages)

- Open source by default (ENG-001)
- Version control for all source code (ENG-002)
- Continuous integration and automated testing (ENG-003)
- HTTPS everywhere (SEC-001)
- Dependency vulnerability scanning (SEC-002)
- Twelve-factor application design (ARC-002)
- Documentation for onboarding (README, ADRs, runbooks) (ENG-004)
- No secrets in source code (SEC-003)
- Input validation and output encoding (SEC-004)
- Container image scanning (SEC-006)
- APIs follow RESTful conventions and are versioned (ARC-003)
- Architecture Decision Records maintained (ARC-004)
- Resilience patterns (retry, circuit-breaker, timeouts) (ARC-005)
- WCAG 2.2 AA compliance (ACC-001)
- Progressive enhancement (ACC-002)
- AI-generated code must be reviewed as any other contribution (EMG-001)
- AI outputs validated before user-facing use (EMG-003)
- API rate limiting (SEC-008)
- CORS explicitly configured (SEC-009)
- Structured logging with correlation IDs (OPS-006)
- Content written in plain English (ACC-003)
- Audit trail for data changes (DAT-005)

## Python

- Use logging module, not print() (PY-001)
- Type hints on public function signatures (PY-002)
- No raw SQL string construction (PY-003)
- No wildcard imports (PY-004)
- Django CSRF protection must not be disabled (PY-005)
- Flask secret key must not be hardcoded (PY-006)
- Use Django ORM or SQLAlchemy, not raw SQL (PY-007)
- Django DEBUG must be False in production config (PY-008)
- Pin dependencies with a lock file (PY-009)
- Use pathlib for file operations (PY-010)

## Java / Spring Boot

- Use constructor injection, not field injection (JV-001)
- No System.out.println in production code (JV-002)
- Use parameterised queries with JPA/JDBC (JV-003)
- REST controllers must validate input with @Valid (JV-004)
- Use SLF4J for logging, not java.util.logging or Log4j directly (JV-006)
- Use records for DTOs (Java 17+) (JV-007)
- Structured logging in JSON format (JV-008)

## TypeScript / React / Node

- Strict mode enabled in tsconfig.json (TS-001)
- No use of 'any' type (TS-002)
- API responses must be typed (TS-003)
- No console.log in production code (TS-004)
- React components must handle error boundaries (TS-005)
- Environment variables validated at startup (TS-006)
- ESLint with strict ruleset configured (TS-007)
- No @ts-ignore without justification (TS-008)

## Before finishing

Ask yourself: would this code pass `python scripts/check_compliance.py`? If not, fix it now rather than letting CI catch it.

## Source

These standards are from the [UK Government Engineering Standards](https://github.com/bv90dsit/Engineering_standards) repository. Each rule traces back to an authoritative framework (GDS Service Standard, NCSC, OWASP, WCAG, etc.).
