# -*- coding: utf-8 -*-
"""Enrich empty-alt leftovers with rich Tilda block locations; rebuild HTML brief."""
from __future__ import annotations

import html as html_lib
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
IN_JSON = ROOT / "_alts-tail-live-2026-09-23.json"
OUT_JSON = IN_JSON
OUT_HTML = ROOT.parent / "tilda-briefs" / "tier2-alts-tail-2026-09-23.html"
ETALON = ROOT.parent / "tilda-briefs" / "tier2-casemarketplace-onpage-2026-09-11.html"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

IMG_RE = re.compile(r"<img\b([^>]*)>", re.I | re.S)
ATTR_RE = re.compile(r"""(\w+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
REC_START = re.compile(
    r'<div id="(rec\d+)"[^>]*?(?:data-record-type="(\d+)")?[^>]*>', re.I
)

PAGE_NAME = {
    "/caseecomsc": "Кейс: интеграция 1С с поставщиками для ООО «СЦ»",
    "/xitsadmarketplace": "Кейс: интеграция 1С с маркетплейсами для ООО «ХИТСАД»",
    "/clients": "Клиенты",
}

SHARED_ALT = {
    "----01.jpg": "Клиенты Аллсан",
    "0001_1.jpg": "Благодарственное письмо клиенту Аллсан",
    "GoodWood.jpg": "Логотип GOOD WOOD",
    "Image_5_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "Tatneft-Logosvg.png": "Логотип Татнефть",
    "X-Com.jpeg": "Логотип X-COM",
    "Xcom.jpg": "Логотип X-COM",
    "_.jpeg": "Благодарственное письмо клиенту Аллсан",
    "_.jpg": "Благодарственное письмо клиенту Аллсан",
    "_.png": "Логотип партнёра Аллсан",
    "__1.jpg": "Благодарственное письмо клиенту Аллсан",
    "__2.jpg": "Благодарственное письмо клиенту Аллсан",
    "_______1_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "__page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "__pdf_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "logo.png": "Логотип партнёра Аллсан",
    "logo-ss-ru.jpg": "Логотип партнёра Аллсан",
    "Logo_LANIT.png": "Логотип ЛАНИТ",
    "logo11_350.jpg": "Логотип партнёра Аллсан",
    "noroot.jpg": "Отзыв клиента Аллсан",
    "noroot.png": "Отзыв клиента Аллсан",
    "photo.jpg": "Отзыв клиента Аллсан",
}


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
    starts = list(REC_START.finditer(html))
    recs = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(html)
        rid = m.group(1)
        typ = m.group(2) or ""
        # sometimes type is only on nested / sibling attr after id
        if not typ:
            head = html[m.start() : m.start() + 400]
            tm = re.search(r'data-record-type="(\d+)"', head)
            typ = tm.group(1) if tm else ""
        recs.append(
            {
                "id": rid,
                "type": typ,
                "start": m.start(),
                "end": end,
                "html": html[m.start() : end],
            }
        )
    return recs


def heading_before(html: str, pos: int) -> str:
    window = html[max(0, pos - 5000) : pos]
    hs = list(re.finditer(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", window, re.I | re.S))
    if hs:
        return textish(hs[-1].group(1))[:160]
    # t-title / tn-atom as fallback
    ts = list(
        re.finditer(
            r'class="[^"]*(?:t-section__title|t-title|t-name|tn-atom)[^"]*"[^>]*>([^<]{4,120})',
            window,
            re.I,
        )
    )
    if ts:
        return textish(ts[-1].group(1))[:160]
    return ""


def titles_in_rec(chunk: str) -> list[str]:
    out = []
    for pat in (
        r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>",
        r'class="[^"]*(?:t-section__title|t-title|t-name|t-card__title|accordion__title)[^"]*"[^>]*>([^<]{3,140})',
        r'field="title"[^>]*>([^<]{3,140})',
    ):
        for m in re.finditer(pat, chunk, re.I | re.S):
            t = textish(m.group(1))
            if t and t not in out and len(t) > 2:
                out.append(t[:140])
    return out[:6]


def near_caption(chunk: str, img_pos_in_chunk: int) -> str:
    before = chunk[max(0, img_pos_in_chunk - 800) : img_pos_in_chunk]
    after = chunk[img_pos_in_chunk : img_pos_in_chunk + 600]
    for part in (before, after):
        for pat in (
            r'class="[^"]*(?:t-name|t-card__title|t-descr|t-text|tn-atom)[^"]*"[^>]*>([^<]{4,140})',
            r"<figcaption[^>]*>(.*?)</figcaption>",
            r"<p[^>]*>([^<]{15,140})</p>",
            r'aria-label="([^"]{4,100})"',
            r'title="([^"]{4,100})"',
        ):
            ms = list(re.finditer(pat, part, re.I | re.S))
            if ms:
                t = textish(ms[-1].group(1))
                if t and "aria" not in t.lower():
                    return t[:140]
    return ""


def block_label(typ: str, class_attr: str) -> str:
    if typ:
        base = f"T{typ}"
    else:
        base = ""
    cl = class_attr or ""
    hints = []
    if "t594" in cl or typ == "594":
        hints.append("лента логотипов / карусель клиентов")
    if "t795" in cl or typ == "795":
        hints.append("галерея / слайдер")
    if "t107" in cl or typ == "107":
        hints.append("картинка")
    if "t396" in cl or typ == "396":
        hints.append("Zero Block")
    if "t670" in cl or typ == "670":
        hints.append("отзывы")
    if "t668" in cl or typ == "668":
        hints.append("отзывы / цитаты")
    if "t850" in cl or typ == "850":
        hints.append("галерея писем")
    if "t978" in cl or typ == "978":
        hints.append("галерея")
    if hints:
        return (base + " - " + ", ".join(hints)).strip(" -")
    return base or "блок на холсте"


def find_img_in_recs(recs: list[dict], html: str, fn: str) -> dict | None:
    fn_l = fn.lower()
    best = None
    for rec in recs:
        for m in IMG_RE.finditer(rec["html"]):
            a = attrs(m.group(1))
            src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
            if not src:
                continue
            if basename(src).lower() != fn_l and fn_l not in src.lower():
                continue
            # prefer non-tiny if several
            score = 0
            if "/resize/20x/" not in src:
                score += 2
            if "/empty/" not in src or "logo" in fn_l:
                score += 1
            alt = (a.get("alt") or "").strip()
            pos_abs = rec["start"] + m.start()
            # index among logos in this rec
            logos = []
            for m2 in IMG_RE.finditer(rec["html"]):
                a2 = attrs(m2.group(1))
                s2 = a2.get("src") or a2.get("data-original") or ""
                if not s2:
                    continue
                logos.append(basename(s2))
            try:
                idx = logos.index(basename(src)) + 1
            except ValueError:
                idx = 0
            titles = titles_in_rec(rec["html"])
            section = titles[0] if titles else heading_before(html, rec["start"])
            # if section empty, look at previous rec titles
            if not section:
                prev = [r for r in recs if r["end"] <= rec["start"]]
                if prev:
                    pt = titles_in_rec(prev[-1]["html"])
                    if pt:
                        section = pt[0]
                    else:
                        section = heading_before(html, rec["start"])
            near = near_caption(rec["html"], m.start())
            if not near and titles:
                near = " / ".join(titles[:2])
            info = {
                "rec": rec["id"],
                "type": rec["type"],
                "block": block_label(rec["type"], a.get("class") or ""),
                "section": section,
                "near": near,
                "src": src.split("?")[0][:240],
                "alt_now": alt,
                "class": (a.get("class") or "")[:120],
                "index_in_block": idx,
                "logos_in_block": len(logos),
                "score": score,
                "titles_in_block": titles,
            }
            if best is None or info["score"] > best["score"]:
                best = info
    return best


def how_to_find(it: dict, loc: dict) -> list[str]:
    lines = []
    path = it["path"]
    name = it.get("page_name") or PAGE_NAME.get(path, path)
    url = it.get("page_url") or ("https://alsn.ru" + path)
    lines.append(f"Страница: «{name}» ({url})")
    lines.append(f"Адрес в списке Тильды: {path.lstrip('/') or 'главная'}")

    section = loc.get("section") or ""
    block = loc.get("block") or ""
    near = loc.get("near") or ""
    rid = loc.get("rec") or ""
    idx = loc.get("index_in_block") or 0
    total = loc.get("logos_in_block") or 0
    fn = it["file"]
    typ = loc.get("type") or ""

    if typ == "594" or "t594" in (loc.get("class") or "") or "лента логотипов" in block:
        lines.append(
            "Прокрутить ниже основного текста кейса / отзывов до ленты логотипов клиентов "
            "(обычно заголовок «Наши клиенты», «Отзывы клиентов» или похожий)."
        )
        if section:
            lines.append(f"Заголовок секции рядом (H2/H3 или title блока): «{section}»")
        else:
            lines.append(
                "Заголовок секции: ищите блок с бегущей/статичной лентой логотипов компаний "
                "(не баннер героя и не фото в тексте кейса)."
            )
        lines.append(f"Тип блока: {block or 'T594 - лента логотипов'}" + (f" · id {rid}" if rid else ""))
        if idx and total:
            lines.append(
                f"В этом блоке картинка №{idx} из {total} (считайте слева направо по логотипам на холсте)."
            )
        if near:
            lines.append(f"Соседний текст у блока: «{near}»")
        lines.append(
            f"Клик по логотипу с файлом «{fn}» (в настройках картинки / CDN видно это имя)."
        )
    elif "page-0001" in fn.lower() or fn.startswith("_") or "0001" in fn or "Image_5" in fn:
        lines.append(
            "Прокрутить к галерее благодарственных писем / сканов отзывов "
            "(не лента цветных логотипов, а карточки писем на бланке)."
        )
        if section:
            lines.append(f"Заголовок секции: «{section}»")
        lines.append(f"Тип блока: {block or 'галерея писем'}" + (f" · id {rid}" if rid else ""))
        if idx and total:
            lines.append(f"Картинка №{idx} из {total} в этом блоке.")
        if near:
            lines.append(f"Соседний текст: «{near}»")
        lines.append(f"Файл в кабинете: {fn}")
    elif "noroot" in fn.lower() or fn == "photo.jpg":
        lines.append(
            "Прокрутить к блоку отзывов с фото / обложкой видеоотзыва "
            "(портрет или превью, не логотип в ленте)."
        )
        if section:
            lines.append(f"Заголовок секции: «{section}»")
        lines.append(f"Тип блока: {block or 'блок отзывов'}" + (f" · id {rid}" if rid else ""))
        if near:
            lines.append(f"Соседний текст / имя рядом: «{near}»")
        lines.append(f"Файл в кабинете: {fn}")
    else:
        if section:
            lines.append(f"Заголовок секции рядом: «{section}»")
        else:
            lines.append("Заголовок секции: смотрите блок, где лежит этот файл (см. тип блока ниже).")
        lines.append(f"Тип блока: {block or 'блок на холсте'}" + (f" · id {rid}" if rid else ""))
        if idx and total and total > 1:
            lines.append(f"Экземпляр: картинка №{idx} из {total} в блоке.")
        if near:
            lines.append(f"Соседний текст / подпись рядом: «{near}»")
        lines.append(f"Файл в кабинете / CDN: {fn}")
    return lines


def esc(s: str) -> str:
    return html_lib.escape(s or "", quote=True)


def build_html(items: list[dict], summary: dict) -> str:
    by_page: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        by_page[it["path"]].append(it)

    order = ["/caseecomsc", "/xitsadmarketplace", "/clients"]
    rest = sorted(p for p in by_page if p not in order)
    page_order = [p for p in order if p in by_page] + rest

    parts: list[str] = []
    parts.append(
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
    .toc li {{ margin:3px 0; }}
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
    table {{ width:100%; border-collapse:collapse; font-size:13.5px; margin:8px 0; background:#fff; }}
    th,td {{ border:1px solid var(--border); padding:7px 9px; text-align:left; vertical-align:top; }}
    th {{ background:#fafaf8; font-weight:650; }}
  </style>
</head>
<body>
<div class="wrap">
  <h1>Хвост Alt - подписи к картинкам</h1>
  <p class="muted">Срез живого alsn.ru: 23.09.2026 · только Тильда · что ещё пусто после sitewide-брифа</p>
  <div class="pills">
    <span class="pill danger">пусто: {summary['empty']}</span>
    <span class="pill info">страниц: {summary['pages']}</span>
    <span class="pill ok">приоритетные услуги / МП / B2B / лицензии: Alt в норме</span>
    <span class="pill warn">Twitter/Bing SKIP</span>
  </div>
  <div class="callout danger">Каждый шаг - после письменного «да». «Опубликовать» - отдельный шаг. robots.txt не трогать.</div>
  <div class="callout ok">Проверено 23.09.2026: на страницах внедрения, поддержки, МП, B2B, лицензий, about_us, cases и партнёров смысловые Alt уже стоят. Хвост - ленты логотипов на двух кейсах и галереи на «Клиенты».</div>
  <div class="callout info">У каждой картинки ниже: страница + URL, как прокрутить, заголовок секции, тип блока (T594 и др.), номер в ленте, соседний текст, имя файла. Не ориентируйтесь только на имя файла.</div>
  <nav class="toc"><strong>Содержание</strong><ol>
    <li><a href="#status">Что уже сделано</a></li>
    <li><a href="#how">Как ставить Alt</a></li>
"""
    )
    for i, path in enumerate(page_order, 1):
        name = by_page[path][0].get("page_name") or PAGE_NAME.get(path, path)
        parts.append(
            f'    <li><a href="#p-{i}">{esc(name)}</a> <span class="muted">({len(by_page[path])})</span></li>\n'
        )
    parts.append(
        '    <li><a href="#pub">Опубликовать</a></li>\n  </ol></nav>\n'
    )

    parts.append(
        """
<section class="task" id="status">
  <h2><span class="num">0</span> Что уже сделано</h2>
  <p>По срезу 23.09.2026 пустых смысловых Alt <strong>нет</strong> на:</p>
  <ul>
    <li>«Внедрение 1С» (https://alsn.ru/development1c)</li>
    <li>«Внедрение 1С:Комплексная автоматизация» (https://alsn.ru/kompleksnaya_avtomatizaciya)</li>
    <li>«Стоимость внедрения 1С:ERP» (https://alsn.ru/erp-time-price)</li>
    <li>«Техподдержка 1С» (https://alsn.ru/support1c)</li>
    <li>«Интеграция с поставщиками» (https://alsn.ru/ecom)</li>
    <li>«Модуль 1С для маркетплейсов» (https://alsn.ru/casemarketplace)</li>
    <li>«Лицензии 1С», «1С:КП», «1С:Фреш»</li>
    <li>«О компании», «Кейсы», «Битрикс24», «ЦРА»</li>
    <li>Страницы партнёров ЭТМ / Мерлион / OCS / Марвел / Treolan / 3logic</li>
  </ul>
  <p class="muted">Не трогать эти страницы в этой инструкции. SVG-иконки и виджет мессенджера не заполняем.</p>
</section>

<section class="task" id="how">
  <h2>Как ставить Alt</h2>
  <span class="lbl">Обычный блок / лента логотипов</span>
  <ol class="steps">
    <li>Список страниц Тильды → найти адрес из ориентира → карандаш.</li>
    <li>Прокрутить холст по ориентиру (секция → тип блока → номер в ленте / соседний текст).</li>
    <li>Клик по картинке → поле <strong>Alt</strong> / «Альтернативный текст» / «Описание изображения».</li>
    <li>Вставить текст из блока «Копировать Alt» ниже.</li>
    <li>Сохранить блок. Следующую картинку - только после «да» на этот шаг, если правите по одной; в одной ленте можно закрыть все логотипы одним согласованием страницы.</li>
  </ol>
  <div class="path">Список страниц → адрес → ✎ → секция → блок → картинка → Alt → Сохранить</div>
</section>
"""
    )

    alt_i = 0
    for pi, path in enumerate(page_order, 1):
        items_p = by_page[path]
        name = items_p[0].get("page_name") or PAGE_NAME.get(path, path)
        url = items_p[0].get("page_url") or ("https://alsn.ru" + path)
        h1 = items_p[0].get("h1") or name
        parts.append(
            f"""
<section class="task" id="p-{pi}">
  <h2><span class="num">{pi}</span> {esc(name)}</h2>
  <p><strong>Что сделать.</strong> Проставить Alt у пустых смысловых картинок на этой странице ({len(items_p)} шт.).</p>
  <p><strong>Зачем.</strong> Чтобы по поиску и для слабовидящих было понятно, чей логотип или какое письмо на экране, а не «пустая картинка».</p>
  <p class="muted">Страница на сайте: <strong>{esc(h1)}</strong> · <a href="{esc(url)}">{esc(url)}</a> · в Тильде: <code>{esc(path.lstrip('/'))}</code></p>
"""
        )
        if path in ("/caseecomsc", "/xitsadmarketplace"):
            parts.append(
                """
  <div class="callout warn">Все пункты ниже - одна лента логотипов внизу страницы (блок T594), не фото из текста кейса и не обложка сверху. В кабинете кликайте каждый логотип по очереди слева направо.</div>
"""
            )
        if path == "/clients":
            parts.append(
                """
  <div class="callout warn">На «Клиенты» смешаны три типа картинок: лента логотипов, галерея благодарственных писем (сканы) и фото/превью отзывов. Ориентир в каждом пункте разный - читайте список «Где найти» целиком.</div>
"""
            )

        for j, it in enumerate(items_p, 1):
            alt_i += 1
            cid = f"alt-{alt_i}"
            orient = it.get("orient_lines") or []
            li = "".join(f"<li>{esc(line)}</li>" for line in orient)
            parts.append(
                f"""
  <article class="img">
    <h3>{j}. Файл <code>{esc(it['file'])}</code></h3>
    <div class="orient">
      <strong>Где найти на холсте</strong>
      <ul>{li}</ul>
    </div>
    <span class="lbl">Вставить в Alt</span>
    <div class="copybox"><pre id="{cid}">{esc(it.get('expected') or SHARED_ALT.get(it['file'], 'Иллюстрация Аллсан'))}</pre><button type="button" data-copy="{cid}">Копировать Alt</button></div>
  </article>
"""
            )
        parts.append("</section>\n")

    parts.append(
        """
<section class="task" id="pub">
  <h2><span class="num">P</span> Опубликовать</h2>
  <p><strong>Что сделать.</strong> Опубликовать только те страницы, где правили Alt.</p>
  <ol class="steps">
    <li>После письменного «да» - кнопка «Опубликовать» у каждой изменённой страницы.</li>
    <li>«Опубликовать все страницы» не нужно.</li>
  </ol>
</section>
<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-alts-tail-2026-09-23.html</code> · полный бриф: <code>tier2-alts-sitewide-2026-09-21.html</code></p>
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
    data = json.loads(IN_JSON.read_text(encoding="utf-8"))
    items = data["items"]
    paths = sorted({it["path"] for it in items})
    cache: dict[str, tuple[str, list[dict]]] = {}

    enriched = []
    for it in items:
        path = it["path"]
        if path not in cache:
            html = fetch("https://alsn.ru" + path + "?loc=1")
            cache[path] = (html, split_recs(html))
        html, recs = cache[path]
        loc = find_img_in_recs(recs, html, it["file"]) or {}
        # merge
        it2 = dict(it)
        for k in ("section", "near", "block", "rec", "src", "class"):
            if loc.get(k):
                it2[k] = loc[k]
        if loc.get("type") and not it2.get("block"):
            it2["block"] = block_label(loc["type"], loc.get("class") or "")
        it2["index_in_block"] = loc.get("index_in_block") or 0
        it2["logos_in_block"] = loc.get("logos_in_block") or 0
        it2["titles_in_block"] = loc.get("titles_in_block") or []
        if not it2.get("expected"):
            it2["expected"] = SHARED_ALT.get(it2["file"], "Иллюстрация Аллсан")
        it2["orient_lines"] = how_to_find(it2, {**loc, **{k: it2.get(k) for k in ("section", "near", "block", "rec", "class", "type")}})
        # drop resize-only noise for clients if we couldn't find a better src - keep but mark
        enriched.append(it2)
        print(
            path,
            it2["file"],
            "->",
            it2.get("block"),
            it2.get("section", "")[:40],
            f"#{it2.get('index_in_block')}/{it2.get('logos_in_block')}",
        )

    summary = {
        "empty": len(enriched),
        "pages": len({x["path"] for x in enriched}),
        "brief_ok": data.get("summary", {}).get("brief_ok", 0),
        "brief_empty": data.get("summary", {}).get("brief_empty", 0),
    }
    payload = {"date": "2026-09-23", "summary": summary, "items": enriched}
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_HTML.write_text(build_html(enriched, summary), encoding="utf-8")
    print("SUMMARY", summary)
    print("HTML", OUT_HTML)


if __name__ == "__main__":
    main()
