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

{% include citation.html lookup="Dynamic Resource Task Negotiation to Enable Product Agent Exploration in
    Multi-Agent Manufacturing Systems" style="rich" %}

{% include section.html %}

## All

{% include search-box.html %}

{% include search-info.html %}

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
    {% include citation.html lookup=c.id | default: c.title style="rich" %}
  {% endif %}
{% endfor %}

{% endfor %}


