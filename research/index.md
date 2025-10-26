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

{% assign sorted = site.data.citations | sort: "date" | reverse %}
{% assign sep = "|" %}
{% assign uniq_all = "" %}
{% assign ilya = "ilya" %}
{% assign kov = "kovalenko" %}

## Journal Articles

{% assign uniq_j = "" %}
{% for c in sorted %}
  {% assign authors_arr = c.authors | default: c.author | default: "" | split: "" %}
  {% assign names = "" %}
  {% for a in authors_arr %}
    {% assign nm = "" %}
    {% if a.name %}{% assign nm = a.name %}
    {% elsif a.literal %}{% assign nm = a.literal %}
    {% elsif a.family or a.given %}{% assign nm = a.given | default: "" | append: " " | append: a.family | strip %}
    {% else %}{% assign nm = a %}{% endif %}
    {% assign names = names | append: " " | append: nm %}
  {% endfor %}
  {% assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " %}
  {% assign doi = c.DOI | default: c.doi | default: "" | downcase %}
  {% assign key = doi %}
  {% if key == "" %}{% assign key = c.id | default: c.title | downcase %}{% endif %}
  {% assign pad = sep | append: key | append: sep %}
  {% assign t = c.type | default: c.genre | default: "" | downcase %}
  {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
  {% assign url_all = c.link | default: "" | downcase %}
  {% assign is_arxiv = false %}
  {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
  {% if doi contains "10.48550/arxiv" or url_all contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
  {% assign is_book = false %}
  {% if t contains "book" or t contains "chapter" %}{% assign is_book = true %}{% endif %}
  {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "springer" or venue contains "wiley" %}{% assign is_book = true %}{% endif %}
  {% assign is_conf = false %}
  {% if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" %}{% assign is_conf = true %}{% endif %}
  {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "manufacturing equipment and automation" or venue contains "manufacturing systems" or venue contains "mechatronics" %}{% assign is_conf = true %}{% endif %}
  {% assign is_journal = false %}
  {% if t contains "journal" or t contains "article" %}{% assign is_journal = true %}{% endif %}
  {% if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "international journal" or venue contains "battery energy" or venue contains "control engineering practice" or venue contains "smart and sustainable manufacturing systems" or venue contains "robotics and computer-integrated manufacturing" %}{% assign is_journal = true %}{% endif %}
  {% if venue contains "ifac-papersonline" or venue contains "procedia " %}{% assign is_journal = false %}{% endif %}
  {% if (an contains ilya and an contains kov) or (an contains " kovalenko i ") %}
    {% if is_arxiv or is_book or is_conf %}{% assign is_journal = false %}{% endif %}
    {% if is_journal and uniq_all contains pad %}{% assign is_journal = false %}{% endif %}
    {% if is_journal %}
      {% assign lookup_key = c.id | default: c.title %}
      {% include citation.html lookup=lookup_key style="rich" %}
      {% assign uniq_all = uniq_all | append: pad %}
      {% assign uniq_j = uniq_j | append: pad %}
    {% endif %}
  {% endif %}
{% endfor %}

{% include section.html %}

## Conference Papers

{% assign uniq_c = "" %}
{% for c in sorted %}
  {% assign authors_arr = c.authors | default: c.author | default: "" | split: "" %}
  {% assign names = "" %}
  {% for a in authors_arr %}
    {% assign nm = "" %}
    {% if a.name %}{% assign nm = a.name %}
    {% elsif a.literal %}{% assign nm = a.literal %}
    {% elsif a.family or a.given %}{% assign nm = a.given | default: "" | append: " " | append: a.family | strip %}
    {% else %}{% assign nm = a %}{% endif %}
    {% assign names = names | append: " " | append: nm %}
  {% endfor %}
  {% assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " %}
  {% assign doi = c.DOI | default: c.doi | default: "" | downcase %}
  {% assign key = doi %}
  {% if key == "" %}{% assign key = c.id | default: c.title | downcase %}{% endif %}
  {% assign pad = sep | append: key | append: sep %}
  {% assign t = c.type | default: c.genre | default: "" | downcase %}
  {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
  {% assign url_all = c.link | default: "" | downcase %}
  {% assign is_arxiv = false %}
  {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
  {% if doi contains "10.48550/arxiv" or url_all contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
  {% assign is_book = false %}
  {% if t contains "book" or t contains "chapter" %}{% assign is_book = true %}{% endif %}
  {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "springer" or venue contains "wiley" %}{% assign is_book = true %}{% endif %}
  {% assign is_conf = false %}
  {% if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" %}{% assign is_conf = true %}{% endif %}
  {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "manufacturing equipment and automation" or venue contains "manufacturing systems" or venue contains "mechatronics" %}{% assign is_conf = true %}{% endif %}
  {% if (an contains ilya and an contains kov) or (an contains " kovalenko i ") %}
    {% if is_arxiv or is_book %}{% assign is_conf = false %}{% endif %}
    {% if is_conf and uniq_all contains pad %}{% assign is_conf = false %}{% endif %}
    {% if is_conf %}
      {% assign lookup_key = c.id | default: c.title %}
      {% include citation.html lookup=lookup_key style="rich" %}
      {% assign uniq_all = uniq_all | append: pad %}
      {% assign uniq_c = uniq_c | append: pad %}
    {% endif %}
  {% endif %}
{% endfor %}

{% include section.html %}

## Books / Chapters

{% assign uniq_b = "" %}
{% for c in sorted %}
  {% assign authors_arr = c.authors | default: c.author | default: "" | split: "" %}
  {% assign names = "" %}
  {% for a in authors_arr %}
    {% assign nm = "" %}
    {% if a.name %}{% assign nm = a.name %}
    {% elsif a.literal %}{% assign nm = a.literal %}
    {% elsif a.family or a.given %}{% assign nm = a.given | default: "" | append: " " | append: a.family | strip %}
    {% else %}{% assign nm = a %}{% endif %}
    {% assign names = names | append: " " | append: nm %}
  {% endfor %}
  {% assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " %}
  {% assign doi = c.DOI | default: c.doi | default: "" | downcase %}
  {% assign key = doi %}
  {% if key == "" %}{% assign key = c.id | default: c.title | downcase %}{% endif %}
  {% assign pad = sep | append: key | append: sep %}
  {% assign t = c.type | default: c.genre | default: "" | downcase %}
  {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
  {% assign is_book = false %}
  {% if t contains "book" or t contains "chapter" %}{% assign is_book = true %}{% endif %}
  {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "springer" or venue contains "wiley" %}{% assign is_book = true %}{% endif %}
  {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "ccta" or venue contains "msec" or venue contains "etfa" or venue contains "ifac" %}{% assign is_book = false %}{% endif %}
  {% if (an contains ilya and an contains kov) or (an contains " kovalenko i ") %}
    {% if is_book and uniq_all contains pad %}{% assign is_book = false %}{% endif %}
    {% if is_book %}
      {% assign lookup_key = c.id | default: c.title %}
      {% include citation.html lookup=lookup_key style="rich" %}
      {% assign uniq_all = uniq_all | append: pad %}
      {% assign uniq_b = uniq_b | append: pad %}
    {% endif %}
  {% endif %}
{% endfor %}

{% include section.html %}

## Preprints (arXiv)

{% assign uniq_p = "" %}
{% for c in sorted %}
  {% assign authors_arr = c.authors | default: c.author | default: "" | split: "" %}
  {% assign names = "" %}
  {% for a in authors_arr %}
    {% assign nm = "" %}
    {% if a.name %}{% assign nm = a.name %}
    {% elsif a.literal %}{% assign nm = a.literal %}
    {% elsif a.family or a.given %}{% assign nm = a.given | default: "" | append: " " | append: a.family | strip %}
    {% else %}{% assign nm = a %}{% endif %}
    {% assign names = names | append: " " | append: nm %}
  {% endfor %}
  {% assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " %}
  {% assign doi = c.DOI | default: c.doi | default: "" | downcase %}
  {% assign key = doi %}
  {% if key == "" %}{% assign key = c.id | default: c.title | downcase %}{% endif %}
  {% assign pad = sep | append: key | append: sep %}
  {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
  {% assign url_all = c.link | default: "" | downcase %}
  {% assign is_arxiv = false %}
  {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
  {% if doi contains "10.48550/arxiv" or url_all contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
  {% if (an contains ilya and an contains kov) or (an contains " kovalenko i ") %}
    {% if is_arxiv and uniq_all contains pad %}{% assign is_arxiv = false %}{% endif %}
    {% if is_arxiv %}
      {% assign lookup_key = c.id | default: c.title %}
      {% include citation.html lookup=lookup_key style="rich" %}
      {% assign uniq_all = uniq_all | append: pad %}
      {% assign uniq_p = uniq_p | append: pad %}
    {% endif %}
  {% endif %}
{% endfor %}

{% include section.html %}

## Other Publications

{% assign uniq_o = "" %}
{% for c in sorted %}
  {% assign authors_arr = c.authors | default: c.author | default: "" | split: "" %}
  {% assign names = "" %}
  {% for a in authors_arr %}
    {% assign nm = "" %}
    {% if a.name %}{% assign nm = a.name %}
    {% elsif a.literal %}{% assign nm = a.literal %}
    {% elsif a.family or a.given %}{% assign nm = a.given | default: "" | append: " " | append: a.family | strip %}
    {% else %}{% assign nm = a %}{% endif %}
    {% assign names = names | append: " " | append: nm %}
  {% endfor %}
  {% assign an = names | downcase | replace: ".", "" | replace: ",", " " | replace: ";", " " | strip | replace: "  ", " " %}
  {% assign doi = c.DOI | default: c.doi | default: "" | downcase %}
  {% assign key = doi %}
  {% if key == "" %}{% assign key = c.id | default: c.title | downcase %}{% endif %}
  {% assign pad = sep | append: key | append: sep %}
  {% assign t = c.type | default: c.genre | default: "" | downcase %}
  {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
  {% assign url_all = c.link | default: "" | downcase %}
  {% assign is_arxiv = false %}
  {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
  {% if doi contains "10.48550/arxiv" or url_all contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
  {% assign is_book = false %}
  {% if t contains "book" or t contains "chapter" %}{% assign is_book = true %}{% endif %}
  {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "springer" or venue contains "wiley" %}{% assign is_book = true %}{% endif %}
  {% assign is_conf = false %}
  {% if t contains "proceedings" or t contains "conference" or t contains "workshop" or t contains "symposium" %}{% assign is_conf = true %}{% endif %}
  {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "manufacturing equipment and automation" or venue contains "manufacturing systems" or venue contains "mechatronics" %}{% assign is_conf = true %}{% endif %}
  {% assign is_journal = false %}
  {% if t contains "journal" or t contains "article" %}{% assign is_journal = true %}{% endif %}
  {% if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "international journal" or venue contains "battery energy" or venue contains "control engineering practice" or venue contains "smart and sustainable manufacturing systems" or venue contains "robotics and computer-integrated manufacturing" %}{% assign is_journal = true %}{% endif %}
  {% if venue contains "ifac-papersonline" or venue contains "procedia " %}{% assign is_journal = false %}{% endif %}
  {% assign classified = false %}
  {% if is_arxiv or is_book or is_conf or is_journal %}{% assign classified = true %}{% endif %}
  {% if (an contains ilya and an contains kov) or (an contains " kovalenko i ") %}
    {% unless classified or (uniq_all contains pad) %}
      {% assign lookup_key = c.id | default: c.title %}
      {% include citation.html lookup=lookup_key style="rich" %}
      {% assign uniq_all = uniq_all | append: pad %}
      {% assign uniq_o = uniq_o | append: pad %}
    {% endunless %}
  {% endif %}
{% endfor %}
