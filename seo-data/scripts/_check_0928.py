# -*- coding: utf-8 -*-
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _audit_breadcrumbs_live_0928 import URLS  # noqa: E402

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
SKIP = re.compile(
    r"(?i)(\.svg|Tilda_Icons|/resize/20x/|/libtilda|favicon|sprite|1x1|blank|spacer|/empty/)"
)


def fetch(path):
    url = "https://alsn.ru" + ("" if path == "/" else path) + "?c=2809b"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


out = {}
for p in URLS:
    try:
        h = fetch(p)
    except Exception as e:
        out[p] = {"err": str(e)}
        continue
    empty = []
    for m in re.finditer(r"<img\b[^>]*>", h, re.I):
        tag = m.group(0)
        src = re.search(r'''(?:data-original|data-src|src)=["']([^"']+)["']''', tag)
        src = src.group(1) if src else ""
        if not src or SKIP.search(src) or "mc.yandex" in src:
            continue
        alt = re.search(r'''\balt=(["'])(.*?)\1''', tag, re.S)
        if alt is None or not alt.group(2).strip():
            empty.append(src.rsplit("/", 1)[-1])
    # zero-block bg images / t-bgimg are not <img>; ignore
    info = {"empty_alt": len(empty), "files": sorted(set(empty))}
    if p in ("/cases", "/persons", "/dopolnitelnie_licenzii", "/publication", "/blog"):
        lds = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I)
        info["ld_types"] = [re.findall(r'"@type"\s*:\s*"([^"]+)"', x)[:3] for x in lds]
        vis = re.search(r'aria-label="Хлебные крошки"(.{0,1500})', h, re.S)
        info["crumb_text"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", vis.group(1)))[:200] if vis else ""
        info["crumb_blocks"] = len(re.findall(r'aria-label="Хлебные крошки"', h))
        sc = [m.start() for m in re.finditer(r"ООО «СЦ»", h)]
        info["sc_mentions"] = len(sc)
        if sc:
            s = sc[0]
            info["sc_ctx"] = re.sub(r"\s+", " ", h[max(0, s - 700): s + 100])[:800]
    out[p] = info

Path(__file__).with_name("_check-0928.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
tot = 0
for p, i in out.items():
    if i.get("err"):
        print("ERR", p, i["err"])
        continue
    tot += i["empty_alt"]
    if i["empty_alt"]:
        print(f"{p}: empty_alt={i['empty_alt']} {i['files'][:12]}")
print("TOTAL empty alt", tot)
