---
title: Research
nav:
  order: 1
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-microscope" %}Research



{% include section.html %}

## Highlighted

{% include citation.html lookup="The model-based product agent: A control oriented architecture for intelligent products in multi-agent manufacturing systems" style="rich" %}

{% include citation.html lookup="doi:10.1109/lra.2019.2921947" style="rich" %}

{% include section.html %}

## All

{% include search-box.html %}

{% include search-info.html %}

{% for c in site.data.citations %}
  {% assign authors_arr = c.authors %}
  {% if authors_arr == nil %}{% assign authors_arr = c.author %}{% endif %}
  {% if authors_arr == nil %}{% assign authors_arr = '' | split: '' %}{% endif %}

  {% assign names = '' %}
  {% for a in authors_arr %}
    {% assign nm = '' %}
    {% if a.name %}
      {% assign nm = a.name %}
    {% elsif a.literal %}
      {% assign nm = a.literal %}
    {% elsif a.family or a.given %}
      {% assign nm = a.given | default: '' | append: ' ' | append: a.family | strip %}
    {% else %}
      {% assign nm = a %}
    {% endif %}
    {% assign names = names | append: ' ' | append: nm %}
  {% endfor %}

  {% assign a = names | downcase | replace: '.', '' | replace: ',', ' ' | replace: ';', ' ' | strip | replace: '  ', ' ' | replace: '  ', ' ' %}

  {% if a contains 'ilya' and a contains 'kovalenko' %}
    {% assign lookup_key = c.id %}
    {% if lookup_key == nil or lookup_key == '' %}
      {% assign lookup_key = c.title %}
    {% endif %}
    {% include citation.html lookup=lookup_key style="rich" %}
  {% endif %}
{% endfor %}



