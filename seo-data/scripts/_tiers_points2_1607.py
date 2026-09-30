# -*- coding: utf-8 -*-
import re
from _tiers_mp_0929 import get

h = get("https://alsn.ru/casemarketplace?c=16072")
for m in re.finditer("со скидкой", h):
    print("CASE ...", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h[max(0, m.start() - 300): m.end() + 150])), "...")
h = get("https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz?c=16072")
for m in re.finditer("79 ?000", h):
    print("CARD ...", re.sub(r"\s+", " ", h[max(0, m.start() - 200): m.end() + 80]), "...")
