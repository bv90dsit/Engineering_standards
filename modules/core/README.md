# Core Engineering Standards

Cross-cutting standards that apply to every UK Government digital service regardless of language or framework.

## Standards

| ID | Standard | Level | Enforcement | Why it exists |
|----|----------|-------|-------------|---------------|
| ENG-001 | Make source code open | MUST | automated, periodic-audit | UK Gov policy since 2017; enables reuse and scrutiny |
| ENG-002 | Use version control | MUST | automated, peer-review | Foundation for collaboration, audit, and rollback |
| ENG-003 | Use continuous integration | MUST | automated | Catches defects before production; enables safe frequent deployment |
| ENG-004 | Maintain documentation | SHOULD | automated, peer-review | Government teams have high turnover; poor docs = weeks of lost productivity |
| ENG-005 | Track technical debt | SHOULD | ways-of-working | Untracked debt accumulates until velocity collapses |
| ENG-006 | Conduct code reviews | COULD | ways-of-working | Reduces knowledge silos and bus factor |
| ENG-007 | Keep pull requests small and short-lived | SHOULD | ways-of-working | Stale PRs block deployment frequency (DORA lead time) |
| SEC-001 | Enforce TLS everywhere | MUST | automated, periodic-audit | Minimum bar for data in transit |
| SEC-002 | Scan dependencies for vulnerabilities | MUST | automated | Third-party deps are the most common attack vector |
| SEC-003 | Never commit secrets | MUST | automated | #1 source of government security incidents |
| SEC-004 | Validate and sanitise all input | MUST | peer-review, automated | Injection is consistently OWASP Top 10 |
| SEC-005 | Use established auth frameworks | MUST | periodic-audit | Custom auth = guaranteed vulnerabilities |
| SEC-006 | Scan container images | SHOULD | automated | Container images have their own vulnerability lifecycle |
| SEC-007 | Conduct security reviews | MUST | periodic-audit | Automated tools miss business logic flaws |
| SEC-008 | Implement rate limiting | MUST | automated, periodic-audit | Government services are high-value targets for bots |
| SEC-009 | Configure CORS correctly | MUST | peer-review, automated | Misconfigured CORS = data exfiltration |
| ARC-001 | Use cloud hosting | SHOULD | periodic-audit | Cloud-first is UK Gov policy since 2013 |
| ARC-002 | Use infrastructure as code | SHOULD | peer-review, periodic-audit | Prevents "only works in prod" and enables portability |
| ARC-003 | Design API-first | SHOULD | peer-review, automated | APIs are how government services connect |
| ARC-004 | Document architecture decisions | SHOULD | peer-review | Context disappears when people leave |
| ARC-005 | Design for resilience | SHOULD | peer-review, periodic-audit | Without resilience, one failure cascades to all |
| ARC-006 | Define SLOs | SHOULD | periodic-audit | Public services have availability obligations |
| OPS-001 | Implement structured logging and monitoring | MUST | periodic-audit, ways-of-working | You can't fix what you can't see |
| OPS-002 | Deploy frequently | SHOULD | periodic-audit, ways-of-working | Infrequent deployment = high-risk big-bang releases |
| OPS-003 | Conduct blameless post-mortems | MUST | ways-of-working | Without post-mortems, the same incident repeats |
| OPS-004 | Test disaster recovery | MUST | periodic-audit | Untested DR plans are fiction |
| OPS-005 | Track change failure rate | SHOULD | periodic-audit, ways-of-working | Measures whether changes are causing failures |
| OPS-006 | Use correlation IDs | MUST | peer-review, automated | Without correlation IDs, debugging across services is guessing |
| OPS-007 | Define on-call responsibilities | MUST | periodic-audit, ways-of-working | Assessors ask "who's responsible when it breaks?" |
| DAT-001 | Classify data | MUST | ways-of-working, periodic-audit | Classification determines handling controls |
| DAT-002 | Define data retention policies | MUST | periodic-audit | UK GDPR storage limitation principle |
| DAT-003 | Test backup restoration | MUST | periodic-audit, ways-of-working | Untested backups are not backups |
| DAT-004 | Publish open data | SHOULD | periodic-audit | Public data belongs to the public |
| DAT-005 | Maintain audit trails | MUST | peer-review, periodic-audit | GDPR accountability -- prove who changed what |
| ACC-001 | Meet WCAG 2.2 AA | MUST | automated, periodic-audit | Legal requirement (Public Sector Bodies Accessibility Regulations 2018) |
| ACC-002 | Apply progressive enhancement | SHOULD | peer-review | Users on old devices, corporate proxies, assistive tech |
| ACC-003 | Write in plain English | SHOULD | peer-review | Government content must be readable by everyone |
| EMG-001 | Require human accountability for AI outputs | MUST | peer-review, ways-of-working | Accountability stays with humans, not tools |
| EMG-002 | Disclose AI-generated content | SHOULD | periodic-audit | Public trust requires transparency about AI use |
| EMG-003 | Validate AI outputs before use | MUST | peer-review, automated | AI hallucinates; government services must be accurate |
| EMG-004 | Assess AI systems for bias | SHOULD | periodic-audit | Biased training data produces discriminatory outcomes |

## How to use

Query all core standards:

```bash
python scripts/query_standards.py --module core
```

Filter by conformance level:

```bash
python scripts/query_standards.py --module core --conformance MUST
```

Filter by category:

```bash
python scripts/query_standards.py --module core --category SEC
```
