---
layout: default
title: Future Sources
permalink: /future-sources/
---

# Future Sources to Consider

International government and industry frameworks that may inform future standards. These have not been formally assessed or adopted — they are candidates for review.

## International Government

| Source | Country | URL | What it covers | Potentially informs |
|--------|---------|-----|----------------|---------------------|
| US Digital Service Playbook | USA | https://playbook.cio.gov/ | 13 plays for digital service delivery | ENG, OPS, ARC |
| 18F Engineering Practices | USA | https://engineering.18f.gov/ | Coding standards, testing, CI/CD, accessibility | ENG, ACC, SEC |
| Singapore SGTS | Singapore | https://www.developer.tech.gov.sg/ | Reference architectures, approved tooling, security baseline | ARC, SEC |
| Australia DTA Digital Service Standard | Australia | https://www.dta.gov.au/help-and-advice/about-digital-service-standard | 13 criteria modelled on UK GDS | ENG, OPS, ACC |
| EU Interoperability Framework | EU | https://joinup.ec.europa.eu/collection/nifo-national-interoperability-framework-observatory/european-interoperability-framework-detail | Cross-border interoperability, open standards, API design | ARC, DAT |
| Canada CDS | Canada | https://digital.canada.ca/standards/ | Digital standards, accessibility, bilingual delivery | ACC, ENG |
| Estonia X-Road | Estonia | https://x-road.global/ | Secure data exchange infrastructure | ARC, SEC |
| NZ Digital Service Standard | New Zealand | https://www.digital.govt.nz/standards-and-guidance/ | Digital standards, privacy, accessibility | ENG, ACC |

## Industry & Research

| Source | URL | What it covers | Potentially informs |
|--------|-----|----------------|---------------------|
| CNCF Cloud Native Maturity Model | https://maturitymodel.cncf.io/ | Cloud-native best practices, Kubernetes patterns | ARC, OPS |
| ThoughtWorks Technology Radar | https://www.thoughtworks.com/radar | Industry trends, tool recommendations | ENG (advisory) |
| IEEE Software Engineering Standards | https://www.ieee.org/communities/societies/computer-society.html | Formal software engineering processes | ENG (formal) |
| NIST Secure Software Development Framework | https://csrc.nist.gov/Projects/ssdf | Secure development lifecycle practices | SEC |
| ISO 25010 (Software Quality) | https://www.iso.org/standard/35733.html | Quality characteristics model | ENG, OPS |

## How to propose adding a source

If you believe one of these (or another framework) should become a formal source:

1. Open an issue explaining which standards it would inform and why
2. Include: the specific clause/section, how it differs from what we already cite, and why it adds authority
3. A maintainer assesses against the [trusted sources criteria](sources.md) (Tier 1 or Tier 2)
4. If accepted: update `trusted_sources.yaml`, add to relevant standards' traceability tables, update the sources graph

## Assessment criteria

From [docs/sources.md](sources.md):

- Would a GDS service assessor accept this as evidence?
- Is it a primary source (not a blog about a primary source)?
- Is it recognised by the UK Gov digital community?
- Has it been stable for 3+ years?
