# Java / Spring Boot Standards

Standards for Java services using Spring Boot. Apply these alongside core.

## Standards

| ID | Standard | Level | Enforcement | Why it exists |
|----|----------|-------|-------------|---------------|
| JV-001 | Use constructor injection | SHOULD | peer-review | Field injection hides dependencies and prevents immutability |
| JV-002 | Use SLF4J for logging | SHOULD | automated | System.out bypasses the logging framework; lost in production |
| JV-003 | Use parameterised queries | MUST | automated, peer-review | String concatenation in SQL = injection |
| JV-004 | Validate request DTOs with @Valid | SHOULD | peer-review | Without @Valid, malformed requests reach business logic |
| JV-005 | Secure all Spring Boot endpoints | MUST | periodic-audit | Unauthenticated Spring Boot service = one URL away from breach |
| JV-006 | Use SLF4J abstraction over Log4j directly | SHOULD | automated | Direct Log4j = exposure to Log4Shell-class vulnerabilities |
| JV-007 | Use records for data carriers | SHOULD | peer-review | 50 lines of getters/setters when a record does it in 1 |
| JV-008 | Use structured logging (JSON) | SHOULD | peer-review, automated | Plain text logs can't be parsed by log aggregators |

## How to use

Query all Java standards:

```bash
python scripts/query_standards.py --module java
```

Filter by conformance level:

```bash
python scripts/query_standards.py --module java --conformance MUST
```
