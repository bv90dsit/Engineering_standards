---
layout: default
title: Engineering Standards
---

<h1>UK Government Engineering Standards</h1>
<p>Machine-readable, context-aware engineering standards for UK Government digital services.</p>

<div class="filters">
  <button class="filter-btn" onclick="clearAllFilters()" aria-label="Clear all filters" style="margin-bottom:12px;">Clear all filters</button>

  <div class="filters__group">
    <span class="filters__label" id="conformance-label">Conformance</span>
    <div class="filters__buttons" role="group" aria-labelledby="conformance-label">
      <button class="filter-btn filter-btn--active" data-filter-group="conformance" data-filter-value="all" aria-pressed="true" onclick="filterByConformance('all')">All</button>
      <button class="filter-btn" data-filter-group="conformance" data-filter-value="MUST" aria-pressed="false" onclick="filterByConformance('MUST')">MUST</button>
      <button class="filter-btn" data-filter-group="conformance" data-filter-value="SHOULD" aria-pressed="false" onclick="filterByConformance('SHOULD')">SHOULD</button>
      <button class="filter-btn" data-filter-group="conformance" data-filter-value="COULD" aria-pressed="false" onclick="filterByConformance('COULD')">COULD</button>
    </div>
  </div>

  <div class="filters__group">
    <span class="filters__label" id="category-label">Category</span>
    <div class="filters__buttons" role="group" aria-labelledby="category-label">
      <button class="filter-btn filter-btn--active" data-filter-group="category" data-filter-value="all" aria-pressed="true" onclick="filterByCategory('all')">All</button>
      {% assign categories = site.standards | map: "category" | compact | uniq | sort %}
      {% for cat in categories %}
      <button class="filter-btn" data-filter-group="category" data-filter-value="{{ cat }}" aria-pressed="false" onclick="filterByCategory('{{ cat }}')">{{ cat }}</button>
      {% endfor %}
    </div>
  </div>

  <div class="filters__group">
    <span class="filters__label" id="enforcement-label">Enforcement</span>
    <div class="filters__buttons" role="group" aria-labelledby="enforcement-label">
      <button class="filter-btn filter-btn--active" data-filter-group="enforcement" data-filter-value="all" aria-pressed="true" onclick="filterByEnforcement('all')">All</button>
      {% assign enforcements = site.standards | map: "enforcement" | compact | uniq | sort %}
      {% for enf in enforcements %}
      <button class="filter-btn" data-filter-group="enforcement" data-filter-value="{{ enf }}" aria-pressed="false" onclick="filterByEnforcement('{{ enf }}')">{{ enf }}</button>
      {% endfor %}
    </div>
  </div>
</div>

<div class="category-key">
  <h3>Core</h3>
  <div class="category-key__items">
    <span><strong>ENG</strong> Engineering practice</span>
    <span><strong>SEC</strong> Security</span>
    <span><strong>ARC</strong> Architecture</span>
    <span><strong>OPS</strong> Operations</span>
    <span><strong>DAT</strong> Data</span>
    <span><strong>ACC</strong> Accessibility</span>
    <span><strong>EMG</strong> Emerging tech (AI)</span>
  </div>
  <h3 style="margin-top: 12px;">Extensions</h3>
  <div class="category-key__items">
    <span><strong>PY</strong> Python / Django / Flask</span>
    <span><strong>JV</strong> Java / Spring Boot</span>
    <span><strong>TS</strong> TypeScript / React / Node</span>
    <span><strong>ORG</strong> Org-specific</span>
  </div>
</div>

{% assign grouped = site.standards | group_by: "category" %}
{% for group in grouped %}
<div class="category-section" data-category="{{ group.name }}">
  <h2>{{ group.name }}</h2>
  <ul class="standards-list">
    {% assign sorted_items = group.items | sort: "standard_id" %}
    {% for standard in sorted_items %}
    <li class="standards-list__item" data-conformance="{{ standard.conformance }}" data-category="{{ standard.category }}" data-enforcement="{{ standard.enforcement }}">
      <a href="{{ standard.url | relative_url }}" class="standards-list__link">
        {{ standard.standard_id }}: {{ standard.title }}
      </a>
      <div class="standards-list__meta">
        {% if standard.conformance == "MUST" %}
          <span class="badge badge--must">MUST</span>
        {% elsif standard.conformance == "SHOULD" %}
          <span class="badge badge--should">SHOULD</span>
        {% else %}
          <span class="badge badge--could">COULD</span>
        {% endif %}
        <span>Category: {{ standard.category }}</span>
        {% if standard.enforcement %}<span>Enforcement: {{ standard.enforcement }}</span>{% endif %}
        {% if standard.module %}<span>Module: {{ standard.module }}</span>{% endif %}
      </div>
    </li>
    {% endfor %}
  </ul>
</div>
{% endfor %}

<div id="filter-status" role="status" aria-live="polite" aria-atomic="true" style="font-size:14px; color:#3d4648; margin:12px 0;"></div>

<script>
var activeConformance = 'all';
var activeCategory = 'all';
var activeEnforcement = 'all';

function applyFilters() {
  var count = 0;
  document.querySelectorAll('.standards-list__item').forEach(function(item) {
    var conf = item.dataset.conformance || '';
    var cat = item.dataset.category || '';
    var enf = item.dataset.enforcement || '';
    var show = (activeConformance === 'all' || conf === activeConformance) &&
               (activeCategory === 'all' || cat === activeCategory) &&
               (activeEnforcement === 'all' || enf.indexOf(activeEnforcement) !== -1);
    item.style.display = show ? '' : 'none';
    if (show) count++;
  });
  document.querySelectorAll('.category-section').forEach(function(section) {
    var items = section.querySelectorAll('.standards-list__item');
    var visible = Array.from(items).some(function(i) { return i.style.display !== 'none'; });
    section.style.display = visible ? '' : 'none';
  });
  document.getElementById('filter-status').textContent = count + ' standard' + (count !== 1 ? 's' : '') + ' shown';
  updateButtons();
}

function filterByConformance(val) { activeConformance = val; applyFilters(); }
function filterByCategory(val) { activeCategory = val; applyFilters(); }
function filterByEnforcement(val) { activeEnforcement = val; applyFilters(); }
function clearAllFilters() { activeConformance = 'all'; activeCategory = 'all'; activeEnforcement = 'all'; applyFilters(); }

function updateButtons() {
  document.querySelectorAll('[data-filter-group]').forEach(function(btn) {
    var group = btn.dataset.filterGroup;
    var val = btn.dataset.filterValue;
    var active = (group === 'conformance' && val === activeConformance) ||
                 (group === 'category' && val === activeCategory) ||
                 (group === 'enforcement' && val === activeEnforcement);
    btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    btn.classList.toggle('filter-btn--active', active);
  });
}
</script>
