# Force-Directed Source Graph Template

A reusable, self-contained D3.js force-directed graph for visualising relationships between sources and the things they inform (standards, requirements, policies, etc.).

**[Live example →](https://bv90dsit.github.io/Engineering_standards/sources-graph/)**

## Quick start

1. Copy `force-graph.html` into your project
2. Open it in a browser — it works immediately with placeholder data
3. Edit the `SOURCES` array with your own data
4. Deploy anywhere (GitHub Pages, static hosting, or embed in an existing site)

## Configuration

All customisation is in the clearly marked `CONFIGURATION` section at the top of the file.

### Source groups

Define your tiers/layers — each gets a colour in the legend:

```js
const SOURCE_GROUPS = [
  { key: "tier1", label: "Authoritative", colour: "#1d70b8" },
  { key: "tier2", label: "Established",   colour: "#f47738" },
];
```

### Sources and linkages

Each source has an ID, display label, group, optional URL, and the items it connects to:

```js
const SOURCES = [
  {
    id: "my-source",
    label: "Source Name",        // use \n for line breaks
    group: "tier1",              // must match a SOURCE_GROUPS key
    url: "https://example.com",  // opened on double-click
    items: ["ITEM-001", "ITEM-002"]
  },
];
```

### Item categories (optional)

By default, filtering uses the ID prefix (e.g. `SEC-001` → category `SEC`). Override with:

```js
const ITEM_CATEGORIES = {
  "ITEM-001": "CustomCategory",
};
```

### Item navigation (optional)

Set `ITEM_BASE_URL` to make items clickable:

```js
const ITEM_BASE_URL = "/standards/"; // links to /standards/item-001/
```

### Layout tuning

```js
const CONFIG = {
  width: 900,
  height: 700,
  linkDistance: 60,       // space between connected nodes
  linkStrength: 0.8,     // how strongly links pull nodes together
  chargeStrength: -120,  // repulsion between nodes (more negative = more spread)
  collisionPadding: 15,  // minimum gap between nodes
};
```

## Features

- Drag nodes to rearrange
- Filter by category (auto-generated from item IDs)
- Click items to navigate (if `ITEM_BASE_URL` is set)
- Double-click sources to open their URL
- Keyboard accessible (tab + enter)
- Responsive (SVG scales to container width)
- No build step — single HTML file, D3 loaded from CDN

## Embedding in Jekyll / GitHub Pages

Rename to `index.md` (or `graph.md`) and add frontmatter:

```markdown
---
layout: default
title: My Graph
permalink: /graph/
---

<!-- paste the <style>, HTML, and <script> blocks here -->
```

## Dependencies

- [D3.js v7](https://d3js.org/) (loaded from CDN, no install needed)

## Licence

MIT — same as the parent repository.
