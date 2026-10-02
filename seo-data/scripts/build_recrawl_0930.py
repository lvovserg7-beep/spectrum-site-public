# -*- coding: utf-8 -*-
"""Список переобхода после правок 30.09.2026: шапка, подвал, первый экран модуля, крошки по новой структуре."""
import json
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parents[1] / "seo-data/tilda-briefs/recrawl-struktura-2026-09-30.txt"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
SITE = "https://alsn.ru"

HERO = ["/casemarketplace", "/1c-ozon", "/1c-wildberries"]
CRUMBS_DONE = ["/1_obschepit_fastfood", "/integrationsite", "/integraciya-1c-dlya-prodavcov-kompyuternoy-tehniki",
               "/perevystavlenie-uslug-posledney-mili-ozon-v-1s", "/dopolnitelnie_licenzii",
               "/upt8", "/buhv8", "/zup8", "/upravlenie_nashei_firmoi", "/products", "/1cfresh", "/dokumentooborot8"]
SC_DONE = ["/upt8", "/buhv8", "/zup8", "/upravlenie_nashei_firmoi", "/products", "/1cfresh", "/dokumentooborot8"]
SHOWCASES = ["/its"]
NOINDEX = ["/vacancy", "/whatsapp"]


def get(url):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            time.sleep(3)
    return ""


def path(u):
    return u.replace(SITE, "").rstrip("/") or "/"


site = [path(u) for u in json.load(open(HERE / "_sitemap_0930.json", encoding="utf-8"))["urls"]]
store = re.findall(r"<loc>(.*?)</loc>", get(f"{SITE}/sitemap-store.xml"))
def cards_of(sc):
    return sorted(u for u in store if any(f"alsn.ru{s}/tproduct/" in u for s in sc) and "?" not in u)


cards = cards_of(SHOWCASES)
cards_done = cards_of(SC_DONE)

first = HERO + CRUMBS_DONE
skip = set(first) | set(SHOWCASES) | set(NOINDEX)
rest = [p for p in site if p not in skip]
wave1 = first + rest + cards_done
wave2 = SHOWCASES

urls = list(dict.fromkeys(u if u.startswith("http") else SITE + u for u in wave1))
OUT.write_text("\n".join(urls) + "\n", encoding="utf-8")
print(OUT, len(urls), "URL; не вошли до С-5:", len(wave2) + len(cards))
