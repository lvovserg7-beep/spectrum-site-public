# -*- coding: utf-8 -*-
"""Rebuild detailed Alt-tail brief with accurate locations."""
from __future__ import annotations

import html as html_lib
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "_alts-tail-live-2026-09-28.json"
OUT_HTML = ROOT.parent / "tilda-briefs" / "tier2-alts-tail-2026-09-28.html"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

PAGES = {
    "/caseecomsc": {
        "name": "Кейс: интеграция 1С с поставщиками для ООО «СЦ»",
        "h1": "Кейс: интеграция 1С с поставщиками телеком- и IT-оборудования для ООО «СЦ»",
    },
    "/xitsadmarketplace": {
        "name": "Кейс: интеграция 1С с маркетплейсами для ООО «ХИТСАД»",
        "h1": "Кейс: интеграция 1С с маркетплейсами для ООО «ХИТСАД»",
    },
    "/clients": {
        "name": "Клиенты",
        "h1": "Клиенты",
    },
}

# Known alts
ALT = {
    "Tatneft-Logosvg.png": "Логотип Татнефть",
    "logo.png": "Логотип партнёра Аллсан",
    "logo-ss-ru.jpg": "Логотип партнёра Аллсан",
    "Logo_LANIT.png": "Логотип ЛАНИТ",
    "logo11_350.jpg": "Логотип партнёра Аллсан",
    "_.png": "Логотип партнёра Аллсан",
    "_.jpg": "Благодарственное письмо клиенту Аллсан",
    "_.jpeg": "Благодарственное письмо клиенту Аллсан",
    "__1.jpg": "Благодарственное письмо клиенту Аллсан",
    "__2.jpg": "Благодарственное письмо клиенту Аллсан",
    "_______1_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "__page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "__pdf_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "0001_1.jpg": "Благодарственное письмо клиенту Аллсан",
    "Image_5_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "GoodWood.jpg": "Логотип GOOD WOOD",
    "Xcom.jpg": "Логотип X-COM",
    "X-Com.jpeg": "Логотип X-COM",
    "thumb_6478_participa.png": "Логотип партнёра Аллсан",
    "c8561e493ab77c8933fc.png": "Логотип партнёра Аллсан",
    "5e82004a227a092f3923.png": "Логотип партнёра Аллсан",
    "image.png": "Иллюстрация к кейсу Аллсан",
    "noroot.jpg": "Отзыв клиента Аллсан",
    "noroot.png": "Отзыв клиента Аллсан",
    "photo.jpg": "Отзыв клиента Аллсан",
}

SKIP_FN = re.compile(
    r"(?i)(?:\.svg$|Tilda_Icons|kisspng|emoji|Vector_|Layer_|favicon|sprite|"
    r"1x1|blank|spacer|29557530|_5\.png|_9\.png)"
)

IMG_RE = re.compile(r"<img\b([^>]*)>", re.I | re.S)
ATTR_RE = re.compile(r"""(\w+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ru-RU,ru;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def textish(s: str) -> str:
    return WS.sub(" ", html_lib.unescape(STRIP.sub(" ", s or ""))).strip()


def attrs(inner: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in ATTR_RE.finditer(inner):
        k = m.group(1).lower()
        v = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[k] = v or ""
    return out


def basename(src: str) -> str:
    return urlparse(src).path.rsplit("/", 1)[-1]


def split_recs(html: str) -> list[dict]:
    starts = list(re.finditer(r'<div id="(rec\d+)"[^>]*>', html))
    recs = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(html)
        head = html[m.start() : m.start() + 500]
        tm = re.search(r'data-record-type="(\d+)"', head)
        recs.append(
            {
                "id": m.group(1),
                "type": tm.group(1) if tm else "",
                "start": m.start(),
                "end": end,
                "html": html[m.start() : end],
            }
        )
    return recs


def titles_in(chunk: str) -> list[str]:
    out = []
    for pat in (
        r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>",
        r'class="[^"]*(?:t-section__title|t-title|t-name)[^"]*"[^>]*>([^<]{3,140})',
        r'field="title"[^>]*>([^<]{3,140})',
    ):
        for m in re.finditer(pat, chunk, re.I | re.S):
            t = textish(m.group(1))
            if t and t not in out:
                out.append(t[:140])
    return out


def neighbor_section(recs: list[dict], idx: int) -> str:
    # prefer title in same rec, then previous, then next
    own = titles_in(recs[idx]["html"])
    if own:
        return own[0]
    for j in range(idx - 1, max(-1, idx - 4), -1):
        ts = titles_in(recs[j]["html"])
        if ts:
            # skip mega-menu / footer-ish
            t = ts[0]
            if t not in ("Внедрение 1С", "Аллсан Интеграция", "Разработка 1с"):
                return t
    for j in range(idx + 1, min(len(recs), idx + 4)):
        ts = titles_in(recs[j]["html"])
        if ts:
            t = ts[0]
            if t in ("Наши клиенты", "Отзывы клиентов", "Сертификаты", "Отзывы клиентов о компании Аллсан Интеграция"):
                return t
            if t not in ("Внедрение 1С", "Аллсан Интеграция"):
                return t
    return ""


def block_label(typ: str, class_attr: str = "") -> str:
    cl = class_attr or ""
    if typ == "594" or "t594" in cl:
        return "T594 - лента логотипов клиентов"
    if typ == "795":
        return "T795 - галерея / слайдер"
    if typ == "396":
        return "T396 - Zero Block"
    if typ == "316":
        return "T316 - форма / баннер с картинкой"
    if typ == "487":
        return "T487 - цитата / отзыв"
    if typ == "670":
        return "T670 - отзывы"
    if typ == "107":
        return "T107 - картинка"
    return f"T{typ}" if typ else "блок на холсте"


def classify_file(fn: str) -> str:
    low = fn.lower()
    if (
        "logo" in low
        or "tatneft" in low
        or "lanit" in low
        or "goodwood" in low
        or "xcom" in low
        or low == "_.png"
        or low.startswith("thumb_")
        or low in ("c8561e493ab77c8933fc.png", "5e82004a227a092f3923.png")
    ):
        return "logo"
    if "page-0001" in low or "0001" in low or (
        low.startswith("_") and low.endswith((".jpg", ".jpeg"))
    ):
        return "letter"
    if "noroot" in low or low == "photo.jpg":
        return "review"
    if low == "image.png":
        return "other"
    return "other"


def guess_alt(fn: str) -> str:
    if fn in ALT:
        return ALT[fn]
    kind = classify_file(fn)
    if kind == "logo":
        return "Логотип партнёра Аллсан"
    if kind == "letter":
        return "Благодарственное письмо клиенту Аллсан"
    if kind == "review":
        return "Отзыв клиента Аллсан"
    return "Иллюстрация Аллсан"


def scan_page(path: str) -> list[dict]:
    meta = PAGES[path]
    url = "https://alsn.ru" + path
    html = fetch(url + "?alt=detail")
    recs = split_recs(html)
    items = []
    seen = set()

    for ri, rec in enumerate(recs):
        # collect imgs in rec with empty alt
        logos_order = []
        empties = []
        for m in IMG_RE.finditer(rec["html"]):
            a = attrs(m.group(1))
            src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
            if not src:
                continue
            fn = basename(src)
            if not fn or SKIP_FN.search(fn):
                continue
            # skip brand site logo
            if fn in ("_5.png", "_9.png"):
                continue
            logos_order.append(fn)
            alt = (a.get("alt") or "").strip()
            if alt and alt.lower() not in {"image", "img", "фото", "картинка"}:
                continue
            # skip pure decorative tiny if not in our ALT / meaningful names
            kind = classify_file(fn)
            if kind == "other" and ("/resize/20x/" in src):
                continue
            # CTA form decorative on clients - noroot in T316 with «экспресс-аудит»
            section_probe = neighbor_section(recs, ri)
            if (
                path == "/clients"
                and fn == "noroot.png"
                and "аудит" in section_probe.lower()
            ):
                # decorative form art - still empty, include with clear location
                pass
            empties.append(
                {
                    "fn": fn,
                    "src": src.split("?")[0][:240],
                    "class": (a.get("class") or "")[:120],
                    "pos": m.start(),
                }
            )

        if not empties:
            continue

        section = neighbor_section(recs, ri)
        # special: T594 on cases - title often in NEXT T795 «Наши клиенты»
        if rec["type"] == "594":
            section = section or "Наши клиенты"
            # look forward for exact
            for j in range(ri + 1, min(len(recs), ri + 3)):
                ts = titles_in(recs[j]["html"])
                if ts and "клиент" in ts[0].lower():
                    section = ts[0]
                    break
            # also check previous for «Отзывы»
            for j in range(ri - 1, max(-1, ri - 5), -1):
                ts = titles_in(recs[j]["html"])
                if ts and ("отзыв" in ts[0].lower() or "клиент" in ts[0].lower()):
                    # keep Наши клиенты as primary for logo strip if next has it
                    break

        # Zero Block: find covering title; on cases these sit between quote and logo strip
        if rec["type"] == "396":
            for j in range(ri - 1, -1, -1):
                ts = titles_in(recs[j]["html"])
                if ts:
                    t = ts[0]
                    if t not in ("Внедрение 1С", "Аллсан Интеграция", "Разработка 1с"):
                        section = t
                        break
            if path == "/clients" and not section:
                section = "Отзывы клиентов о компании Аллсан Интеграция"
            if path in ("/caseecomsc", "/xitsadmarketplace") and not section:
                section = "Отзывы и письма клиентов (под текстом кейса, выше ленты «Наши клиенты»)"

        for e in empties:
            fn = e["fn"]
            key = (path, fn, rec["id"])
            if key in seen:
                continue
            seen.add(key)
            try:
                idx = logos_order.index(fn) + 1
            except ValueError:
                idx = 0
            # near text inside rec
            near = ""
            chunk = rec["html"]
            before = chunk[max(0, e["pos"] - 600) : e["pos"]]
            after = chunk[e["pos"] : e["pos"] + 400]
            for part in (before, after):
                for pat in (
                    r'class="[^"]*(?:t-name|t-descr|t-text|tn-atom)[^"]*"[^>]*>([^<]{4,120})',
                    r"<p[^>]*>([^<]{12,120})</p>",
                ):
                    ms = list(re.finditer(pat, part, re.I | re.S))
                    if ms:
                        near = textish(ms[-1].group(1))[:120]
                        break
                if near:
                    break
            if not near:
                near = section

            kind = classify_file(fn)
            expected = guess_alt(fn)
            # уточнение Alt по месту
            if fn == "noroot.png" and rec["type"] == "316":
                expected = "Иллюстрация к форме консультации по 1С"
            elif fn == "noroot.png" and rec["type"] == "487":
                expected = "Фото к отзыву клиента Аллсан"
            elif fn == "image.png":
                expected = "Иллюстрация к кейсу Аллсан"

            items.append(
                {
                    "path": path,
                    "page_url": url,
                    "page_name": meta["name"],
                    "h1": meta["h1"],
                    "file": fn,
                    "src": e["src"],
                    "alt_now": "",
                    "expected": expected,
                    "section": section,
                    "near": near or section,
                    "block": block_label(rec["type"], e["class"]),
                    "rec": rec["id"],
                    "type": rec["type"],
                    "class": e["class"],
                    "index_in_block": idx,
                    "logos_in_block": len(logos_order),
                    "kind": kind,
                }
            )
    return items


def orient_lines(it: dict) -> list[str]:
    lines = [
        f"Страница: «{it['page_name']}» ({it['page_url']})",
        f"Адрес в списке Тильды: {it['path'].lstrip('/')}",
    ]
    kind = it.get("kind") or classify_file(it["file"])
    section = it.get("section") or ""
    block = it.get("block") or ""
    rid = it.get("rec") or ""
    idx = it.get("index_in_block") or 0
    total = it.get("logos_in_block") or 0
    near = it.get("near") or ""
    fn = it["file"]

    if it.get("type") == "594":
        lines.append(
            "Прокрутить вниз страницы мимо текста кейса и блока «У нас есть решение для» "
            "до ленты логотипов компаний (серые/цветные логотипы в ряд)."
        )
        lines.append(
            f"Заголовок секции рядом: «{section or 'Наши клиенты'}» "
            "(заголовок может быть в соседнем блоке T795 сразу под или над лентой)."
        )
        lines.append(f"Тип блока: {block}" + (f" · id блока {rid}" if rid else ""))
        if idx and total:
            lines.append(
                f"В ленте это логотип №{idx} слева направо (всего в блоке видно {total} картинок, "
                "включая повторы карусели)."
            )
        lines.append(
            "Не путать с меню услуг сверху и с логотипом Аллсан в шапке/подвале."
        )
        if near and near != section:
            lines.append(f"Соседний текст у блока: «{near}»")
        lines.append(f"В настройках картинки имя файла: {fn}")
    elif it.get("type") == "396" and kind == "logo":
        lines.append(
            "Прокрутить к Zero Block с логотипами клиентов (карточки/плитка логотипов), "
            "не к нижней бегущей ленте T594 «Наши клиенты»."
        )
        if section:
            lines.append(f"Заголовок секции рядом: «{section}»")
        lines.append(f"Тип блока: {block}" + (f" · id {rid}" if rid else ""))
        if idx and total:
            lines.append(f"В этом Zero Block картинка №{idx} из {total} на холсте блока.")
        if near:
            lines.append(f"Соседний текст рядом: «{near}»")
        lines.append(f"Файл в кабинете: {fn}")
    elif kind == "letter":
        lines.append(
            "Прокрутить к галерее благодарственных писем (сканы на бланке с печатью/подписи), "
            "не к цветной ленте логотипов T594."
        )
        if section:
            lines.append(f"Заголовок секции рядом: «{section}»")
        lines.append(f"Тип блока: {block}" + (f" · id {rid}" if rid else ""))
        if idx and total:
            lines.append(f"В этом Zero Block картинка №{idx} из {total} на холсте блока.")
        if near:
            lines.append(f"Соседний текст / подпись рядом: «{near}»")
        lines.append(f"Файл в кабинете: {fn}")
    elif kind == "review":
        if "аудит" in (section or "").lower() or "эффективность" in (section or "").lower():
            lines.append(
                "Картинка в блоке формы/баннера с призывом "
                f"«{section or 'консультация / аудит'}» (не галерея отзывов и не лента логотипов)."
            )
        elif it.get("type") == "487":
            lines.append(
                "Прокрутить к блоку цитаты / отзыва под заголовком "
                f"«{section or 'Достигнутые результаты'}» - фото рядом с текстом отзыва."
            )
        else:
            lines.append(
                "Прокрутить к блоку отзывов с фото или превью (портрет / обложка), "
                "не к ленте логотипов."
            )
        if section:
            lines.append(f"Заголовок секции / блока: «{section}»")
        lines.append(f"Тип блока: {block}" + (f" · id {rid}" if rid else ""))
        if near:
            lines.append(f"Соседний текст рядом: «{near}»")
        lines.append(f"Файл в кабинете: {fn}")
    else:
        if section:
            lines.append(f"Заголовок секции: «{section}»")
        lines.append(f"Тип блока: {block}" + (f" · id {rid}" if rid else ""))
        if idx and total > 1:
            lines.append(f"Картинка №{idx} из {total} в блоке.")
        if near:
            lines.append(f"Соседний текст: «{near}»")
        lines.append(f"Файл: {fn}")
    return lines


def esc(s: str) -> str:
    return html_lib.escape(s or "", quote=True)


def build_html(items: list[dict]) -> str:
    by_page: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        by_page[it["path"]].append(it)
    order = [p for p in ("/caseecomsc", "/xitsadmarketplace", "/clients") if p in by_page]

    parts = [
        f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Хвост Alt - alsn.ru - 23.09.2026</title>
  <style>
    :root {{
      --bg:#f4f3ef; --card:#fff; --text:#1a1a1a; --muted:#5c5c5c; --border:#e2e2de;
      --ok:#1a7f4b; --ok-bg:#e8f6ee; --warn:#9a6700; --warn-bg:#fff6e0;
      --danger:#b42318; --danger-bg:#fdecea; --info:#0b6e99; --info-bg:#e8f4fa; --code:#0f172a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin:0; font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; color:var(--text); background:var(--bg); }}
    .wrap {{ max-width:960px; margin:0 auto; padding:24px 18px 72px; }}
    h1 {{ font-size:26px; margin:0 0 6px; }}
    h2 {{ font-size:20px; margin:0 0 10px; }}
    h3 {{ font-size:16px; margin:16px 0 8px; }}
    p {{ margin:0 0 8px; }}
    a {{ color:#0b5cad; }}
    .muted {{ color:var(--muted); font-size:14px; }}
    .pills {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 16px; }}
    .pill {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:12px; font-weight:650; border:1px solid var(--border); background:#fff; }}
    .pill.ok {{ color:var(--ok); background:var(--ok-bg); border-color:#c6e6d3; }}
    .pill.warn {{ color:var(--warn); background:var(--warn-bg); border-color:#f0dfa0; }}
    .pill.danger {{ color:var(--danger); background:var(--danger-bg); border-color:#f5c2c0; }}
    .pill.info {{ color:var(--info); background:var(--info-bg); border-color:#bddceb; }}
    .callout {{ border-radius:10px; padding:12px 14px; margin:12px 0 18px; border:1px solid var(--border); background:var(--card); font-size:14px; }}
    .callout.danger {{ background:var(--danger-bg); border-color:#f5c2c0; }}
    .callout.warn {{ background:var(--warn-bg); border-color:#f0dfa0; }}
    .callout.info {{ background:var(--info-bg); border-color:#bddceb; }}
    .callout.ok {{ background:var(--ok-bg); border-color:#c6e6d3; }}
    .toc {{ background:var(--card); border:1px solid var(--border); border-radius:10px; padding:12px 16px; margin:0 0 20px; }}
    .toc ol {{ margin:6px 0 0; padding-left:22px; }}
    .task {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:16px 18px 18px; margin:0 0 18px; }}
    .num {{ display:inline-block; background:#111; color:#fff; border-radius:999px; font-size:12px; font-weight:700; padding:2px 10px; margin-right:6px; }}
    .lbl {{ display:block; font-size:11px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; color:var(--muted); margin:12px 0 4px; }}
    ol.steps {{ margin:4px 0 0; padding-left:22px; }}
    ol.steps > li {{ margin:6px 0; }}
    .path {{ font-family:ui-monospace,Consolas,monospace; font-size:12.5px; background:#111; color:#f5f5f4; border-radius:8px; padding:8px 10px; margin:6px 0 8px; overflow-x:auto; }}
    .orient {{ background:#fafaf8; border:1px solid var(--border); border-radius:8px; padding:10px 12px; margin:8px 0; font-size:14px; }}
    .orient ul {{ margin:4px 0 0; padding-left:18px; }}
    .orient li {{ margin:4px 0; }}
    .copybox {{ position:relative; margin:6px 0 10px; }}
    .copybox pre {{ margin:0; background:var(--code); color:#e5e7eb; border-radius:10px; padding:12px 12px 40px; overflow-x:auto; white-space:pre-wrap; word-break:break-word; font:13px/1.4 ui-monospace,Consolas,monospace; }}
    .copybox button {{ position:absolute; right:8px; bottom:8px; background:#fff; border:1px solid #ccc; border-radius:8px; padding:4px 10px; font-size:12px; font-weight:650; cursor:pointer; }}
    .copybox.ok button {{ background:var(--ok-bg); }}
    article.img {{ border-top:1px solid var(--border); padding:12px 0 6px; margin-top:8px; }}
    article.img:first-of-type {{ border-top:0; padding-top:0; }}
    code {{ font-family:ui-monospace,Consolas,monospace; font-size:12.5px; }}
    table {{ width:100%; border-collapse:collapse; font-size:13px; margin:8px 0 12px; background:#fff; }}
    th,td {{ border:1px solid var(--border); padding:6px 8px; text-align:left; vertical-align:top; }}
    th {{ background:#fafaf8; }}
  </style>
</head>
<body>
<div class="wrap">
  <h1>Хвост Alt - подписи к картинкам</h1>
  <p class="muted">Срез живого alsn.ru: 23.09.2026 · только Тильда · подробные ориентиры: секция, блок, номер в ленте, соседний текст</p>
  <div class="pills">
    <span class="pill danger">пусто: {len(items)}</span>
    <span class="pill info">страниц: {len(by_page)}</span>
    <span class="pill ok">услуги / МП / B2B / лицензии: ок</span>
    <span class="pill warn">Twitter/Bing SKIP</span>
  </div>
  <div class="callout danger">Каждый шаг - после письменного «да». «Опубликовать» - отдельно. robots.txt не трогать.</div>
  <div class="callout ok">На внедрении, поддержке, МП, B2B, лицензиях, about_us, cases и страницах партнёров смысловые Alt на срезе уже стоят. Ниже только хвост.</div>
  <nav class="toc"><strong>Содержание</strong><ol>
    <li><a href="#status">Что уже сделано</a></li>
    <li><a href="#how">Как ставить Alt</a></li>
"""
    ]
    for i, path in enumerate(order, 1):
        name = by_page[path][0]["page_name"]
        parts.append(
            f'    <li><a href="#p-{i}">{esc(name)}</a> <span class="muted">({len(by_page[path])})</span></li>\n'
        )
    parts.append('    <li><a href="#pub">Опубликовать</a></li>\n  </ol></nav>\n')

    parts.append(
        """
<section class="task" id="status">
  <h2><span class="num">0</span> Что уже сделано</h2>
  <p>По срезу 23.09.2026 пустых смысловых Alt нет на страницах внедрения, КА, ERP, техподдержки, ecom, casemarketplace, лицензий, 1С:КП, 1С:Фреш, «О компании», «Кейсы», Битрикс24, ЦРА и партнёров (ЭТМ, Мерлион, OCS, Марвел, Treolan, 3logic).</p>
  <p class="muted">Эти страницы в этой инструкции не трогать. SVG-иконки и виджет мессенджера не заполнять.</p>
</section>

<section class="task" id="how">
  <h2>Как ставить Alt</h2>
  <ol class="steps">
    <li>Список страниц Тильды → адрес из ориентира → карандаш.</li>
    <li>Прокрутить холст по списку «Где найти» (секция → тип блока → номер в ленте).</li>
    <li>Клик по картинке → поле <strong>Alt</strong> / «Альтернативный текст».</li>
    <li>Вставить текст из «Копировать Alt» → сохранить блок.</li>
  </ol>
  <div class="path">Список страниц → адрес → ✎ → секция → блок → картинка → Alt → Сохранить</div>
</section>
"""
    )

    alt_i = 0
    for pi, path in enumerate(order, 1):
        items_p = by_page[path]
        # sort: T594 logos first, then Zero Block logos, letters, reviews, other
        def sort_key(x):
            typ = x.get("type") or ""
            kind = x.get("kind") or ""
            if typ == "594":
                group = 0
            elif typ == "396" and kind == "logo":
                group = 1
            elif kind == "letter":
                group = 2
            elif kind == "review":
                group = 3
            else:
                group = 4
            return (group, x.get("rec") or "", x.get("index_in_block") or 0, x["file"])

        items_p = sorted(items_p, key=sort_key)
        name = items_p[0]["page_name"]
        url = items_p[0]["page_url"]
        h1 = items_p[0]["h1"]
        parts.append(
            f"""
<section class="task" id="p-{pi}">
  <h2><span class="num">{pi}</span> {esc(name)}</h2>
  <p><strong>Что сделать.</strong> Проставить Alt у пустых смысловых картинок ({len(items_p)} шт.).</p>
  <p><strong>Зачем.</strong> Чтобы в поиске и для слабовидящих было понятно, чей логотип или какое письмо на экране.</p>
  <p class="muted">На сайте: <strong>{esc(h1)}</strong> · <a href="{esc(url)}">{esc(url)}</a> · в Тильде: <code>{esc(path.lstrip('/'))}</code></p>
"""
        )
        if path in ("/caseecomsc", "/xitsadmarketplace"):
            parts.append(
                """
  <div class="callout warn">Основной хвост - лента T594 внизу. Заголовок «Наши клиенты» часто в соседнем T795. Дополнительно ниже могут быть пустые noroot в форме/цитате - у них свой ориентир.</div>
  <p class="lbl">Карта ленты логотипов T594 (слева направо)</p>
  <table><thead><tr><th>№</th><th>Файл</th><th>Alt</th></tr></thead><tbody>
"""
            )
            logos = [x for x in items_p if x.get("type") == "594"]
            logos = sorted(logos, key=lambda x: x.get("index_in_block") or 0)
            for lg in logos:
                parts.append(
                    f"<tr><td>{lg.get('index_in_block') or '—'}</td><td><code>{esc(lg['file'])}</code></td><td>{esc(lg['expected'])}</td></tr>\n"
                )
            parts.append("</tbody></table>\n")

        if path == "/clients":
            parts.append(
                """
  <div class="callout warn">На «Клиенты» три типа картинок: логотипы в Zero Block, сканы благодарственных писем и фото/превью отзывов. Читайте ориентир у каждого файла.</div>
"""
            )

        for j, it in enumerate(items_p, 1):
            alt_i += 1
            cid = f"alt-{alt_i}"
            lines = orient_lines(it)
            li = "".join(f"<li>{esc(line)}</li>" for line in lines)
            parts.append(
                f"""
  <article class="img">
    <h3>{j}. Файл <code>{esc(it['file'])}</code></h3>
    <div class="orient">
      <strong>Где найти на холсте</strong>
      <ul>{li}</ul>
    </div>
    <span class="lbl">Вставить в Alt</span>
    <div class="copybox"><pre id="{cid}">{esc(it['expected'])}</pre><button type="button" data-copy="{cid}">Копировать Alt</button></div>
  </article>
"""
            )
        parts.append("</section>\n")

    parts.append(
        """
<section class="task" id="pub">
  <h2><span class="num">P</span> Опубликовать</h2>
  <p><strong>Что сделать.</strong> Опубликовать только страницы, где правили Alt.</p>
  <ol class="steps">
    <li>После письменного «да» - «Опубликовать» у каждой изменённой страницы.</li>
    <li>«Опубликовать все страницы» не нужно.</li>
  </ol>
</section>
<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-alts-tail-2026-09-28.html</code></p>
</div>
<script>
function flash(btn){btn.classList.add("ok");const t=btn.textContent;btn.textContent="Скопировано";setTimeout(()=>{btn.textContent=t;btn.classList.remove("ok");},1200);}
document.querySelectorAll(".copybox button[data-copy]").forEach(btn=>{
  btn.addEventListener("click",async()=>{
    const pre=document.getElementById(btn.getAttribute("data-copy"));
    if(!pre)return;
    await navigator.clipboard.writeText(pre.textContent);
    flash(btn);
  });
});
</script>
</body></html>
"""
    )
    return "".join(parts)


def main() -> None:
    all_items: list[dict] = []
    for path in PAGES:
        print("scan", path)
        items = scan_page(path)
        print(" ", len(items), "empty")
        for it in items:
            print(
                " ",
                it["file"],
                it["block"],
                f"#{it['index_in_block']}/{it['logos_in_block']}",
                it["section"][:40] if it["section"] else "-",
            )
        all_items.extend(items)

    summary = {"empty": len(all_items), "pages": len({x["path"] for x in all_items})}
    OUT_JSON.write_text(
        json.dumps({"date": "2026-09-28", "summary": summary, "items": all_items}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    OUT_HTML.write_text(build_html(all_items), encoding="utf-8")
    print("SUMMARY", summary)
    print("HTML", OUT_HTML)


if __name__ == "__main__":
    main()
