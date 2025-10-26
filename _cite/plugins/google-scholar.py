# _cite/plugins/google-scholar.py
# -*- coding: utf-8 -*-

"""
Google Scholar plugin (SerpAPI-backed) for LWT/Manubot citation pipeline.

- Reads `gsid` (Google Scholar author id) from a data entry provided by cite.py
- Requires env GOOGLE_SCHOLAR_API_KEY
- Fetches all publications with pagination
- Emits Manubot-compatible source ids:
    * Prefer DOI (including DataCite arXiv DOI like 10.48550/arXiv.YYYY.NNNNN)
    * Else derive arXiv id from arxiv.org/abs|pdf/YYYY.NNNNN
- Prints progress and returns [{"id": "..."}...]
"""

from __future__ import annotations
import os
import re
import json
import time
from typing import Dict, Any, Iterable, List, Optional
import requests

# --- Regex helpers -----------------------------------------------------------

_DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.IGNORECASE)
_ARXIV_DOI_RE = re.compile(r"10\.48550/arXiv\.\d{4}\.\d{5}", re.IGNORECASE)
_ARXIV_URL_RE = re.compile(r"arxiv\.org/(abs|pdf)/(\d{4}\.\d{5})(?:v\d+)?", re.IGNORECASE)

# --- Small utils -------------------------------------------------------------

def _get_env_required(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return v

def _extract_doi(text: str | None) -> Optional[str]:
    if not text:
        return None
    m = _DOI_RE.search(text)
    return m.group(0) if m else None

def _extract_arxiv_id_from_url(url: str | None) -> Optional[str]:
    if not url:
        return None
    m = _ARXIV_URL_RE.search(url)
    return m.group(2) if m else None

def _norm_id_from_entry(entry: Dict[str, Any]) -> Optional[str]:
    """
    Build a Manubot id from a Scholar publication dict.
    Preference:
      1) DOI (normalize, lowercase)
      2) arxiv:<id> from arxiv.org URL
      3) None (caller may skip)
    """
    # Try dedicated fields first
    doi = entry.get("doi")
    if not doi:
        # probe common text-ish fields
        for k in ("publication_info", "snippet", "title"):
            doi = _extract_doi(entry.get(k, ""))
            if doi:
                break
        # also check link/url if they contain doi.org/...
        if not doi:
            for k in ("link", "url"):
                doi = _extract_doi(entry.get(k, ""))
                if doi:
                    break

    if doi:
        doi = doi.strip().strip(".").strip()
        return f"doi:{doi.lower()}"

    # try arXiv url
    for k in ("link", "url"):
        aid = _extract_arxiv_id_from_url(entry.get(k, ""))
        if aid:
            return f"arxiv:{aid}"

    return None

def _safe_get(d: Dict[str, Any], *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return default
    return d

# --- SerpAPI calls -----------------------------------------------------------

SERP_BASE = "https://serpapi.com/search.json"

def _fetch_author_page(gsid: str, api_key: str, start: int = 0) -> Dict[str, Any]:
    """
    One page of author publications via SerpAPI google_scholar_author engine.
    """
    params = {
        "engine": "google_scholar_author",
        "author_id": gsid,
        "api_key": api_key,
        "sort": "pubdate",   # newest first
        "num": 20,           # SerpAPI default page size
        "start": start,      # pagination offset
    }
    r = requests.get(SERP_BASE, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def _iter_all_publications(gsid: str, api_key: str) -> Iterable[Dict[str, Any]]:
    """
    Iterate all publications with pagination.
    """
    start = 0
    seen_keys = set()
    while True:
        data = _fetch_author_page(gsid, api_key, start=start)

        # articles in this page
        articles = data.get("articles") or []
        if not isinstance(articles, list):
            articles = []

        for art in articles:
            # de-dupe by a stable key (prefer cite_id or link)
            key = _safe_get(art, "cite_id") or art.get("link") or art.get("title")
            if not key:
                key = json.dumps(art, sort_keys=True)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            yield art

        # pagination
        pag = data.get("serpapi_pagination") or {}
        next_url = pag.get("next")
        next_offset = pag.get("next_offset")
        if next_url and isinstance(next_offset, int):
            start = next_offset
            # be nice to API / avoid rate limiting
            time.sleep(0.8)
            continue
        break

# --- Cache helpers (optional, safe no-op if folder missing) ------------------

def _write_cache(path: str, obj: Any) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
    except Exception:
        # cache is optional – ignore errors
        pass

# --- Public entrypoint -------------------------------------------------------

def main(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Expected to be called by _cite/cite.py:
        expanded = import_module("plugins.google-scholar").main(entry)
    `entry` comes from `_cite/data/google-scholar.yaml`, e.g.:
        - gsid: secQmYUAAAAJ
    Returns: [{"id": "doi:..."}, {"id": "arxiv:..."} ...]
    """
    api_key = _get_env_required("GOOGLE_SCHOLAR_API_KEY")

    gsid = (entry.get("gsid") or entry.get("author_id") or "").strip()
    if not gsid:
        raise RuntimeError('google-scholar: missing required "gsid" in data entry')

    print(f"    Processing data file google-scholar.yaml")
    print(f"Processing entry 1 of 1, gsid: {gsid}", flush=True)

    # Walk all pages
    results: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()

    # (optional) fetch and cache author metadata
    try:
        author_meta = _fetch_author_page(gsid, api_key, start=0).get("author", {})
        _write_cache(f"_data/.cache/google-scholar/{gsid}.author.json", author_meta)
    except Exception:
        author_meta = {}

    idx = 0
    for pub in _iter_all_publications(gsid, api_key):
        idx += 1

        # Try to derive a canonical Manubot id
        source_id = _norm_id_from_entry(pub)

        # 额外兜底：从 publication_info 的外链里再尝试一次 DOI / arXiv
        if not source_id:
            pubinfo = pub.get("publication_info") or ""
            # SerpAPI 有时 publication_info 是纯文本
            if isinstance(pubinfo, str):
                doi2 = _extract_doi(pubinfo)
                if doi2:
                    source_id = f"doi:{doi2.lower().strip().strip('.')}"
            # 尝试 link/url
            if not source_id:
                source_id = _norm_id_from_entry({
                    "link": pub.get("link") or "",
                    "url": pub.get("link") or "",
                })

        if not source_id:
            # 放行：无法确定引用标识就跳过该条目
            continue

        # 统一去重（doi 忽略大小写）
        norm = source_id.lower().strip()
        if norm in seen_ids:
            continue
        seen_ids.add(norm)

        # 输出与返回
        print(f"id: {norm}")
        results.append({"id": norm})

    # 也把所有解析过的 publication 列表缓存下来（便于调试）
    try:
        _write_cache(f"_data/.cache/google-scholar/{gsid}.resolved.json", results)
    except Exception:
        pass

    print(f"            {len(results)} source(s)")
    return results


# 允许本地调试（可选）
if __name__ == "__main__":
    # 简单自测：设置环境变量后执行
    try:
        main({"gsid": os.environ.get("GOOGLE_SCHOLAR_GSID", "secQmYUAAAAJ")})
    except Exception as e:
        print(f"google-scholar plugin error: {e}")
        raise
