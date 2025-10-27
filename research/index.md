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
{%- assign seen_all = "" -%}
{%- assign bar = "|" -%}

### Journal Articles
{%- for c in sorted -%}
  {%- assign authors_arr = c.authors -%}{%- if authors_arr == nil -%}{%- assign authors_arr = c.author -%}{%- endif -%}{%- if authors_arr == nil -%}{%- assign authors_arr = "" | split: "" -%}{%- endif -%}
  {%- assign names = "" -%}{%- for a in authors_arr -%}{%- assign nm = "" -%}{%- if a.name -%}{%- assign nm = a.name -%}{%- elsif a.literal -%}{%- assign nm = a.literal -%}{%- elsif a.family or a.given -%}{%- assign nm = a.given | default: "" | append: " " | append: a.family | strip -%}{%- else -%}{%- assign nm = a -%}{%- endif -%}{%- assign names = names | append: " " | append: nm -%}{%- endfor -%}
  {%- assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " | replace: "  ", " " -%}
  {%- assign doi_raw = c.DOI | default: c.doi | default: c.id | default: "" | downcase -%}
  {%- assign doi_norm = doi_raw | replace: "https://doi.org/", "" | replace: "http://doi.org/", "" | replace: "doi.org/", "" | replace: "doi:", "" | strip -%}
  {%- if doi_norm contains ".v" -%}{%- assign parts = doi_norm | split: ".v" -%}{%- assign doi_base = parts[0] -%}{%- else -%}{%- assign doi_base = doi_norm -%}{%- endif -%}
  {%- assign key = doi_base -%}{%- if key == "" -%}{%- assign key = c.title | default: c.id | downcase -%}{%- endif -%}
  {%- assign pad = bar | append: key | append: bar -%}
  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}
  {%- assign link_lc = c.link | default: "" | downcase -%}
  {%- assign doi_lc = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign is_arxiv = false -%}{%- if c.id and c.id contains "arxiv:" -%}{%- assign is_arxiv = true -%}{%- endif -%}{%- if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" -%}{%- assign is_arxiv = true -%}{%- endif -%}
  {%- assign is_book = false -%}{%- if t contains "chapter" or t contains "book" -%}{%- assign is_book = true -%}{%- endif -%}{%- if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" -%}{%- assign is_book = true -%}{%- endif -%}
  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "volume " -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if doi_lc contains "/msec" or doi_lc contains "/dscc" or doi_lc contains "/detc" or doi_lc contains "/case" or doi_lc contains "/ccta" or doi_lc contains "/acc" or doi_lc contains "/cdc" or doi_lc contains "/etfa" or doi_lc contains "/arso" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- assign is_journal = false -%}
  {%- if t contains "journal" or t contains "article" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "nature" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "international journal" or venue contains "battery energy" or venue contains "control engineering practice" or venue contains "smart and sustainable manufacturing systems" or venue contains "robotics and computer-integrated manufacturing" or venue contains "journal of medical devices" or venue contains "procedia manufacturing" or venue contains "procedia cirp" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "ifac-papersonline" -%}{%- assign is_journal = false -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "ieee access" or venue contains "procedia manufacturing" or venue contains "procedia cirp" -%}{%- assign is_conf = false -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if an contains "ilya" and an contains "kovalenko" or an contains " kovalenko i " -%}
    {%- unless is_arxiv or is_book or is_conf -%}
      {%- unless seen_all contains pad -%}
        {%- assign lookup_key = c.id | default: c.title -%}
        {% include citation.html lookup=lookup_key style="rich" %}
        {%- assign seen_all = seen_all | append: pad -%}
      {%- endunless -%}
    {%- endunless -%}
  {%- endif -%}
{%- endfor -%}

### Conference Papers
{%- for c in sorted -%}
  {%- assign authors_arr = c.authors -%}{%- if authors_arr == nil -%}{%- assign authors_arr = c.author -%}{%- endif -%}{%- if authors_arr == nil -%}{%- assign authors_arr = "" | split: "" -%}{%- endif -%}
  {%- assign names = "" -%}{%- for a in authors_arr -%}{%- assign nm = "" -%}{%- if a.name -%}{%- assign nm = a.name -%}{%- elsif a.literal -%}{%- assign nm = a.literal -%}{%- elsif a.family or a.given -%}{%- assign nm = a.given | default: "" | append: " " | append: a.family | strip -%}{%- else -%}{%- assign nm = a -%}{%- endif -%}{%- assign names = names | append: " " | append: nm -%}{%- endfor -%}
  {%- assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " | replace: "  ", " " -%}
  {%- assign doi_raw = c.DOI | default: c.doi | default: c.id | default: "" | downcase -%}
  {%- assign doi_norm = doi_raw | replace: "https://doi.org/", "" | replace: "http://doi.org/", "" | replace: "doi.org/", "" | replace: "doi:", "" | strip -%}
  {%- if doi_norm contains ".v" -%}{%- assign parts = doi_norm | split: ".v" -%}{%- assign doi_base = parts[0] -%}{%- else -%}{%- assign doi_base = doi_norm -%}{%- endif -%}
  {%- assign key = doi_base -%}{%- if key == "" -%}{%- assign key = c.title | default: c.id | downcase -%}{%- endif -%}
  {%- assign pad = bar | append: key | append: bar -%}
  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}
  {%- assign link_lc = c.link | default: "" | downcase -%}
  {%- assign doi_lc = c.DOI | default: c.doi | default: "" | downcase -%}
  {%- assign is_arxiv = false -%}{%- if c.id and c.id contains "arxiv:" -%}{%- assign is_arxiv = true -%}{%- endif -%}{%- if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" -%}{%- assign is_arxiv = true -%}{%- endif -%}
  {%- assign is_book = false -%}{%- if t contains "chapter" or t contains "book" -%}{%- assign is_book = true -%}{%- endif -%}{%- if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" -%}{%- assign is_book = true -%}{%- endif -%}
  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "volume " -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if doi_lc contains "/msec" or doi_lc contains "/dscc" or doi_lc contains "/detc" or doi_lc contains "/case" or doi_lc contains "/ccta" or doi_lc contains "/acc" or doi_lc contains "/cdc" or doi_lc contains "/etfa" or doi_lc contains "/arso" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "ieee access" or venue contains "procedia manufacturing" or venue contains "procedia cirp" -%}{%- assign is_conf = false -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if an contains "ilya" and an contains "kovalenko" or an contains " kovalenko i " -%}
    {%- if is_conf -%}
      {%- unless is_arxiv or is_book -%}
        {%- unless seen_all contains pad -%}
          {%- assign lookup_key = c.id | default: c.title -%}
          {% include citation.html lookup=lookup_key style="rich" %}
          {%- assign seen_all = seen_all | append: pad -%}
        {%- endunless -%}
      {%- endunless -%}
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}

### Other Publications
{%- for c in sorted -%}
  {%- assign authors_arr = c.authors -%}{%- if authors_arr == nil -%}{%- assign authors_arr = c.author -%}{%- endif -%}{%- if authors_arr == nil -%}{%- assign authors_arr = "" | split: "" -%}{%- endif -%}
  {%- assign names = "" -%}{%- for a in authors_arr -%}{%- assign nm = "" -%}{%- if a.name -%}{%- assign nm = a.name -%}{%- elsif a.literal -%}{%- assign nm = a.literal -%}{%- elsif a.family or a.given -%}{%- assign nm = a.given | default: "" | append: " " | append: a.family | strip -%}{%- else -%}{%- assign nm = a -%}{%- endif -%}{%- assign names = names | append: " " | append: nm -%}{%- endfor -%}
  {%- assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " | replace: "  ", " " -%}
  {%- assign doi_raw = c.DOI | default: c.doi | default: c.id | default: "" | downcase -%}
  {%- assign doi_norm = doi_raw | replace: "https://doi.org/", "" | replace: "http://doi.org/", "" | replace: "doi.org/", "" | replace: "doi:", "" | strip -%}
  {%- if doi_norm contains ".v" -%}{%- assign parts = doi_norm | split: ".v" -%}{%- assign doi_base = parts[0] -%}{%- else -%}{%- assign doi_base = doi_norm -%}{%- endif -%}
  {%- assign key = doi_base -%}{%- if key == "" -%}{%- assign key = c.title | default: c.id | downcase -%}{%- endif -%}
  {%- assign pad = bar | append: key | append: bar -%}
  {%- assign t = c.type | default: c.genre | default: "" | downcase -%}
  {%- assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase -%}
  {%- assign link_lc = c.link | default: "" | downcase -%}
  {%- assign doi_lc = c.DOI | default: c.doi | default: "" | downcase -%}

  {%- assign is_arxiv = false -%}{%- if c.id and c.id contains "arxiv:" -%}{%- assign is_arxiv = true -%}{%- endif -%}{%- if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" -%}{%- assign is_arxiv = true -%}{%- endif -%}
  {%- assign is_book = false -%}{%- if t contains "chapter" or t contains "book" -%}{%- assign is_book = true -%}{%- endif -%}{%- if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" -%}{%- assign is_book = true -%}{%- endif -%}
  {%- assign is_conf = false -%}
  {%- if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "volume " -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if doi_lc contains "/msec" or doi_lc contains "/dscc" or doi_lc contains "/detc" or doi_lc contains "/case" or doi_lc contains "/ccta" or doi_lc contains "/acc" or doi_lc contains "/cdc" or doi_lc contains "/etfa" or doi_lc contains "/arso" -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- assign is_journal = false -%}
  {%- if t contains "journal" or t contains "article" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "nature" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "international journal" or venue contains "battery energy" or venue contains "control engineering practice" or venue contains "smart and sustainable manufacturing systems" or venue contains "robotics and computer-integrated manufacturing" or venue contains "journal of medical devices" or venue contains "procedia manufacturing" or venue contains "procedia cirp" -%}{%- assign is_journal = true -%}{%- endif -%}
  {%- if venue contains "ifac-papersonline" -%}{%- assign is_journal = false -%}{%- assign is_conf = true -%}{%- endif -%}
  {%- if venue contains "ieee access" or venue contains "procedia manufacturing" or venue contains "procedia cirp" -%}{%- assign is_conf = false -%}{%- assign is_journal = true -%}{%- endif -%}

  {%- if an contains "ilya" and an contains "kovalenko" or an contains " kovalenko i " -%}
    {%- if is_journal == false and is_conf == false -%}
      {%- unless seen_all contains pad -%}
        {%- assign lookup_key = c.id | default: c.title -%}
        {% include citation.html lookup=lookup_key style="rich" %}
        {%- assign seen_all = seen_all | append: pad -%}
      {%- endunless -%}
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}