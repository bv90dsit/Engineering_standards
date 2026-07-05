---
layout: default
title: About
permalink: /about/
---

# What are these standards?

A set of engineering rules that UK Government digital teams follow when building services. They cover security, accessibility, operations, architecture, and how to use AI responsibly.

## Why do they exist?

Government digital services affect millions of people. These standards exist to ensure services are:

- **Secure** — protecting citizen data from breaches
- **Accessible** — usable by everyone, including people with disabilities (it's the law)
- **Reliable** — available when people need them
- **Maintainable** — sustainable beyond the team that built them

## Who are they for?

| Role | How you use them |
|------|-----------------|
| **Engineers** | Follow the standards when writing code; tooling catches issues automatically |
| **Tech leads** | Add the CI check to your repos; choose which modules apply to your stack |
| **Delivery managers** | Use the conformance levels (MUST/SHOULD/COULD) to plan what's needed for assessment |
| **Security leads** | Filter by the SEC category to see the security baseline |
| **Service assessors** | Standards trace back to GDS Service Standard and NCSC — use them as evidence criteria |

## How they work

Every standard has:

- **A conformance level** — MUST (required), SHOULD (expected), or COULD (recommended)
- **An enforcement mechanism** — how compliance is checked (automated in CI, peer review, service assessment, or team practice)
- **Source traceability** — links to the authoritative framework it derives from (GDS, NCSC, OWASP, etc.)
- **Practical guidance** — copy-paste config and code examples so engineers can comply immediately

## How to adopt

1. **Run the scanner** against your repo — it tells you which standards apply
2. **Add the CI check** — one YAML file, every PR checks compliance automatically
3. **Install the VS Code extension** — instant feedback as you type

Full technical setup: [GitHub Repository](https://github.com/bv90dsit/Engineering_standards)

## Key numbers

- **69 standards** across 5 modules
- **35 MUST** (non-negotiable) / **33 SHOULD** / **1 COULD**
- **22 rules** checked automatically in your editor
- Every standard traces to at least one published authoritative source
