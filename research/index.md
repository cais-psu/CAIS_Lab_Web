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

{%- assign needles = "ilya,kovalenko,ilya kovalenko,i kovalenko" | split: "," -%}
{%- assign ilya_citations = "" | split: "" -%}

{%- for c in site.data.citations -%}
  {%- assign authors_arr = c.authors | default: empty -%}
  {%- assign authors_str = authors_arr | join: ' ' | downcase -%}
  {%- assign authors_str = authors_str
      | replace: '.', ''
      | replace: ',', ' '
      | replace: ';', ' '
      | strip
      | replace: '  ', ' '
      | replace: '  ', ' '
  -%}
  {%- assign authors_pad = ' ' | append: authors_str | append: ' ' -%}

  {%- assign matched = false -%}
  {%- for n in needles -%}
    {%- assign needle = ' ' | append: n | strip | append: ' ' -%}
    {%- if authors_pad contains needle -%}
      {%- assign matched = true -%}{%- break -%}
    {%- endif -%}
  {%- endfor -%}

  {%- if matched -%}
    {%- assign ilya_citations = ilya_citations | push: c -%}
  {%- endif -%}
{%- endfor -%}

{% include list.html collection=ilya_citations component="citation" style="rich" %}


