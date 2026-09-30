# -*- coding: utf-8 -*-
"""Rewrite Tilda catalog SEO title/descr/keywords. Other columns unchanged."""
from __future__ import annotations

import csv
import re
from pathlib import Path

SRC = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
DST = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005-seo.csv")
REPORT = Path(
    r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_store-seo-report.txt"
)

KEEP_SKU = {
    "4601546117588",
    "4601546117595",
    "2900001833547",
    "2900001833585",
}

SUFFIX = " | Аллсан"
TITLE_MAX = 70
DESCR_MAX = 175

ART_RE = re.compile(
    r"(?:^|[\s(])(?:арт\.?|артикул)\s+"
    r"[A-Za-zА-Яа-яЁё]*\d[\dA-Za-zА-Яа-яЁё._-]*",
    re.I,
)
ART_PAREN_RE = re.compile(
    r"\([^()]*(?:арт\.?|артикул)[^()]*\)",
    re.I,
)
HANGING = {
    "и", "на", "из", "для", "с", "со", "по", "в", "во", "к", "ко",
    "о", "об", "от", "до", "при", "без", "над", "под", "или", "а",
}
DELIVERY_RE = re.compile(
    r"[\(\s,]*"
    r"(?:электронная|коробочная|физическая)\s+поставка"
    r"[\)\s,]*",
    re.I,
)
SPACE_RE = re.compile(r"\s+")


def money(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    try:
        n = int(float(raw.replace(" ", "").replace(",", ".")))
    except ValueError:
        return ""
    if n <= 0:
        return ""
    s = f"{n:,}".replace(",", " ")
    return f"{s} ₽"


def delivery(row: dict) -> str:
    v = (row.get("Characteristics:Вид поставки") or "").strip()
    title = row.get("Title") or ""
    blob = f"{v} {title}".lower()
    if "электронн" in blob:
        return "электронная поставка"
    if "физическ" in blob or "короб" in blob:
        return "коробочная поставка"
    return ""


def delivery_short(d: str) -> str:
    if d.startswith("электрон"):
        return "эл. поставка"
    if d.startswith("короб"):
        return "коробка"
    return ""


def clean_name(title: str) -> str:
    t = title or ""
    t = t.replace("1C", "1С")
    t = ART_RE.sub(" ", t)
    t = ART_PAREN_RE.sub(" ", t)
    t = re.sub(r"\(\s*\)", " ", t)
    t = SPACE_RE.sub(" ", t)
    t = t.replace(" )", ")").replace("( ", "(")
    t = t.replace("1С:", "1С ")
    t = t.replace("1С КП", "1С:КП")
    t = SPACE_RE.sub(" ", t).strip(" -.,;:")
    t = t.replace("ПРОФ.", "ПРОФ")
    return t


def core_name(title: str) -> str:
    t = clean_name(title)
    t = DELIVERY_RE.sub(" ", t)
    t = SPACE_RE.sub(" ", t).strip(" -.,;:")
    t = t.replace(" - ", " ")
    return t


def abbreviate(name: str) -> str:
    out = name
    out = re.sub(r"ЗУП\s+Зарплата и Управление Персоналом", "ЗУП", out, flags=re.I)
    out = re.sub(r"УТ\s+Управление торговлей", "УТ", out, flags=re.I)
    out = re.sub(r"УНФ\s+Управление нашей фирмой", "УНФ", out, flags=re.I)
    out = re.sub(r"КА\s+Комплексная автоматизация", "КА", out, flags=re.I)
    pairs = [
        ("Зарплата и Управление Персоналом", "ЗУП"),
        ("Зарплата и управление персоналом", "ЗУП"),
        ("Управление нашей фирмой", "УНФ"),
        ("Управление торговлей", "УТ"),
        ("Комплексная автоматизация", "КА"),
        ("Документооборот", "ДО"),
        (
            "Бухгалтерия сельскохозяйственного предприятия",
            "бухгалтерия сельхозпредприятия",
        ),
        ("Клиентские лицензии на рабочие места", "клиентские лицензии"),
        ("рабочих мест", "мест"),
        ("на 12 месяцев по схеме 8+4 (4 месяца в подарок)", "8+4 на 12 мес"),
        ("по схеме 8+4 (4 месяца в подарок)", "8+4"),
        ("(4 месяца в подарок)", ""),
        ("Льготная цена (Продление ИТС)", "продление ИТС"),
        ("на 12 месяцев", "на 12 мес"),
        ("УСН и патент с сотрудниками", "УСН+патент"),
        ("Автоматизированное составление расписания", "АСР"),
        ("Распознавание первичных документов", "РПД"),
        (
            "Дополнительная лицензия на доступ из мобильных приложений и веб-сайтов",
            "доп. лицензия веб и моб.",
        ),
        ("Управление сбытом и закупками электроэнергии", "сбыт электроэнергии"),
        ("Предприятие 8 через Интернет", "Фреш"),
        ("Интернет-версия", ""),
        ("через Интернет", ""),
    ]
    for a, b in pairs:
        out = re.sub(re.escape(a), b, out, flags=re.I)
    out = re.sub(r"Фреш[\s\-]+1С\s+Фреш", "Фреш", out, flags=re.I)
    out = re.sub(r"1С Фреш-1С Фреш", "1С:Фреш", out, flags=re.I)
    out = re.sub(r"1С Фреш 1С ", "1С:Фреш ", out, flags=re.I)
    out = re.sub(r"Касса\.?\s*Стандартный", "Касса Стандарт", out, flags=re.I)
    return SPACE_RE.sub(" ", out).strip(" -.,")


def kind(row: dict) -> str:
    cat = (row.get("Category") or "").lower()
    title = (row.get("Title") or "").lower()
    blob = f"{cat} {title}"
    if "техническая поддержка" in cat or blob.startswith("техподдержка"):
        return "support"
    if "модуль для маркетплейсов" in cat or "модуль интеграции 1с с" in title:
        return "mp"
    if cat.startswith("итс") or "1с:кп" in title or " итс" in title or title.startswith("итс"):
        return "its"
    if "фреш" in cat or "фреш" in title or "fresh" in title:
        return "fresh"
    return "buy"


def fit_title(lead: str, core: str) -> str:
    def pack(c: str) -> str:
        return SPACE_RE.sub(" ", f"{lead}{c.strip(' ,.;')}{SUFFIX}").strip()

    cands: list[str] = []
    for c in (abbreviate(core), core):
        c = SPACE_RE.sub(" ", c).strip(" ,.;")
        if c and c not in cands:
            cands.append(c)
        c2 = re.sub(r",?\s*(эл\. поставка|коробка)\s*$", "", c, flags=re.I).strip(" ,")
        if c2 and c2 not in cands:
            cands.append(c2)
        c3 = re.sub(r"\s*редакция\s*\d+", "", c2 or c, flags=re.I).strip(" ,")
        if c3 and c3 not in cands:
            cands.append(c3)
    for c in cands:
        if len(pack(c)) <= TITLE_MAX:
            return pack(c)
    c = abbreviate(core)
    while len(pack(c)) > TITLE_MAX and " " in c:
        c = c.rsplit(" ", 1)[0].rstrip(" ,.;-(")
    while " " in c and c.rsplit(" ", 1)[-1].lower() in HANGING:
        c = c.rsplit(" ", 1)[0].rstrip(" ,.;-(")
    if c.count("(") > c.count(")"):
        c = c.rsplit("(", 1)[0].rstrip(" ,.;-")
    return pack(c)


def descr_buy(name: str, d: str, price: str) -> str:
    parts = [f"Купить {name}."]
    if d:
        parts.append(f"{d[0].upper() + d[1:]}.")
    if price:
        parts.append(f"Цена {price} у официального партнёра 1С.")
    else:
        parts.append("Официальный партнёр 1С.")
    parts.append("Консультация — Аллсан.")
    text = " ".join(parts)
    if len(text) <= DESCR_MAX:
        return text
    parts = [f"Купить {abbreviate(name)}."]
    if d:
        parts.append(f"{d[0].upper() + d[1:]}.")
    if price:
        parts.append(f"Цена {price} у официального партнёра 1С.")
    parts.append("Консультация — Аллсан.")
    text = " ".join(parts)
    if len(text) > DESCR_MAX:
        while len(text) > DESCR_MAX - 1 and " " in text:
            text = text.rsplit(" ", 1)[0].rstrip(" .,")
        text = text.rstrip(" .,") + "."
    return text


def keywords(kind_name: str, core: str) -> str:
    bits = ["купить", "1С", "Аллсан"]
    if kind_name == "support":
        bits = ["техподдержка 1С", "сопровождение 1С", "Аллсан"]
    elif kind_name == "mp":
        bits = ["модуль 1С", "маркетплейсы", "Ozon", "Wildberries", "Аллсан"]
    elif kind_name == "its":
        bits = ["купить ИТС", "1С:КП", "Аллсан"]
    elif kind_name == "fresh":
        bits = ["купить 1С:Фреш", "1С в облаке", "Аллсан"]
    extra = abbreviate(core)
    extra = extra.replace(" | Аллсан", "")
    if extra and extra.lower() not in " ".join(bits).lower():
        while len(extra) > 60 and " " in extra:
            extra = extra.rsplit(" ", 1)[0].rstrip(" ,.;-")
        bits.insert(1, extra)
    out = ", ".join(dict.fromkeys(b.strip() for b in bits if b.strip()))
    return out[:180]


def make_seo(row: dict) -> tuple[str, str, str]:
    sku = (row.get("SKU") or "").strip()
    if sku in KEEP_SKU:
        kws = keywords("buy", core_name(row.get("Title") or ""))
        return (
            (row.get("SEO title") or "").strip(),
            (row.get("SEO descr") or "").strip(),
            kws,
        )

    title = row.get("Title") or ""
    k = kind(row)
    d = delivery(row)
    ds = delivery_short(d)
    price = money(row.get("Price") or "")
    core = core_name(title)
    # parent of editions: title may not have seat count
    parent = (row.get("Parent UID") or "").strip()
    seats = re.search(r"(?:^|[\s-])(\d+)\s*$", core)
    if parent and seats:
        n = int(seats.group(1))
        word = "место" if n == 1 else "мест"
        core = re.sub(r"[\s-]+\d+\s*$", "", core).strip()
        core = f"{core} на {n} {word}"

    if k == "support":
        # Title like «Техподдержка по 1С на 1 час / 1 мес»
        short = title.replace("Техподдержка по 1С", "Техподдержка 1С")
        short = short.replace(" / ", ", ")
        seo_t = fit_title("", short)
        if not seo_t.endswith("Аллсан"):
            seo_t = fit_title("", short)
        seo_d = (
            f"Сопровождение 1С: {title}. Реакция от ~15 мин, "
            f"программист + аналитик + руководитель проектов."
        )
        if price:
            seo_d += f" От {price}."
        seo_d += " Официальный партнёр 1С — Аллсан."
        if len(seo_d) > DESCR_MAX:
            seo_d = seo_d[: DESCR_MAX - 1].rstrip(" .,") + "."
        return seo_t, seo_d, keywords(k, short)

    if k == "mp":
        tlow = title.lower()
        if "ozon" in tlow and "wildberries" not in tlow and "wb" not in tlow and "озон+wb" not in tlow:
            core_mp = "модуль 1С для Ozon"
        elif "wildberries" in tlow and "ozon" not in tlow:
            core_mp = "модуль 1С для Wildberries"
        else:
            core_mp = "модуль 1С для Ozon и Wildberries"
        seo_t = fit_title("Купить ", core_mp)
        seo_d = descr_buy(
            f"{core_mp}: остатки и заказы в 1С",
            "",
            price,
        )
        return seo_t, seo_d, keywords(k, core_mp)

    if k == "its":
        seo_t = fit_title("Купить ", core)
        seo_d = descr_buy(abbreviate(core), "Комплект поддержки 1С:КП / ИТС", price)
        return seo_t, seo_d, keywords(k, core)

    if k == "fresh":
        c = core
        if "фреш" not in c.lower():
            c = "1С:Фреш " + c
        c = abbreviate(c)
        c = re.sub(r"1С:?\s*Фреш[\s\-]*1С:?\s*Фреш", "1С:Фреш", c, flags=re.I)
        seo_t = fit_title("Купить ", c)
        seo_d = descr_buy(c, "Работа в 1С через интернет, 12 месяцев" if "12" in title else "1С в облаке", price)
        return seo_t, seo_d, keywords(k, c)

    # buy / licenses / boxes
    show = core
    if ds and ds not in show.lower() and "поставка" not in show.lower():
        show_title = f"{core}, {ds}"
    else:
        show_title = core
    seo_t = fit_title("Купить ", show_title)
    seo_d = descr_buy(abbreviate(core), d, price)
    return seo_t, seo_d, keywords(k, core)


def main() -> None:
    with SRC.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    report = []
    changed = 0
    for r in rows:
        old_t = (r.get("SEO title") or "").strip()
        old_d = (r.get("SEO descr") or "").strip()
        nt, nd, nk = make_seo(r)
        if "Алсан" in nt or "Алсан" in nd or "Алсан" in nk:
            raise SystemExit(f"typo Алсан: {r.get('SKU')} {nt}")
        if "классные подарки" in nd.lower() or "телеграм" in nd.lower() or "telegram" in nd.lower():
            raise SystemExit(f"forbidden: {r.get('SKU')} {nd}")
        r["SEO title"] = nt
        r["SEO descr"] = nd
        r["SEO keywords"] = nk
        if nt != old_t or nd != old_d or (r.get("SKU") in KEEP_SKU):
            changed += 1
        mark = "KEEP" if (r.get("SKU") or "") in KEEP_SKU else "SET"
        report.append(
            f"{mark}\t{(r.get('SKU') or '')[:18]}\t{len(nt)}\t{nt}\n    {nd}"
        )

    with DST.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=";",
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
        )
        w.writeheader()
        w.writerows(rows)

    REPORT.write_text(
        f"rows={len(rows)} changed~={changed}\nout={DST}\n\n" + "\n".join(report),
        encoding="utf-8",
    )
    long_t = [x for x in rows if len(x["SEO title"]) > TITLE_MAX]
    long_d = [x for x in rows if len(x["SEO descr"]) > DESCR_MAX]
    print("wrote", DST)
    print("report", REPORT)
    print("titles >", TITLE_MAX, len(long_t))
    print("descr >", DESCR_MAX, len(long_d))
    print("empty title", sum(1 for r in rows if not r["SEO title"]))
    print("empty descr", sum(1 for r in rows if not r["SEO descr"]))
    print("empty kw", sum(1 for r in rows if not r["SEO keywords"]))


if __name__ == "__main__":
    main()
