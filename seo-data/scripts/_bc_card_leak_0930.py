# -*- coding: utf-8 -*-
"""Статичный путь витрины в HEAD карточек tproduct (HEAD витрины копируется на карточки)."""
import re
import time
import urllib.request

import _bc_struct_verify_0930 as V  # noqa: F401  (перепроверка страниц при импорте)

SHOW = ["upt8", "buhv8", "zup8", "upravlenie_nashei_firmoi", "products", "its", "1cfresh",
        "dokumentooborot8", "dopolnitelnie_licenzii"]

st, xml = V.get("https://alsn.ru/sitemap-store.xml")
cards = re.findall(r"<loc>(.*?)</loc>", xml)
for s in SHOW:
    c = next((u for u in cards if f"alsn.ru/{s}/tproduct/" in u), "")
    if not c:
        print(f"{s:<28} карточки в sitemap-store не нашлось")
        continue
    st, page = V.get(c)
    head = page[:page.find("</head>")]
    static = [l["items"] for l in V.lds(head)]
    print(f"{s:<28} {st} статичных путей в HEAD карточки: {len(static)} {static[:1]} {c}")
    time.sleep(1)
