# -*- coding: utf-8 -*-
"""Live check of sitewide alt brief leftovers with rich location context."""
from __future__ import annotations

import html as html_lib
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
BRIEF = ROOT.parent / "tilda-briefs" / "tier2-alts-sitewide-2026-09-21.html"
OUT_JSON = ROOT / "_alts-tail-live-2026-09-23.json"
OUT_HTML = ROOT.parent / "tilda-briefs" / "tier2-alts-tail-2026-09-23.html"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

ICON_RE = re.compile(
    r"(?i)(?:\.svg$|Tilda_Icons|kisspng|emoji|money-bag|rocket_|stopwatch_|"
    r"Vector_\d|Layer_\d|education_contact|documents\.svg|^\d+\.svg$|"
    r"re_helmet|re_sales|cowork_mac|25fn_|White_Matte|Telegram_2019|"
    r"Power_bi_logo|rXUagvFl|/resize/20x/|/empty/noroot|/libtilda|"
    r"favicon|sprite|1x1|blank|spacer|29557530$)"
)

SHARED_ALT = {
    "----01.jpg": "Клиенты Аллсан",
    "0001_1.jpg": "Благодарственное письмо клиенту Аллсан",
    "5e82004a227a092f3923.png": "Логотип партнёра Аллсан",
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
    "c8561e493ab77c8933fc.png": "Логотип партнёра Аллсан",
    "logo.png": "Логотип партнёра Аллсан",
    "logo-ss-ru.jpg": "Логотип партнёра Аллсан",
    "Logo_LANIT.png": "Логотип ЛАНИТ",
    "logo11_350.jpg": "Логотип партнёра Аллсан",
    "maxresdefault1-Photo.png": "Видеоотзыв клиента Аллсан",
    "noroot.jpg": "Отзыв клиента Аллсан",
    "noroot.png": "Отзыв клиента Аллсан",
    "photo.jpg": "Отзыв клиента Аллсан",
    "thumb_6478_participa.png": "Логотип партнёра Аллсан",
}

# Priority pages to scan deeply (product + cases + company)
PRIORITY = [
    "/development1c",
    "/kompleksnaya_avtomatizaciya",
    "/erp-time-price",
    "/support1c",
    "/ecom",
    "/casemarketplace",
    "/caseecomsc",
    "/xitsadmarketplace",
    "/dopolnitelnie_licenzii",
    "/its",
    "/1cfresh",
    "/about_us",
    "/clients",
    "/bitrix24",
    "/cra",
    "/cases",
    "/etm-ipro",
    "/merlion",
    "/ocs",
    "/marvel",
    "/treolan",
    "/3logic",
]

PAGE_NAME = {
    "/development1c": "Внедрение 1С",
    "/kompleksnaya_avtomatizaciya": "Внедрение 1С:Комплексная автоматизация",
    "/erp-time-price": "Стоимость внедрения 1С:ERP",
    "/support1c": "Техподдержка 1С",
    "/ecom": "Интеграция с поставщиками",
    "/casemarketplace": "Модуль 1С для маркетплейсов",
    "/caseecomsc": "Кейс: интеграция 1С с поставщиками для ООО «СЦ»",
    "/xitsadmarketplace": "Кейс: интеграция 1С с маркетплейсами для ООО «ХИТСАД»",
    "/dopolnitelnie_licenzii": "Лицензии 1С",
    "/its": "1С:КП",
    "/1cfresh": "1С:Фреш",
    "/about_us": "О компании",
    "/clients": "Клиенты",
    "/bitrix24": "Битрикс24",
    "/cra": "ЦРА",
    "/cases": "Кейсы",
    "/etm-ipro": "ЭТМ iPRO",
    "/merlion": "Мерлион",
    "/ocs": "OCS",
    "/marvel": "Марвел",
    "/treolan": "Treolan",
    "/3logic": "3logic",
}

IMG_RE = re.compile(r"<img\b([^>]*)>", re.I | re.S)
ATTR_RE = re.compile(r"""(\w+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
H2_RE = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.I | re.S)
STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")

# Parse brief expected alts: file + page url + alt text
BRIEF_ITEM_RE = re.compile(
    r'файл в кабинете:\s*([^\s<]+).*?</p>\s*'
    r'(?:<p class="muted">.*?</p>\s*)?'
    r'<div class="copybox"><pre id="[^"]+">([^<]+)</pre>',
    re.I | re.S,
)
BRIEF_PAGE_RE = re.compile(
    r'страница\s*[«"]([^»"]+)[»"]\s*\((https://alsn\.ru[^)]+)\)',
    re.I,
)
BRIEF_SHARED_RE = re.compile(
    r'Файл\s*<code>([^<]+)</code>.*?'
    r'(?:пример страницы:\s*<a href="(https://alsn\.ru[^"]+)"[^>]*>.*?</a>)?.*?'
    r'<div class="copybox"><pre id="sh-alt-\d+">([^<]+)</pre>',
    re.I | re.S,
)


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


def nearby_heading(html: str, pos: int) -> str:
    window = html[max(0, pos - 3500) : pos]
    hs = list(re.finditer(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", window, re.I | re.S))
    if not hs:
        return ""
    return textish(hs[-1].group(1))[:140]


def nearby_text(html: str, pos: int) -> str:
    before = html[max(0, pos - 1500) : pos]
    after = html[pos : pos + 1000]
    for chunk in (before, after):
        for pat in (
            r'class="[^"]*(?:t-name|t-card__title|accordion__title|t-title|tn-atom)[^"]*"[^>]*>([^<]{4,120})',
            r"<figcaption[^>]*>(.*?)</figcaption>",
            r"<p[^>]*>([^<]{20,140})</p>",
            r"<li[^>]*>([^<]{10,100})</li>",
        ):
            ms = list(re.finditer(pat, chunk, re.I | re.S))
            if ms:
                t = textish(ms[-1].group(1))
                if t and "aria-label" not in t.lower():
                    return t[:120]
    return ""


def block_hint(html: str, pos: int) -> str:
    window = html[max(0, pos - 1200) : pos + 300]
    m = re.search(r'data-record-type="(\d+)"', window)
    if m:
        return f"T{m.group(1)}"
    m = re.search(r'id="(rec\d+)"', window)
    return m.group(1) if m else ""


def rec_id(html: str, pos: int) -> str:
    window = html[max(0, pos - 2000) : pos]
    ms = list(re.finditer(r'id="(rec\d+)"', window))
    return ms[-1].group(1) if ms else ""


def guess_alt(fn: str, section: str, near: str) -> str:
    if fn in SHARED_ALT:
        return SHARED_ALT[fn]
    low = fn.lower()
    if "logo" in low or "lanit" in low or "tatneft" in low:
        return "Логотип партнёра Аллсан"
    if "xcom" in low or "x-com" in low:
        return "Логотип X-COM"
    if "goodwood" in low:
        return "Логотип GOOD WOOD"
    if "page-0001" in low or "0001" in low:
        return "Благодарственное письмо клиенту Аллсан"
    if "maxresdefault" in low:
        return "Видеоотзыв клиента Аллсан"
    if "noroot" in low or "photo.jpg" in low:
        return "Отзыв клиента Аллсан"
    if section:
        return f"Иллюстрация: {section[:80]}"
    if near:
        return f"Иллюстрация: {near[:80]}"
    return "Иллюстрация Аллсан"


def parse_brief_expected() -> list[dict]:
    raw = BRIEF.read_text(encoding="utf-8")
    items = []
    # page-specific
    for m in re.finditer(
        r'<p><strong>\d+\.</strong>\s*(.*?)</p>\s*<div class="copybox"><pre id="pg-alt-\d+">([^<]+)</pre>',
        raw,
        re.I | re.S,
    ):
        loc = m.group(1)
        alt = textish(m.group(2))
        pm = BRIEF_PAGE_RE.search(loc)
        fm = re.search(r"файл в кабинете:\s*([^\s<]+)", loc, re.I)
        if not pm or not fm:
            continue
        items.append(
            {
                "kind": "page",
                "page_name": pm.group(1).strip(),
                "page_url": pm.group(2).rstrip("/"),
                "file": fm.group(1).strip(),
                "expected": alt,
                "brief_loc": textish(loc)[:200],
            }
        )
    # shared
    for m in BRIEF_SHARED_RE.finditer(raw):
        fn = m.group(1).strip()
        url = (m.group(2) or "https://alsn.ru/clients").rstrip("/")
        alt = textish(m.group(3))
        items.append(
            {
                "kind": "shared",
                "page_name": PAGE_NAME.get(urlparse(url).path or "/", url),
                "page_url": url,
                "file": fn,
                "expected": alt,
                "brief_loc": f"общий файл {fn}",
            }
        )
    return items


def scan_page(path: str) -> list[dict]:
    url = "https://alsn.ru" + path
    html = fetch(url + "?alt=2309")
    h1m = H1_RE.search(html)
    h1 = textish(h1m.group(1)) if h1m else ""
    out = []
    for m in IMG_RE.finditer(html):
        a = attrs(m.group(1))
        src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
        if not src:
            continue
        if src.startswith("//"):
            src = "https:" + src
        fn = basename(src)
        if not fn or ICON_RE.search(fn) or ICON_RE.search(src):
            continue
        # skip tiny thumbs
        if "/resize/20x/" in src or "/empty/" in src and "logo" not in fn.lower():
            # keep logos even from empty/ path
            if "logo" not in fn.lower() and "tatneft" not in fn.lower() and "lanit" not in fn.lower():
                if "/empty/" in src or "/resize/20x/" in src:
                    continue
        alt = (a.get("alt") or "").strip()
        if alt and alt.lower() not in {"image", "img", "фото", "картинка"}:
            continue
        pos = m.start()
        section = nearby_heading(html, pos)
        near = nearby_text(html, pos)
        block = block_hint(html, pos)
        rid = rec_id(html, pos)
        out.append(
            {
                "path": path,
                "page_url": url,
                "page_name": PAGE_NAME.get(path, h1 or path),
                "h1": h1,
                "file": fn,
                "src": src.split("?")[0][:220],
                "alt_now": alt,
                "expected": guess_alt(fn, section, near),
                "section": section,
                "near": near,
                "block": block,
                "rec": rid,
                "class": (a.get("class") or "")[:100],
            }
        )
    return out


def check_brief_item(it: dict, page_cache: dict[str, str]) -> dict | None:
    url = it["page_url"]
    path = urlparse(url).path or "/"
    if path not in page_cache:
        try:
            page_cache[path] = fetch(url + "?alt=brief")
        except Exception as e:
            return {**it, "status": "ERR", "error": str(e)}
    html = page_cache[path]
    fn = it["file"]
    # find img with this filename
    found = False
    live_alt = ""
    pos = -1
    src = ""
    for m in IMG_RE.finditer(html):
        a = attrs(m.group(1))
        s = a.get("src") or a.get("data-original") or a.get("data-src") or ""
        if fn.lower() in s.lower() or basename(s).lower() == fn.lower():
            found = True
            live_alt = (a.get("alt") or "").strip()
            pos = m.start()
            src = s
            break
    if not found:
        # file may be in bgimg style
        if fn.lower() in html.lower():
            # present as background - skip or note
            return {**it, "status": "BG_OR_HIDDEN", "live_alt": ""}
        return {**it, "status": "NOT_ON_EXAMPLE_PAGE", "live_alt": ""}
    ok = live_alt == it["expected"] or (
        live_alt and it["expected"].lower() in live_alt.lower()
    )
    if ok or (live_alt and len(live_alt) >= 8):
        return {**it, "status": "OK", "live_alt": live_alt}
    return {
        **it,
        "status": "EMPTY",
        "live_alt": live_alt,
        "section": nearby_heading(html, pos) if pos >= 0 else "",
        "near": nearby_text(html, pos) if pos >= 0 else "",
        "block": block_hint(html, pos) if pos >= 0 else "",
        "rec": rec_id(html, pos) if pos >= 0 else "",
        "src": src.split("?")[0][:220],
    }


def esc(s: str) -> str:
    return html_lib.escape(s or "", quote=True)


def build_html(leftovers: list[dict], brief_empty: list[dict], summary: dict) -> str:
    # group leftovers by page
    by_page: dict[str, list[dict]] = defaultdict(list)
    for it in leftovers:
        by_page[it["path"]].append(it)

    parts = []
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
    h4 {{ font-size:14px; margin:12px 0 6px; }}
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
    .orient li {{ margin:3px 0; }}
    .copybox {{ position:relative; margin:6px 0 10px; }}
    .copybox pre {{ margin:0; background:var(--code); color:#e5e7eb; border-radius:10px; padding:12px 12px 40px; overflow-x:auto; white-space:pre-wrap; word-break:break-word; font:13px/1.4 ui-monospace,Consolas,monospace; }}
    .copybox button {{ position:absolute; right:8px; bottom:8px; background:#fff; border:1px solid #ccc; border-radius:8px; padding:4px 10px; font-size:12px; font-weight:650; cursor:pointer; }}
    .copybox.ok button {{ background:var(--ok-bg); }}
    table {{ width:100%; border-collapse:collapse; font-size:13.5px; margin:6px 0; background:#fff; }}
    th,td {{ border:1px solid var(--border); padding:7px 9px; text-align:left; vertical-align:top; }}
    th {{ background:#fafaf8; font-weight:650; }}
    article.img {{ border-top:1px solid var(--border); padding:12px 0 6px; margin-top:8px; }}
    article.img:first-of-type {{ border-top:0; }}
    code {{ font-family:ui-monospace,Consolas,monospace; font-size:12.5px; }}
  </style>
</head>
<body>
<div class="wrap">
  <h1>Хвост Alt - подписи к картинкам</h1>
  <p class="muted">Срез живого alsn.ru: 23.09.2026 · только Тильда · смысловые фото (иконки/SVG не трогаем)</p>
  <div class="pills">
    <span class="pill danger">пусто: {summary['empty']}</span>
    <span class="pill info">страниц: {summary['pages']}</span>
    <span class="pill ok">из брифа уже ок: {summary['brief_ok']}</span>
    <span class="pill warn">Twitter/Bing SKIP</span>
  </div>
  <div class="callout danger">Каждый шаг - после письменного «да». «Опубликовать» - отдельно. robots.txt не трогать.</div>
  <div class="callout ok">Каталог товаров (карточки) по leftover 17.09 - в основном закрыт. Этот хвост - обычные страницы и ленты логотипов/отзывов.</div>
  <div class="callout info">Ориентир для каждой картинки: имя страницы + URL, заголовок секции рядом, тип блока (T594 / T107 / …), соседний текст, имя файла в кабинете.</div>
  <nav class="toc"><strong>Содержание</strong><ol>
    <li><a href="#how">Как ставить Alt</a></li>
    <li><a href="#skip">Что не заполнять</a></li>
"""
    )
    n = 1
    for path in sorted(by_page.keys()):
        name = PAGE_NAME.get(path, path)
        parts.append(
            f'    <li><a href="#p-{n}">{esc(name)}</a> <span class="muted">({len(by_page[path])})</span></li>\n'
        )
        n += 1
    parts.append(
        '    <li><a href="#pub">Опубликовать</a></li>\n  </ol></nav>\n'
    )

    parts.append(
        """
<section class="task" id="how">
  <h2><span class="num">0</span> Как ставить Alt</h2>
  <span class="lbl">Обычный блок / Zero Block</span>
  <ol class="steps">
    <li>Открыть страницу в списке Тильды по адресу из ориентира → карандаш.</li>
    <li>Найти картинку по ориентиру (секция → тип блока → соседний текст).</li>
    <li>Клик по картинке → поле <strong>Alt</strong> / «Альтернативный текст» / «Описание изображения».</li>
    <li>Вставить текст из блока «Копировать Alt».</li>
    <li>Сохранить блок.</li>
  </ol>
  <span class="lbl">Лента логотипов T594 / карусель</span>
  <ol class="steps">
    <li>Прокрутить к заголовку «Наши клиенты» (или «Клиенты»).</li>
    <li>Клик по каждому логотипу по очереди → Alt.</li>
    <li>Если бренд на логотипе читается - можно имя бренда; иначе текст из таблицы.</li>
  </ol>
  <div class="path">Список страниц → адрес → ✎ → блок → картинка → Alt → Сохранить</div>
</section>

<section class="task" id="skip">
  <h2>Что не заполнять</h2>
  <ul>
    <li>SVG-иконки, Vector_*, kisspng, emoji, мелкие иконки кнопок.</li>
    <li>Миниатюры <code>/resize/20x/</code> без смысла.</li>
    <li>Иконка виджета мессенджера <code>29557530</code>.</li>
    <li>Карточки каталога <code>tproduct</code> - отдельный бриф, здесь не трогаем.</li>
  </ul>
</section>
"""
    )

    idx = 1
    alt_i = 0
    for path in sorted(by_page.keys(), key=lambda p: (0 if p in ("/caseecomsc", "/xitsadmarketplace", "/clients", "/development1c") else 1, p)):
        items = by_page[path]
        name = items[0]["page_name"]
        url = items[0]["page_url"]
        h1 = items[0].get("h1") or name
        parts.append(
            f"""
<section class="task" id="p-{idx}">
  <h2><span class="num">{idx}</span> {esc(name)}</h2>
  <p class="muted">Страница на сайте: <strong>{esc(h1)}</strong> · <a href="{esc(url)}">{esc(url)}</a> · адрес в Тильде: <code>{esc(path.lstrip('/') or 'главная')}</code></p>
  <p class="muted">Пустых смысловых картинок на срезе: <strong>{len(items)}</strong></p>
"""
        )
        for j, it in enumerate(items, 1):
            alt_i += 1
            cid = f"alt-{alt_i}"
            block = it.get("block") or "блок на холсте"
            section = it.get("section") or "(секция без H2 рядом - смотрите соседний текст)"
            near = it.get("near") or "(соседнего текста рядом с тегом картинки мало - ориентируйтесь на секцию и файл)"
            rec = it.get("rec") or ""
            parts.append(
                f"""
  <article class="img">
    <h3>{j}. Файл <code>{esc(it['file'])}</code></h3>
    <div class="orient">
      <strong>Где найти на холсте</strong>
      <ul>
        <li>Страница: {esc(name)} (<a href="{esc(url)}">{esc(url)}</a>)</li>
        <li>Заголовок секции рядом: <strong>{esc(section)}</strong></li>
        <li>Тип блока: <strong>{esc(block)}</strong>{(' · id ' + esc(rec)) if rec else ''}</li>
        <li>Соседний текст / подпись рядом: <em>{esc(near)}</em></li>
        <li>Имя файла в кабинете / CDN: <code>{esc(it['file'])}</code></li>
      </ul>
    </div>
    <span class="lbl">Вставить в Alt</span>
    <div class="copybox"><pre id="{cid}">{esc(it['expected'])}</pre><button type="button" data-copy="{cid}">Копировать Alt</button></div>
  </article>
"""
            )
        parts.append("</section>\n")
        idx += 1

    parts.append(
        """
<section class="task" id="pub">
  <h2><span class="num">P</span> Опубликовать</h2>
  <ol class="steps">
    <li>После письменного «да» - опубликовать каждую страницу, где правили Alt.</li>
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
    print("Scanning priority pages…")
    leftovers: list[dict] = []
    for path in PRIORITY:
        try:
            items = scan_page(path)
            leftovers.extend(items)
            print(f"  {path}: {len(items)} empty meaningful")
        except Exception as e:
            print(f"  {path}: ERR {e}")

    # dedupe by path+file+section
    seen = set()
    uniq = []
    for it in leftovers:
        key = (it["path"], it["file"], it.get("section", ""), it.get("block", ""))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(it)
    leftovers = uniq

    brief_ok = 0
    brief_empty = []
    if BRIEF.exists():
        print("Checking brief expected…")
        expected = parse_brief_expected()
        cache: dict[str, str] = {}
        for it in expected:
            if it["file"] == "29557530":
                continue
            rec = check_brief_item(it, cache)
            if not rec:
                continue
            if rec.get("status") == "OK":
                brief_ok += 1
            elif rec.get("status") == "EMPTY":
                brief_empty.append(rec)
                # merge into leftovers if not already
                path = urlparse(it["page_url"]).path or "/"
                leftovers.append(
                    {
                        "path": path,
                        "page_url": it["page_url"],
                        "page_name": it["page_name"],
                        "h1": it["page_name"],
                        "file": it["file"],
                        "src": rec.get("src", ""),
                        "alt_now": rec.get("live_alt", ""),
                        "expected": it["expected"],
                        "section": rec.get("section", ""),
                        "near": rec.get("near", ""),
                        "block": rec.get("block", ""),
                        "rec": rec.get("rec", ""),
                        "class": "",
                        "from_brief": True,
                    }
                )

    # dedupe again preferring expected from brief
    by_key: dict[tuple, dict] = {}
    for it in leftovers:
        key = (it["path"], it["file"])
        prev = by_key.get(key)
        if not prev or it.get("from_brief"):
            by_key[key] = it
    leftovers = list(by_key.values())
    leftovers.sort(key=lambda x: (x["path"], x["file"]))

    summary = {
        "empty": len(leftovers),
        "pages": len({x["path"] for x in leftovers}),
        "brief_ok": brief_ok,
        "brief_empty": len(brief_empty),
    }
    payload = {"date": "2026-09-23", "summary": summary, "items": leftovers}
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    html = build_html(leftovers, brief_empty, summary)
    OUT_HTML.write_text(html, encoding="utf-8")
    print("SUMMARY", summary)
    print("JSON", OUT_JSON)
    print("HTML", OUT_HTML)


if __name__ == "__main__":
    main()
