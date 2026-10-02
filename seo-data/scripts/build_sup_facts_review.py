# -*- coding: utf-8 -*-
"""Таблица фактов о поставщиках для проверки перед текстами страниц.

Вход: seo-data/sup-facts/batch-*.json
Выход: seo-data/sup-facts/facts-review-2026-10-02.html
"""
import glob
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sup_cards_v3 as c  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FACT = os.path.join(HERE, "..", "sup-facts")
OUT = os.path.join(FACT, "facts-review-2026-10-02.html")

NOTES = {
    "it-proekt": "Возможное совпадение, не подтверждено: у дистрибьютора IT Partner (i-t-p.pro) есть открытая документация B2B API (каталог, цены, остатки, заказы). Название в таблице /ecom другое, поэтому в текст страницы это не берём.",
    "narmak": "Другой компании с таким именем в оборудовании не нашлось. Если в модуле подключён именно этот поставщик, на странице честно пишем про орехи и бакалею.",
    "dkc": "Нужно выбрать: производитель АО «ДКС» (dkc.ru, API для дистрибьюторов) или розничный магазин dkc.market (ИП).",
    "energon": "Взят energon.ru (аккумуляторы, есть страница обмена API/FTP). Тёзка energon.pro продаёт электронные компоненты.",
    "asbis": "ASBIS в России сменил название на «Астрониум». asbis.ru открывается пустым. Нужно подтвердить, с кем работает модуль.",
    "bion": "Похоже на торговую марку дистрибьютора NETLAB, а не на отдельную компанию.",
    "ak-systems": "Официальный сайт не открылся. Два кандидата в справочниках, фактов для текста нет.",
    "distribution-center": "Найденный сайт торгует мобильной электроникой. Есть тёзки в Казахстане и 3PL в Видном.",
    "tfn": "Взят tfnopt.ru: у него есть API и резерв, это совпадает с отметками таблицы. Тёзка tfn.ru продаёт погрузчики.",
    "kvk": "Взят КВК Трейд (картриджи). Рядом в таблице RM-Company, тоже расходники. Есть тёзка KVK-Cable.",
    "maksprofit": "Единственный найденный сайт продаёт измерительные приборы, не телеком.",
    "novye-tehnologii": "Взят nt-rt.ru (Казань). Компаний «Новые технологии» много.",
}


def clip(s, n=280):
    s = (s or "").replace("\u2014", "-").replace("\u2013", "-").strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def status(v):
    if v.get("confidence") == "low" or not v.get("about"):
        return "Проверить", "bad"
    if not v.get("api"):
        return "Без API на сайте", "warn"
    return "Можно в текст", "ok"


def main():
    facts = {}
    for f in glob.glob(os.path.join(FACT, "batch-*.json")):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            if not k.startswith("_"):
                facts[k] = v
    rows, n_bad, n_warn = [], 0, 0
    for s in c.ALL_SUP:
        v = facts[s["slug"]]
        st, cls = status(v)
        n_bad += cls == "bad"
        n_warn += cls == "warn"
        src = "".join(f'<a href="{html.escape(u)}">{html.escape(u.split("//", 1)[-1][:42])}</a>' for u in v.get("sources") or [])
        note = NOTES.get(s["slug"], "")
        rows.append(f"""<tr class="{cls}">
<td><b>{html.escape(s["name"])}</b><div class="m">{s["slug"]} · {c.data_short(s)}</div></td>
<td><span class="st {cls}">{st}</span></td>
<td>{('<a href="' + html.escape(v.get("site") or "") + '">' + html.escape((v.get("site") or "").split("//")[-1][:28]) + "</a>") if v.get("site") else "нет"}</td>
<td>{html.escape(clip(v.get("about"), 220))}{('<div class="note">' + html.escape(note) + "</div>") if note else ""}</td>
<td>{html.escape(", ".join(v.get("categories") or []) or "-")}</td>
<td>{html.escape(clip(v.get("b2b"), 180) or "-")}</td>
<td>{html.escape(clip(v.get("api"), 220) or "-")}</td>
<td class="src">{src or "-"}</td>
</tr>""")
    doc = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Факты о поставщиках на проверку - 02.10.2026</title>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body{{margin:0;font-family:Onest,Arial,sans-serif;background:#F7F8FA;color:#212121}}
.w{{max-width:1480px;margin:0 auto;padding:36px 22px 60px}}
h1{{font-size:32px;margin:0 0 8px}}
.s{{color:#6b7075;max-width:860px;line-height:1.5}}
.pills{{display:flex;gap:8px;margin:16px 0 22px}}
.pill{{border-radius:999px;padding:4px 12px;font-size:13px;font-weight:600}}
.ok{{background:#e7f6ec;color:#146c36}}.warn{{background:#fff4e5;color:#8a4b08}}.bad{{background:#fde7de;color:#9a3412}}
table{{width:100%;border-collapse:collapse;background:#fff;font-size:13.5px}}
th{{text-align:left;background:#111214;color:#fff;padding:10px;position:sticky;top:0}}
td{{padding:10px;border-top:1px solid #D7DADD;vertical-align:top;line-height:1.45}}
tr.bad td{{background:#fff8f5}}
.m{{color:#6b7075;font-size:12px;margin-top:2px}}
.st{{display:inline-block;border-radius:999px;padding:2px 8px;font-size:12px;font-weight:700;white-space:nowrap}}
.note{{margin-top:6px;color:#9a3412}}
.src a,.w a{{color:#F55823}}
.src{{display:flex;flex-direction:column;gap:3px;max-width:220px;word-break:break-all}}
</style></head><body><div class="w">
<h1>Факты о 44 поставщиках</h1>
<p class="s">Собрано 02.10.2026 с официальных сайтов. В тексты страниц пойдёт только то, что в колонке «Можно в текст» и «Без API на сайте». Строки «Проверить» в тексты не берём, пока вы не подтвердите компанию. Детали API со сторонних сайтов интеграторов в таблицу не включены.</p>
<div class="pills"><span class="pill bad">Проверить: {n_bad}</span><span class="pill warn">Без API на сайте: {n_warn}</span><span class="pill ok">Можно в текст: {44 - n_bad - n_warn}</span></div>
<table>
<thead><tr><th>Поставщик</th><th>Статус</th><th>Сайт</th><th>Кто это</th><th>Что продаёт</th><th>Кабинет</th><th>API</th><th>Источники</th></tr></thead>
<tbody>
{"".join(rows)}
</tbody></table>
</div></body></html>"""
    assert "\u2014" not in doc and "\u2013" not in doc
    open(OUT, "w", encoding="utf-8").write(doc)
    print(OUT, "bad", n_bad, "warn", n_warn)


if __name__ == "__main__":
    main()
