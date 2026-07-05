# TypeScript / React / Node Standards

Standards for TypeScript frontends and Node.js services. Apply these alongside core.

## Standards

| ID | Standard | Level | Enforcement | Why it exists |
|----|----------|-------|-------------|---------------|
| TS-001 | Enable strict mode in tsconfig | MUST | automated | Without strict mode, TypeScript is barely better than JavaScript |
| TS-002 | Avoid using `any` | SHOULD | automated, peer-review | `any` defeats the entire type system |
| TS-003 | Type all API responses | SHOULD | peer-review | Untyped API responses mean backend changes silently break frontend |
| TS-004 | Use a structured logger instead of console.log | SHOULD | automated | console.log leaks info, no levels, no routing |
| TS-005 | Use React error boundaries | SHOULD | peer-review | Without error boundaries, one component crash blanks the page |
| TS-006 | Validate environment variables at startup | MUST | peer-review, automated | Missing env var at request time = 500 error in production |
| TS-007 | Enable and configure ESLint | SHOULD | automated | ESLint catches bugs the type system misses |
| TS-008 | Never use @ts-ignore without explanation | MUST | automated, peer-review | @ts-ignore without comment silently defeats type safety |

## How to use

Query all TypeScript standards:

```bash
python scripts/query_standards.py --module typescript
```

Filter by conformance level:

```bash
python scripts/query_standards.py --module typescript --conformance MUST
```
