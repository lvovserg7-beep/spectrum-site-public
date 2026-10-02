# -*- coding: utf-8 -*-
"""Подтвердить: первый кусок nominify = HEAD сайта (одинаковый везде), второй = HEAD страницы (копируется на карточки)."""
import random
import re
import time
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
DIR = Path(__file__).parent / "_sc_pages_0930"


def get(url):
    for _ in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(4)
    return ""


def pieces(page):
    head = page[:page.find("</head>")]
    return [head[m.end():head.find("<!-- nominify end -->", m.end())] for m in re.finditer(r"<!-- nominify begin -->", head)], \
        'data-tilda-page-headcode="yes"' in page


upt8 = (DIR / "upt8.html").read_text(encoding="utf-8")
p_upt8, _ = pieces(upt8)
for url in ["https://alsn.ru/about_us", "https://alsn.ru/contacts", "https://alsn.ru/cases"]:
    p, has = pieces(get(f"{url}?v={random.randint(1, 10**6)}"))
    print(url, "HEAD страницы есть:", has, "| кусков:", len(p), "| первый = первый у upt8:", bool(p) and p[0] == p_upt8[0])
    time.sleep(2)

card = re.search(r'href="(https://alsn\.ru/upt8/tproduct/[^"]+)"', upt8)
if card:
    p, has = pieces(get(card.group(1)))
    print("карточка", card.group(1), "| кусков:", len(p), "| второй = HEAD страницы upt8:", len(p) > 1 and p[1] == p_upt8[1])
