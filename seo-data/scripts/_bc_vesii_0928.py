# -*- coding: utf-8 -*-
import json
import re
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
h = urllib.request.urlopen(urllib.request.Request("https://alsn.ru/vesii?v=1", headers=UA), timeout=40).read().decode("utf-8")
head_end = h.find("</head>")
for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I):
    body = m.group(1).strip()
    if "BreadcrumbList" not in body:
        continue
    where = "HEAD" if m.start() < head_end else "BODY"
    rec = re.findall(r'id="rec(\d+)"', h[: m.start()])
    print(where, "rec", rec[-1] if (where == "BODY" and rec) else "-", "len", len(body))
    try:
        json.loads(body)
        print("valid")
    except Exception as e:
        print("ERROR", e)
        pos = getattr(e, "pos", 0)
        print(repr(body[max(0, pos - 200): pos + 80]))
    names = re.findall(r'"name"\s*:\s*"([^"]+)"', body)
    print("names", names[:8])
