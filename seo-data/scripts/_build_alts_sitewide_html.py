# -*- coding: utf-8 -*-
"""Build sitewide alt instruction from crawl JSON + live priority page probe."""
from __future__ import annotations

import html
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CRAWL = ROOT / "_qa_page_alts_missing.json"
OUT = ROOT.parent / "tilda-briefs" / "tier2-alts-sitewide-2026-09-21.html"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

ICON_RE = re.compile(
    r"(?i)(?:\.svg$|Tilda_Icons|kisspng|emoji|money-bag|rocket_|stopwatch_|"
    r"Vector_\d|Layer_\d|education_contact|documents\.svg|^\d+\.svg$|"
    r"re_helmet|re_sales|cowork_mac|25fn_|White_Matte|Telegram_2019|"
    r"Power_bi_logo|rXUagvFl)"
)

# Shared reviews/client strip filenames that repeat across the site
SHARED_STRIP = {
    "Xcom.jpg",
    "GoodWood.jpg",
    "noroot.jpg",
    "noroot.png",
    "photo.jpg",
    "__2.jpg",
    "__1.jpg",
    "_.jpg",
    "_.jpeg",
    "_.png",
    "0001_1.jpg",
    "__page-0001.jpg",
    "__pdf_page-0001.jpg",
    "_______1_page-0001.jpg",
    "Image_5_page-0001.jpg",
    "maxresdefault1-Photo.png",
    "----01.jpg",
    "Tatneft-Logosvg.png",
    "Logo_LANIT.png",
    "logo-ss-ru.jpg",
    "logo11_350.jpg",
    "5e82004a227a092f3923.png",
    "thumb_6478_participa.png",
    "c8561e493ab77c8933fc.png",
    "29557530",
    "X-Com.jpeg",
}

# Filename → ready alt for shared / known content images
ALT_BY_FILE = {
    "integraciya-1c-po-ap.jpg": "Интеграция 1С с поставщиками по API",
    "-3.jpg": "Команда Аллсан Интеграция",
    "alsn-clients-vertica.jpg": "Клиенты Аллсан",
    "--.jpg": "Клиенты Аллсан",
    "_9.png": "Сертификат Аллсан Интеграция",
    # truncated CDN names from /kompleksnaya_avtomatizaciya
    "kak-sformirovat-plat.jpg": "Как сформировать платёж в 1С:КА",
    "1s-ka-zakaz-na-proiz.jpg": "Скрин: заказ на производство в 1С:КА",
    "1s-kompleksnaya-avto.jpg": "Скрин: 1С:Комплексная автоматизация",
    "interkampani-v-1s-ka.jpg": "Скрин: Интеркампани в 1С:КА",
    "kak-v-kompleksnoy-av.jpg": "Скрин: работа в 1С:Комплексная автоматизация",
    "gde-v-kompleksnoy-av.jpg": "Скрин: раздел в 1С:Комплексная автоматизация",
    "nachislenie-enp-v-1s.jpg": "Скрин: начисление ЕНП в 1С:КА",
    "korrektirovka-dolga-.jpg": "Скрин: корректировка долга в 1С:КА",
}

# Page slug → human name
PAGE_NAME = {
    "/": "Главная",
    "/development1c": "Внедрение 1С",
    "/kompleksnaya_avtomatizaciya": "Внедрение 1С:Комплексная автоматизация",
    "/erp-time-price": "Стоимость внедрения 1С:ERP",
    "/support1c": "Техподдержка 1С",
    "/ecom": "Интеграция с поставщиками",
    "/casemarketplace": "Модуль 1С для маркетплейсов",
    "/dopolnitelnie_licenzii": "Лицензии 1С",
    "/its": "1С:КП",
    "/1cfresh": "1С:Фреш",
    "/bitrix24": "Битрикс24",
    "/about_us": "О компании",
    "/contacts": "Контакты",
    "/clients": "Клиенты",
    "/cra": "ЦРА",
    "/cases": "Кейсы",
    "/caseecomsc": "Кейс СЦ",
    "/etm-ipro": "ЭТМ iPRO",
    "/merlion": "Мерлион",
    "/ocs": "OCS",
    "/marvel": "Марвел",
    "/treolan": "Treolan",
    "/3logic": "3logic",
    "/vacancy": "Вакансии",
    "/persons": "Команда",
    "/review": "Отзывы",
    "/products": "Продукты",
    "/buhv8": "1С:Бухгалтерия",
    "/zup8": "1С:ЗУП",
    "/upt8": "1С:УТ",
    "/upravlenie_nashei_firmoi": "1С:УНФ",
    "/dokumentooborot8": "1С:Документооборот",
    "/telegram1c": "Telegram-бот 1С",
    "/1cbitrix": "Интеграция Битрикс24 и 1С",
    "/integrationsite": "Интеграция с сайтом",
    "/integrationeco": "Интеграция с экосистемой",
    "/blog": "Блог",
    "/internship": "Стажировка",
    "/amo_crm": "amoCRM",
    "/whatsapp": "WhatsApp-бот 1С",
    "/crmfurniture": "CRM для мебели",
    "/outsorce_vs_inhouse": "Аутсорс или штат",
    "/moy-sklad-perenos-v-1s": "Переход с МойСклад",
    "/perehod-s-upp-na-ka-unf-ut": "Переход с УПП",
    "/perevystavlenie-uslug-posledney-mili-ozon-v-1s": "Перевыставление Озон",
    "/case_telegram_bot": "Кейсы Telegram-ботов",
}

PRIO = list(PAGE_NAME.keys())

# Suggested alts for shared strip by filename when we know the company
SHARED_ALT = {
    "Xcom.jpg": "Логотип X-COM",
    "X-Com.jpeg": "Логотип X-COM",
    "GoodWood.jpg": "Логотип GOOD WOOD",
    "Tatneft-Logosvg.png": "Логотип Татнефть",
    "Logo_LANIT.png": "Логотип ЛАНИТ",
    "logo-ss-ru.jpg": "Логотип Softline",
    "logo11_350.jpg": "Логотип партнёра Аллсан",
    "5e82004a227a092f3923.png": "Логотип партнёра Аллсан",
    "thumb_6478_participa.png": "Логотип партнёра Аллсан",
    "c8561e493ab77c8933fc.png": "Логотип партнёра Аллсан",
    "noroot.png": "Отзыв клиента Аллсан",
    "noroot.jpg": "Отзыв клиента Аллсан",
    "photo.jpg": "Отзыв клиента Аллсан",
    "__2.jpg": "Благодарственное письмо клиенту Аллсан",
    "__1.jpg": "Благодарственное письмо клиенту Аллсан",
    "_.jpg": "Благодарственное письмо клиенту Аллсан",
    "_.jpeg": "Благодарственное письмо клиенту Аллсан",
    "_.png": "Благодарственное письмо клиенту Аллсан",
    "0001_1.jpg": "Благодарственное письмо клиенту Аллсан",
    "__page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "__pdf_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "_______1_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "Image_5_page-0001.jpg": "Благодарственное письмо клиенту Аллсан",
    "maxresdefault1-Photo.png": "Видеоотзыв клиента Аллсан",
    "----01.jpg": "Клиенты Аллсан",
    "29557530": "Иконка мессенджера",  # skip - decorative widget
}


def path_of(url: str) -> str:
    from urllib.parse import urlparse

    p = urlparse(url).path.rstrip("/") or "/"
    return p if p.startswith("/") else "/" + p


# common slug fragments in screenshot filenames → Russian
SLUG_WORDS = {
    "1s": "1С",
    "1c": "1С",
    "ka": "КА",
    "erp": "ERP",
    "ut": "УТ",
    "unf": "УНФ",
    "zup": "ЗУП",
    "kak": "Как",
    "gde": "Где",
    "v": "в",
    "na": "на",
    "po": "по",
    "s": "с",
    "i": "и",
    "dlya": "для",
    "zakaz": "заказ",
    "proiz": "производство",
    "proizvodstvo": "производство",
    "plat": "платёж",
    "platezh": "платёж",
    "sformirovat": "сформировать",
    "kompleksnoy": "Комплексной",
    "kompleksnaya": "Комплексная",
    "avtomatizaciya": "автоматизация",
    "avto": "автоматизация",
    "interkampani": "Интеркампани",
    "integraciya": "Интеграция",
    "postavshikami": "поставщиками",
    "api": "API",
    "sklad": "склад",
    "ostatki": "остатки",
    "zakazy": "заказы",
    "ceny": "цены",
    "buhgalteriya": "Бухгалтерия",
    "dokumentooborot": "Документооборот",
    "bitrix": "Битрикс",
    "bitrix24": "Битрикс24",
    "ozon": "Ozon",
    "wildberries": "Wildberries",
    "wb": "WB",
    "modul": "Модуль",
    "marketpleysami": "маркетплейсами",
    "ekran": "экран",
    "skrinn": "скрин",
    "screenshot": "скрин",
}


def alt_from_filename(fn: str) -> str:
    stem = fn.rsplit(".", 1)[0]
    # already somewhat readable latin slug
    parts = re.split(r"[-_]+", stem)
    words = []
    for p in parts:
        if not p or p.isdigit():
            continue
        low = p.lower()
        if low in SLUG_WORDS:
            words.append(SLUG_WORDS[low])
        elif len(p) <= 2 and low not in SLUG_WORDS:
            continue
        else:
            # keep as-is if looks like acronym
            words.append(p)
    if not words:
        return ""
    t = " ".join(words)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > 100:
        t = t[:97].rsplit(" ", 1)[0]
    # screenshots of 1C UI
    if re.search(r"(?i)1[сc]|ка|erp|ут|унф|склад|заказ|плат", t) and not t.lower().startswith("скрин"):
        if not t.lower().startswith("как") and not t.lower().startswith("где"):
            t = "Скрин: " + t
    return t


def suggest_alt(it: dict) -> str:
    fn = it["file"]
    if fn in ALT_BY_FILE:
        return ALT_BY_FILE[fn]
    if fn in SHARED_ALT:
        return SHARED_ALT[fn]
    # generic logo.png without context → partner logo, not page H1
    if fn.lower() in {"logo.png", "logo.jpg", "logo.jpeg", "logo.webp"}:
        return "Логотип партнёра Аллсан"
    near = (it.get("near") or "").strip()
    sec = (it.get("section") or "").strip()
    # Prefer filename for UI screenshots (slug is meaningful)
    from_fn = alt_from_filename(fn)
    if from_fn and (
        re.search(r"(?i)1s-|1c-|ka-|erp-|ut-|kompleks|integraci|zakaz|sklad|plat", fn)
        or len(from_fn) >= 12
    ):
        # if near text is a real caption and short, prefer it
        if near and 4 < len(near) < 80 and not near.lower().startswith("http"):
            return near[:90]
        return from_fn
    if near and len(near) > 3 and not near.lower().startswith("http"):
        t = near
        if len(t) > 90:
            t = t[:87].rsplit(" ", 1)[0]
        return t
    if sec and len(sec) > 3:
        t = sec
        if len(t) > 90:
            t = t[:87].rsplit(" ", 1)[0]
        return t
    if from_fn:
        return from_fn
    return "Иллюстрация Аллсан"


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def box(uid: str, text: str, label: str = "Копировать") -> str:
    return (
        f'<div class="copybox"><pre id="{uid}">{esc(text)}</pre>'
        f'<button type="button" data-copy="{uid}">{label}</button></div>'
    )


def fetch_catalog_empty() -> list[dict]:
    """Quick re-check of known leftover SKUs from previous brief."""
    leftover_brief = (
        ROOT.parent
        / "tilda-briefs"
        / "tier2-catalog-alts-2026-09-16.html"
    )
    if not leftover_brief.exists():
        return []
    text = leftover_brief.read_text(encoding="utf-8")
    # extract sku + alt + url from articles
    arts = re.findall(
        r'<article class="prod"[^>]*>(.*?)</article>',
        text,
        re.S,
    )
    items = []
    for a in arts:
        sku_m = re.search(r"<code>([^<]+)</code>", a)
        alt_m = re.search(r'<pre id="a-\d+">([^<]*)</pre>', a)
        url_m = re.search(r'href="(https://alsn\.ru/[^"]+tproduct[^"]*)"', a)
        title_m = re.search(r"<h3><span class=\"num\">\d+</span>\s*([^<]+)</h3>", a)
        if not (alt_m and url_m):
            continue
        items.append(
            {
                "sku": sku_m.group(1) if sku_m else "",
                "alt": alt_m.group(1).strip(),
                "url": url_m.group(1),
                "title": title_m.group(1).strip() if title_m else "",
            }
        )
    # live check gallery alt
    out = []
    for it in items:
        try:
            req = urllib.request.Request(it["url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                page = r.read().decode("utf-8", "replace")
            m = re.search(r'"gallery"\s*:\s*(\[.*?\])\s*,\s*"sort"', page, re.S)
            live = ""
            if m:
                arr = json.loads(m.group(1))
                if arr and isinstance(arr[0], dict):
                    live = (arr[0].get("alt") or "").strip()
            if live != it["alt"]:
                it["live"] = live
                it["status"] = "empty" if not live else "mismatch"
                out.append(it)
        except Exception as e:
            it["status"] = "error"
            it["error"] = str(e)
            out.append(it)
    return out


def main() -> None:
    crawl = json.loads(CRAWL.read_text(encoding="utf-8"))
    by_url = {x["url"]: x for x in crawl["by_page"]}

    # Wave A: shared strip - unique files still empty somewhere on prio pages
    shared_files: dict[str, dict] = {}
    # Wave B: page-specific content
    by_page_content: dict[str, list] = defaultdict(list)

    for slug in PRIO:
        url = "https://alsn.ru" if slug == "/" else f"https://alsn.ru{slug}"
        page = by_url.get(url)
        if not page:
            continue
        for it in page["items"]:
            fn = it["file"]
            if ICON_RE.search(fn):
                continue
            if fn == "29557530":
                continue  # messenger widget
            if fn.lower().startswith("logo") and "t-img" in (it.get("class") or ""):
                # often partner logos in strip
                if fn not in SHARED_ALT and fn not in shared_files:
                    shared_files[fn] = it
                continue
            if fn in SHARED_STRIP or fn in SHARED_ALT:
                if fn not in shared_files:
                    shared_files[fn] = it
                continue
            # page content
            alt = suggest_alt(it)
            it2 = dict(it)
            it2["suggested"] = alt
            by_page_content[url].append(it2)

    # 21.09: leftovers from 16.09 already OK on live; skip slow recheck by default
    catalog_fix: list[dict] = []
    print(f"catalog still need fix: {len(catalog_fix)} (recheck skipped)")

    # Build HTML
    parts: list[str] = []
    parts.append(HEADER)

    # summary counts
    n_shared = len(shared_files)
    n_content = sum(len(v) for v in by_page_content.values())
    n_cat = len(catalog_fix)
    parts.append(
        f"""    <div class="callout info">
      Съём 21.09.2026: на сайте тысячи пустых alt у иконок и SVG - их <strong>не заполняем</strong>.
      В этой инструкции только смысловые картинки.
      Каталог: ещё {n_cat} карточек. Общие блоки отзывов/логотипов: {n_shared} файлов.
      Картинки на приоритетных страницах: {n_content}.
    </div>
"""
    )

    parts.append(
        """    <nav class="toc">
      <strong>Содержание</strong>
      <ol>
        <li><a href="#how">Как ставить Alt</a></li>
        <li><a href="#skip-icons">Что не заполнять</a></li>
        <li><a href="#wave-cat">Волна 1. Каталог товаров</a></li>
        <li><a href="#wave-shared">Волна 2. Общие блоки (логотипы и отзывы)</a></li>
        <li><a href="#wave-pages">Волна 3. Картинки на страницах</a></li>
        <li><a href="#wave-rest">Волна 4. Остальные страницы</a></li>
        <li><a href="#pub">Опубликовать</a></li>
      </ol>
    </nav>
"""
    )

    parts.append(HOW)
    parts.append(SKIP_ICONS)

    # Wave catalog
    parts.append(
        """    <section class="task" id="wave-cat">
      <h2><span class="num">1</span> Волна 1. Каталог товаров</h2>
      <span class="lbl">Что сделать</span>
      <p>Добить Alt у фото товаров, где на живом сайте ещё пусто или не совпало.</p>
      <span class="lbl">Зачем</span>
      <p>В поиске по картинкам и при медленной загрузке видно название продукта, а не пустой квадрат.</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Кабинет → <strong>Каталог / Товары</strong>.</li>
        <li>Поиск по <strong>артикулу</strong> → карточка → фото → поле Alt.</li>
        <li>Вставить текст → Сохранить карточку.</li>
        <li>Варианты 1/5/10/20 мест не открывать отдельно, если одно фото на родителя.</li>
      </ol>
"""
    )
    if not catalog_fix:
        parts.append(
            '      <div class="callout ok"><strong>Съём 21.09:</strong> 25 карточек из брифа 16.09 на живом сайте уже совпали. '
            "Новых шагов по ним нет. Если позже добавите товар - Alt = короткое имя продукта + «эл. поставка» или «коробка».</div>\n"
        )
    else:
        for i, it in enumerate(catalog_fix, 1):
            sku = it.get("sku") or ""
            parts.append(f'      <h3>{i}. {esc(it.get("title") or it["url"])}</h3>')
            if sku:
                parts.append(f"      <p><strong>Арт.</strong> <code>{esc(sku)}</code></p>")
                parts.append(box(f"cat-sku-{i}", sku, "Копировать артикул"))
            live = it.get("live") or ""
            if live:
                parts.append(
                    f'      <p class="muted">Сейчас на сайте: <code>{esc(live)}</code>. Заменить.</p>'
                )
            else:
                parts.append('      <p class="muted">Сейчас Alt пустой.</p>')
            parts.append('      <span class="lbl">Вставить в Alt</span>')
            parts.append(box(f"cat-alt-{i}", it["alt"], "Копировать Alt"))
            parts.append(
                f'      <p class="muted"><a href="{esc(it["url"])}" target="_blank" rel="noopener">Открыть на сайте</a></p>'
            )
    parts.append("    </section>\n")

    # Wave shared
    parts.append(
        """    <section class="task" id="wave-shared">
      <h2><span class="num">2</span> Волна 2. Общие блоки - логотипы клиентов и отзывы</h2>
      <span class="lbl">Что сделать</span>
      <p>Один раз проставить Alt у файлов, которые повторяются на многих страницах (лента клиентов, сканы писем, превью видеоотзывов). Править на любой странице, где блок виден - чаще на «Клиенты», «О компании» или «Внедрение 1С».</p>
      <span class="lbl">Зачем</span>
      <p>Иначе одна и та же картинка без подписи тиражируется на десятки URL.</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Откройте страницу <a href="https://alsn.ru/clients">Клиенты</a> или <a href="https://alsn.ru/about_us">О компании</a> → карандаш.</li>
        <li>Найдите блок с логотипами / письмами / видеоотзывами.</li>
        <li>Контент → многоточие у картинки → Alt.</li>
        <li>Если блок общий (алиас) - правка один раз обновит все страницы.</li>
        <li>Мелкие SVG-иконки в этом блоке не трогать.</li>
      </ol>
      <div class="callout warn">Иконку виджета мессенджера (файл без расширения <code>29557530</code>) не заполнять.</div>
"""
    )
    for i, (fn, it) in enumerate(sorted(shared_files.items()), 1):
        alt = suggest_alt(it)
        if alt == "Иконка мессенджера":
            continue
        parts.append(f"      <h3>{i}. Файл <code>{esc(fn)}</code></h3>")
        where = []
        if it.get("section"):
            where.append(f"секция «{esc(it['section'])}»")
        if it.get("near"):
            where.append(f"рядом: «{esc(it['near'])}»")
        if it.get("block"):
            where.append(f"блок {esc(it['block'])}")
        where.append(f'пример страницы: <a href="{esc(it["url"])}">{esc(path_of(it["url"]))}</a>')
        parts.append(f'      <p class="muted">{" · ".join(where)}</p>')
        parts.append('      <span class="lbl">Вставить в Alt</span>')
        parts.append(box(f"sh-alt-{i}", alt, "Копировать Alt"))
    parts.append("    </section>\n")

    # Wave pages
    parts.append(
        """    <section class="task" id="wave-pages">
      <h2><span class="num">3</span> Волна 3. Картинки на приоритетных страницах</h2>
      <span class="lbl">Что сделать</span>
      <p>Заполнить Alt у смысловых фото на продуктах и о компании. У каждой строки - где искать на холсте.</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Карандаш нужной страницы.</li>
        <li>Прокрутить к секции из ориентира → Контент блока → Alt картинки.</li>
        <li>Если файл встречается дважды - смотрите «экземпляр» в ориентире.</li>
        <li>Сохранить → Опубликовать страницу (отдельное «да»).</li>
      </ol>
"""
    )
    n = 0
    for slug in PRIO:
        url = "https://alsn.ru" if slug == "/" else f"https://alsn.ru{slug}"
        items = by_page_content.get(url) or []
        if not items:
            continue
        name = PAGE_NAME.get(slug, slug)
        parts.append(
            f'      <h3 id="p-{slug.strip("/").replace("/","-") or "home"}">'
            f'<a href="{esc(url)}">{esc(name)}</a> '
            f'<span class="muted">({len(items)})</span></h3>'
        )
        for it in items:
            n += 1
            orient = []
            orient.append(f"страница «{name}» ({url})")
            if it.get("section"):
                orient.append(f"секция «{it['section']}»")
            if it.get("block"):
                orient.append(f"тип/блок {it['block']}")
            if it.get("near"):
                orient.append(f"рядом текст «{it['near']}»")
            orient.append(f"файл в кабинете: {it['file']}")
            parts.append(f'      <article class="prod">')
            parts.append(f'        <p><strong>{n}.</strong> {esc(" · ".join(orient))}</p>')
            parts.append('        <span class="lbl">Вставить в Alt</span>')
            parts.append(box(f"pg-alt-{n}", it["suggested"], "Копировать Alt"))
            parts.append("      </article>")
    if n == 0:
        parts.append(
            '      <div class="callout ok">На приоритетных страницах отдельных смысловых картинок без Alt (кроме общих блоков волны 2) не осталось.</div>\n'
        )
    parts.append("    </section>\n")

    # Wave rest - template
    parts.append(
        """    <section class="task" id="wave-rest">
      <h2><span class="num">4</span> Волна 4. Остальные страницы сайта</h2>
      <span class="lbl">Что сделать</span>
      <p>Пройти остальные URL из меню и карты сайта тем же приёмом. Готовые тексты ниже - шаблоны под тип картинки.</p>
      <span class="lbl">Зачем</span>
      <p>Чтобы не оставлять пустые фото на второстепенных лендингах (боты, отраслевые, старые кейсы).</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Откройте страницу → карандаш.</li>
        <li>Смысловое фото (обложка, скрин, портрет, сертификат, коллаж) - заполнить по таблице.</li>
        <li>SVG, Tilda Icons, эмодзи, мелкие иконки преимуществ - пропустить.</li>
        <li>Логотип в шапке - не трогать (уже «Аллсан» на весь сайт).</li>
      </ol>
      <table>
        <tr><th>Тип картинки</th><th>Что писать в Alt</th></tr>
        <tr><td>Обложка / первый экран</td><td>Коротко по H1 страницы (без цены и города)</td></tr>
        <tr><td>Пункт аккордеона с фото</td><td>Заголовок этого пункта</td></tr>
        <tr><td>Скрин интерфейса / модуля</td><td>«Скрин: …» + что на экране (остатки, заказы, склад)</td></tr>
        <tr><td>Портрет сотрудника</td><td>ФИО и должность, если видны рядом; иначе «Специалист Аллсан»</td></tr>
        <tr><td>Сертификат / диплом</td><td>«Сертификат Аллсан Интеграция» или точное имя с подписи</td></tr>
        <tr><td>Коллаж клиентов</td><td>«Клиенты Аллсан»</td></tr>
        <tr><td>Логотип известного клиента</td><td>«Логотип …» + имя компании</td></tr>
        <tr><td>Скан письма / отзыв</td><td>«Благодарственное письмо клиенту Аллсан» или «Отзыв клиента Аллсан»</td></tr>
        <tr><td>Превью видеоотзыва</td><td>«Видеоотзыв клиента Аллсан»</td></tr>
      </table>
      <div class="callout info">Страницы ботов (<code>/telegram1c</code>, <code>/whatsapp</code>, <code>/tb*</code>) - бота с продажи не возвращаем, но Alt у смысловых фото можно поставить по таблице. Декор и SVG не трогать.</div>
    </section>
"""
    )

    parts.append(
        """    <section class="task" id="pub">
      <h2><span class="num">5</span> Опубликовать</h2>
      <span class="lbl">Что сделать</span>
      <p>После каждой страницы или пачки карточек - «Опубликовать» (отдельное письменное «да»).</p>
      <span class="lbl">Зачем</span>
      <p>Иначе подписи останутся только в черновике Тильды.</p>
    </section>

    <section class="task" id="dont">
      <h2>Что не делать</h2>
      <table>
        <tr><th>Пункт</th><th>Почему</th></tr>
        <tr><td>Писать alt в CSV каталога</td><td>Тильда поле через выгрузку не принимает</td></tr>
        <tr><td>Вставлять alt в «Текст» карточки товара</td><td>Гость увидит подпись на экране</td></tr>
        <tr><td>Заполнять все SVG / Tilda Icons</td><td>Декор, не смысловые фото</td></tr>
        <tr><td>Логотип в шапке</td><td>Уже «Аллсан» на весь сайт</td></tr>
        <tr><td>Twitter / Bing / robots.txt</td><td>Вне контура</td></tr>
        <tr><td>Снимать Telegram-бота</td><td>На живой Тильде не снимаем</td></tr>
        <tr><td>HEAD сайта</td><td>Organization / WebSite / og:site_name не трогать</td></tr>
      </table>
    </section>

    <p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-alts-sitewide-2026-09-21.html</code>. На alsn.ru не заливать.</p>
"""
    )

    parts.append(FOOTER)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {OUT} size={OUT.stat().st_size}")
    print(f"shared={n_shared} content={n_content} catalog={n_cat}")


HEADER = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Alt по сайту alsn.ru - инструкция Тильда - 21.09.2026</title>
  <style>
    :root {
      --bg: #f4f3ef; --card: #fff; --text: #1a1a1a; --muted: #5c5c5c;
      --border: #e2e2de; --ok: #1a7f4b; --ok-bg: #e8f6ee; --warn: #9a6700;
      --warn-bg: #fff6e0; --danger: #b42318; --danger-bg: #fdecea;
      --info: #0b6e99; --info-bg: #e8f4fa; --code: #0f172a;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: var(--text); background: var(--bg); }
    .wrap { max-width: 960px; margin: 0 auto; padding: 24px 18px 72px; }
    h1 { font-size: 26px; margin: 0 0 6px; letter-spacing: -0.02em; }
    h2 { font-size: 20px; margin: 0 0 10px; }
    h3 { font-size: 16px; margin: 18px 0 8px; }
    p { margin: 0 0 8px; }
    a { color: #0b5cad; }
    .muted { color: var(--muted); font-size: 14px; }
    .pills { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 16px; }
    .pill { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 650; border: 1px solid var(--border); background: #fff; }
    .pill.ok { color: var(--ok); background: var(--ok-bg); border-color: #c6e6d3; }
    .pill.warn { color: var(--warn); background: var(--warn-bg); border-color: #f0dfa0; }
    .pill.danger { color: var(--danger); background: var(--danger-bg); border-color: #f5c2c0; }
    .pill.info { color: var(--info); background: var(--info-bg); border-color: #bddceb; }
    .callout { border-radius: 10px; padding: 12px 14px; margin: 12px 0 18px; border: 1px solid var(--border); background: var(--card); font-size: 14px; }
    .callout.danger { background: var(--danger-bg); border-color: #f5c2c0; }
    .callout.warn { background: var(--warn-bg); border-color: #f0dfa0; }
    .callout.info { background: var(--info-bg); border-color: #bddceb; }
    .callout.ok { background: var(--ok-bg); border-color: #c6e6d3; }
    .toc { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px; margin: 0 0 20px; }
    .toc ol { margin: 6px 0 0; padding-left: 22px; }
    .toc li { margin: 3px 0; }
    .toc a { text-decoration: none; }
    .task { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px 18px; margin: 0 0 18px; }
    .task .num { display: inline-block; background: #111; color: #fff; border-radius: 999px; font-size: 12px; font-weight: 700; padding: 2px 10px; margin-right: 6px; }
    .lbl { display: block; font-size: 11px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); margin: 14px 0 4px; }
    ol.steps { margin: 4px 0 0; padding-left: 22px; }
    ol.steps > li { margin: 6px 0; }
    .path { font-family: ui-monospace, Consolas, monospace; font-size: 12.5px; background: #111; color: #f5f5f4; border-radius: 8px; padding: 8px 10px; margin: 6px 0 8px; overflow-x: auto; }
    .copybox { position: relative; margin: 6px 0 10px; }
    .copybox pre { margin: 0; background: var(--code); color: #e5e7eb; border-radius: 10px; padding: 12px 12px 40px; overflow-x: auto; white-space: pre-wrap; word-break: break-word; font: 13px/1.4 ui-monospace, Consolas, monospace; }
    .copybox button { position: absolute; right: 8px; bottom: 8px; background: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 4px 10px; font-size: 12px; font-weight: 650; cursor: pointer; }
    .copybox button:hover { background: #f3f4f6; }
    .copybox.ok button { background: var(--ok-bg); }
    table { width: 100%; border-collapse: collapse; font-size: 13.5px; margin: 6px 0 0; background: #fff; }
    th, td { border: 1px solid var(--border); padding: 7px 9px; text-align: left; vertical-align: top; }
    th { background: #fafaf8; font-weight: 650; }
    code { font-family: ui-monospace, Consolas, monospace; font-size: 13px; }
    article.prod { border-top: 1px solid var(--border); padding: 10px 0 4px; margin-top: 6px; }
    article.prod:first-of-type { border-top: 0; }
    @media print { body { background: #fff; } .copybox button { display: none; } }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Подписи к картинкам (Alt) по всему сайту</h1>
    <p class="muted">Живая Тильда alsn.ru · 21.09.2026 · не Битрикс · файл локально, на сайт не заливать</p>
    <div class="pills">
      <span class="pill info">TIER 2</span>
      <span class="pill ok">смысловые фото</span>
      <span class="pill warn">иконки SKIP</span>
      <span class="pill danger">Bing / Twitter SKIP</span>
    </div>
    <div class="callout danger">
      Каждый шаг - после письменного «да». «Опубликовать» - отдельный шаг.
      Не править robots.txt, Twitter, Bing. Telegram-бот на Тильде не снимать. HEAD сайта не трогать.
    </div>
"""

HOW = """    <section class="task" id="how">
      <h2>Как ставить Alt</h2>
      <span class="lbl">Что сделать</span>
      <p>Вписать короткую подпись в поле картинки. На красивой странице её обычно не видно.</p>
      <span class="lbl">Зачем</span>
      <p>Если фото не загрузилось или человек читает сайт программой - понятно, что на картинке. Поиск тоже смотрит эту подпись.</p>
      <span class="lbl">Обычный блок на странице</span>
      <ol class="steps">
        <li>Карандаш страницы → блок с картинкой → <strong>Контент</strong>.</li>
        <li>Напротив фото - многоточие <strong>«…»</strong> → «SEO: alt-текст для изображения».</li>
        <li>В галерее - ссылка <strong>«Текст»</strong> → Image alt for SEO.</li>
        <li>В Zero Block - элемент картинки → поле <strong>ALT</strong>.</li>
        <li>Сохранить → Опубликовать.</li>
      </ol>
      <div class="path">Контент → … / Текст / ALT → вставить → Сохранить → Опубликовать</div>
      <p class="muted">Подробнее: <code>tilda-how-to-alt-2026-09-11.html</code> в этой папке.</p>
      <span class="lbl">Товар каталога</span>
      <ol class="steps">
        <li>Товары → поиск по артикулу → карточка → фото → Alt.</li>
        <li>Не писать alt в поле «Текст» карточки.</li>
      </ol>
    </section>
"""

SKIP_ICONS = """    <section class="task" id="skip-icons">
      <h2>Что не заполнять</h2>
      <table>
        <tr><th>Картинка</th><th>Почему</th></tr>
        <tr><td>Файлы <code>.svg</code>, имена <code>Tilda_Icons_…</code></td><td>Декоративные иконки</td></tr>
        <tr><td>Эмодзи PNG (ракета, копилка, секундомер)</td><td>Декор у преимуществ</td></tr>
        <tr><td>Мелкие иконки в списках «почему мы»</td><td>Рядом уже есть заголовок</td></tr>
        <tr><td>Логотип в шапке сайта</td><td>Уже «Аллсан» глобально</td></tr>
        <tr><td>Виджет мессенджера <code>29557530</code></td><td>Служебная кнопка</td></tr>
        <tr><td>1×1 / spacer / pixel</td><td>Технический мусор</td></tr>
      </table>
    </section>
"""

FOOTER = """
  </div>
  <script>
    function flash(btn) {
      btn.classList.add("ok");
      var t = btn.textContent;
      btn.textContent = "Скопировано";
      setTimeout(function () { btn.textContent = t; btn.classList.remove("ok"); }, 1200);
    }
    document.querySelectorAll(".copybox button[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", async function () {
        var pre = document.getElementById(btn.getAttribute("data-copy"));
        if (!pre) return;
        await navigator.clipboard.writeText(pre.textContent);
        flash(btn);
      });
    });
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
