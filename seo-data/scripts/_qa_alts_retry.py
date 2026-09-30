# -*- coding: utf-8 -*-
"""Retry leftover cards that failed with SSL."""
import html as htmlmod
import json
import re
import ssl
import urllib.request
from pathlib import Path

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
GALLERY_RE = re.compile(r'"gallery"\s*:\s*(\[.*?\])\s*,\s*"sort"', re.S)
CTX = ssl.create_default_context()

URLS = [
    (
        "2900001833554",
        "1С:Предприятие 8 ПРОФ Клиентская лицензия на 50 рабочих мест, эл. поставка",
        "https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-159637201592-1s-predpriyatie-8-prof-klientskaya-litse",
    ),
    (
        "фастфуд коробка",
        "1С:Фастфуд и Ресторан. Клиентские лицензии на рабочие места, коробка",
        "https://alsn.ru/1_obschepit_fastfood/tproduct/419928619-845146210291-1sfastfud-i-restoran-klientskie-litsenzi",
    ),
    (
        "2900001850223",
        "1С:ЗУП Зарплата и Управление Персоналом 8 ПРОФ, эл. поставка",
        "https://alsn.ru/zup8/tproduct/382489805-684572207481-1s-zup-zarplata-i-upravlenie-personalom",
    ),
    (
        "4601546091970",
        "1С:Бухгалтерия 8 КОРП, коробка",
        "https://alsn.ru/buhv8/tproduct/379482785-472094879401-1sbuhgalteriya-8-korp-korobochnaya-posta",
    ),
    (
        "4601546081506",
        "1С:Зарплата и Управление Персоналом 8 КОРП, коробка",
        "https://alsn.ru/zup8/tproduct/382489805-323583267611-1szarplata-i-upravlenie-personalom-8-kor",
    ),
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        return r.read().decode("utf-8", "replace")


def gallery_alt(page: str) -> str:
    m = GALLERY_RE.search(page)
    if not m:
        return ""
    arr = json.loads(m.group(1))
    if not arr:
        return ""
    return htmlmod.unescape((arr[0].get("alt") or "").strip())


out = Path(__file__).with_name("_qa_alts_retry.txt")
lines = []
for sku, exp, url in URLS:
    try:
        live = gallery_alt(fetch(url))
        st = "ok" if live == exp else ("empty" if not live else "mismatch")
        lines.append(f"{st}\t{sku}")
        lines.append(f"  ждали: {exp}")
        lines.append(f"  сейчас: {live}")
        lines.append(f"  {url}")
        lines.append("")
    except Exception as e:
        lines.append(f"error\t{sku}\t{e}")
        lines.append(f"  {url}")
        lines.append("")

out.write_text("\n".join(lines), encoding="utf-8")
print(out.read_text(encoding="utf-8"))
