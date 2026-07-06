---
layout: default
title: Methodology
permalink: /methodology/
---

<style>
.method-hero {
  background: linear-gradient(135deg, #1d70b8 0%, #003078 100%);
  color: white;
  padding: 48px 32px;
  border-radius: 8px;
  margin: -20px 0 40px;
}
.method-hero h1 { color: white; margin: 0 0 12px; font-size: 2rem; }
.method-hero p { font-size: 1.1rem; opacity: 0.9; margin: 0; }

/* Tier cards */
.method-tiers {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 24px 0 40px;
}
.method-tier {
  border-radius: 8px;
  padding: 24px;
  position: relative;
  border-left: 5px solid;
}
.method-tier--1 {
  border-left-color: var(--govuk-blue);
  background: #e8f0fe;
}
.method-tier--2 {
  border-left-color: var(--govuk-amber);
  background: #fef3e5;
}
.method-tier--rejected {
  border-left-color: var(--govuk-grey-2);
  background: var(--govuk-grey-3);
  border-left-style: dashed;
}
.method-tier__header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}
.method-tier__name {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
}
.method-tier__badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
}
.method-tier--1 .method-tier__badge { background: var(--govuk-blue); color: white; }
.method-tier--2 .method-tier__badge { background: var(--govuk-amber); color: white; }
.method-tier--rejected .method-tier__badge { background: var(--govuk-grey-2); color: white; }
.method-tier__desc {
  margin: 0 0 10px;
  font-size: 0.95rem;
  color: var(--govuk-grey-1);
}
.method-tier__meta {
  display: flex;
  gap: 24px;
  font-size: 0.85rem;
  color: var(--govuk-grey-1);
}
.method-tier__meta strong { color: var(--govuk-black); }

/* Trust criteria */
.method-criteria {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin: 24px 0 40px;
}
.method-criterion {
  background: var(--govuk-grey-3);
  border-radius: 8px;
  padding: 20px;
  border-top: 3px solid var(--govuk-blue);
  position: relative;
}
.method-criterion__number {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--govuk-blue);
  opacity: 0.3;
  position: absolute;
  top: 12px;
  right: 16px;
}
.method-criterion h4 { margin: 0 0 6px; font-size: 0.95rem; }
.method-criterion p { margin: 0; font-size: 0.85rem; color: var(--govuk-grey-1); }

/* Synthesis principles (timeline) */
.method-principles {
  position: relative;
  padding-left: 40px;
  margin: 24px 0 40px;
}
.method-principles::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--govuk-blue);
  border-radius: 2px;
}
.method-principle {
  position: relative;
  margin-bottom: 20px;
  padding: 4px 0;
}
.method-principle:last-child { margin-bottom: 0; }
.method-principle::before {
  content: attr(data-num);
  position: absolute;
  left: -40px;
  top: 2px;
  width: 28px;
  height: 28px;
  background: var(--govuk-blue);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
}
.method-principle__text {
  font-size: 0.95rem;
  line-height: 1.5;
}
.method-principle__text strong { color: var(--govuk-black); }

/* Worked example */
.method-example {
  margin: 24px 0 40px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}
.method-example__header {
  background: var(--govuk-dark-blue);
  color: white;
  padding: 16px 24px;
}
.method-example__header h3 { color: white; margin: 0; font-size: 1.1rem; }
.method-example__header p { margin: 4px 0 0; font-size: 0.85rem; opacity: 0.8; }

.method-sources {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  padding: 24px;
  background: #f8f9fa;
}
.method-source {
  background: white;
  border-radius: 6px;
  padding: 16px;
  border-top: 3px solid;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.method-source--ncsc { border-top-color: var(--govuk-blue); }
.method-source--owasp { border-top-color: var(--govuk-red); }
.method-source--gds { border-top-color: var(--govuk-green); }
.method-source__name {
  font-weight: 700;
  font-size: 0.85rem;
  margin: 0 0 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.method-source--ncsc .method-source__name { color: var(--govuk-blue); }
.method-source--owasp .method-source__name { color: var(--govuk-red); }
.method-source--gds .method-source__name { color: var(--govuk-green); }
.method-source__ref {
  font-size: 0.8rem;
  color: var(--govuk-grey-1);
  margin: 0 0 8px;
}
.method-source__quote {
  font-size: 0.85rem;
  line-height: 1.4;
  margin: 0;
  font-style: italic;
  color: var(--govuk-grey-1);
}

.method-flow-arrow {
  text-align: center;
  padding: 16px;
  background: #f8f9fa;
  font-size: 1.5rem;
  color: var(--govuk-blue);
  font-weight: 700;
  letter-spacing: 2px;
}
.method-flow-arrow span {
  display: inline-block;
  background: var(--govuk-blue);
  color: white;
  padding: 6px 20px;
  border-radius: 20px;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.method-result {
  padding: 24px;
}
.method-result__table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}
.method-result__table th,
.method-result__table td {
  padding: 10px 14px;
  border: 1px solid #e0e0e0;
  text-align: left;
}
.method-result__table th {
  background: var(--govuk-grey-3);
  font-weight: 700;
}
.method-result__tag {
  display: inline-block;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
}
.method-result__tag--ncsc { background: #e8f0fe; color: var(--govuk-blue); }
.method-result__tag--owasp { background: #fce4e4; color: var(--govuk-red); }
.method-result__tag--gds { background: #e6f4ea; color: var(--govuk-green); }
.method-result__tag--all { background: #f3e8ff; color: #6b21a8; }

.method-excluded {
  margin: 0;
  padding: 20px 24px;
  background: var(--govuk-grey-3);
  border-top: 1px solid #e0e0e0;
}
.method-excluded__title {
  font-weight: 700;
  font-size: 0.9rem;
  margin: 0 0 10px;
  color: var(--govuk-grey-1);
}
.method-excluded ul {
  margin: 0;
  padding-left: 18px;
  font-size: 0.85rem;
  color: var(--govuk-grey-1);
}
.method-excluded li { margin-bottom: 6px; }

/* CTA */
.method-cta {
  background: var(--govuk-grey-3);
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  margin: 40px 0 0;
}
.method-cta h3 { margin: 0 0 8px; }
.method-cta p { margin: 0 0 16px; font-size: 0.95rem; color: var(--govuk-grey-1); }
.method-cta__links {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}
.method-cta__link {
  display: inline-block;
  padding: 10px 24px;
  border-radius: 4px;
  font-weight: 700;
  font-size: 0.9rem;
  text-decoration: none;
}
.method-cta__link--primary {
  background: var(--govuk-blue);
  color: white;
}
.method-cta__link--primary:hover { background: var(--govuk-dark-blue); }
.method-cta__link--secondary {
  background: white;
  color: var(--govuk-blue);
  border: 2px solid var(--govuk-blue);
}
.method-cta__link--secondary:hover { background: #e8f0fe; }

/* Responsive */
@media (max-width: 640px) {
  .method-hero { padding: 32px 20px; }
  .method-hero h1 { font-size: 1.5rem; }
  .method-tier__meta { flex-direction: column; gap: 6px; }
  .method-sources { grid-template-columns: 1fr; }
  .method-criteria { grid-template-columns: 1fr; }
}
</style>

<div class="method-hero">
  <h1>How Standards Are Made</h1>
  <p>Every standard traces to published authority and is synthesised with rigour. No opinions, no invented requirements — just the tightest common ground from trusted frameworks, enforced by tooling.</p>
</div>

## Source Tiers

Only authoritative and established sources can back a standard. We reject library docs, blogs, and books as foundations — they belong in implementation guidance, not requirements.

<div class="method-tiers">
  <div class="method-tier method-tier--1">
    <div class="method-tier__header">
      <h3 class="method-tier__name">Tier 1 — Authoritative</h3>
      <span class="method-tier__badge">Can justify a MUST</span>
    </div>
    <p class="method-tier__desc">Government bodies, legislation, international standards organisations (OWASP, W3C, NIST, ISO)</p>
    <div class="method-tier__meta">
      <span><strong>Examples:</strong> NCSC Secure by Design, WCAG 2.2, UK GDPR</span>
      <span><strong>CI enforced:</strong> Yes — domain in trusted_sources.yaml</span>
    </div>
  </div>
  <div class="method-tier method-tier--2">
    <div class="method-tier__header">
      <h3 class="method-tier__name">Tier 2 — Established</h3>
      <span class="method-tier__badge">Supports a standard</span>
    </div>
    <p class="method-tier__desc">Recognised industry research (DORA, Google SRE), official language and framework documentation</p>
    <div class="method-tier__meta">
      <span><strong>Examples:</strong> DORA Metrics, 12-Factor App, PEP 484</span>
      <span><strong>CI enforced:</strong> Yes — pair with Tier 1 for MUST</span>
    </div>
  </div>
  <div class="method-tier method-tier--rejected">
    <div class="method-tier__header">
      <h3 class="method-tier__name">Not Accepted</h3>
      <span class="method-tier__badge">Implementation only</span>
    </div>
    <p class="method-tier__desc">Library documentation, practitioner blogs, book publishers — these go in "What good looks like" sections</p>
    <div class="method-tier__meta">
      <span><strong>Examples:</strong> getpino.io, martinfowler.com, pragprog.com</span>
      <span><strong>CI enforced:</strong> Rejected if used in source traceability</span>
    </div>
  </div>
</div>

## How We Decide What to Trust

Four questions determine whether a source qualifies:

<div class="method-criteria">
  <div class="method-criterion">
    <span class="method-criterion__number">1</span>
    <h4>Would a GDS assessor accept this as evidence?</h4>
    <p>If you'd be embarrassed citing it in a service assessment, it doesn't belong in source traceability.</p>
  </div>
  <div class="method-criterion">
    <span class="method-criterion__number">2</span>
    <h4>Is it a primary source?</h4>
    <p>Not a blog post about a primary source. We cite the standard itself, not someone's explanation of it.</p>
  </div>
  <div class="method-criterion">
    <span class="method-criterion__number">3</span>
    <h4>Is it recognised by the UK Gov digital community?</h4>
    <p>Referenced in GDS guidance, NCSC recommendations, or cross-government architecture decisions.</p>
  </div>
  <div class="method-criterion">
    <span class="method-criterion__number">4</span>
    <h4>Has it been stable for 3+ years?</h4>
    <p>A source that might disappear next year isn't a foundation for a standard.</p>
  </div>
</div>

## Synthesis Principles

When multiple frameworks cover the same concern, we combine their strengths following five rules:

<div class="method-principles">
  <div class="method-principle" data-num="1">
    <p class="method-principle__text"><strong>Tightest common ground</strong> — the standard statement captures only what all sources agree on</p>
  </div>
  <div class="method-principle" data-num="2">
    <p class="method-principle__text"><strong>Most detailed source wins for guidance</strong> — "What good looks like" pulls specifics from whichever source is most concrete</p>
  </div>
  <div class="method-principle" data-num="3">
    <p class="method-principle__text"><strong>Never contradict a source</strong> — if sources disagree on strictness, we take the stricter position</p>
  </div>
  <div class="method-principle" data-num="4">
    <p class="method-principle__text"><strong>Never invent beyond sources</strong> — enforcement and tooling are our value-add, not the requirement itself</p>
  </div>
  <div class="method-principle" data-num="5">
    <p class="method-principle__text"><strong>Cite the specific clause</strong> — the source traceability table references the exact section, not just the framework name</p>
  </div>
</div>

## Worked Example: SEC-001 (HTTPS Everywhere)

<div class="method-example">
  <div class="method-example__header">
    <h3>Three sources inform this standard</h3>
    <p>Each contributes something different — together they form a complete requirement</p>
  </div>

  <div class="method-sources">
    <div class="method-source method-source--ncsc">
      <p class="method-source__name">NCSC</p>
      <p class="method-source__ref">Secure by Design — Transport Layer Security</p>
      <p class="method-source__quote">"Use TLS 1.2 or above for all connections. Enable HSTS."</p>
    </div>
    <div class="method-source method-source--owasp">
      <p class="method-source__name">OWASP</p>
      <p class="method-source__ref">ASVS — V9.1.1</p>
      <p class="method-source__quote">"Verify that TLS is used for all client connectivity, not just limited to sensitive endpoints."</p>
    </div>
    <div class="method-source method-source--gds">
      <p class="method-source__name">GDS</p>
      <p class="method-source__ref">Service Standard — Point 9</p>
      <p class="method-source__quote">"Protect users' privacy… evaluate what data the service collects, stores and provides."</p>
    </div>
  </div>

  <div class="method-flow-arrow">
    <span>Synthesised into</span>
  </div>

  <div class="method-result">
    <table class="method-result__table">
      <thead>
        <tr>
          <th>Requirement</th>
          <th>Derived from</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>All services MUST use HTTPS for every connection, with no HTTP fallback</td>
          <td><span class="method-result__tag method-result__tag--all">All three</span></td>
        </tr>
        <tr>
          <td>TLS 1.2 is the minimum; TLS 1.3 SHOULD be preferred</td>
          <td><span class="method-result__tag method-result__tag--ncsc">NCSC</span></td>
        </tr>
        <tr>
          <td>HSTS headers with a minimum max-age of 1 year</td>
          <td><span class="method-result__tag method-result__tag--ncsc">NCSC</span></td>
        </tr>
        <tr>
          <td>No mixed content warnings</td>
          <td><span class="method-result__tag method-result__tag--owasp">OWASP</span></td>
        </tr>
        <tr>
          <td>Certificate renewal is automated</td>
          <td><span class="method-result__tag method-result__tag--gds">Operational guidance</span></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="method-excluded">
    <p class="method-excluded__title">What was deliberately left out</p>
    <ul>
      <li><strong>GDS Point 9 is broader than HTTPS</strong> — we didn't expand the standard to cover all of Point 9; each concern gets its own standard</li>
      <li><strong>OWASP cipher suite sub-requirements</strong> — kept SEC-001 focused on the core requirement; cipher suites would be a separate standard</li>
      <li><strong>No source specifies enforcement mechanism</strong> — that's our addition (automated grep + periodic audit), not theirs</li>
    </ul>
  </div>
</div>

<div class="method-cta">
  <h3>Explore the full source framework</h3>
  <p>See every source we reference, how standards connect to them, and how to propose new ones.</p>
  <div class="method-cta__links">
    <a href="{{ '/sources-graph' | relative_url }}" class="method-cta__link method-cta__link--primary">Source Graph</a>
    <a href="https://github.com/bv90dsit/Engineering_standards/blob/main/docs/sources.md" class="method-cta__link method-cta__link--secondary">Full Sources List</a>
  </div>
</div>
