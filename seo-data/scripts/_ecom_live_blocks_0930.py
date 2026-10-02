"""Разбор живой alsn.ru/ecom: блоки холста, HEAD страницы, попапы. Для инструкции переноса v3."""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
url = sys.argv[1] if len(sys.argv) > 1 else "https://alsn.ru/ecom"
h = urllib.request.urlopen(urllib.request.Request(url + "?c=ecomv3", headers={"User-Agent": UA})).read().decode("utf-8")
Path(__file__).with_name("_ecom_live_0930.html").write_text(h, encoding="utf-8")

head = h[:h.index("</head>")]
print("== LD in head")
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
    try:
        d = json.loads(m.group(1))
        print(" ", d.get("@type"), d.get("name") or d.get("@id") or "", len(d.get("mainEntity", [])) if isinstance(d.get("mainEntity"), list) else "")
    except Exception as e:
        print("  bad json", e)
print("robots:", re.findall(r'<meta name="robots"[^>]*>', head))
print("desc:", re.findall(r'<meta name="description" content="([^"]*)"', head))
print("style tags in head:", head.count("<style"))

body = h[h.index("<body"):]
recs = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body)]
print("== records", len(recs))
for i, (pos, rid, typ) in enumerate(recs):
    end = recs[i + 1][0] if i + 1 < len(recs) else len(body)
    chunk = body[pos:end]
    off = 't-rec_pc_hide' in chunk[:400] or 'data-record-type' in chunk[:0]
    txt = re.sub(r"<(script|style).*?</\1>", " ", chunk, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    txt = re.sub(r"\s+", " ", txt).strip()
    print(f"{i+1:2d} rec{rid} T{typ} | {txt[:130]}")
print("== popups", sorted(set(re.findall(r'#popup:[\w-]+', h))))
print("== order hooks", sorted(set(re.findall(r'#order[\w:-]*', h)))[:10])
