---
layout: default
title: Source Graph
permalink: /sources-graph/
---

# Source Frameworks — Graph View

Visual map of which source frameworks inform which standards, coloured by tier.

<style>
.graph-container {
  width: 100%;
  height: 700px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 20px 0;
}
.legend {
  display: flex;
  gap: 20px;
  margin: 16px 0;
  flex-wrap: wrap;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}
.legend-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}
.tier1 { background: #1d70b8; }
.tier2 { background: #f47738; }
.standard-node { background: #505a5f; }
</style>

<div class="legend">
  <div class="legend-item"><div class="legend-dot tier1"></div> Tier 1 — Authoritative (government, legislation, standards bodies)</div>
  <div class="legend-item"><div class="legend-dot tier2"></div> Tier 2 — Established (industry research, official framework docs)</div>
  <div class="legend-item"><div class="legend-dot standard-node"></div> Standard</div>
</div>

<div class="graph-container" id="graph"></div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const sources = {
  tier1: [
    { id: "tcop", label: "Technology Code of Practice", standards: ["ENG-001","ENG-002","ARC-001","DAT-004","ENG-005","EMG-001"] },
    { id: "gds", label: "GDS Service Standard", standards: ["ENG-003","OPS-001","OPS-002","ACC-002","ARC-004","ARC-005","ENG-004","ENG-006","OPS-003","OPS-006","OPS-007"] },
    { id: "ncsc", label: "NCSC Secure by Design", standards: ["SEC-001","SEC-003","SEC-005","SEC-006","SEC-007","SEC-008","DAT-003","OPS-004"] },
    { id: "owasp", label: "OWASP Top 10 / ASVS", standards: ["SEC-001","SEC-002","SEC-004","SEC-009","PY-003","PY-005","JV-003"] },
    { id: "wcag", label: "WCAG 2.2", standards: ["ACC-001"] },
    { id: "iso27001", label: "ISO 27001", standards: ["DAT-003"] },
    { id: "iso22301", label: "ISO 22301", standards: ["OPS-004"] },
    { id: "nist", label: "NIST SP 800-53/63", standards: ["SEC-002","SEC-005"] },
    { id: "ukgdpr", label: "UK GDPR", standards: ["DAT-002","DAT-005"] },
    { id: "accessibility", label: "Accessibility Regulations 2018", standards: ["ACC-001"] },
    { id: "gsc", label: "Government Security Classifications", standards: ["DAT-001"] },
    { id: "cddo-ai", label: "CDDO AI Framework", standards: ["EMG-002","EMG-003","EMG-004"] },
    { id: "cis", label: "CIS Benchmarks", standards: ["SEC-006"] },
    { id: "ietf", label: "IETF RFCs", standards: ["SEC-008"] },
  ],
  tier2: [
    { id: "dora", label: "DORA Metrics", standards: ["OPS-002","OPS-005","ENG-007"] },
    { id: "12factor", label: "12-Factor App", standards: ["ARC-002","TS-006","OPS-006"] },
    { id: "sre", label: "Google SRE Book", standards: ["OPS-001","OPS-003"] },
    { id: "aws-wa", label: "AWS Well-Architected", standards: ["ARC-005","ARC-006"] },
    { id: "accelerate", label: "Accelerate", standards: ["OPS-002","OPS-005","ENG-007"] },
    { id: "openapi", label: "OpenAPI Specification", standards: ["ARC-003"] },
    { id: "spring", label: "Spring Framework", standards: ["JV-001","JV-005"] },
    { id: "python-docs", label: "Python/PEP", standards: ["PY-002","PY-004","PY-010"] },
    { id: "django", label: "Django Docs", standards: ["PY-005","PY-007","PY-008"] },
    { id: "typescript", label: "TypeScript Handbook", standards: ["TS-001","TS-002","TS-003"] },
    { id: "slf4j", label: "SLF4J", standards: ["JV-006"] },
    { id: "react", label: "React Docs", standards: ["TS-005"] },
    { id: "mdn", label: "MDN Web Docs", standards: ["SEC-009"] },
  ]
};

// Build nodes and links
const nodes = [];
const links = [];
const standardSet = new Set();

sources.tier1.forEach(s => {
  nodes.push({ id: s.id, label: s.label, group: "tier1" });
  s.standards.forEach(std => {
    standardSet.add(std);
    links.push({ source: s.id, target: std });
  });
});

sources.tier2.forEach(s => {
  nodes.push({ id: s.id, label: s.label, group: "tier2" });
  s.standards.forEach(std => {
    standardSet.add(std);
    links.push({ source: s.id, target: std });
  });
});

standardSet.forEach(std => {
  nodes.push({ id: std, label: std, group: "standard" });
});

// D3 force layout
const container = document.getElementById("graph");
const width = container.clientWidth;
const height = container.clientHeight;

const svg = d3.select("#graph").append("svg")
  .attr("width", width)
  .attr("height", height);

const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(80))
  .force("charge", d3.forceManyBody().strength(-200))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collision", d3.forceCollide().radius(30));

const link = svg.append("g")
  .selectAll("line")
  .data(links)
  .join("line")
  .attr("stroke", "#ccc")
  .attr("stroke-width", 1);

const node = svg.append("g")
  .selectAll("g")
  .data(nodes)
  .join("g")
  .call(d3.drag()
    .on("start", (event, d) => { if (!event.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag", (event, d) => { d.fx = event.x; d.fy = event.y; })
    .on("end", (event, d) => { if (!event.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; })
  );

node.append("circle")
  .attr("r", d => d.group === "standard" ? 6 : 12)
  .attr("fill", d => d.group === "tier1" ? "#1d70b8" : d.group === "tier2" ? "#f47738" : "#505a5f");

node.append("text")
  .text(d => d.label)
  .attr("x", d => d.group === "standard" ? 10 : 16)
  .attr("y", 4)
  .attr("font-size", d => d.group === "standard" ? "10px" : "12px")
  .attr("font-weight", d => d.group === "standard" ? "normal" : "bold")
  .attr("fill", "#333");

simulation.on("tick", () => {
  link
    .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("transform", d => `translate(${d.x},${d.y})`);
});
</script>

<p style="color:#666; font-size:12px; margin-top:16px;">
  Drag nodes to rearrange. Blue = Tier 1 (authoritative), Orange = Tier 2 (established), Grey = standard.
  Edges show which sources inform which standards.
</p>
