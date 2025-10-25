---
title: Research
nav:
  order: 1
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-microscope" %}Research



{% include section.html %}

## Highlighted

{% include citation.html lookup="Open collaborative writing with Manubot" style="rich" %}

{% include section.html %}

## All

{% include search-box.html %}

{% include search-info.html %}

{%- assign ilya_citations = "" | split: "" -%}
{%- for c in site.data.citations -%}
  {%- assign authors_arr = c.authors | default: c.author | default: empty -%}
  {%- assign a = authors_arr | join: ' ' | downcase -%}
  {%- assign a = a
      | replace: '.', ''
      | replace: ',', ' '
      | replace: ';', ' '
      | strip
      | replace: '  ', ' '
      | replace: '  ', ' '
  -%}
  {%- if a contains 'ilya' and a contains 'kovalenko' -%}
    {%- assign ilya_citations = ilya_citations | push: c -%}
  {%- endif -%}
{%- endfor -%}

{% include list.html collection=ilya_citations component="citation" style="rich" %}
