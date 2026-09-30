# -*- coding: utf-8 -*-
import re
from _tiers_mp_0929 import get, txt

h = get("https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz?c=1607")
print("card Ozon+WB priceold:", re.findall(r'priceold[^>]*>([^<]*)<', h)[:5], "| 79 000:", "79 000" in h or "79000" in h)

for u in ("https://alsn.ru/development1c", "https://alsn.ru/erp-time-price", "https://alsn.ru/kompleksnaya_avtomatizaciya"):
    t = txt(get(u + "?c=1607"))
    print(u, "| H2 Полезные страницы:", "Полезные страницы по внедрению 1С" in t)

h = get("https://alsn.ru/vacancy?c=1607")
d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', h)
print("vacancy description:", d.group(1) if d else None)

for u in ("https://alsn.ru/cracasesoftvideo", "https://alsn.ru/persons/interw_lvov", "https://alsn.ru/1_obschepit_fastfood"):
    hh = get(u + "?c=1607")
    print(u, "| T758:", 'data-record-type="758"' in hh, "| breadcrumb LD:", "BreadcrumbList" in hh)
