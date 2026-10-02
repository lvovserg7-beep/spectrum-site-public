# -*- coding: utf-8 -*-
"""Точечные проверки для отчёта по тирам 01.10.2026."""
import random
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def get(path):
    for _ in range(5):
        try:
            u = f"https://alsn.ru{path}?v={random.randint(1, 10**6)}"
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(4)
    return ""


home = get("/")
promo = re.search(r'<aside class="promo"><span class="k">Лицензии</span>.*?</aside>', home, re.S)
print("меню: шапка T123 rec4350962801:", "rec4350962801" in home, "| ЦРА ссылкой в промо:", bool(promo and 'href="/cra"' in promo.group(0)))
print("подвал T123 rec4363360101:", "rec4363360101" in home)
time.sleep(2)
for p in ["/development1c", "/erp-time-price", "/kompleksnaya_avtomatizaciya"]:
    s = get(p)
    print(p, "| H2 «Полезные страницы по внедрению 1С»:", "Полезные страницы по внедрению 1С" in s, "| v3:", ".v3 " in s[:s.find("</head>")])
    time.sleep(2)
for p in ["/ecom", "/casemarketplace", "/1c-ozon", "/1c-wildberries", "/support1c"]:
    s = get(p)
    head = s[:s.find("</head>")]
    print(p, "| v3:", ".v3 " in head, "| рамка .hf:", 'class="hf' in s, "| подпись под фото на телефоне:", "position:static" in head and ".who" in head)
    time.sleep(2)
its = get("/its")
last = its[:its.find("</head>")]
last = last[last.rfind("<!-- nominify begin -->"):]
print("/its путь в HEAD страницы:", "BreadcrumbList" in last)
