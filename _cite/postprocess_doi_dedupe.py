import yaml, re, sys, collections
p = "_data/citations.yaml"
data = yaml.safe_load(open(p, "r", encoding="utf-8")) or []
seen = set()
out = []
for it in data:
    doi = (it.get("DOI") or it.get("doi") or "").strip()
    if doi:
        doi_low = doi.lower()
        it["DOI"] = doi_low
        it["doi"] = doi_low
        key = f"doi:{doi_low}"
    else:
        key = (it.get("id") or it.get("title") or "").strip().lower()
    if key and key in seen:
        continue
    seen.add(key)
    out.append(it)
yaml.safe_dump(out, open(p, "w", encoding="utf-8"), sort_keys=False, allow_unicode=True)
print(f"kept {len(out)} of {len(data)}")
