# -*- coding: utf-8 -*-
"""Какие адреса меню (MENU из build_menu_preview_0930) живые на alsn.ru и что в текущей шапке T228."""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_menu_preview_0930 import MENU  # noqa: E402

OUT = Path(__file__).parent / "_menu_live_0930.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128 Safari/537.36"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.geturl(), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # noqa: BLE001
        return 0, url, str(e)


def urls():
    seen = []
    for name, allink, promo, cols in MENU:
        if allink:
            seen.append(allink[1])
        if promo:
            seen.append(promo[3])
        for t, href, d, kids in cols:
            seen.append(href)
            seen.extend(h for _, h, _ in kids)
    return [u for i, u in enumerate(seen) if u.startswith("/") and u not in seen[:i]]


def main():
    res = {}
    for u in urls():
        for _ in range(3):
            st, final, body = fetch(f"https://alsn.ru{u}?nocache={int(time.time())}")
            if st:
                break
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
        title = re.search(r"<title>(.*?)</title>", body, re.S)
        res[u] = {"status": st, "final": final,
                  "title": re.sub(r"\s+", " ", title.group(1)).strip() if title else "",
                  "h1": re.sub(r"<[^>]+>|\s+", " ", h1.group(1)).strip() if h1 else ""}
        print(st, u, res[u]["title"][:70])
    st, _, home = fetch(f"https://alsn.ru/?nocache={int(time.time())}")
    rec = re.search(r'<div id="rec172603117".*?</div>\s*</div>\s*</div>', home, re.S)
    hrefs = sorted(set(re.findall(r'href="(#[^"]+)"', home)))
    t985 = "t985" in home or "t-search" in home
    print("home", st, "popup/anchor hrefs:", hrefs[:40], "search block:", t985)
    m = re.search(r'id="rec172603117"(.{0,6000})', home, re.S)
    res["_home"] = {"anchors": hrefs, "search": t985, "t228": m.group(1)[:6000] if m else ""}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
