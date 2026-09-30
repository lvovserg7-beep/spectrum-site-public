# -*- coding: utf-8 -*-
"""Живой срез 29.09: крошки (канон / стрелка T758 / нет), пустые Alt в ряду писем и логотипов."""
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _audit_breadcrumbs_all_0928 as bc  # noqa: E402
from _audit_alts_tail import SHARED_ALT, IMG_RE, attrs, basename  # noqa: E402

bc.OUT = Path(__file__).with_name("_bc-all-2026-09-29.json")
OUT = Path(__file__).with_name("_tiers_live_0929.json")


def extra(url):
    if "/tproduct/" in url:
        return None
    h = bc.get(url + "?tl=2909")
    t758 = 0
    blocks = list(re.finditer(r'data-record-type="(\d+)"', h))
    t758 = sum(1 for b in blocks if b.group(1) == "758")
    empty = []
    for m in IMG_RE.finditer(h):
        a = attrs(m.group(1))
        src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
        fn = basename(src)
        if fn in SHARED_ALT and not (a.get("alt") or "").strip():
            empty.append(fn)
    return {"path": url.replace("https://alsn.ru", "") or "/", "t758": t758, "empty_alt": empty,
            "noindex": bool(re.search(r'<meta[^>]+name="robots"[^>]+noindex', h))}


def main():
    urls = bc.sitemap_urls()
    pages = [u for u in urls if "/tproduct/" not in u]
    with ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(bc.run, pages))
        ext = list(ex.map(lambda u: (lambda: extra(u))() if True else None, pages))
    by = {e["path"]: e for e in ext if e}
    for r in rows:
        r.update(by.get(r["path"], {}))
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("pages", len(rows))
    print("style", Counter(r.get("style") for r in rows))
    t758 = [r for r in rows if r.get("t758")]
    print("T758 total", len(t758), "double with canon", sum(1 for r in t758 if r.get("style") == "CANON"))
    alt = [r for r in rows if r.get("empty_alt")]
    print("pages with empty alt in letters row", len(alt), "imgs", sum(len(r["empty_alt"]) for r in alt))
    print("NONE:", [r["path"] for r in rows if r.get("style") == "NONE"])
    print("NOT CANON:", [(r["path"], r.get("style")) for r in rows if r.get("style") not in ("CANON", "NONE")])
    print("mismatch:", [r["path"] for r in rows if r.get("style") == "CANON" and not r.get("name_match")])
    print("T758 pages:", [r["path"] for r in t758])
    print("alt pages:", [(r["path"], len(r["empty_alt"])) for r in alt])
    print("errors:", [(r["path"], r.get("err")) for r in rows if r.get("kind") == "err"])


if __name__ == "__main__":
    main()
