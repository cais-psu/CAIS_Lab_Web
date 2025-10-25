#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Scholar plugin for Greene Lab LWT (CAIS-PSU customized).

Implements your 1–4 steps:
1) From a Google Scholar author ID (GSID) fetch all publications (with cluster ids)
2) Resolve each paper's original URL (DOI/arXiv/publisher), not the Scholar URL
   - Use SerpAPI "google_scholar_author" first, then "google_scholar" with cluster=...
   - Skip scholar.google.com links
   - Persist raw fetch artifacts under _data/.cache/google-scholar/
3) Convert resolved URL to a Manubot id: doi:/arxiv:/url: (fallback to Crossref title search)
4) Return sources list for cite.py to generate citations; site lists them via research page include.

Environment:
- GOOGLE_SCHOLAR_API_KEY (required)
- CROSSREF_MAILTO (optional)
"""

from __future__ import annotations

import os
import re
import json
import time
import pathlib
import logging
from typing import Any, Dict, List, Optional, Tuple

import requests

# ---------------- Config ----------------
CACHE_DIR = pathlib.Path("_data/.cache/google-scholar")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"
CROSSREF_ENDPOINT = "https://api.crossref.org/works"

REQ_TIMEOUT = 20
MAX_RETRY = 4
BACKOFF_BASE = 1.8

ARXIV_RE = re.compile(r"arxiv\.org/(abs|pdf)/([0-9]+\.[0-9]+)(v[0-9]+)?", re.I)
DOI_URL_RE = re.compile(r"doi\.org/([^/\s]+/[^/\s]+)", re.I)

# ---------------- Utils ----------------
def _get_env_required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val

def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": "CAIS-PSU-LWT-GS/1.1 (+https://cais-psu.github.io/CAIS_Lab_Web/)"})
    return s

def _sleep(attempt: int):  # exponential backoff
    time.sleep((BACKOFF_BASE ** attempt) + 0.25 * attempt)

def _norm(s: Optional[str]) -> str:
    import re as _re
    return _re.sub(r"\s+", " ", s or "").strip()

def _year_from(v: Any) -> Optional[int]:
    try:
        y = int(str(v)[:4])
        if 1800 <= y <= 2100:
            return y
    except Exception:
        pass
    return None

def _dump_json(path: pathlib.Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _coerce_authors(obj) -> List[str]:
    """Normalize authors to ['Alice', 'Bob'] regardless of source structure."""
    out: List[str] = []
    if not obj:
        return out
    if isinstance(obj, list):
        for a in obj:
            if isinstance(a, dict):
                n = a.get("name") or a.get("author") or a.get("full_name")
                if n:
                    out.append(str(n))
            elif isinstance(a, str):
                s = a.strip()
                if s:
                    out.append(s)
    elif isinstance(obj, dict):
        n = obj.get("name") or obj.get("author") or obj.get("full_name")
        if n:
            out.append(str(n))
    return out

# ---------------- Manubot id helpers ----------------
def _arxiv_id_from(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    m = ARXIV_RE.search(url)
    return f"arxiv:{m.group(2)}" if m else None

def _doi_id_from(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    m = DOI_URL_RE.search(url)
    return f"doi:{m.group(1).lower()}" if m else None

def _non_scholar(url: Optional[str]) -> bool:
    return bool(url) and ("scholar.google." not in url)

def _prefer_original(links: List[str]) -> Optional[str]:
    """Select best 'original' URL: doi.org > arxiv.org > publisher (non-scholar) > else None."""
    if not links:
        return None
    # dedupe & keep order
    seen, ordered = set(), []
    for u in links:
        if u and u not in seen:
            seen.add(u); ordered.append(u)

    # 1) doi.org
    for u in ordered:
        if "doi.org/" in u:
            return u
    # 2) arxiv
    for u in ordered:
        if "arxiv.org/" in u:
            return u
    # 3) any non-scholar http
    for u in ordered:
        if u.startswith("http") and _non_scholar(u):
            return u
    return None

def _mb_id_from_links(links: List[str]) -> Optional[str]:
    # Try DOI
    for u in links:
        d = _doi_id_from(u)
        if d: return d
    # Then arXiv
    for u in links:
        a = _arxiv_id_from(u)
        if a: return a
    # Then non-scholar URL
    for u in links:
        if u and u.startswith("http") and _non_scholar(u):
            return "url:" + u
    return None

# ---------------- SerpAPI ----------------
def _serpapi_author_pubs(s: requests.Session, gsid: str, api_key: str) -> List[Dict[str, Any]]:
    pubs: List[Dict[str, Any]] = []
    start = 0
    while True:
        params = {
            "engine": "google_scholar_author",
            "author_id": gsid,
            "num": "100",
            "hl": "en",
            "api_key": api_key,
            "start": str(start),
            "sort": "pubdate",
        }
        for attempt in range(1, MAX_RETRY+1):
            try:
                r = s.get(SERPAPI_ENDPOINT, params=params, timeout=REQ_TIMEOUT)
                if r.status_code == 429:
                    _sleep(attempt); continue
                r.raise_for_status()
                data = r.json()
                page_items = data.get("articles") or data.get("publications") or []
                pubs.extend(page_items)
                next_link = data.get("serpapi_pagination", {}).get("next")
                if next_link:
                    start += 100
                    break
                return pubs
            except Exception as e:
                logging.warning(f"SerpAPI author fetch error (attempt {attempt}): {e}")
                if attempt >= MAX_RETRY:
                    raise
                _sleep(attempt)

def _serpapi_cluster_detail(s: requests.Session, cluster_id: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Resolve a scholar cluster to detailed search result.
    Returns a dict with potential original links (resources, inline_links, publication_info.link).
    """
    params = {
        "engine": "google_scholar",
        "cluster": cluster_id,
        "hl": "en",
        "api_key": api_key,
    }
    for attempt in range(1, MAX_RETRY+1):
        try:
            r = s.get(SERPAPI_ENDPOINT, params=params, timeout=REQ_TIMEOUT)
            if r.status_code == 429:
                _sleep(attempt); continue
            r.raise_for_status()
            data = r.json()
            # SerpAPI returns an "organic_results" list; first is usually the canonical item
            res = (data.get("organic_results") or [None])[0]
            return res
        except Exception as e:
            logging.warning(f"SerpAPI cluster fetch error (attempt {attempt}): {e}")
            if attempt >= MAX_RETRY:
                return None
            _sleep(attempt)
    return None

# ---------------- Crossref fallback ----------------
def _crossref_find_doi(s: requests.Session, title: str, authors: List[str], year: Optional[int]) -> Optional[str]:
    if not title:
        return None
    params = {"query.title": title, "rows": 3}
    if authors:
        params["query.author"] = authors[0].split()[-1]
    if year:
        params["filter"] = f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31"

    headers = {}
    mailto = os.getenv("CROSSREF_MAILTO")
    if mailto:
        headers["User-Agent"] = f"CAIS-PSU-LWT-GS/1.1 (mailto:{mailto})"

    for attempt in range(1, MAX_RETRY+1):
        try:
            r = s.get(CROSSREF_ENDPOINT, params=params, headers=headers, timeout=REQ_TIMEOUT)
            if r.status_code == 429:
                _sleep(attempt); continue
            r.raise_for_status()
            items = r.json().get("message", {}).get("items", [])
            title_norm = _norm(title).lower()
            for it in items:
                doi = (it.get("DOI") or "").lower()
                cr_titles = it.get("title") or []
                cr_title = _norm(cr_titles[0] if cr_titles else "").lower()
                if doi and cr_title and (title_norm in cr_title or cr_title in title_norm):
                    return "doi:" + doi
            if items and items[0].get("DOI"):
                return "doi:" + items[0]["DOI"].lower()
            return None
        except Exception as e:
            logging.warning(f"Crossref error (attempt {attempt}): {e}")
            if attempt >= MAX_RETRY:
                return None
            _sleep(attempt)

# ---------------- Core normalize ----------------
def _extract_links_from_author_item(it: Dict[str, Any]) -> List[str]:
    """
    Pull candidate links from the author publications item.
    """
    links: List[str] = []
    if it.get("link"):
        links.append(it["link"])
    # Sometimes publication_info.link holds the publisher page
    pi = it.get("publication_info") or {}
    if isinstance(pi, dict) and pi.get("link"):
        links.append(pi["link"])
    # resources may contain PDFs
    for res in (it.get("resources") or []):
        if isinstance(res, dict) and res.get("link"):
            links.append(res["link"])
        elif isinstance(res, str):
            links.append(res)
    # Remove pure scholar links here is not necessary yet; we'll prefer non-scholar later.
    return links

def _extract_links_from_cluster_detail(detail: Dict[str, Any]) -> List[str]:
    """
    Pull more/better links from cluster organic result:
    - resources: [{'title':'PDF','link':...}, ...]
    - inline_links: {'versions':[{'link':...}], 'pdf': {'link':...}, 'related_pages':[...] }
    - publication_info: {'link': ...}
    - link: main result link
    """
    links: List[str] = []
    if not detail:
        return links

    # main link
    if detail.get("link"):
        links.append(detail["link"])

    # publication_info.link
    pubinfo = detail.get("publication_info") or {}
    if isinstance(pubinfo, dict) and pubinfo.get("link"):
        links.append(pubinfo["link"])

    # resources list
    for res in (detail.get("resources") or []):
        if isinstance(res, dict) and res.get("link"):
            links.append(res["link"])
        elif isinstance(res, str):
            links.append(res)

    # inline_links could have many types
    inl = detail.get("inline_links") or {}
    if isinstance(inl, dict):
        # pdf
        pdf = inl.get("pdf") or {}
        if isinstance(pdf, dict) and pdf.get("link"):
            links.append(pdf["link"])
        elif isinstance(pdf, list):
            for x in pdf:
                if isinstance(x, dict) and x.get("link"):
                    links.append(x["link"])

        # versions
        for v in (inl.get("versions") or []):
            if isinstance(v, dict) and v.get("link"):
                links.append(v["link"])

        # related pages
        for v in (inl.get("related_pages") or []):
            if isinstance(v, dict) and v.get("link"):
                links.append(v["link"])

    # dedupe
    seen, out = set(), []
    for u in links:
        if u and u not in seen:
            seen.add(u); out.append(u)
    return out

def _normalize_item(it: Dict[str, Any], s: requests.Session, api_key: str) -> Tuple[Optional[str], Dict[str, Any], Dict[str, Any]]:
    """
    Returns (manubot_id, manual_fallback_fields, debug_info)
    manual_fallback_fields is dict with title/date/link when mb_id is None
    debug_info records what we looked at (candidate links, chosen link, cluster detail)
    """
    title = _norm(it.get("title") or it.get("name"))
    year  = _year_from(
        it.get("year")
        or (it.get("publication_info") or {}).get("year")
        or (it.get("citation") or {}).get("year")
    )
    authors = _coerce_authors(it.get("authors"))
    cluster_id = it.get("citation_id") or it.get("result_id") or None

    cand_links = _extract_links_from_author_item(it)

    # If author item only has Scholar links, resolve cluster for original links
    chosen_detail = None
    if (not any(_non_scholar(u) for u in cand_links)) and cluster_id:
        chosen_detail = _serpapi_cluster_detail(s, cluster_id, api_key)
        cand_links.extend(_extract_links_from_cluster_detail(chosen_detail or {}))

    # Choose best "original" url (skip Scholar)
    best_url = _prefer_original(cand_links) if cand_links else None

    # Build Manubot id
    mb_id = _mb_id_from_links([best_url] if best_url else [])

    # Fallback: Crossref (title/year/author) to get DOI
    if not mb_id and title:
        mb_id = _crossref_find_doi(s, title, authors, year)

    # Debug record
    dbg = {
        "title": title,
        "year": year,
        "cluster_id": cluster_id,
        "author_item_links": cand_links,
        "best_url": best_url,
        "cluster_detail_used": bool(chosen_detail),
    }

    if not mb_id:
        manual = {
            "title": title or None,
            "publisher": None,
            "date": f"{year}-01-01" if year else None,
            "link": best_url or None,  # still non-scholar if we found one
        }
        # prune None
        manual = {k: v for k, v in manual.items() if v}
        return None, manual, dbg

    return mb_id, {}, dbg

# ---------------- Plugin entry ----------------
def main(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Required by cite.py: take one entry from _data/google-scholar*.yaml
    and return a list of "sources" dicts.
    """
    # optional local .env
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass

    gsid = (entry or {}).get("gsid")
    if not gsid:
        logging.info("google-scholar entry without 'gsid'; skipping.")
        return []

    forward_tags = {k: v for k, v in (entry or {}).items() if k != "gsid"}
    api_key = _get_env_required("GOOGLE_SCHOLAR_API_KEY")
    s = _session()

    logging.info(f"Processing GSID: {gsid}")
    pubs = _serpapi_author_pubs(s, gsid, api_key)
    _dump_json(CACHE_DIR / f"{gsid}.author.json", pubs)

    out: List[Dict[str, Any]] = []
    dbg_all: List[Dict[str, Any]] = []

    for it in pubs:
        try:
            mb_id, manual, dbg = _normalize_item(it, s, api_key)
            dbg_all.append(dbg)
            if mb_id:
                out.append({"id": mb_id, **forward_tags})
            else:
                # manual fallback still produces a visible entry on site
                out.append({**manual, **forward_tags})
        except Exception as e:
            t = _norm(it.get("title") or it.get("name"))
            logging.warning(f"Normalize error for '{t}': {e}")
            continue

    # persist debug resolution data
    _dump_json(CACHE_DIR / f"{gsid}.resolved.json", dbg_all)

    # de-duplicate: by id or by (title|date)
    deduped: List[Dict[str, Any]] = []
    seen = set()
    for it in out:
        key = it.get("id") or f"{it.get('title','')}|{it.get('date','')}"
        if key in seen: continue
        seen.add(key); deduped.append(it)

    logging.info(f"Resolved {len(deduped)} item(s) for GSID {gsid}")
    # Optional: show a few stats in logs
    n_doi = sum(1 for x in deduped if (x.get("id") or "").startswith("doi:"))
    n_axv = sum(1 for x in deduped if (x.get("id") or "").startswith("arxiv:"))
    n_url = sum(1 for x in deduped if (x.get("id") or "").startswith("url:"))
    n_man = sum(1 for x in deduped if "id" not in x)
    logging.info(f"Stats → doi:{n_doi}  arxiv:{n_axv}  url:{n_url}  manual:{n_man}")

    return deduped
