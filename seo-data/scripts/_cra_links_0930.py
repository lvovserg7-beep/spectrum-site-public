# -*- coding: utf-8 -*-
"""Где на живом alsn.ru упоминается ТОП 10 ЦРА и есть ли ссылка на /cra (по sitemap.xml)."""
import json
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
urls = json.load(open("_sitemap_0930.json", encoding="utf-8"))["urls"]


def get(u):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(3)
    return ""


for u in urls:
    if u.rstrip("/").endswith("/cra"):
        continue
    page = get(u)
    body = page[page.find("</head>"):]
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S)
    foot = body.find('id="t-footer"')
    body = body[:foot] if foot > 0 else body
    hits = [m.start() for m in re.finditer(r"ТОП[\s\u00a0-]*10[^<]{0,20}ЦРА|TOP[\s\u00a0-]*10[^<]{0,20}ЦРА|ЦРА", body)]
    if not hits:
        continue
    linked = 0
    for h in hits:
        a_open = body.rfind("<a ", 0, h)
        a_close = body.rfind("</a>", 0, h)
        if a_open > a_close and "cra" in body[a_open:body.find(">", a_open)]:
            linked += 1
    print(f"{u:<70} упоминаний {len(hits)}, со ссылкой на /cra {linked}")
    time.sleep(0.8)
