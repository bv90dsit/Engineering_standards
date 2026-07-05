---
layout: default
title: About
permalink: /about/
---

<style>
.hero {
  background: linear-gradient(135deg, #1d70b8 0%, #003078 100%);
  color: white;
  padding: 48px 32px;
  border-radius: 8px;
  margin: -20px 0 32px;
}
.hero h1 { color: white; margin: 0 0 12px; font-size: 2rem; }
.hero p { font-size: 1.1rem; opacity: 0.9; margin: 0; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin: 32px 0;
}
.stat-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}
.stat-card__number {
  font-size: 2.2rem;
  font-weight: bold;
  color: #1d70b8;
  line-height: 1;
}
.stat-card__label {
  font-size: 0.85rem;
  color: #505a5f;
  margin-top: 6px;
}

.pill-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}
.pill {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}
.pill--must { background: #fce4e4; color: #d4351c; }
.pill--should { background: #fef3e5; color: #f47738; }
.pill--could { background: #e6f4ea; color: #00703c; }
.pill--automated { background: #e8f0fe; color: #1d70b8; }
.pill--peer { background: #f3e8ff; color: #6b21a8; }
.pill--audit { background: #fef3e5; color: #b45309; }
.pill--culture { background: #e6f4ea; color: #065f46; }

.bar-chart {
  margin: 24px 0;
}
.bar-chart__row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
.bar-chart__label {
  width: 80px;
  font-size: 13px;
  font-weight: 500;
  color: #505a5f;
}
.bar-chart__bar {
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding-left: 8px;
  font-size: 12px;
  color: white;
  font-weight: bold;
}

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin: 24px 0;
}
.role-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  border-left: 4px solid #1d70b8;
}
.role-card h4 { margin: 0 0 6px; font-size: 0.95rem; }
.role-card p { margin: 0; font-size: 0.85rem; color: #505a5f; }

.adopt-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin: 24px 0;
}
.adopt-step {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  position: relative;
  border-top: 3px solid #1d70b8;
}
.adopt-step__number {
  font-size: 2rem;
  font-weight: bold;
  color: #1d70b8;
  opacity: 0.3;
  position: absolute;
  top: 12px;
  right: 16px;
}
.adopt-step h4 { margin: 0 0 8px; }
.adopt-step p { margin: 0; font-size: 0.85rem; color: #505a5f; }
</style>

<div class="hero">
  <h1>UK Government Engineering Standards</h1>
  <p>A single, machine-readable set of engineering rules — enforceable by tooling, traceable to authority, and filterable by your team's context.</p>
  <p style="margin-top: 16px; padding: 10px 16px; background: rgba(255,255,255,0.15); border-radius: 4px; font-size: 0.9rem;">
    ⚠️ <strong>Early ideation</strong> — this is a concept under active development. Nothing here is finalised or officially adopted. Standards, tooling, and structure may change significantly based on feedback.
  </p>
</div>

<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-card__number">69</div>
    <div class="stat-card__label">Standards</div>
  </div>
  <div class="stat-card">
    <div class="stat-card__number">5</div>
    <div class="stat-card__label">Modules</div>
  </div>
  <div class="stat-card">
    <div class="stat-card__number">22</div>
    <div class="stat-card__label">IDE Rules</div>
  </div>
  <div class="stat-card">
    <div class="stat-card__number">49</div>
    <div class="stat-card__label">Tests</div>
  </div>
</div>

## Why these exist

Government digital services affect millions. These standards ensure services are **secure**, **accessible**, **reliable**, and **maintainable** — backed by published authoritative frameworks, not opinion.

## Conformance breakdown

<div class="bar-chart">
  <div class="bar-chart__row">
    <span class="bar-chart__label">MUST</span>
    <div class="bar-chart__bar" style="width: 50%; background: #d4351c;">35</div>
  </div>
  <div class="bar-chart__row">
    <span class="bar-chart__label">SHOULD</span>
    <div class="bar-chart__bar" style="width: 47%; background: #f47738;">33</div>
  </div>
  <div class="bar-chart__row">
    <span class="bar-chart__label">COULD</span>
    <div class="bar-chart__bar" style="width: 2%; min-width: 30px; background: #00703c;">1</div>
  </div>
</div>

## How they're enforced

<div class="pill-grid">
  <span class="pill pill--automated">Automated (IDE + CI)</span>
  <span class="pill pill--peer">Peer review</span>
  <span class="pill pill--audit">Service assessment</span>
  <span class="pill pill--culture">Team practice</span>
</div>

Standards checked **automatically** give you feedback as you type in VS Code and block non-compliant PRs in CI. Others are checked by reviewers, assessors, or documented in team charters.

## Who are these for?

<div class="roles-grid">
  <div class="role-card">
    <h4>Engineers</h4>
    <p>Follow standards; tooling catches issues before you push</p>
  </div>
  <div class="role-card">
    <h4>Tech Leads</h4>
    <p>Add CI check; choose modules for your stack</p>
  </div>
  <div class="role-card">
    <h4>Delivery Managers</h4>
    <p>MUST standards = assessment requirements; each has evidence criteria</p>
  </div>
  <div class="role-card">
    <h4>Security Leads</h4>
    <p>Filter by SEC category for the full security baseline</p>
  </div>
  <div class="role-card">
    <h4>Service Assessors</h4>
    <p>Standards trace back to GDS Service Standard and NCSC</p>
  </div>
  <div class="role-card">
    <h4>AI Agents</h4>
    <p>Query standards via MCP server; check code in real time</p>
  </div>
</div>

## How to adopt

<div class="adopt-steps">
  <div class="adopt-step">
    <span class="adopt-step__number">1</span>
    <h4>Scan your repo</h4>
    <p>Auto-detects your stack and recommends which standards apply</p>
  </div>
  <div class="adopt-step">
    <span class="adopt-step__number">2</span>
    <h4>Install the extension</h4>
    <p>VS Code gives you inline warnings as you type — instant feedback</p>
  </div>
  <div class="adopt-step">
    <span class="adopt-step__number">3</span>
    <h4>Add CI check</h4>
    <p>One YAML file — every PR checks compliance automatically</p>
  </div>
  <div class="adopt-step">
    <span class="adopt-step__number">4</span>
    <h4>Connect AI agents</h4>
    <p>MCP server lets coding agents query standards and check code in real time</p>
  </div>
</div>

## Source authority

Every standard traces back to at least one published framework:

<div class="pill-grid">
  <span class="pill pill--automated">GDS Service Standard</span>
  <span class="pill pill--automated">NCSC Secure by Design</span>
  <span class="pill pill--automated">OWASP Top 10</span>
  <span class="pill pill--automated">WCAG 2.2</span>
  <span class="pill pill--automated">DORA Metrics</span>
  <span class="pill pill--automated">UK GDPR</span>
  <span class="pill pill--peer">AWS Well-Architected</span>
  <span class="pill pill--peer">12-Factor App</span>
  <span class="pill pill--peer">Google SRE Book</span>
</div>

See the [Source Graph](/Engineering_standards/sources-graph/) for how they connect.
