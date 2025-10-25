---
title: Research
nav:
  order: 1
  tooltip: Published works
---

# {% include icon.html icon="fa-solid fa-microscope" %}Research



{% include section.html %}

## Highlighted

{% include citation.html lookup="doi:10.1016/j.conengprac.2019.03.009" style="rich" %}

{% include citation.html lookup="doi:10.1109/lra.2019.2921947" style="rich" %}

{% include section.html %}

## All

{% include search-box.html %}
{% include search-info.html %}

{%- assign uniq = "" -%}
{%- assign uniques = "" | split: "" -%}
{%- for c in site.data.citations -%}
  {%- assign authors_arr = c.authors -%}
  {%- if authors_arr == nil -%}{%- assign authors_arr = c.author -%}{%- endif -%}
  {%- if authors_arr == nil -%}{%- assign authors_arr = "" | split: "" -%}{%- endif -%}
  {%- assign names = "" -%}
  {%- for a in authors_arr -%}
    {%- assign nm = "" -%}
    {%- if a.name -%}{%- assign nm = a.name -%}
    {%- elsif a.literal -%}{%- assign nm = a.literal -%}
    {%- elsif a.family or a.given -%}{%- assign nm = a.given | default: "" | append: " " | append: a.family | strip -%}
    {%- else -%}{%- assign nm = a -%}{%- endif -%}
    {%- assign names = names | append: " " | append: nm -%}
  {%- endfor -%}
  {%- assign a = names | downcase | replace: '.', '' | replace: ',', ' ' | replace: ';', ' ' | strip | replace: '  ', ' ' | replace: '  ', ' ' -%}
  {%- if a contains 'ilya' and a contains 'kovalenko' -%}
    {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
    {%- assign key = doi -%}
    {%- if key == "" -%}{%- assign key = c.id | default: c.title | downcase -%}{%- endif -%}
    {%- assign pad = '|' | append: key | append: '|' -%}
    {%- unless uniq contains pad -%}
      {%- assign uniques = uniques | push: c -%}
      {%- assign uniq = uniq | append: pad -%}
    {%- endunless -%}
  {%- endif -%}
{%- endfor -%}

{%- assign journals = "" | split: "" -%}
{%- assign conferences = "" | split: "" -%}
{%- for c in uniques -%}
  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}
  {%- assign is_journal = false -%}
  {%- assign is_conf = false -%}
  {%- if t contains 'journal' or t contains 'article' -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains 'journal' or venue contains 'letters' or venue contains 'transactions' or venue contains 'access' -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if t contains 'proceedings' or t contains 'conference' -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains 'conference' or venue contains 'proceedings' or venue contains 'case' or venue contains 'icra' or venue contains 'iros' or venue contains 'acc' or venue contains 'cdc' or venue contains 'msec' or venue contains 'ccta' or venue contains 'etfa' -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if is_journal -%}
    {%- assign journals = journals | push: c -%}
  {%- elsif is_conf -%}
    {%- assign conferences = conferences | push: c -%}
  {%- else -%}
    {%- assign journals = journals | push: c -%}
  {%- endif -%}
{%- endfor -%}

### Journal Articles
{% include list.html collection=journals component="citation" style="rich" %}

### Conference Papers
{% include list.html collection=conferences component="citation" style="rich" %}

