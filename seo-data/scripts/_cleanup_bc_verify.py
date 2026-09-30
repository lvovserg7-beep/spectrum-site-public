# -*- coding: utf-8 -*-
"""Сверка инструкций крошек и Alt с живым alsn.ru, 29.09.2026."""
import html as H
import json
import re
import sys
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _audit_breadcrumbs_all_0928 as bc  # noqa: E402
from _audit_alts_tail import IMG_RE, attrs, basename  # noqa: E402

D = Path(__file__).parent
BR = D.parent / "tilda-briefs"
OUT = D / "_cleanup_bc_verify.txt"
cache = {}


def page(path):
    if path not in cache:
        cache[path] = bc.get("https://alsn.ru" + ("" if path == "/" else path) + "?chk=2909bc")
    return cache[path]


def imgs(h):
    res = []
    for m in IMG_RE.finditer(h):
        a = attrs(m.group(1))
        src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
        res.append((basename(src), (a.get("alt") or "").strip()))
    # Zero Block / bg images with data-original on div
    for m in re.finditer(r'<div\b([^>]*data-original="[^"]+"[^>]*)>', h):
        a = attrs(m.group(1))
        res.append((basename(a.get("data-original", "")), "(bg)"))
    return res


lines = []
P = lines.append

# 1. HEAD checks
P("== HEAD")
h = page("/cases"); P("cases caseecom#breadcrumb: %s" % ("caseecom#breadcrumb" in h))
h = page("/vesii"); P("vesii caseecomsc url in ld: %s" % bool(re.search(r'"url":\s*"https://alsn.ru/caseecomsc"', h)))
h = page("/1_obschepit_fastfood"); P("fastfood alsn-bc-jsonld: %s ; tproduct test: %s" % ("alsn-bc-jsonld" in h, "tproduct" in h[:h.find("</head>")]))
h = page("/dopolnitelnie_licenzii"); P("licenzii alsn-bc-jsonld: %s" % ("alsn-bc-jsonld" in h))
nav = re.search(r'<nav aria-label="Хлебные крошки"[^>]*>', h); P("licenzii nav: %s ; arrow→ in nav area: %s" % (nav.group(0)[:200] if nav else None, "→</span>" in h))
for p in ["/persons", "/publication", "/blog", "/cracasesoftvideo", "/persons/interw_lvov"]:
    h = page(p)
    ids = re.findall(r'"@id":\s*"(https://alsn.ru[^"]*#breadcrumb)"', h)
    P("%s breadcrumb ids: %s" % (p, ids))

# 2. alts-sitewide-21 wave 3
raw = (BR / "tier2-alts-sitewide-2026-09-21.html").read_text(encoding="utf-8")
items = re.findall(r'<strong>(\d+)\.</strong> страница «(.*?)» \((https://alsn\.ru[^)]*)\)[^<]*?файл в кабинете: ([^<]+?)</p>\s*<span class="lbl">Вставить в Alt</span>\s*<div class="copybox"><pre id="([^"]+)">([^<]*)</pre>', raw)
P("== WAVE3 items %d" % len(items))
paths = sorted({re.sub(r"https://alsn\.ru", "", u) or "/" for _, _, u, _, _, _ in items})
with ThreadPoolExecutor(6) as ex:
    list(ex.map(page, paths))
w3 = Counter()
for n, name, url, fn, pid, alt in items:
    path = re.sub(r"https://alsn\.ru", "", url) or "/"
    found = [a for f, a in imgs(page(path)) if f == fn.strip()]
    if not found:
        st = "ABSENT"
    elif any(a == "" for a in found):
        st = "EMPTY"
    else:
        st = "FILLED"
    w3[st] += 1
    P("%s | %s | %s | %s | %s | live=%s" % (n, st, path, fn, H.unescape(alt), found[:4]))
P("wave3 %s" % dict(w3))

# 3. wave 2 shared files across all pages
shared = re.findall(r'<h3>\d+\. Файл <code>([^<]+)</code></h3>', raw.split('id="wave-shared"')[1].split('id="wave-pages"')[0])
rows = json.loads((D / "_tiers_live_0929.json").read_text(encoding="utf-8"))
allp = [r["path"] for r in rows]
with ThreadPoolExecutor(6) as ex:
    list(ex.map(page, allp))
P("== WAVE2 shared %d" % len(shared))
for fn in shared:
    emp = [p for p in allp if any(f == fn and a == "" for f, a in imgs(page(p)))]
    fil = [p for p in allp if any(f == fn and a not in ("", "(bg)") for f, a in imgs(page(p)))]
    P("%s | empty on %d pages | filled on %d | ex empty %s" % (fn, len(emp), len(fil), emp[:4]))

# 4. alt tails: 3 pages, all empty non-svg images
P("== TAIL pages")
for p in ["/caseecomsc", "/xitsadmarketplace", "/clients"]:
    emp = [f for f, a in imgs(page(p)) if a == "" and f and not f.endswith(".svg")]
    P("%s empty %d: %s" % (p, len(emp), Counter(emp)))
for fname in ["tier2-alts-tail-2026-09-23.html", "tier2-alts-tail-2026-09-28.html"]:
    t = (BR / fname).read_text(encoding="utf-8")
    for sec in re.split(r'<section class="task" id="p-\d+">', t)[1:]:
        title = re.search(r"</span> ([^<]+)</h2>", sec).group(1)
        fns = re.findall(r"<h3>\d+\. Файл <code>([^<]+)</code></h3>", sec)
        P("%s | %s | %d | %s" % (fname, title, len(fns), Counter(fns)))

OUT.write_text("\n".join(lines), encoding="utf-8")
print("ok", len(lines))
