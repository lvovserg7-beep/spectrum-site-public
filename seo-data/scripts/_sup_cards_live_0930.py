"""Разбор 13 живых карточек поставщиков alsn.ru: title, description, H1, блоки холста, HEAD. Для инструкции v3."""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
SLUGS = ["merlion", "ocs", "treolan", "marvel", "digis", "elko", "3logic", "etm-ipro", "resurs-media", "auvix",
         "vtt", "dssl", "russkiy-svet"]
OUT = Path(__file__).with_name("_sup_cards_live_0930.json")


def txt(chunk):
    t = re.sub(r"<(script|style).*?</\1>", " ", chunk, flags=re.S)
    t = html.unescape(re.sub(r"<br\s*/?>", "\n", t))
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*", "\n", t)).strip()


res = {}
for s in SLUGS:
    h = urllib.request.urlopen(urllib.request.Request(f"https://alsn.ru/{s}?c=sup0930", headers={"User-Agent": UA})).read().decode("utf-8")
    head = h[:h.index("</head>")]
    lds = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
        try:
            d = json.loads(m.group(1))
            lds.append(d.get("@type"))
        except Exception:
            lds.append("bad")
    body = h[h.index("<body"):]
    recs = [(m.start(), m.group(1), m.group(2)) for m in
            re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body)]
    blocks = []
    for i, (pos, rid, typ) in enumerate(recs):
        end = recs[i + 1][0] if i + 1 < len(recs) else len(body)
        ch = body[pos:end]
        imgs = re.findall(r'(?:data-original|src)="(https://[^"]*tildacdn[^"]*)"', ch)
        blocks.append({"rec": rid, "type": typ, "text": txt(ch)[:3000], "imgs": sorted(set(imgs))[:6]})
    res[s] = {
        "title": html.unescape(re.search(r"<title>(.*?)</title>", head, re.S).group(1)),
        "desc": html.unescape((re.search(r'<meta name="description" content="([^"]*)"', head) or [None, ""])[1]),
        "h1": [txt(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.S)],
        "ld": lds, "styles_head": head.count("<style"),
        "robots": re.findall(r'<meta name="robots"[^>]*>', head),
        "pageid": (re.search(r'data-tilda-page-id="(\d+)"', h) or [None, ""])[1],
        "blocks": blocks,
    }
    print(s, res[s]["pageid"], len(blocks), res[s]["title"])
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
