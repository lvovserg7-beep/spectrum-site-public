# -*- coding: utf-8 -*-
import re
import urllib.request
from pathlib import Path

urls = [
    "https://rarus.ru/1c8/1c8-lic5-elektronnaya-postavka/",
    "https://rarus.ru/1c8/1c8-lic5/",
    "https://rarus.ru/1c8/1c8-lic/",
    "https://axioma-soft.ru/products/klientskie-litsenzii-1s/1s-predpriyatie-8-klientskaya-litsenziya-na-1-r-m/",
    "https://axioma-soft.ru/products/klientskie-litsenzii-1s/1s-predpriyatie-8-korp-klientskaya-litsenziya-na-5-r-m/",
    "https://axioma-soft.ru/products/litsenzii-1s/",
    "https://stupino.1cbit.ru/1csoft/litsenzii-1s-predpriyatie/",
    "https://moscow.1cbit.ru/1csoft/litsenzii-1s-predpriyatie/",
    "https://www.1cbit.ru/1csoft/litsenzii-1s-predpriyatie/",
    "https://novoros.1cbit.ru/1csoft/1s-predpriyatie-8-komplekt-prikladnykh-resheniy-na-5-328/",
    "https://orenburg.1cbit.ru/1csoft/1s-bukhgalteriya-8-red-3-0/",
]

hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
out = []
sku_re = re.compile(r"арт\.?|артикул|4601546\d+|290000\d+", re.I)

for u in urls:
    req = urllib.request.Request(u, headers=hdr)
    try:
        html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    except Exception as e:
        out.append(f"ERR {u}\n{e}\n")
        continue
    title_m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    desc_m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']',
        html,
        re.I | re.S,
    )
    if not desc_m:
        desc_m = re.search(
            r'<meta[^>]+content=["\'](.*?)["\'][^>]*name=["\']description["\']',
            html,
            re.I | re.S,
        )
    t = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
    d = re.sub(r"\s+", " ", desc_m.group(1)).strip() if desc_m else ""
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    h1 = re.sub(r"<[^>]+>", " ", h1_m.group(1) if h1_m else "")
    h1 = re.sub(r"\s+", " ", h1).strip()
    out.append(u)
    out.append("TITLE: " + t)
    out.append("H1: " + h1[:200])
    out.append("DESC: " + d[:240])
    out.append("SKU in title: " + str(bool(sku_re.search(t))))
    out.append("SKU in h1: " + str(bool(sku_re.search(h1))))
    out.append("SKU in desc: " + str(bool(sku_re.search(d))))
    out.append("---")

Path(__file__).with_name("_comp_titles.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote", len(out))
