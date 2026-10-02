# -*- coding: utf-8 -*-
"""Уникальный текст карточки поставщика из проверенных фактов (seo-data/sup-facts).

В текст страницы не попадает: оговорка «не подтверждено», данные сторонних интеграторов,
пустой портрет АК Системс. Асбис и TFN в факты не берём: их убрали из списка 02.10.2026.
"""
import glob
import html
import json
import os

FACT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sup-facts")

# Подтверждено заказчиком 02.10.2026. Пустой about = раздел «кто это» не показываем.
OVERRIDES = {
    "ak-systems": {"about": "", "categories": [], "brands": [], "geo": "", "b2b": "", "api": "", "unique": []},
    "narmak": {
        "about": "NARMAK - бренд бакалеи: орехи, сухофрукты, семена и сопутствующие продукты. Оптовые заказы на сайте принимают письменно, отдельного кабинета партнёра нет.",
        "categories": ["орехи", "сухофрукты", "семена", "бакалея"],
        "api": "",
    },
    "bion": {
        "about": "BION - торговая марка дистрибьютора NETLAB. В линейке картриджи, сетевое оборудование, кабели и переходники. Оптом марку продаёт сам NETLAB.",
        "b2b": "Заказы BION идут через B2B-программу NETLAB NL-Dealer: для дилеров, магазинов и интеграторов.",
        "categories": ["картриджи", "сетевое оборудование", "кабели и переходники"],
    },
    "maksprofit": {
        "about": "ООО «Макспрофит» поставляет контрольно-измерительные приборы оптом и в розницу, есть ремонт и сервис. На сайте указаны Fluke, Rohde & Schwarz, Tektronix, Rigol, Flir и Keithley.",
        "categories": ["контрольно-измерительные приборы", "источники питания", "осциллографы", "тепловизоры"],
    },
    "novye-tehnologii": {
        "about": "ГК «Новые технологии» (nt-rt.ru, Казань) поставляет оборудование многих отраслей: от телекома и СКС до кабеля и ИБП. Отдельное направление - телекоммуникационные шкафы и стойки.",
        "categories": ["телеком и СКС", "компьютерная техника", "кабель", "аккумуляторы и ИБП", "телекоммуникационные шкафы"],
    },
    "distribution-center": {
        "about": "ООО «Центр дистрибьюции» поставляет средства связи и электронику для мобильной розницы: сами поставки, логистика и маркетинг.",
        "b2b": "Заказы оформляют в онлайн-системе: там наличие и цены с учётом акций. Доступ присылают после договора поставки.",
        "categories": ["средства связи", "мобильная электроника"],
    },
    "kvk": {
        "about": "ООО «КВК Трейд» оптом поставляет совместимые картриджи для лазерных принтеров и МФУ под маркой KVK.",
        "b2b": "Отдельные условия для дилеров, интернет-магазинов и розницы. Для магазинов предлагают выгрузку остатков склада на сайт.",
        "categories": ["совместимые картриджи", "расходные материалы для печати"],
        "api": "",
    },
    "energon": {
        "about": "ЭНЕРГОН разрабатывает и поставляет решения для хранения энергии: промышленные аккумуляторы, солнечные модули и инверторы. Среди применений - телеком, ИБП и системы безопасности.",
        "api": "На сайте есть страница «Обмен данными»: API для наличия, FTP-файлы с остатками, EDI и ЭДО. Через обмен доступны прайсы, статусы заказов и заявки. Публичной документации нет, доступ через sales@energon.ru.",
        "categories": ["промышленные аккумуляторы", "литий-ионные аккумуляторы", "солнечные модули", "инверторы", "батареи для ИБП"],
    },
    "dkc": {
        "site": "https://www.dkc.ru/",
        "about": "АО «ДКС» производит кабеленесущие системы и низковольтное оборудование: лотки, кабель-каналы, гофру, ИБП.",
        "b2b": "Система онлайн-сервисов ДКС для дистрибьюторов: заказы, отгрузки, остатки и коммерческие предложения.",
        "api": "ДКС выдаёт доступ к API или FTP: база продукции, характеристики, изображения и остатки, плюс EDI-обмен заказами. Запрос доступа - через форму на dkc.ru.",
        "categories": ["кабеленесущие системы", "кабель-каналы", "низковольтное оборудование", "ИБП"],
    },
    "it-proekt": {
        "site": "https://www.i-t-p.pro/",
        "about": "IT Partner входит в Partners Group и с 2013 года оптом поставляет IT-оборудование. На сайте указаны своя B2B-система, доставка по городам Центрального округа и более 250 000 наименований в каталоге.",
        "b2b": "Оптовые клиенты работают через B2B-систему, которую Partners Group сделала сама. Доступ клиентский: логин и пароль.",
        "api": "Документация B2B API открыта: каталог, наличие и цены, заказы. Обмен идёт по HTTP в формате JSON-RPC.",
        "categories": ["IT-оборудование широкого профиля"],
        "sources": ["https://www.i-t-p.pro/", "https://b2b.i-t-p.pro/download/docs/api/api.html"],
    },
}


def _load():
    out = {}
    for f in glob.glob(os.path.join(FACT, "batch-*.json")):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            if not k.startswith("_"):
                out[k] = dict(v)
    for slug, patch in OVERRIDES.items():
        base = out.get(slug, {})
        base.update(patch)
        out[slug] = base
    return out


FACTS = _load()


def _cut_third_party(text):
    text = text or ""
    for mark in ("По данным сторонних", "По неофициальному", "по сторонним источникам"):
        i = text.find(mark)
        if i > 40:
            text = text[:i]
    return text.replace("\u2014", "-").replace("\u2013", "-").strip(" .;")


def _clip(text, n):
    text = _cut_third_party(text)
    if len(text) <= n:
        return text
    return text[:n].rsplit(" ", 1)[0]


def fact(slug):
    v = FACTS.get(slug) or {}
    about = _cut_third_party(v.get("about") or "")
    if "не подтверждено" in about or "тёзка" in about.lower() or "тезка" in about.lower():
        about = ""
    return {
        "about": about,
        "categories": [x for x in (v.get("categories") or []) if x][:6],
        "brands": [x for x in (v.get("brands") or []) if x][:6],
        "geo": _clip(v.get("geo") or "", 220),
        "b2b": _clip(v.get("b2b") or "", 260),
        "api": _clip(v.get("api") or "", 280),
        "unique": [_cut_third_party(x) for x in (v.get("unique") or []) if x][:2],
    }


def voice(slug):
    return sum(ord(ch) for ch in slug) % 4


def esc(s):
    return html.escape(s or "", quote=False)


def about_html(s):
    f = fact(s["slug"])
    if not f["about"]:
        return ""
    nm = s["name"]
    h2 = (
        f"Кто такой {nm}",
        f"Что продаёт {nm}",
        f"{nm}: коротко о поставщике",
        f"Чем {nm} отличается от других в списке",
    )[voice(s["slug"])]
    parts = [f"<p>{esc(f['about'])}</p>"]
    if f["categories"]:
        parts.append(f"<p><b>В ассортименте:</b> {esc(', '.join(f['categories']))}.</p>")
    if f["brands"]:
        parts.append(f"<p><b>Бренды на сайте:</b> {esc(', '.join(f['brands']))}.</p>")
    if f["geo"]:
        parts.append(f"<p>{esc(f['geo'])}</p>")
    if f["b2b"]:
        parts.append(f"<p>{esc(f['b2b'])}</p>")
    if f["unique"]:
        parts.append("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in f["unique"]) + "</ul>")
    return h2, "\n    ".join(parts)


def faq_extra(s, data_phrase):
    """Вопросы, которых нет у соседних карточек: ассортимент, кабинет, API."""
    f = fact(s["slug"])
    items = []
    if f["categories"]:
        items.append((
            f"Что входит в каталог {s['gen']}?",
            f"На сайте {s['name']} указаны: {', '.join(f['categories'])}. "
            f"В 1С по этой интеграции приходят {data_phrase}.",
        ))
    if f["b2b"]:
        items.append((f"Как устроен кабинет {s['name']}?", f["b2b"]))
    if f["api"]:
        items.append((f"Что известно про API {s['gen']}?", f["api"]))
    return items
