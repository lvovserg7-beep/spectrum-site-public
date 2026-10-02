# -*- coding: utf-8 -*-
"""Проверка нового подвала (tier2-footer-v3-2026-09-30.html) на живом alsn.ru."""
import random
import re
import sys
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
CODE = open("../tilda-briefs/_footer-t123-2026-09-30.txt", encoding="utf-8").read()
OLD = ["984444341", "984550646", "1250142141", "984550511", "984444346", "1193054101", "1209876901", "1209811296"]
FORMS = ["855302703", "855355208", "855366805", "1086000871"]


def get(path):
    for _ in range(4):
        try:
            u = f"https://alsn.ru{path}?v={random.randint(1, 10**7)}"
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, ""
        except Exception:
            pass
        time.sleep(3)
    return 0, ""


def norm(s):
    return re.sub(r"\s+", "", s)


def check(path):
    st, page = get(path)
    print(f"##### {path}: {st}")
    if st != 200:
        return
    fi = page.find('id="t-footer"')
    body, foot = (page[:fi], page[fi:]) if fi > 0 else (page, "")
    robots = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]+)"', page)
    print("  robots:", robots.group(1) if robots else "-")
    for where, part in (("контент страницы", body), ("общий подвал", foot)):
        n = part.count('id="alsnMf"')
        if not n:
            continue
        m = re.search(r'<div id="rec(\d+)"[^>]*data-record-type="(\d+)"[^>]*>(?:(?!<div id="rec).)*?id="alsnMf"', part, re.S)
        rec = f"rec{m.group(1)} type {m.group(2)}" if m else "?"
        tag = re.search(rf'<div id="rec{m.group(1)}"[^>]*>', part).group(0) if m else ""
        pad = re.findall(r"padding-(?:top|bottom):(\d+)px", tag)
        bg = re.search(r"background-color:([^;\"]+)", tag)
        html_ok = norm(CODE.split("</style>", 1)[1].split("<script>")[0]) in norm(part)
        css_ok = norm(CODE.split("<style>", 1)[1].split("</style>")[0])[:3000] in norm(part)
        js_ok = "alsnMfLb" in part and "navigator.clipboard" in part
        print(f"  новый подвал: {where}, {rec}, раз: {n}, отступы {pad or '0'}, фон {bg.group(1).strip() if bg else 'пусто'}; "
              f"разметка как в коде: {html_ok}, стили: {css_ok}, скрипт: {js_ok}")
    if foot:
        on = [r for r in OLD if re.search(rf'<div id="rec{r}"', foot)]
        print("  старые блоки, ещё видны в подвале:", on or "нет")
        miss = [r for r in FORMS if not re.search(rf'<div id="rec{r}"', foot)]
        print("  формы T702:", "все 4 на месте" if not miss else f"НЕТ {miss}")
    for hook in ("#popup:konsultacia", "#opensearch"):
        print(f"  {hook}: ссылок {page.count(hook)}")
    imgs = re.findall(r'(https://(?:static|thb)\.tildacdn\.com/[^"\s)]+)', page[page.find('id="alsnMf"'):page.find('id="alsnMfLb"')] if 'id="alsnMf"' in page else "")
    print("  картинок в новом подвале:", len(set(imgs)))


for p in sys.argv[1:] or ["/test-footer", "/", "/1c-ozon"]:
    check(p)
