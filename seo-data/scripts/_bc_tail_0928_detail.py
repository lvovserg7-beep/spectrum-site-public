# -*- coding: utf-8 -*-
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"


def fetch(p):
    req = urllib.request.Request("https://alsn.ru" + p + "?d=2809c", headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


for p in ["/cases", "/dopolnitelnie_licenzii", "/persons", "/publication", "/blog"]:
    h = fetch(p)
    head_end = h.find("</head>")
    print("=====", p)
    print(" title:", text(re.search(r"<title>(.*?)</title>", h, re.S).group(1)))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    print(" h1:", text(h1.group(1))[:120] if h1 else None)
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        where = "HEAD" if m.start() < head_end else "BODY"
        rec = re.findall(r'id="rec(\d+)"', h[: m.start()])
        body = re.sub(r"\s+", " ", m.group(1))
        ids = re.findall(r'"@id"\s*:\s*"([^"]+)"', body)[:3]
        types = re.findall(r'"@type"\s*:\s*"([^"]+)"', body)[:2]
        print(f"  LD {where} rec={rec[-1] if (where=='BODY' and rec) else '-'} types={types} ids={ids}")
    nav = re.search(r'aria-label="Хлебные крошки"', h)
    if nav:
        rec = re.findall(r'id="rec(\d+)"', h[: nav.start()])
        print("  crumbs in rec", rec[-1] if rec else "?", "| text:", text(h[nav.start(): nav.start() + 1500])[:120])
    # first 4 blocks of the page body
    blocks = list(re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"([^>]*)>', h))
    for b in blocks[:4]:
        attrs = b.group(2)
        typ = re.search(r'data-record-type="(\d+)"', attrs)
        bg = re.search(r"background-color:\s*([^;\"']+)", attrs)
        chunk = h[b.end(): b.end() + 6000]
        img = re.search(r"""data-original=["']([^"']+)["']""", chunk)
        cover = "t-cover" in chunk[:3000] or "t-bgimg" in chunk[:3000]
        artbg = re.search(r"t396__artboard\{[^}]*background-color:\s*([^;]+)", h[b.start(): b.start() + 20000])
        first_text = text(chunk)[:90]
        print(f"   block rec{b.group(1)} T{typ.group(1) if typ else '?'} bg={bg.group(1) if bg else '-'} artboard_bg={artbg.group(1) if artbg else '-'} cover={cover} img={img.group(1).rsplit('/',1)[-1] if img else '-'} | {first_text}")
