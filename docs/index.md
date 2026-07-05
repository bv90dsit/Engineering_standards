---
layout: default
title: Engineering Standards
---

<h1>UK Government Engineering Standards</h1>
<p>Machine-readable, context-aware engineering standards for UK Government digital services.</p>

<div class="filters">
  <div class="filters__group">
    <span class="filters__label">Conformance</span>
    <div class="filters__buttons">
      <a href="{{ '/' | relative_url }}" class="filter-btn filter-btn--active">All</a>
      <a href="#must" class="filter-btn" onclick="filterByConformance('MUST')">MUST</a>
      <a href="#should" class="filter-btn" onclick="filterByConformance('SHOULD')">SHOULD</a>
      <a href="#could" class="filter-btn" onclick="filterByConformance('COULD')">COULD</a>
    </div>
  </div>

  <div class="filters__group">
    <span class="filters__label">Category</span>
    <div class="filters__buttons">
      <a href="#" class="filter-btn filter-btn--active" onclick="filterByCategory('all')">All</a>
      {% assign categories = site.standards | map: "category" | compact | uniq | sort %}
      {% for cat in categories %}
      <a href="#{{ cat | downcase }}" class="filter-btn" onclick="filterByCategory('{{ cat }}')">{{ cat }}</a>
      {% endfor %}
    </div>
  </div>

  <div class="filters__group">
    <span class="filters__label">Enforcement</span>
    <div class="filters__buttons">
      <a href="#" class="filter-btn filter-btn--active" onclick="filterByEnforcement('all')">All</a>
      {% assign enforcements = site.standards | map: "enforcement" | compact | uniq | sort %}
      {% for enf in enforcements %}
      <a href="#{{ enf | slugify }}" class="filter-btn" onclick="filterByEnforcement('{{ enf }}')">{{ enf }}</a>
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

<script>
function filterByConformance(value) {
  var items = document.querySelectorAll('.standards-list__item');
  items.forEach(function(item) {
    if (value === 'all' || item.getAttribute('data-conformance') === value) {
      item.style.display = '';
    } else {
      item.style.display = 'none';
    }
  });
}

function filterByCategory(value) {
  var sections = document.querySelectorAll('.category-section');
  sections.forEach(function(section) {
    if (value === 'all' || section.getAttribute('data-category') === value) {
      section.style.display = '';
    } else {
      section.style.display = 'none';
    }
  });
}

function filterByEnforcement(value) {
  var items = document.querySelectorAll('.standards-list__item');
  items.forEach(function(item) {
    if (value === 'all' || item.getAttribute('data-enforcement') === value) {
      item.style.display = '';
    } else {
      item.style.display = 'none';
    }
  });
}
</script>
