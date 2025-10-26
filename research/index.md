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

{% assign items_all = site.data.citations | sort: "date" | reverse %}

{% assign SEP = "|" %}
{% assign seen = "" %}
{% assign dedup = "" %}

{% for c in items_all %}
  {% assign authors_str = c.authors | join: " " %}
  {% if authors_str contains "Kovalenko" %}
    {% assign key = c.DOI | default: c.doi | default: c.id | default: c.title | downcase %}
    {% assign pad = SEP | append: key | append: SEP %}
    {% unless seen contains pad %}
      {% assign dedup = dedup | push: c %}
      {% assign seen = seen | append: pad %}
    {% endunless %}
  {% endif %}
{% endfor %}

{% assign journal_keys = "journal,letters,transactions,magazine,frontiers,ieee access,robotics and automation letters,international journal,battery energy,control engineering practice,smart and sustainable manufacturing systems,robotics and computer-integrated manufacturing" | split: "," %}
{% assign conf_keys = "conference,proceedings,workshop,symposium,case,acc,cdc,msec,ccta,etfa,arso,aps/ursi,detc,dscc,ifac,ifac-papersonline,procedia manufacturing,procir,manufacturing equipment and systems,manufacturing equipment and automation,manufacturing systems,mechatronics" | split: "," %}
{% assign book_keys = "lecture notes,encyclopedia,handbook,springer,wiley,book,chapter" | split: "," %}

{% assign journals = "" | split: "|" %}
{% assign confs = "" | split: "|" %}
{% assign books = "" | split: "|" %}
{% assign preprints = "" | split: "|" %}
{% assign others = "" | split: "|" %}

{% for c in dedup %}
  {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
  {% assign link_lc = c.link | default: "" | downcase %}
  {% assign doi_lc = c.DOI | default: c.doi | default: "" | downcase %}

  {% assign is_arxiv = false %}
  {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
  {% if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}

  {% assign is_book = false %}
  {% for k in book_keys %}
    {% assign k2 = k | strip %}
    {% if venue contains k2 %}{% assign is_book = true %}{% endif %}
  {% endfor %}

  {% assign is_conf = false %}
  {% for k in conf_keys %}
    {% assign k2 = k | strip %}
    {% if venue contains k2 %}{% assign is_conf = true %}{% endif %}
  {% endfor %}

  {% assign is_journal = false %}
  {% for k in journal_keys %}
    {% assign k2 = k | strip %}
    {% if venue contains k2 %}{% assign is_journal = true %}{% endif %}
  {% endfor %}

  {% if venue contains "ifac-papersonline" or venue contains "procedia " %}
    {% assign is_journal = false %}
    {% assign is_conf = true %}
  {% endif %}

  {% if is_arxiv %}
    {% assign preprints = preprints | push: c %}
  {% elsif is_book %}
    {% assign books = books | push: c %}
  {% elsif is_conf %}
    {% assign confs = confs | push: c %}
  {% elsif is_journal %}
    {% assign journals = journals | push: c %}
  {% else %}
    {% assign others = others | push: c %}
  {% endif %}
{% endfor %}

## Journal Articles
{% for c in journals %}
  {% assign lookup_key = c.id | default: c.title %}
  {% include citation.html lookup=lookup_key style="rich" %}
{% endfor %}

{% include section.html %}

## Conference Papers
{% for c in confs %}
  {% assign lookup_key = c.id | default: c.title %}
  {% include citation.html lookup=lookup_key style="rich" %}
{% endfor %}

{% include section.html %}

## Books / Chapters
{% for c in books %}
  {% assign lookup_key = c.id | default: c.title %}
  {% include citation.html lookup=lookup_key style="rich" %}
{% endfor %}

{% include section.html %}

## Preprints (arXiv)
{% for c in preprints %}
  {% assign lookup_key = c.id | default: c.title %}
  {% include citation.html lookup=lookup_key style="rich" %}
{% endfor %}

{% include section.html %}

## Other Publications
{% for c in others %}
  {% assign lookup_key = c.id | default: c.title %}
  {% include citation.html lookup=lookup_key style="rich" %}
{% endfor %}

