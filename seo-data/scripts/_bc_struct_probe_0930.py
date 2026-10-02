# -*- coding: utf-8 -*-
"""Крошки на живом alsn.ru по страницам карты структуры (30.09.2026): видимый T123, старый T758, BreadcrumbList в HEAD."""
import html as H
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import build_struktura_karta_0930 as K

OUT = Path(__file__).with_name("_bc-struct-2026-09-30.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def get(url):
    err = None
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(1.5)
    return 0, str(err)


def txt(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def rec_of(page, pos):
    starts = [m for m in re.finditer(r'<div id="rec(\d+)"[^>]*>', page[:pos])]
    if not starts:
        return None, ""
    m = starts[-1]
    return m.group(1), m.group(0)


def probe(path):
    st, page = get(f"https://alsn.ru{path}?bc=3009")
    row = {"path": path, "status": st}
    if st != 200:
        return row
    head = page[: page.find("</head>")]
    body = page[page.find("</head>"):]
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    row["h1"] = txt(h1.group(1))[:120] if h1 else ""
    navs = []
    for m in re.finditer(r'<nav[^>]*aria-label="Хлебные крошки"[^>]*>.*?</nav>', body, re.S):
        raw = m.group(0)
        rid, rtag = rec_of(body, m.start())
        bg = re.search(r"background-color:\s*(#[0-9a-fA-F]{3,6})", rtag)
        color = re.search(r"color:\s*(#[0-9a-fA-F]{3,6})", raw)
        parts = re.findall(r'<(a|span)\b([^>]*)>(.*?)</\1>', raw, re.S)
        links, names = [], []
        for tag, attrs, inner in parts:
            t = txt(inner)
            if not t or t == "/":
                continue
            href = re.search(r'href="([^"]+)"', attrs)
            names.append(t)
            links.append(href.group(1) if tag == "a" and href else None)
        navs.append({"rec": rid, "bg": bg.group(1) if bg else "", "color": color.group(1) if color else "",
                     "names": names, "links": links, "raw": raw})
    row["navs"] = navs
    t758 = []
    for m in re.finditer(r'<div id="rec(\d+)"[^>]*data-record-type="758"[^>]*>(.*?)(?=<div id="rec\d+")', body, re.S):
        t758.append({"rec": m.group(1), "text": txt(m.group(2))[:200]})
    row["t758"] = t758
    lds = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', head, re.S | re.I):
        raw = m.group(0)
        if "BreadcrumbList" not in raw:
            continue
        try:
            data = json.loads(m.group(1))
        except Exception:  # noqa: BLE001
            lds.append({"raw": raw, "bad": True})
            continue
        graph = isinstance(data, dict) and "@graph" in data
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for g in nodes:
            if isinstance(g, dict) and g.get("@type") == "BreadcrumbList":
                lds.append({"raw": raw, "graph": graph, "id": g.get("@id", ""),
                            "items": [(it.get("name"), it.get("item")) for it in g.get("itemListElement") or []]})
    row["lds"] = lds
    first = re.search(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body)
    return row


def paths():
    ps = [r[2] for r in K.SCHEMA if r[2] and r[2].startswith("/") and "…" not in r[2]]
    ps += [p for p, _, _ in K.OUTSIDE]
    ps += list(K.HAVE_SUP.values())
    out = []
    for p in ps:
        if p not in out:
            out.append(p)
    return out


def main():
    ps = paths()
    with ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(probe, ps))
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in rows:
        if r["status"] != 200:
            print(r["status"], r["path"])
            continue
        vis = " | ".join(" / ".join(n["names"]) + f" [bg {n['bg']}]" for n in r["navs"]) or "-"
        ld = " | ".join(" / ".join(str(a) for a, _ in l.get("items", [])) + (" (graph)" if l.get("graph") else "") for l in r["lds"]) or "-"
        old = "T758" if r["t758"] else ""
        print(f"{r['path']:<48} vis: {vis:<70} ld: {ld} {old}")
    print(OUT)


if __name__ == "__main__":
    main()
