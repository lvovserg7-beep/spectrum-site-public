# -*- coding: utf-8 -*-
"""После С-5: HEAD страницы витрин и карточки товаров (одна на витрину) без путей и WebPage витрины."""
import random
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
SC = ["upt8", "buhv8", "zup8", "upravlenie_nashei_firmoi", "products", "its", "1cfresh", "dokumentooborot8"]


def get(url):
    for _ in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(4)
    return ""


def page_head(page):
    head = page[:page.find("</head>")]
    ms = list(re.finditer(r"<!-- nominify begin -->", head))
    if len(ms) < 2:
        return ""
    b = ms[-1].end()
    return head[b:head.find("<!-- nominify end -->", b)]


def types(s):
    return re.findall(r'"@type":\s*"(WebPage|BreadcrumbList)"', s)


store = re.findall(r"<loc>(.*?)</loc>", get("https://alsn.ru/sitemap-store.xml"))
for s in SC:
    page = get(f"https://alsn.ru/{s}?v={random.randint(1, 10**6)}")
    ph = page_head(page)
    body = page[page.find("</head>"):]
    robots = re.findall(r'<meta name="robots"[^>]*>', ph)
    card = next((u for u in store if f"alsn.ru/{s}/tproduct/" in u), "")
    cph = page_head(get(card)) if card else ""
    print(f"{s:<26} HEAD страницы: {types(ph) or 'без путей'} {robots} | холст: {types(body)} | карточка: "
          f"{(types(cph) or 'чисто') if card else 'нет в sitemap'}")
    time.sleep(2)
