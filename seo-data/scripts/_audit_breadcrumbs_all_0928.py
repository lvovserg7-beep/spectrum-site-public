# -*- coding: utf-8 -*-
"""Breadcrumbs audit for every URL in alsn.ru sitemaps (pages + tproduct)."""
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _audit_breadcrumbs_live_0928 as base  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
OUT = Path(__file__).with_name("_bc-all-2026-09-28.json")


def get(url):
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
        except Exception as e:
            err = e
            time.sleep(1.5)
    raise err


def sitemap_urls():
    urls = []
    for sm in ["https://alsn.ru/sitemap.xml", "https://alsn.ru/sitemap-store.xml"]:
        try:
            t = get(sm)
        except Exception as e:
            print("sitemap fail", sm, e)
            continue
        locs = re.findall(r"<loc>(.*?)</loc>", t)
        subs = [x for x in locs if x.endswith(".xml")]
        urls += [x for x in locs if not x.endswith(".xml")]
        for s in subs:
            if "feeds" in s:
                continue
            urls += re.findall(r"<loc>(.*?)</loc>", get(s))
    seen, out = set(), []
    for u in urls:
        u = u.strip()
        if u.startswith("https://alsn.ru") and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def audit_page(url):
    path = url.replace("https://alsn.ru", "") or "/"
    base.fetch = lambda p: get("https://alsn.ru" + ("" if p == "/" else p) + "?bca=2809")
    row = base.audit_one(path)
    html = get("https://alsn.ru" + ("" if path == "/" else path) + "?bca=2809")
    items = []
    for block in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        body = block.group(1).strip()
        if "BreadcrumbList" not in body:
            continue
        try:
            data = json.loads(body)
        except Exception:
            continue
        graphs = data.get("@graph", [data]) if isinstance(data, dict) else data
        for g in graphs if isinstance(graphs, list) else [graphs]:
            if isinstance(g, dict) and g.get("@type") == "BreadcrumbList":
                items.append([(it.get("name"), it.get("item")) for it in g.get("itemListElement") or []])
    row["lists"] = items
    row["n_lists"] = len(items)
    last_urls = [lst[-1][1] for lst in items if lst]
    row["last_url_ok"] = all((u or "").rstrip("/") == url.rstrip("/") for u in last_urls) if last_urls else None
    row["visible_blocks"] = len(re.findall(r'aria-label=["\']Хлебные крошки["\']', html))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    row["h1"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h1.group(1))).strip()[:90] if h1 else ""
    row["kind"] = "page"
    return row


def audit_product(url):
    html = get(url + ("&" if "?" in url else "?") + "bca=2809")
    head = html[: html.find("</head>")]
    has_st340 = bool(re.search(r"t-store__prod-popup__brdcrmbs|t-store__breadcrumbs|js-store-breadcrumbs|brdcrmbs", html))
    has_script = "tproduct" in head and "BreadcrumbList" in head
    sku = re.search(r'itemprop="sku"[^>]*content="([^"]+)"|itemprop="sku"[^>]*>([^<]+)<', html)
    name = re.search(r'itemprop="name"[^>]*content="([^"]+)"', html) or re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    return {
        "path": url.replace("https://alsn.ru", ""),
        "kind": "tproduct",
        "st340_markup": has_st340,
        "head_script": has_script,
        "sku": (sku.group(1) or sku.group(2)).strip() if sku else "",
        "name": re.sub(r"<[^>]+>", "", name.group(1)).strip()[:80] if name else "",
    }


def run(url):
    try:
        return audit_product(url) if "/tproduct/" in url else audit_page(url)
    except Exception as e:
        return {"path": url.replace("https://alsn.ru", ""), "kind": "err", "err": str(e)}


def main():
    urls = sitemap_urls()
    print("urls", len(urls), "tproduct", sum("/tproduct/" in u for u in urls), "tpost", sum("/tpost/" in u for u in urls))
    with ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(run, urls))
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    pages = [r for r in rows if r["kind"] == "page"]
    print("pages style", Counter(r["style"] for r in pages))
    print("tproduct", Counter((r["st340_markup"], r["head_script"]) for r in rows if r["kind"] == "tproduct"))
    print("errors", [(r["path"], r["err"]) for r in rows if r["kind"] == "err"])
    print("--- problem pages")
    for r in pages:
        bad = []
        if r["style"] != "CANON":
            bad.append(r["style"])
        if r["style"] == "CANON" and not r["name_match"]:
            bad.append("name_mismatch")
        if r["n_lists"] == 0 and r["style"] != "NONE":
            bad.append("no_LD")
        if r["n_lists"] > 1:
            bad.append(f"LD_x{r['n_lists']}")
        if not r["bc_ok"]:
            bad.append("INVALID_JSON")
        if r["last_url_ok"] is False:
            bad.append("LD_url_mismatch")
        if r["visible_blocks"] > 1:
            bad.append(f"visible_x{r['visible_blocks']}")
        if bad:
            print(f"{r['path']:<60} {','.join(bad):<40} vis='{r['last_vis']}' ld='{r['last_ld']}' h1='{r['h1'][:50]}'")


if __name__ == "__main__":
    main()
