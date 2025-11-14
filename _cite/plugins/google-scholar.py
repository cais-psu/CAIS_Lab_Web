#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Scholar plugin for Greene Lab LWT (CAIS-PSU customized).

- 从 GSID 获取所有 publications（SerpAPI）
- 只从已有链接中提取 DOI / arXiv / URL，不调用 Crossref，不猜 DOI
- 返回的每条记录包含：
    id, title, authors, publisher, date, link, 以及 entry 中的其他字段（image, plugin, file 等）
- 对 SerpAPI author 结果做 24 小时缓存（_data/.cache/google-scholar/{gsid}.author.json）
- 如果标题相同，保留 date 更晚的一条记录
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

def _sleep(attempt: int):
    # exponential backoff
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
    不做任何“修正”或“猜测”，只是截取 doi.org/... 后面的部分，然后统一小写。
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
    不调用 Crossref，不猜 DOI，只从已有的链接中找：
    - 先 DOI
    - 再 arXiv
    - 再非 scholar 的 URL
    """
    for u in links:
        d = _doi_id_from(u)
        if d:
            return d
    for u in links:
        a = _arxiv_id_from(u)
        if a:
            return a
    for u in links:
        if u and u.startswith("http") and _non_scholar(u):
            return "url:" + u
    return None

# ---------------- SerpAPI ----------------
def _serpapi_author_pubs(s: requests.Session, gsid: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Fetch publications for GSID from SerpAPI.
    24 小时缓存：_data/.cache/google-scholar/{gsid}.author.json
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
                # fall through to live fetch

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
                _dump_json(cache_path, pubs)
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

    # inline_links
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
    Returns (manubot_id, manual_fallback_fields, debug_info)

    - manubot_id 只来自已有链接（doi.org / arxiv.org / publisher url）
    - 不调用 Crossref，不猜 DOI
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

    # 如果当前链接都是 scholar，尝试通过 cluster 再拿原始链接
    chosen_detail = None
    if (not any(_non_scholar(u) for u in cand_links)) and cluster_id:
        chosen_detail = _serpapi_cluster_detail(s, cluster_id, api_key)
        cand_links.extend(_extract_links_from_cluster_detail(chosen_detail or {}))

    # 从所有候选链接中选一个“原始链接”
    best_url = _prefer_original(cand_links) if cand_links else None

    # 构造 Manubot id
    mb_id = _mb_id_from_links([best_url] if best_url else [])

    dbg = {
        "title": title,
        "year": year,
        "cluster_id": cluster_id,
        "author_item_links": cand_links,
        "best_url": best_url,
        "cluster_detail_used": bool(chosen_detail),
        "authors": authors,
    }

    if not mb_id:
        manual = {
            "title": title or None,
            "publisher": None,
            "date": f"{year}-01-01" if year else None,
            "link": best_url or None,
        }
        manual = {k: v for k, v in manual.items() if v}
        return None, manual, dbg

    return mb_id, {}, dbg

# ---------------- Plugin entry ----------------
def main(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Required by cite.py: take one entry from _data/google-scholar*.yaml
    and return a list of "sources" dicts.

    输出格式类似你给的例子：
    - id: doi:...
      title: ...
      authors: [...]
      publisher: ...
      date: 'YYYY-01-01'
      link: https://doi.org/...
      <entry中的其他字段...>
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

    # entry 中其他字段全部原样透传（比如 image, plugin, file, tags 等）
    forward_tags = {k: v for k, v in (entry or {}).items() if k != "gsid"}

    api_key = _get_env_required("GOOGLE_SCHOLAR_API_KEY")
    s = _session()

    logging.info(f"Processing GSID: {gsid}")
    pubs = _serpapi_author_pubs(s, gsid, api_key)

    out: List[Dict[str, Any]] = []
    dbg_all: List[Dict[str, Any]] = []

    for it in pubs:
        try:
            # 先拿基础信息
            title = _norm(it.get("title") or it.get("name"))
            year = _year_from(
                it.get("year")
                or (it.get("publication_info") or {}).get("year")
                or (it.get("citation") or {}).get("year")
            )
            date_str = f"{year}-01-01" if year else ""
            authors = _coerce_authors(it.get("authors"))
            pubinfo = it.get("publication_info") or {}
            publisher = pubinfo.get("summary") or it.get("publication") or ""

            mb_id, manual, dbg = _normalize_item(it, s, api_key)
            dbg_all.append(dbg)

            # 组合一条统一格式的记录
            record: Dict[str, Any] = {}
            record.update(manual)  # 可能包含 title/date/link（如果 mb_id 为空时）

            if title:
                record["title"] = title
            if authors:
                record["authors"] = authors
            if publisher and not record.get("publisher"):
                record["publisher"] = publisher
            if date_str:
                record["date"] = date_str

            # link：优先 manual.link -> dbg.best_url -> it.link
            if not record.get("link"):
                record["link"] = dbg.get("best_url") or it.get("link", "")

            # id：只有在我们确实解析到 mb_id 时才写入
            if mb_id:
                record["id"] = mb_id
            else:
                # 没有 id 的情况就保持 manual 的结构（让前端至少能显示）
                pass

            # 把 entry 的其他 tag 合并进去（image, plugin, file, 等）
            record.update(forward_tags)

            out.append(record)

        except Exception as e:
            t = _norm(it.get("title") or it.get("name"))
            logging.warning(f"Normalize error for '{t}': {e}")
            if t:
                fallback = {"title": t}
                fallback.update(forward_tags)
                out.append(fallback)
            continue

    # 持久化 debug 信息
    _dump_json(CACHE_DIR / f"{gsid}.resolved.json", dbg_all)

    # -------- 去重：同 title 保留 date 最新的一条 --------
    by_title: Dict[str, Dict[str, Any]] = {}
    others: List[Dict[str, Any]] = []
    others_seen = set()

    for it in out:
        t_raw = it.get("title", "")
        t_norm = _norm(t_raw).lower()

        if t_norm:
            existing = by_title.get(t_norm)
            if existing is None:
                by_title[t_norm] = it
            else:
                # 比较日期，保留最新
                d_new = it.get("date", "")
                d_old = existing.get("date", "")
                # 简单按字符串比较（YYYY-MM-DD 格式适用）
                better = False
                if d_new and not d_old:
                    better = True
                elif d_new and d_old and d_new > d_old:
                    better = True
                elif (not d_new and not d_old) and (not existing.get("id") and it.get("id")):
                    # 都没 date，就优先有 id 的
                    better = True

                if better:
                    by_title[t_norm] = it
        else:
            # 没有标题的条目，按 id/date/link 做简单去重
            key = it.get("id") or f"{it.get('title','')}|{it.get('date','')}|{it.get('link','')}"
            if key in others_seen:
                continue
            others_seen.add(key)
            others.append(it)

    deduped: List[Dict[str, Any]] = list(by_title.values()) + others

    logging.info(f"Resolved {len(deduped)} item(s) for GSID {gsid}")
    n_doi = sum(1 for x in deduped if (x.get("id") or "").startswith("doi:"))
    n_axv = sum(1 for x in deduped if (x.get("id") or "").startswith("arxiv:"))
    n_url = sum(1 for x in deduped if (x.get("id") or "").startswith("url:"))
    n_man = sum(1 for x in deduped if "id" not in x)
    logging.info(f"Stats → doi:{n_doi}  arxiv:{n_axv}  url:{n_url}  manual:{n_man}")

    return deduped
