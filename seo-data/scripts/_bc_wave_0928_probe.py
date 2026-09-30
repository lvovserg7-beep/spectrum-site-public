# -*- coding: utf-8 -*-
"""Collect locations/backgrounds for breadcrumbs wave brief 28.09."""
import io
import json
import re
import urllib.request
from pathlib import Path

from PIL import Image

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
SKIP_TYPES = {"257", "985", "217", "270", "1093", "702", "390", "886"}
PAGES = [
    "/cracasesoftvideo", "/persons/interw_lvov", "/1c-ozon-old",
    "/vtt", "/dssl", "/elko", "/digis", "/auvix", "/resurs-media", "/russkiy-svet",
    "/perehod-s-ut-na-unf", "/perehod-s-dokumentooborota-2-1-na-3-0", "/perehod-s-ut-10-3",
    "/moy-sklad-perenos-v-1s", "/sinhronizaciya-bp-i-bp", "/sinhronizaciya-mezhdu-zup-i-zup",
    "/sinhronizaciya-mezhdu-ut-i-ut", "/perevystavlenie-uslug-posledney-mili-ozon-v-1s",
    "/1_obschepit_fastfood", "/merlion",
]


def get(url, binary=False):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
    return raw if binary else raw.decode("utf-8", "replace")


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def top_color(url):
    try:
        im = Image.open(io.BytesIO(get(url, True))).convert("RGB")
        w, h = im.size
        return "#%02x%02x%02x" % im.crop((0, 0, w, max(1, h // 20))).resize((1, 1)).getpixel((0, 0))
    except Exception as e:
        return f"err {e}"


out = {}
for p in PAGES:
    try:
        h = get("https://alsn.ru" + p + "?w=2809")
    except Exception as e:
        out[p] = {"err": str(e)}
        print("==", p, "ERR", e)
        continue
    head_end = h.find("</head>")
    info = {}
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    info["title"] = text(t.group(1)) if t else ""
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    info["h1"] = text(h1.group(1))[:140] if h1 else ""
    info["robots"] = re.findall(r'<meta name="robots" content="([^"]+)"', h)
    info["canonical"] = re.findall(r'<link rel="canonical" href="([^"]+)"', h)
    nav = re.search(r'<nav aria-label="Хлебные крошки".*?</nav>', h, re.S)
    if nav:
        rec = re.findall(r'id="rec(\d+)"', h[: nav.start()])
        info["nav_rec"] = rec[-1] if rec else ""
        info["nav_html"] = nav.group(0)
    lds = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
        body = m.group(1)
        where = "HEAD" if m.start() < head_end else "BODY"
        rec = re.findall(r'id="rec(\d+)"', h[: m.start()])
        lds.append({
            "where": where,
            "rec": rec[-1] if where == "BODY" and rec else "",
            "types": re.findall(r'"@type"\s*:\s*"([^"]+)"', body)[:3],
            "ids": re.findall(r'"@id"\s*:\s*"([^"]+)"', body)[:3],
            "is_bc": "BreadcrumbList" in body,
        })
    info["lds"] = lds
    if p == "/1_obschepit_fastfood":
        info["head_has_tproduct_script"] = "tproduct" in h[:head_end]
    blocks = list(re.finditer(r'<div id="rec(\d+)" class="r t-rec([^"]*)"([^>]*)>', h))
    first = []
    for b in blocks:
        typ = re.search(r'data-record-type="(\d+)"', b.group(3))
        typ = typ.group(1) if typ else "?"
        if typ in SKIP_TYPES:
            continue
        e = blocks[blocks.index(b) + 1].start() if blocks.index(b) + 1 < len(blocks) else b.end() + 20000
        chunk = h[b.start(): e]
        rid = b.group(1)
        bg = re.search(r"background-color:\s*([^;\"']+)", b.group(3))
        art = re.search(r"#rec%s \.t396__artboard\{[^}]*?background-color:\s*([^;}]+)" % rid, h)
        filt = re.search(r"t-cover__filter[^>]*style=\"([^\"]+)\"", chunk)
        bgimg = re.search(r"""(?:t-cover__carrier|t-bgimg|t396__carrier)[^>]*data-original=["']([^"']+)["']""", chunk)
        art_img = re.search(r"#rec%s \.t396__artboard\{[^}]*?background-image:\s*url\('?([^')]+)" % rid, h)
        img_url = (bgimg.group(1) if bgimg else (art_img.group(1) if art_img else ""))
        first.append({
            "rec": rid, "type": typ,
            "bg": bg.group(1).strip() if bg else "",
            "artboard_bg": art.group(1).strip() if art else "",
            "filter": filt.group(1)[:140] if filt else "",
            "bg_image": img_url.rsplit("/", 1)[-1] if img_url else "",
            "bg_image_top": top_color(img_url) if img_url else "",
            "text": text(re.sub(r"<style.*?</style>|<script.*?</script>", " ", chunk, flags=re.S))[:120],
        })
        if len(first) >= 2:
            break
    info["first_blocks"] = first
    out[p] = info
    print("==", p, "|", info["h1"][:70])
    print("   robots", info["robots"], "canon", info["canonical"])
    if nav:
        print("   nav rec", info["nav_rec"], text(info["nav_html"])[:80])
    for l in lds:
        print("   LD", l)
    for f in first:
        print("   BLOCK", {k: v for k, v in f.items() if v})

# universal showcase script from a working showcase HEAD
for sp in ["/dopolnitelnie_licenzii", "/its", "/1cfresh"]:
    h = get("https://alsn.ru" + sp + "?w=2809")
    head = h[: h.find("</head>")]
    for m in re.finditer(r"<script(?![^>]*ld\+json)[^>]*>(.*?)</script>", head, re.S):
        if "tproduct" in m.group(1) and "BreadcrumbList" in m.group(1):
            out["_showcase_script"] = {"from": sp, "code": m.group(0)}
            break
    if "_showcase_script" in out:
        break
print("showcase script from", out.get("_showcase_script", {}).get("from"), "len", len(out.get("_showcase_script", {}).get("code", "")))
Path(__file__).with_name("_bc-wave-probe-2026-09-28.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
