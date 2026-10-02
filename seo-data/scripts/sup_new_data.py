# -*- coding: utf-8 -*-
"""Новые страницы поставщиков (решение 02.10.2026): все профильные строки таблицы /ecom с отметками.

tab - имя (имена) строки в таблице https://alsn.ru/ecom, отметки берутся оттуда.
name - в тексте, gen - «у ... / со складов ...», ins - «с ...», po - «по ...», crumb - в крошках и чипах.
"""


def _n(slug, tab, name, h1b=None, gen=None, ins=None, po=None, full=None, crumb=None):
    tab = tab if isinstance(tab, (list, tuple)) else [tab]
    return dict(slug=slug, tab=list(tab), name=name, h1b=h1b or ins or name, gen=gen or name, ins=ins or name,
                po=po or name, full=full or tab[0], crumb=crumb or name)


NEW = [
    _n("dihouse", "diHouse", "diHouse"),
    _n("superwave", "Superwave group", "Superwave", full="Superwave group"),
    _n("klavtorg", "Клавторг", "Клавторг", gen="Клавторга", ins="Клавторгом", po="Клавторгу"),
    _n("narmak", "NARMAK", "NARMAK"),
    _n("ak-systems", "АК Системс", "АК Системс"),
    _n("karin", "KARIN", "KARIN"),
    _n("mics", "MICS distribution company", "MICS", full="MICS distribution company"),
    _n("bion", "BION", "BION", full="BION, торговая марка NETLAB"),
    _n("maksprofit", "Макспрофит", "Макспрофит", gen="Макспрофита", ins="Макспрофитом", po="Макспрофиту"),
    _n("novye-tehnologii", "ГК НОВЫЕ ТЕХНОЛОГИИ", "ГК «Новые технологии»", h1b="ГК «Новые технологии»",
       full="ГК «Новые технологии»", crumb="Новые технологии"),
    _n("svyazkomplekt", "СвязьКомплект", "СвязьКомплект", gen="СвязьКомплекта", ins="СвязьКомплектом", po="СвязьКомплекту"),
    _n("distribution-center", "Distribution Center", "Distribution Center"),
    _n("nag", "НАГ", "НАГ"),
    _n("hyperline", "Hyperline", "Hyperline"),
    _n("mont", "MONT", "MONT"),
    _n("emilink", "Emilink", "Emilink"),
    _n("proway", "ProWay", "ProWay"),
    _n("kvk", "KVK", "KVK"),
    _n("rm-company", "RM-Company", "RM-Company"),
    _n("sds", "SDS LLC", "SDS", full="SDS LLC"),
    _n("taile", "Тайле", "Тайле"),
    _n("v1-electronics", "ТД В1 Электроникс", "В1 Электроникс", full="ТД В1 Электроникс"),
    _n("f5it", "F5it", "F5it"),
    _n("legion-project", "legion project", "Legion Project", full="legion project"),
    _n("energon", "ENERGON", "ENERGON"),
    _n("forum-electro", "Форум электро", "Форум Электро"),
    _n("nienschanz", "Ниеншанц-Автоматика", "Ниеншанц-Автоматика", gen="Ниеншанц-Автоматики",
       ins="Ниеншанц-Автоматикой", po="Ниеншанц-Автоматике"),
    _n("dkc", "DKC.MARKET", "ДКС", h1b="ДКС", full="АО «ДКС»", crumb="ДКС"),
    _n("it-proekt", "IT PROEKT", "IT Partner", h1b="IT Partner", full="IT Partner (Partners Group)", crumb="IT Partner"),
]

# Решение 02.10.2026: этих строк в таблице /ecom больше нет, страницы не делаем.
DROP_ROWS = {"Асбис", "TFN", "ТФН"}

# имя строки таблицы /ecom -> slug, для ссылок из таблицы
NEW_CARDS = {t: s["slug"] for s in NEW for t in s["tab"]}
