---
layout: default
title: Source Graph
permalink: /sources-graph/
---

# Source Frameworks

How our standards trace back to authoritative sources.

<style>
.legend {
  display: flex;
  gap: 24px;
  margin: 16px 0 8px;
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
  display: inline-block;
}
.tier1 { background: #1d70b8; }
.tier2 { background: #f47738; }
.standard-node { background: #505a5f; }
svg { display: block; margin: 0 auto; }
.node-label { pointer-events: none; }
.link { stroke: #b1b4b6; stroke-width: 1px; }
.source-label { font-weight: bold; font-size: 11px; }
.std-label { font-size: 9px; fill: #505a5f; }
</style>

<div class="legend">
  <div class="legend-item"><div class="legend-dot tier1"></div> Tier 1 — Authoritative</div>
  <div class="legend-item"><div class="legend-dot tier2"></div> Tier 2 — Established</div>
  <div class="legend-item"><div class="legend-dot standard-node"></div> Standard</div>
</div>

<div class="category-key">
  <h3>Categories</h3>
  <div class="category-key__items">
    <span><strong>ENG</strong> Engineering practice</span>
    <span><strong>SEC</strong> Security</span>
    <span><strong>ARC</strong> Architecture</span>
    <span><strong>OPS</strong> Operations</span>
    <span><strong>DAT</strong> Data</span>
    <span><strong>ACC</strong> Accessibility</span>
    <span><strong>EMG</strong> Emerging tech (AI)</span>
    <span><strong>PY</strong> Python</span>
    <span><strong>JV</strong> Java</span>
    <span><strong>TS</strong> TypeScript</span>
    <span><strong>ORG</strong> Org-specific</span>
  </div>
</div>

<svg id="graph" width="900" height="900"></svg>

<p style="color:#666; font-size:12px; margin-top:8px;">
  Click any grey standard node to view it. Drag nodes to rearrange. Blue = government/legislation/standards bodies. Orange = industry research/framework docs.
</p>

## Source → Standards reference

| Source | Tier | Standards it informs |
|--------|:----:|---------------------|
| Technology Code of Practice | 1 | [ENG-001](/Engineering_standards/standards/ENG-001/), [ENG-002](/Engineering_standards/standards/ENG-002/), [ARC-001](/Engineering_standards/standards/ARC-001/), [DAT-004](/Engineering_standards/standards/DAT-004/), [ENG-005](/Engineering_standards/standards/ENG-005/), [EMG-001](/Engineering_standards/standards/EMG-001/) |
| GDS Service Standard | 1 | [ENG-003](/Engineering_standards/standards/ENG-003/), [OPS-001](/Engineering_standards/standards/OPS-001/), [OPS-002](/Engineering_standards/standards/OPS-002/), [ARC-004](/Engineering_standards/standards/ARC-004/), [ARC-005](/Engineering_standards/standards/ARC-005/), [OPS-003](/Engineering_standards/standards/OPS-003/), [OPS-006](/Engineering_standards/standards/OPS-006/), [OPS-007](/Engineering_standards/standards/OPS-007/) |
| NCSC Secure by Design | 1 | [SEC-001](/Engineering_standards/standards/SEC-001/), [SEC-003](/Engineering_standards/standards/SEC-003/), [SEC-005](/Engineering_standards/standards/SEC-005/), [SEC-006](/Engineering_standards/standards/SEC-006/), [SEC-007](/Engineering_standards/standards/SEC-007/), [SEC-008](/Engineering_standards/standards/SEC-008/) |
| OWASP Top 10 / ASVS | 1 | [SEC-001](/Engineering_standards/standards/SEC-001/), [SEC-002](/Engineering_standards/standards/SEC-002/), [SEC-004](/Engineering_standards/standards/SEC-004/), [SEC-009](/Engineering_standards/standards/SEC-009/), [PY-003](/Engineering_standards/standards/PY-003/), [JV-003](/Engineering_standards/standards/JV-003/) |
| WCAG 2.2 | 1 | [ACC-001](/Engineering_standards/standards/ACC-001/) |
| UK GDPR | 1 | [DAT-002](/Engineering_standards/standards/DAT-002/), [DAT-005](/Engineering_standards/standards/DAT-005/) |
| CDDO AI Framework | 1 | [EMG-002](/Engineering_standards/standards/EMG-002/), [EMG-003](/Engineering_standards/standards/EMG-003/), [EMG-004](/Engineering_standards/standards/EMG-004/) |
| DORA Metrics | 2 | [OPS-002](/Engineering_standards/standards/OPS-002/), [OPS-005](/Engineering_standards/standards/OPS-005/), [ENG-007](/Engineering_standards/standards/ENG-007/) |
| 12-Factor App | 2 | [ARC-002](/Engineering_standards/standards/ARC-002/), [TS-006](/Engineering_standards/standards/TS-006/), [OPS-006](/Engineering_standards/standards/OPS-006/) |
| AWS Well-Architected | 2 | [ARC-005](/Engineering_standards/standards/ARC-005/), [ARC-006](/Engineering_standards/standards/ARC-006/) |
| Google SRE Book | 2 | [OPS-001](/Engineering_standards/standards/OPS-001/), [OPS-003](/Engineering_standards/standards/OPS-003/) |

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const data = {
  tier1: [
    { id: "tcop", label: "Technology\nCode of Practice", standards: ["ENG-001","ENG-002","ARC-001","DAT-004","ENG-005","EMG-001"] },
    { id: "gds", label: "GDS Service\nStandard", standards: ["ENG-003","OPS-001","OPS-002","ACC-002","ARC-004","ARC-005","ENG-004","ENG-006","OPS-003","OPS-006","OPS-007"] },
    { id: "ncsc", label: "NCSC Secure\nby Design", standards: ["SEC-001","SEC-003","SEC-005","SEC-006","SEC-007","SEC-008","DAT-003","OPS-004"] },
    { id: "owasp", label: "OWASP", standards: ["SEC-001","SEC-002","SEC-004","SEC-009","PY-003","PY-005","JV-003"] },
    { id: "wcag", label: "WCAG 2.2", standards: ["ACC-001"] },
    { id: "nist", label: "NIST", standards: ["SEC-002","SEC-005"] },
    { id: "ukgdpr", label: "UK GDPR", standards: ["DAT-002","DAT-005"] },
    { id: "accessibility", label: "Accessibility\nRegs 2018", standards: ["ACC-001"] },
    { id: "cddo-ai", label: "CDDO AI\nFramework", standards: ["EMG-002","EMG-003","EMG-004"] },
    { id: "gsc", label: "Security\nClassifications", standards: ["DAT-001"] },
    { id: "ietf", label: "IETF RFCs", standards: ["SEC-008"] },
  ],
  tier2: [
    { id: "dora", label: "DORA", standards: ["OPS-002","OPS-005","ENG-007"] },
    { id: "12factor", label: "12-Factor", standards: ["ARC-002","TS-006","OPS-006"] },
    { id: "sre", label: "Google SRE", standards: ["OPS-001","OPS-003"] },
    { id: "aws-wa", label: "AWS Well-\nArchitected", standards: ["ARC-005","ARC-006"] },
    { id: "accelerate", label: "Accelerate", standards: ["OPS-002","OPS-005","ENG-007"] },
    { id: "openapi", label: "OpenAPI", standards: ["ARC-003"] },
    { id: "spring", label: "Spring", standards: ["JV-001","JV-005"] },
    { id: "python-docs", label: "Python/PEP", standards: ["PY-002","PY-004","PY-010"] },
    { id: "django", label: "Django", standards: ["PY-005","PY-007","PY-008"] },
    { id: "typescript", label: "TypeScript", standards: ["TS-001","TS-002","TS-003"] },
    { id: "react", label: "React", standards: ["TS-005"] },
    { id: "mdn", label: "MDN", standards: ["SEC-009"] },
  ]
};

const nodes = [];
const links = [];
const stdSet = new Set();

data.tier1.forEach(s => {
  nodes.push({ id: s.id, label: s.label, group: "tier1", radius: 18 });
  s.standards.forEach(std => { stdSet.add(std); links.push({ source: s.id, target: std }); });
});
data.tier2.forEach(s => {
  nodes.push({ id: s.id, label: s.label, group: "tier2", radius: 14 });
  s.standards.forEach(std => { stdSet.add(std); links.push({ source: s.id, target: std }); });
});
const baseUrl = "/Engineering_standards/standards/";
stdSet.forEach(std => {
  nodes.push({ id: std, label: std, group: "standard", radius: 5, url: baseUrl + std + "/" });
});

const width = 900, height = 900;
const svg = d3.select("#graph");

const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(60).strength(0.8))
  .force("charge", d3.forceManyBody().strength(-120))
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("collision", d3.forceCollide().radius(d => d.radius + 15))
  .force("x", d3.forceX(width / 2).strength(0.05))
  .force("y", d3.forceY(height / 2).strength(0.05));

const link = svg.append("g")
  .selectAll("line")
  .data(links)
  .join("line")
  .attr("class", "link");

const node = svg.append("g")
  .selectAll("g")
  .data(nodes)
  .join("g")
  .call(d3.drag()
    .on("start", (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on("end", (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; })
  );

// Make standard nodes clickable
node.filter(d => d.group === "standard")
  .style("cursor", "pointer")
  .on("click", (e, d) => { if (d.url) window.location.href = d.url; });

node.append("circle")
  .attr("r", d => d.radius)
  .attr("fill", d => d.group === "tier1" ? "#1d70b8" : d.group === "tier2" ? "#f47738" : "#505a5f")
  .attr("stroke", d => d.group === "standard" ? "none" : "#fff")
  .attr("stroke-width", d => d.group === "standard" ? 0 : 2);

node.append("title").text(d => d.group === "standard" ? d.label + " (click to view)" : d.label.replace(/\n/g, " "));

// Labels for sources only (standards are too small)
node.filter(d => d.group !== "standard")
  .each(function(d) {
    const lines = d.label.split("\n");
    const text = d3.select(this).append("text")
      .attr("class", "source-label node-label")
      .attr("text-anchor", "middle");
    lines.forEach((line, i) => {
      text.append("tspan")
        .attr("x", 0)
        .attr("dy", i === 0 ? d.radius + 12 : 12)
        .text(line);
    });
  });

// Tiny labels for standards on hover proximity
node.filter(d => d.group === "standard")
  .append("text")
  .attr("class", "std-label node-label")
  .attr("x", 8)
  .attr("y", 3)
  .text(d => d.label);

simulation.on("tick", () => {
  link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("transform", d => `translate(${d.x},${d.y})`);
});
</script>
