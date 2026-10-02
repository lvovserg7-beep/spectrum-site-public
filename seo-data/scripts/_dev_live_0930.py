# -*- coding: utf-8 -*-
"""Разбор живой alsn.ru/development1c для инструкции v3."""
import html
import json
import re
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
here = Path(__file__).with_name("_dev_live_0930.html")
if here.exists() and here.stat().st_size > 10000:
    h = here.read_text(encoding="utf-8")
else:
    url = "https://alsn.ru/development1c?c=v3vn0930"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://alsn.ru/"})
    h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    here.write_text(h, encoding="utf-8")

head = h[: h.index("</head>")]
rep = []


def out(*a):
    rep.append(" ".join(str(x) for x in a))


out("TITLE", re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip())
dm = re.search(r'<meta name="description" content="([^"]*)"', head)
out("DESC", dm.group(1) if dm else "NONE")
ogt = re.search(r'<meta property="og:title" content="([^"]*)"', head)
ogd = re.search(r'<meta property="og:description" content="([^"]*)"', head)
out("OG TITLE", ogt.group(1) if ogt else "NONE")
out("OG DESC", ogd.group(1) if ogd else "NONE")
out("robots", re.findall(r'<meta name="robots"[^>]*>', head))
out("style in head", head.count("<style"))
out("== LD")
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
    try:
        d = json.loads(m.group(1))
        out(" ", d.get("@type"), d.get("name") or d.get("@id") or "")
        if d.get("@type") == "FAQPage":
            out("   FAQ", [x["name"] for x in d.get("mainEntity", [])])
        if d.get("@type") == "HowTo":
            out("   steps", [s.get("name") for s in d.get("step", [])])
            for s in d.get("step", []):
                out("    *", s.get("name"), "|", (s.get("text") or "")[:120])
        if d.get("@type") == "BreadcrumbList":
            out("   items", [(x.get("name"), x.get("item")) for x in d.get("itemListElement", [])])
        if d.get("@type") in ("WebPage", "Service"):
            out("   desc", (d.get("description") or "")[:180])
    except Exception as e:
        out("  bad", e)

out("H1", [re.sub(r"<[^>]+>", "", x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)])
out("H2", [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()[:90] for x in re.findall(r"<h2[^>]*>(.*?)</h2>", h, re.S)][:25])

body = h[h.index("<body") :]
recs = [
    (m.start(), m.group(1), m.group(2))
    for m in re.finditer(
        r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body
    )
]
out("== records", len(recs))
for i, (pos, rid, typ) in enumerate(recs):
    end = recs[i + 1][0] if i + 1 < len(recs) else len(body)
    chunk = body[pos:end]
    flags = []
    headchunk = chunk[:900]
    if "t-rec_hidden" in headchunk or 'style="display:none' in headchunk:
        flags.append("hidden")
    txt = re.sub(r"<(script|style).*?</\1>", " ", chunk, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    txt = re.sub(r"\s+", " ", txt).strip()
    out(f"{i+1:2d} rec{rid} T{typ} {' '.join(flags)} | {txt[:180]}")
out("== popups", sorted(set(re.findall(r"#popup:[\w-]+", h))))
Path(__file__).with_name("_dev_live_0930.txt").write_text("\n".join(rep), encoding="utf-8")
print("ok", len(rep), "lines")
