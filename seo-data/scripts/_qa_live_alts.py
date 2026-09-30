# -*- coding: utf-8 -*-
"""Crawl live tproduct pages and compare gallery alt to expected catalog alts."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = ROOT / "_qa_alts_expected.json"
OUT = ROOT / "_qa_alts_live.json"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
GALLERY_RE = re.compile(r'"gallery"\s*:\s*(\[.*?\])\s*,\s*"sort"', re.S)


def fetch(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ru-RU,ru;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def gallery_alts(html: str) -> list[str]:
    m = GALLERY_RE.search(html)
    if not m:
        return []
    raw = m.group(1)
    try:
        arr = json.loads(raw)
    except json.JSONDecodeError:
        return []
    out = []
    for item in arr:
        if isinstance(item, dict):
            out.append((item.get("alt") or "").strip())
    return out


def check_one(it: dict) -> dict:
    url = it["url"]
    exp = (it["alt"] or "").strip()
    rec = {
        "sku": it["sku"],
        "title": it["title"],
        "url": url,
        "expected": exp,
        "keep": it.get("keep"),
        "parent": it.get("parent"),
    }
    try:
        html = fetch(url)
        alts = gallery_alts(html)
        rec["all_alts"] = alts
        live = alts[0] if alts else ""
        rec["live"] = live
        rec["gallery_n"] = len(alts)
        if not alts:
            rec["status"] = "no_gallery"
        elif not live:
            rec["status"] = "empty"
        elif live == exp:
            rec["status"] = "ok"
        elif exp in alts:
            rec["status"] = "ok_other"
            rec["live"] = exp
        else:
            rec["status"] = "mismatch"
    except urllib.error.HTTPError as e:
        rec["status"] = "error"
        rec["error"] = f"HTTP {e.code}"
    except Exception as e:
        rec["status"] = "error"
        rec["error"] = str(e)
    return rec


def crawl() -> None:
    items = json.loads(EXPECTED.read_text(encoding="utf-8"))
    results = []
    counts = {"ok": 0, "ok_other": 0, "empty": 0, "no_gallery": 0, "mismatch": 0, "error": 0}
    done = 0
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(check_one, it) for it in items]
        for fut in as_completed(futs):
            rec = fut.result()
            results.append(rec)
            counts[rec["status"]] = counts.get(rec["status"], 0) + 1
            done += 1
            if done % 25 == 0 or done == len(items):
                print(
                    f"{done}/{len(items)} ok={counts['ok']} empty={counts['empty']} "
                    f"mismatch={counts['mismatch']} no_gal={counts['no_gallery']} err={counts['error']}"
                )
    results.sort(key=lambda x: (x.get("title") or "", x.get("sku") or ""))
    summary = {"total": len(items), **counts, "results": results}
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)
    print(counts)


if __name__ == "__main__":
    t0 = time.time()
    crawl()
    print("sec", round(time.time() - t0, 1))
