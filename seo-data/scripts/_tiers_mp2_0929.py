# -*- coding: utf-8 -*-
import re
from _tiers_mp_0929 import get, txt


def ctx(t, k, w=90):
    for m in re.finditer(re.escape(k), t):
        print(f"    [{k}] ...{t[max(0, m.start() - w): m.end() + w]}...")


ctx(txt(get("https://alsn.ru/1c-wildberries?c=1")), "rFBS")
ctx(txt(get("https://alsn.ru/1c-ozon?c=1")), "Цены с НДС")
ctx(txt(get("https://alsn.ru/casemarketplace?c=1")), "со скидкой")
h = get("https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz?c=1")
print("card old price:", re.findall(r'priceold[^>]*>([^<]*)<', h)[:5], "| 79 000 in html:", "79 000" in h or "79000" in h)
