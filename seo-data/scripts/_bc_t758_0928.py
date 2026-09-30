# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
rows = json.loads(Path(__file__).with_name("_bc-all-2026-09-28.json").read_text(encoding="utf-8"))
pages = [r["path"] for r in rows if r["kind"] == "page"]


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def one(p):
    try:
        h = urllib.request.urlopen(urllib.request.Request("https://alsn.ru" + p + "?t=2809", headers=UA), timeout=40).read().decode("utf-8", "replace")
    except Exception as e:
        return p, {"err": str(e)}
    res = []
    blocks = list(re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', h))
    for i, b in enumerate(blocks):
        if b.group(2) != "758":
            continue
        e = blocks[i + 1].start() if i + 1 < len(blocks) else b.end() + 8000
        chunk = h[b.start(): e]
        links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', chunk, re.S)
        res.append({"rec": b.group(1), "pos": i, "text": text(re.sub(r"<style.*?</style>|<script.*?</script>", " ", chunk, flags=re.S))[:140],
                    "links": [(u, text(t)) for u, t in links][:5]})
    t123 = "Хлебные крошки" in h
    return p, {"t758": res, "t123": t123}


with ThreadPoolExecutor(max_workers=6) as ex:
    out = dict(ex.map(one, pages))
Path(__file__).with_name("_bc-t758-2026-09-28.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
both = [p for p, v in out.items() if v.get("t758") and v.get("t123")]
only = [p for p, v in out.items() if v.get("t758") and not v.get("t123")]
print("T758 + T123 (double):", len(both))
for p in both:
    print("  ", p, out[p]["t758"][0]["rec"], out[p]["t758"][0]["text"][:90], out[p]["t758"][0]["links"][:3])
print("T758 only:", len(only))
for p in only:
    print("  ", p, out[p]["t758"][0]["rec"], out[p]["t758"][0]["text"][:90], out[p]["t758"][0]["links"][:3])
print("errors", [p for p, v in out.items() if v.get("err")])
