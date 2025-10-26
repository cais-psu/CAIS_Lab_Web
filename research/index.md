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

{% assign items = site.data.citations | sort: "date" | reverse %}

{% assign sep = "|" %}
{% assign seen = "" %}

{% assign has_any = false %}

## Journal Articles
{% assign printed_any = false %}
{% for c in items %}
  {% assign authors_str = c.authors | join: " " %}
  {% if authors_str contains "Kovalenko" %}
    {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
    {% assign link_lc = c.link | default: "" | downcase %}
    {% assign doi_lc = c.DOI | default: c.doi | default: "" | downcase %}
    {% assign is_arxiv = false %}
    {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
    {% if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
    {% assign is_book = false %}
    {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" %}{% assign is_book = true %}{% endif %}
    {% assign is_conf = false %}
    {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "manufacturing equipment and automation" or venue contains "manufacturing systems" or venue contains "mechatronics" or venue contains "volume " %}{% assign is_conf = true %}{% endif %}
    {% assign is_journal = false %}
    {% if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "international journal" or venue contains "battery energy" or venue contains "control engineering practice" or venue contains "smart and sustainable manufacturing systems" or venue contains "robotics and computer-integrated manufacturing" or venue contains "journal of medical devices" %}{% assign is_journal = true %}{% endif %}
    {% if venue contains "ifac-papersonline" or venue contains "procedia " %}{% assign is_journal = false %}{% assign is_conf = true %}{% endif %}
    {% unless is_arxiv or is_book or is_conf %}
      {% if is_journal %}
        {% assign key = c.DOI | default: c.doi | default: c.id | default: c.title | downcase %}
        {% assign pad = sep | append: key | append: sep %}
        {% unless seen contains pad %}
          {% assign seen = seen | append: pad %}
          {% assign lookup_key = c.id | default: c.title %}
          {% include citation.html lookup=lookup_key style="rich" %}
          {% assign printed_any = true %}
          {% assign has_any = true %}
        {% endunless %}
      {% endif %}
    {% endunless %}
  {% endif %}
{% endfor %}
{% unless printed_any %}{% endunless %}

{% include section.html %}

## Conference Papers
{% assign printed_any = false %}
{% for c in items %}
  {% assign authors_str = c.authors | join: " " %}
  {% if authors_str contains "Kovalenko" %}
    {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
    {% assign link_lc = c.link | default: "" | downcase %}
    {% assign doi_lc = c.DOI | default: c.doi | default: "" | downcase %}
    {% assign is_arxiv = false %}
    {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
    {% if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
    {% assign is_book = false %}
    {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" %}{% assign is_book = true %}{% endif %}
    {% assign is_conf = false %}
    {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "manufacturing equipment and automation" or venue contains "manufacturing systems" or venue contains "mechatronics" or venue contains "volume " %}{% assign is_conf = true %}{% endif %}
    {% unless is_arxiv or is_book %}
      {% if is_conf %}
        {% assign key = c.DOI | default: c.doi | default: c.id | default: c.title | downcase %}
        {% assign pad = sep | append: key | append: sep %}
        {% unless seen contains pad %}
          {% assign seen = seen | append: pad %}
          {% assign lookup_key = c.id | default: c.title %}
          {% include citation.html lookup=lookup_key style="rich" %}
          {% assign printed_any = true %}
          {% assign has_any = true %}
        {% endunless %}
      {% endif %}
    {% endunless %}
  {% endif %}
{% endfor %}
{% unless printed_any %}{% endunless %}

{% include section.html %}

## Books / Chapters
{% assign printed_any = false %}
{% for c in items %}
  {% assign authors_str = c.authors | join: " " %}
  {% if authors_str contains "Kovalenko" %}
    {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
    {% assign link_lc = c.link | default: "" | downcase %}
    {% assign doi_lc = c.DOI | default: c.doi | default: "" | downcase %}
    {% assign is_book = false %}
    {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" %}{% assign is_book = true %}{% endif %}
    {% if is_book %}
      {% assign key = c.DOI | default: c.doi | default: c.id | default: c.title | downcase %}
      {% assign pad = sep | append: key | append: sep %}
      {% unless seen contains pad %}
        {% assign seen = seen | append: pad %}
        {% assign lookup_key = c.id | default: c.title %}
        {% include citation.html lookup=lookup_key style="rich" %}
        {% assign printed_any = true %}
        {% assign has_any = true %}
      {% endunless %}
    {% endif %}
  {% endif %}
{% endfor %}
{% unless printed_any %}{% endunless %}

{% include section.html %}

## Preprints (arXiv)
{% assign printed_any = false %}
{% for c in items %}
  {% assign authors_str = c.authors | join: " " %}
  {% if authors_str contains "Kovalenko" %}
    {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
    {% assign link_lc = c.link | default: "" | downcase %}
    {% assign doi_lc = c.DOI | default: c.doi | default: "" | downcase %}
    {% assign is_arxiv = false %}
    {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
    {% if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
    {% if is_arxiv %}
      {% assign key = c.DOI | default: c.doi | default: c.id | default: c.title | downcase %}
      {% assign pad = sep | append: key | append: sep %}
      {% unless seen contains pad %}
        {% assign seen = seen | append: pad %}
        {% assign lookup_key = c.id | default: c.title %}
        {% include citation.html lookup=lookup_key style="rich" %}
        {% assign printed_any = true %}
        {% assign has_any = true %}
      {% endunless %}
    {% endif %}
  {% endif %}
{% endfor %}
{% unless printed_any %}{% endunless %}

{% include section.html %}

## Other Publications
{% assign printed_any = false %}
{% for c in items %}
  {% assign authors_str = c.authors | join: " " %}
  {% if authors_str contains "Kovalenko" %}
    {% assign venue = c["container-title"] | default: c.venue | default: c.publisher | default: "" | downcase %}
    {% assign link_lc = c.link | default: "" | downcase %}
    {% assign doi_lc = c.DOI | default: c.doi | default: "" | downcase %}
    {% assign is_arxiv = false %}
    {% if c.id and c.id contains "arxiv:" %}{% assign is_arxiv = true %}{% endif %}
    {% if doi_lc contains "10.48550/arxiv" or link_lc contains "arxiv.org" or venue contains "arxiv" %}{% assign is_arxiv = true %}{% endif %}
    {% assign is_book = false %}
    {% if venue contains "lecture notes" or venue contains "encyclopedia" or venue contains "handbook" or venue contains "wiley" or venue contains "springer" or venue contains "book" or venue contains "chapter" %}{% assign is_book = true %}{% endif %}
    {% assign is_conf = false %}
    {% if venue contains "conference" or venue contains "proceedings" or venue contains "workshop" or venue contains "symposium" or venue contains "case" or venue contains "acc" or venue contains "cdc" or venue contains "msec" or venue contains "ccta" or venue contains "etfa" or venue contains "arso" or venue contains "aps/ursi" or venue contains "detc" or venue contains "dscc" or venue contains "ifac" or venue contains "ifac-papersonline" or venue contains "procedia manufacturing" or venue contains "procir" or venue contains "manufacturing equipment and systems" or venue contains "manufacturing equipment and automation" or venue contains "manufacturing systems" or venue contains "mechatronics" or venue contains "volume " %}{% assign is_conf = true %}{% endif %}
    {% assign is_journal = false %}
    {% if venue contains "journal" or venue contains "letters" or venue contains "transactions" or venue contains "magazine" or venue contains "frontiers" or venue contains "ieee access" or venue contains "robotics and automation letters" or venue contains "international journal" or venue contains "battery energy" or venue contains "control engineering practice" or venue contains "smart and sustainable manufacturing systems" or venue contains "robotics and computer-integrated manufacturing" or venue contains "journal of medical devices" %}{% assign is_journal = true %}{% endif %}
    {% if venue contains "ifac-papersonline" or venue contains "procedia " %}{% assign is_journal = false %}{% assign is_conf = true %}{% endif %}
    {% unless is_arxiv or is_book or is_conf or is_journal %}
      {% assign key = c.DOI | default: c.doi | default: c.id | default: c.title | downcase %}
      {% assign pad = sep | append: key | append: sep %}
      {% unless seen contains pad %}
        {% assign seen = seen | append: pad %}
        {% assign lookup_key = c.id | default: c.title %}
        {% include citation.html lookup=lookup_key style="rich" %}
        {% assign printed_any = true %}
        {% assign has_any = true %}
      {% endunless %}
    {% endunless %}
  {% endif %}
{% endfor %}
{% unless printed_any %}{% endunless %}
