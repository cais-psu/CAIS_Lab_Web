---
title: Research
nav:
  order: 1
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-microscope" %}Research

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

{% include section.html %}

## Highlighted

{% include citation.html lookup="Open collaborative writing with Manubot" style="rich" %}

{% include section.html %}

## All

{% include search-box.html %}

{% include search-info.html %}

{% assign all = site.data.citations %}
{% comment %} 下面的筛选条件可按你的数据字段微调 {% endcomment %}
{% assign journals = all | where: "type", "journal-article" %}
{% assign conferences = all | where_exp: "c", "c.type contains 'proceedings' or c.genre == 'conference-paper'" %}

### Journal Articles
{% include list.html collection=journals component="citation" %}

### Conference Papers
{% include list.html collection=conferences component="citation" %}

