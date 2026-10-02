# -*- coding: utf-8 -*-
"""1С:КП (С-5) и имя витрины в крошках карточек «Программы 1С» (С-7)."""
import random
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def get(url):
    for _ in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(4)
    return ""


its = get(f"https://alsn.ru/its?v={random.randint(1, 10**6)}")
head, body = its[:its.find("</head>")], its[its.find("</head>"):]
last = head[head.rfind("<!-- nominify begin -->"):]
print("its HEAD страницы:", re.findall(r'"@type":\s*"(WebPage|BreadcrumbList)"', last),
      "| холст:", re.findall(r'"@type":\s*"(WebPage|BreadcrumbList)"', body))

store = re.findall(r"<loc>(.*?)</loc>", get("https://alsn.ru/sitemap-store.xml"))
card = next(u for u in store if "alsn.ru/products/tproduct/" in u)
page = get(card)
print("карточка:", card)
for m in re.finditer(r'(breadcrumb|t-store__prod-popup__breadcrumbs|js-store-breadcrumbs)[^>]*>', page):
    print("  ", page[m.start() - 40:m.end() + 300].replace("\n", " ")[:400])
    break
for key in ("Продукты", "Программы 1С"):
    print(f"  «{key}» в коде карточки:", page.count(key))
m = re.search(r'"breadcrumbs"\s*:\s*"([^"]*)"', page) or re.search(r'breadcrumbs[^{]{0,40}\{[^}]{0,400}', page)
print("  настройка крошек витрины:", m.group(0)[:400] if m else "не найдено")
