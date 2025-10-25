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

{%- assign ilya_citations = site.data.citations
  | where_exp: "c", "c.authors | join: ' ' | downcase | contains: 'ilya kovalenko'"
-%}
{% include list.html collection=ilya_citations component="citation" style="rich" %}



