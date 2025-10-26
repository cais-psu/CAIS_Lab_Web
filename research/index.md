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

### Journal Articles
{%- assign uniq_j = "" -%}
{%- for c in sorted -%}
  {%- assign authors_arr = c.authors | default: c.author | default: "" | split: "" -%}
  {%- assign names = "" -%}
  {%- for a in authors_arr -%}
    {%- assign nm = a.name | default: a.literal | default: a.given | append: " " | append: a.family | default: a | strip -%}
    {%- assign names = names | append: " " | append: nm -%}
  {%- endfor -%}
  {%- assign an = names | downcase -%}

  {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign key = doi | default: c.id | default: c.title | downcase -%}
  {%- assign pad = "|" | append: key | append: "|" -%}

  {%- assign t = c.type | default: c.genre | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}

  {%- assign is_journal = false -%}
  {%- if t contains "journal" or t contains "article" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "nature" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "battery energy" or venue contains "wiley" or venue contains "institute of electrical and electronics engineers" or venue contains "smart and sustainable manufacturing systems" or venue contains "control engineering practice" or venue contains "procedia cirp" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "ifac-papersonline" -%}{%- assign is_journal = false -%}{%- endif -%}

  {%- if (an contains "ilya" and an contains "kovalenko") -%}
    {%- if is_journal and uniq_j contains pad == false -%}
      {% include citation.html lookup=c.id style="rich" %}
      {%- assign uniq_j = uniq_j | append: pad -%}
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}

### Conference Papers
{%- assign uniq_c = "" -%}
{%- for c in sorted -%}
  {%- assign authors_arr = c.authors | default: c.author | default: "" | split: "" -%}
  {%- assign names = "" -%}
  {%- for a in authors_arr -%}
    {%- assign nm = a.name | default: a.literal | default: a.given | append: " " | append: a.family | default: a | strip -%}
    {%- assign names = names | append: " " | append: nm -%}
  {%- endfor -%}
  {%- assign an = names | downcase -%}

  {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign key = doi | default: c.id | default: c.title | downcase -%}
  {%- assign pad = "|" | append: key | append: "|" -%}

  {%- assign t = c.type | default: c.genre | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}

  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "icra" or venue contains "iros" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "dynamics and control" -%}{%- assign is_conf = true -%}{%- endif -%}

  {%- if (an contains "ilya" and an contains "kovalenko") -%}
    {%- if is_conf and uniq_c contains pad == false -%}
      {% include citation.html lookup=c.id style="rich" %}
      {%- assign uniq_c = uniq_c | append: pad -%}
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}

### Books
{%- assign uniq_o = "" -%}
{%- for c in sorted -%}
  {%- assign authors_arr = c.authors | default: c.author | default: "" | split: "" -%}
  {%- assign names = "" -%}
  {%- for a in authors_arr -%}
    {%- assign nm = a.name | default: a.literal | default: a.given | append: " " | append: a.family | default: a | strip -%}
    {%- assign names = names | append: " " | append: nm -%}
  {%- endfor -%}
  {%- assign an = names | downcase -%}

  {%- assign doi = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign key = doi | default: c.id | default: c.title | downcase -%}
  {%- assign pad = "|" | append: key | append: "|" -%}

  {%- assign t = c.type | default: c.genre | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}

  {%- assign is_journal = false -%}
  {%- if t contains "journal" or t contains "article" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "nature" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "battery energy" or venue contains "wiley" or venue contains "institute of electrical and electronics engineers" or venue contains "smart and sustainable manufacturing systems" or venue contains "control engineering practice" or venue contains "procedia cirp" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "ifac-papersonline" -%}{%- assign is_journal = false -%}{%- endif -%}

  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "icra" or venue contains "iros" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "dynamics and control" -%}{%- assign is_conf = true -%}{%- endif -%}

  {%- if (an contains "ilya" and an contains "kovalenko") and uniq_o contains pad == false and (not is_journal) and (not is_conf) -%}
    {% include citation.html lookup=c.id style="rich" %}
    {%- assign uniq_o = uniq_o | append: pad -%}
  {%- endif -%}
{%- endfor -%}
