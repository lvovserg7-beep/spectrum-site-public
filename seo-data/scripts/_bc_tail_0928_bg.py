# -*- coding: utf-8 -*-
import io
import re
import urllib.request

from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read()


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


TARGETS = {"/publication": "869365008", "/blog": "171128811", "/dopolnitelnie_licenzii": "3907172601"}
for p, rid in TARGETS.items():
    h = get("https://alsn.ru" + p + "?g=2809").decode("utf-8", "replace")
    blocks = [m for m in re.finditer(r'<div id="rec(\d+)" class="r t-rec', h)]
    ids = [m.group(1) for m in blocks]
    i = ids.index(rid)
    look = [rid] if p != "/dopolnitelnie_licenzii" else ids[i + 1: i + 2]
    print("=====", p, "check", look)
    for r in look:
        s = h.find(f'id="rec{r}"')
        e = h.find('<div id="rec', s + 10)
        chunk = h[s:e]
        typ = re.search(r'data-record-type="(\d+)"', chunk[:400])
        styles = re.findall(r"#rec%s[^{]*\{[^}]*\}" % r, h)
        filt = re.findall(r"t-cover__filter[^>]*style=\"([^\"]+)\"", chunk)
        bgc = re.findall(r"background-color:\s*([^;\"']+)", chunk[:3000])
        imgs = re.findall(r"""data-original=["']([^"']+)["']""", chunk)
        print(f"  rec{r} T{typ.group(1) if typ else '?'} bg={bgc[:3]} filter={filt[:1]} imgs={[x.rsplit('/',1)[-1] for x in imgs[:2]]}")
        print("   text:", text(chunk)[:160])
        for u in imgs[:1]:
            im = Image.open(io.BytesIO(get(u))).convert("RGB")
            w, hh = im.size
            strip = im.crop((0, 0, w, max(1, hh // 20))).resize((1, 1))
            mid = im.resize((1, 1))
            print(f"   image {w}x{hh} top-edge avg={'#%02x%02x%02x' % strip.getpixel((0, 0))} whole avg={'#%02x%02x%02x' % mid.getpixel((0, 0))}")
