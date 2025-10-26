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

{%- assign sorted = site.data.citations | sort: "date" | reverse -%}

{%- assign uniq_j = "" -%}
### Journal Articles
{%- for c in sorted -%}
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
  {%- assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " | replace: "  ", " " -%}

  {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign key = doi -%}
  {%- if key == "" -%}{%- assign key = c.id | default: c.title | downcase -%}{%- endif -%}
  {%- assign pad = "|" | append: key | append: "|" -%}

  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}

  {%- assign is_journal = false -%}
  {%- if t contains "journal" or t contains "article" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "nature" or venue contains "ieee access" or venue contains "robotics and automation letters" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "ifac-papersonline" -%}{%- assign is_journal = false -%}{%- endif -%}

  {%- if (an contains "ilya" and an contains "kovalenko") or (an contains " kovalenko i ") -%}
    {%- if is_journal and uniq_j contains pad -%}{%- assign is_journal = false -%}{%- endif -%}
    {%- if is_journal -%}
      {%- assign lookup_key = c.id -%}
      {%- if lookup_key == nil or lookup_key == "" -%}{%- assign lookup_key = c.title -%}{%- endif -%}
      {% include citation.html lookup=lookup_key style="rich" %}
      {%- assign uniq_j = uniq_j | append: pad -%}
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}

{%- assign uniq_c = "" -%}
### Conference Papers
{%- for c in sorted -%}
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
  {%- assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " | replace: "  ", " " -%}

  {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign key = doi -%}
  {%- if key == "" -%}{%- assign key = c.id | default: c.title | downcase -%}{%- endif -%}
  {%- assign pad = "|" | append: key | append: "|" -%}

  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}

  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "icra" or venue contains "iros" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" -%}{%- assign is_conf = true -%}{%- endif -%}

  {%- if (an contains "ilya" and an contains "kovalenko") or (an contains " kovalenko i ") -%}
    {%- if is_conf and uniq_c contains pad -%}{%- assign is_conf = false -%}{%- endif -%}
    {%- if is_conf -%}
      {%- assign lookup_key = c.id -%}
      {%- if lookup_key == nil or lookup_key == "" -%}{%- assign lookup_key = c.title -%}{%- endif -%}
      {% include citation.html lookup=lookup_key style="rich" %}
      {%- assign uniq_c = uniq_c | append: pad -%}
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}

{%- assign uniq_o = "" -%}
### Other Publications
{%- for c in sorted -%}
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
  {%- assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " | replace: "  ", " " -%}

  {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign key = doi -%}
  {%- if key == "" -%}{%- assign key = c.id | default: c.title | downcase -%}{%- endif -%}
  {%- assign pad = "|" | append: key | append: "|" -%}

  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}

  {%- assign is_journal = false -%}
  {%- if t contains "journal" or t contains "article" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "nature" or venue contains "ieee access" or venue contains "robotics and automation letters" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "ifac-papersonline" -%}{%- assign is_journal = false -%}{%- endif -%}

  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "icra" or venue contains "iros" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" -%}{%- assign is_conf = true -%}{%- endif -%}

  {%- if (an contains "ilya" and an contains "kovalenko") or (an contains " kovalenko i ") -%}
    {%- unless is_journal or is_conf or (uniq_o contains pad) -%}
      {%- assign lookup_key = c.id -%}
      {%- if lookup_key == nil or lookup_key == "" -%}{%- assign lookup_key = c.title -%}{%- endif -%}
      {% include citation.html lookup=lookup_key style="rich" %}
      {%- assign uniq_o = uniq_o | append: pad -%}
    {%- endunless -%}
  {%- endif -%}
{%- endfor -%}
