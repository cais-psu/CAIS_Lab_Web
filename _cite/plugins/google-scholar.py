#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Scholar plugin for Greene Lab LWT (CAIS-PSU customized).

简化且更保守的版本：
- 从 GSID 获取所有 publications（使用 SerpAPI）
- 仅从现有链接中提取原始 DOI / arXiv / URL，不调用 Crossref、不猜 DOI
- 保留原本 DOI（来自 doi.org/...）
- 每条记录输出 title, authors, publisher, date, link，并附加 id（若可得）
- SerpAPI author 调用结果缓存 24 小时：_data/.cache/google-scholar/{gsid}.author.json
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
    """
    从原始 URL 中提取 DOI。
    不做任何修正或猜测，只是从 doi.org/... 截取后半段并小写。
    """
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
            seen.add(u)
            ordered.append(u)

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
    """
    只根据链接构造 Manubot id：
    - 先 DOI
    - 再 arXiv
    - 再非 scholar 的 URL
    不调用 Crossref、不猜 DOI。
    """
    # Try DOI
    for u in links:
        d = _doi_id_from(u)
        if d:
            return d
    # Then arXiv
    for u in links:
        a = _arxiv_id_from(u)
        if a:
            return a
    # Then non-scholar URL
    for u in links:
        if u and u.startswith("http") and _non_scholar(u):
            return "url:" + u
    return None

# ---------------- SerpAPI ----------------
def _serpapi_author_pubs(s: requests.Session, gsid: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Fetch publications for GSID from SerpAPI.
    加入 24 小时缓存：_data/.cache/google-scholar/{gsid}.author.json
    """
    cache_path = CACHE_DIR / f"{gsid}.author.json"

    # --- 24h valid cache ---
    if cache_path.exists():
        age_hours = (time.time() - cache_path.stat().st_mtime) / 3600.0
        if age_hours <= 24:
            try:
                with cache_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                logging.warning(f"Cached author file {cache_path} is corrupted, refetching.")
                # 坏掉就重新拉
                pass

    # ----- Real SerpAPI Fetch -----
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
        for attempt in range(1, MAX_RETRY + 1):
            try:
                r = s.get(SERPAPI_ENDPOINT, params=params, timeout=REQ_TIMEOUT)
                if r.status_code == 429:
                    _sleep(attempt)
                    continue
                r.raise_for_status()
                data = r.json()
                page_items = data.get("articles") or data.get("publications") or []
                pubs.extend(page_items)
                next_link = data.get("serpapi_pagination", {}).get("next")
                if next_link:
                    start += 100
                    break
                # finished
                _dump_json(cache_path, pubs)   # 保存到缓存
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
    for attempt in range(1, MAX_RETRY + 1):
        try:
            r = s.get(SERPAPI_ENDPOINT, params=params, timeout=REQ_TIMEOUT)
            if r.status_code == 429:
                _sleep(attempt)
                continue
            r.raise_for_status()
            data = r.json()
            res = (data.get("organic_results") or [None])[0]
            return res
        except Exception as e:
            logging.warning(f"SerpAPI cluster fetch error (attempt {attempt}): {e}")
            if attempt >= MAX_RETRY:
                return None
            _sleep(attempt)
    return None

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
    return links

def _extract_links_from_cluster_detail(detail: Dict[str, Any]) -> List[str]:
    """
    Pull more/better links from cluster organic result.
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
            seen.add(u)
            out.append(u)
    return out

def _normalize_item(it: Dict[str, Any], s: requests.Session, api_key: str) -> Tuple[Optional[str], Dict[str, Any], Dict[str, Any]]:
    """
    Returns (manubot_id, core_fields, debug_info)

    core_fields:
      - title
      - authors
      - publisher
      - date
      - link  （展示用链接，可能是 publisher/DOI，也可能是 scholar）

    manubot_id:
      - 只来自非 scholar 链接（doi / arxiv / url）
      - 不调用 Crossref，不猜 DOI
    """
    title = _norm(it.get("title") or it.get("name"))
    year  = _year_from(
        it.get("year")
        or (it.get("publication_info") or {}).get("year")
        or (it.get("citation") or {}).get("year")
    )
    authors = _coerce_authors(it.get("authors"))
    # publisher 优先用 "publication" 字段，其次 publication_info.name
    pubinfo = it.get("publication_info") or {}
    publisher = it.get("publication") or pubinfo.get("name") or None

    cluster_id = it.get("citation_id") or it.get("result_id") or None

    cand_links = _extract_links_from_author_item(it)

    # 如果当前链接都是 scholar，尝试通过 cluster 再拿原始链接
    chosen_detail = None
    if (not any(_non_scholar(u) for u in cand_links)) and cluster_id:
        chosen_detail = _serpapi_cluster_detail(s, cluster_id, api_key)
        cand_links.extend(_extract_links_from_cluster_detail(chosen_detail or {}))

    # 原始链接（只在非 scholar 等时才作为“最佳”）
    best_url = _prefer_original(cand_links) if cand_links else None
    # 展示用链接：如果没有“最佳”非 scholar 链接，就退回到第一条候选（可能是 scholar）
    display_link = best_url or (cand_links[0] if cand_links else None)

    # 构造 Manubot id（只用 best_url）
    mb_id = _mb_id_from_links([best_url] if best_url else [])

    date_str = f"{year}-01-01" if year else None
    core_fields: Dict[str, Any] = {
        "title": title or "",
        "authors": authors or [],
        "publisher": publisher or "",
        "date": date_str or "",
        "link": display_link or "",
    }

    dbg = {
        "title": title,
        "year": year,
        "cluster_id": cluster_id,
        "author_item_links": cand_links,
        "best_url": best_url,
        "display_link": display_link,
        "cluster_detail_used": bool(chosen_detail),
    }

    return mb_id, core_fields, dbg

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

    out: List[Dict[str, Any]] = []
    dbg_all: List[Dict[str, Any]] = []

    for it in pubs:
        try:
            mb_id, fields, dbg = _normalize_item(it, s, api_key)
            dbg_all.append(dbg)
            if mb_id:
                # 有 Manubot id：id + 标准字段 + entry 标签
                out.append({"id": mb_id, **fields, **forward_tags})
            else:
                # 没有 id：至少保留 title/authors/link 等字段
                out.append({**fields, **forward_tags})
        except Exception as e:
            t = _norm(it.get("title") or it.get("name"))
            logging.warning(f"Normalize error for '{t}': {e}")
            if t:
                # 最坏情况也保留 title
                out.append({"title": t, **forward_tags})
            continue

    # 持久化 debug 信息
    _dump_json(CACHE_DIR / f"{gsid}.resolved.json", dbg_all)

    # de-duplicate（保守：优先按 id，其次按 title|date|link）
    deduped: List[Dict[str, Any]] = []
    seen = set()
    for it in out:
        key = it.get("id")
        if not key:
            key = f"{it.get('title','')}|{it.get('date','')}|{it.get('link','')}"
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)

    logging.info(f"Resolved {len(deduped)} item(s) for GSID {gsid}")
    n_doi = sum(1 for x in deduped if (x.get("id") or "").startswith("doi:"))
    n_axv = sum(1 for x in deduped if (x.get("id") or "").startswith("arxiv:"))
    n_url = sum(1 for x in deduped if (x.get("id") or "").startswith("url:"))
    n_man = sum(1 for x in deduped if "id" not in x)
    logging.info(f"Stats → doi:{n_doi}  arxiv:{n_axv}  url:{n_url}  manual:{n_man}")

    return deduped
