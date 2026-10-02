# -*- coding: utf-8 -*-
"""Инструкция для Тильды: новый дизайн страницы «Интеграция 1С с поставщиками» (alsn.ru/ecom) на стилях v3.

Код блоков берётся из макета preview-ecom-v3.html (build_ecom_v3_preview.py), стили - из эталона 1c-ozon
с префиксом .v3, первый экран в рамке - HERO_CSS. Выход:
  seo-data/tilda-briefs/tier4-ecom-v3-2026-09-30.html
  seo-data/tilda-briefs/_head-ecom-2026-09-30.txt
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_ecom_v3_preview as p  # noqa: E402
from mp_hero_frame import HERO_CSS  # noqa: E402

p.main()
BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
OUT = os.path.join(BR, "tier4-ecom-v3-2026-09-30.html")
HEAD_TXT = os.path.join(BR, "_head-ecom-2026-09-30.txt")
URL = "https://alsn.ru/ecom"
DATE_ISO = "2026-09-30"

src = open(os.path.join(p.SCR, "preview-ecom-v3.html"), encoding="utf-8").read()

# ---------------------------------------------------------------- стили
# prefix_css как в build_mp_ozon_v3_brief.py (тот модуль при импорте сам пишет свою инструкцию)
def prefix_selectors(sel):
    out = []
    for s in (x.strip() for x in sel.split(",")):
        if not s:
            continue
        if s.startswith(".lb"):
            out.append(s)
        elif s in (":root", "body"):
            out.append(".v3")
        elif s == "*":
            out.append(".v3 *")
        else:
            out.append(".v3 " + s)
    return ",".join(out)


def prefix_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    res, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        if head.startswith("@media"):
            depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(css[k], 0)
                k += 1
            res.append(head + "{" + prefix_css(css[j + 1:k - 1]) + "}")
            i = k
        else:
            k = css.find("}", j)
            res.append(prefix_selectors(head) + "{" + css[j + 1:k].strip() + "}")
            i = k + 1
    return "\n".join(res)


ozon_raw = re.search(r"<style>(.*?)</style>", open(p.SRC, encoding="utf-8").read(), re.S).group(1)
extra_plain, extra_v3 = [], []
for line in p.EXTRA_CSS.strip().split("\n"):
    if line.startswith((".mh", ".crumb-bar")):
        continue
    (extra_v3 if ".v3 " in line else extra_plain).append(line)
CSS = "\n".join(
    line for line in prefix_css(ozon_raw + "\n" + "\n".join(extra_plain)).split("\n")
    if not line.startswith((".v3 .head{", ".v3 .head .in{", ".v3 .crumb{"))
)
CSS += "\n" + re.sub(r"/\*.*?\*/", "", HERO_CSS).strip() + "\n" + "\n".join(extra_v3)
assert ".v3 .hf{" in CSS and ".v3 .cmp.sup" in CSS and ".v3 .prices.three .pc{" in CSS and ".lb{" in CSS
assert ".v3 .v3" not in CSS and ".mh" not in CSS


# ---------------------------------------------------------------- блоки
def cut(start, end, keep_end=False):
    i = src.index(start)
    j = src.index(end, i)
    return src[i:j + (len(end) if keep_end else 0)].strip()


hero = cut("<!-- HERO -->", "<!-- BODY -->")
body = cut("<!-- BODY -->", '<section class="final">')
final = cut('<section class="final">', "</section>", keep_end=True)
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
for a, c in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
             ("'[data-zoom]'", "'.v3 [data-zoom]'"), ("'a[data-tab]'", "'.v3 a[data-tab]'")):
    script = script.replace(a, c)

IMGS = [
    ("ВСТАВЬТЕ_ССЫЛКУ_ФОТО_ПАВЛА", p.PHOTO, "Фото Павла Агеева с коммутатором", "seo-data/brand-images/allsun-hero-ecom-suppliers.jpg"),
    ("ВСТАВЬТЕ_ССЫЛКУ_ОБЛОЖКА_XCOM", p.IMG_XCOM, "Обложка видеоотзыва X-COM", "seo-data/brand-images/case-xcom-video-cover.jpg"),
] + [
    (f"ВСТАВЬТЕ_ССЫЛКУ_ЭКРАН_{i}", p.SHOTS + f, title, "seo-data/brand-images/ecom-screens/" + f)
    for i, (f, title) in enumerate(
        [(t[1], f"Экран «{t[3]}» (вкладка «{t[0]}»)") for t in p.TABS]
        + [(e[0], f"Экран «{e[2]}»") for e in p.EXTRA_SHOTS], 1)
]
# загружены в Тильду 30.09.2026 (галерея rec4356795101 на /ecom), сверены с файлами пиксель в пиксель
UPLOADED = {
    "allsun-hero-ecom-suppliers.jpg": "https://static.tildacdn.com/tild6664-3537-4661-b433-666437613864/allsun-hero-ecom-sup.jpg",
    "case-xcom-video-cover.jpg": "https://static.tildacdn.com/tild3163-6538-4435-a432-653937326465/case-xcom-video-cove.jpg",
    "ecom-1c-podbor-nalichie-postavshchik.png": "https://static.tildacdn.com/tild3463-3163-4738-a663-336539303730/ecom-1c-podbor-nalic.png",
    "ecom-1c-rezerv-u-postavshchika.png": "https://static.tildacdn.com/tild3235-3065-4930-a232-633338376531/ecom-1c-rezerv-u-pos.png",
    "ecom-1c-sopostavlenie-nomenklatury.png": "https://static.tildacdn.com/tild6664-6265-4662-b234-373138653364/ecom-1c-sopostavleni.png",
    "ecom-1c-ostatki-po-praysam.png": "https://static.tildacdn.com/tild3035-3531-4462-b931-376532646266/ecom-1c-ostatki-po-p.png",
    "ecom-1c-monitor-zagruzki.png": "https://static.tildacdn.com/tild6434-3561-4231-a461-313439633661/ecom-1c-monitor-zagr.png",
    "ecom-1c-monitoring-avtorezerva.png": "https://static.tildacdn.com/tild6266-6662-4661-b434-313534313062/ecom-1c-monitoring-a.png",
    "ecom-1c-otchet-rezervirovanie.png": "https://static.tildacdn.com/tild3933-3534-4239-a639-653231353966/ecom-1c-otchet-rezer.png",
}
GALLERY_REC = "rec4356795101"
for _, local, _, _ in IMGS:
    url = UPLOADED[local.rsplit("/", 1)[-1]]
    hero, body = hero.replace(local, url), body.replace(local, url)
assert "../../" not in hero + body + final, "остались локальные пути"
assert "ВСТАВЬТЕ" not in hero + body and sum((hero + body).count(u) for u in UPLOADED.values()) >= 9

B1 = f'<div class="v3">\n{hero}\n</div>'
B2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'
B3 = f'<div class="v3">\n{final}\n</div>'


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


FAQ = [(strip_tags(q), strip_tags(a)) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body)]
assert len(FAQ) == 7, len(FAQ)


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


NAME = "Интеграция 1С с поставщиками телеком- и IT-оборудования"
HEAD = "\n".join([
    '<meta name="robots" content="index, follow">',
    ld({
        "@context": "https://schema.org", "@type": "Service", "@id": URL + "#service", "name": NAME,
        "serviceType": "Интеграция 1С с личными кабинетами и API поставщиков", "url": URL,
        "description": "Обмен 1С с ЛК и API поставщиков телеком- и IT-оборудования: остатки, цены и резерв без ручной выгрузки прайса.",
        "provider": {"@id": "https://alsn.ru/#organization"}, "areaServed": {"@type": "Country", "name": "RU"},
        "audience": {"@type": "Audience", "audienceType": "Системные интеграторы и компании, которые торгуют телеком- и IT-оборудованием"},
        "offers": {"@type": "AggregateOffer", "lowPrice": "15645", "highPrice": "208950", "priceCurrency": "RUB", "offerCount": "3"},
    }),
    ld({
        "@context": "https://schema.org", "@type": "WebPage", "@id": URL + "#webpage", "name": NAME,
        "description": "Обмен 1С с личными кабинетами и API поставщиков телеком- и IT-оборудования: остатки, цены и резерв без ручной выгрузки прайса.",
        "url": URL, "inLanguage": "ru-RU", "dateModified": DATE_ISO,
        "isPartOf": {"@type": "WebSite", "@id": "https://alsn.ru/#website"}, "about": {"@id": URL + "#service"},
    }),
    ld({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "@id": URL + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/"},
            {"@type": "ListItem", "position": 2, "name": "Интеграция с поставщиками", "item": URL},
        ],
    }),
    ld({
        "@context": "https://schema.org", "@type": "FAQPage", "@id": URL + "#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    }),
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">',
    "<style>\n" + CSS + "\n</style>",
])

TITLE_OLD = "Интеграция 1С с поставщиками \u2014 телеком и IT | Аллсан"
TITLE_NEW = "Интеграция 1С с поставщиками - телеком и IT | Аллсан"
DESC_OLD = ("Интеграция 1С с поставщиками телеком и IT: обмен остатками, ценами и резервом через ЛК и API. "
            "Без ручной выгрузки прайса. Заявка на консультацию \u2014 Аллсан.")
DESC_NEW = DESC_OLD.replace(" \u2014 ", " - ")

for s in (HEAD, B1, B2, B3, TITLE_NEW, DESC_NEW):
    assert "\u2014" not in s and "\u2013" not in s


def box(cid, text, tpl=False):
    cls = ' class="tpl"' if tpl else ""
    return (f'<div class="copybox"><pre id="{cid}"{cls}>{html.escape(text, quote=False)}</pre>'
            f'<button type="button" data-copy="{cid}">Копировать</button></div>')


def swap(cid, old, new):
    return f'<span class="lbl">Найти</span>\n{box(cid + "f", old)}\n<span class="lbl">Заменить на</span>\n{box(cid + "r", new)}'


OLD_ROWS = [
    ("Первый экран: «Однократная оплата без ежегодного продления!», заголовок «Интеграция 1С с поставщиками телеком- и IT-оборудования», кнопка «Консультация», картинка справа", "обложка с картинкой"),
    ("Форма «Проверьте эффективность и незадействованный потенциал работы 1С», кнопка «Отправить запрос»", "форма"),
    ("Заголовок «Список доступных для интеграции B2B поставщиков, дистрибьютеров, интернет-магазинов»", "заголовок"),
    ("Таблица «Поставщик / Загрузка остатков / Загрузка цен / Резервирование / Снять/поставить в прайс на сайте*» (Марвел, OCS Distribution, Мерлион…)", "HTML-код"),
    ("Кнопка «Заказать консультацию» (первая)", "кнопка"),
    ("«Интеграция 1С с поставщиками телеком- и IT-оборудования по API» и «Что вы получите в результате интеграции…»", "текст с картинкой"),
    ("Заголовок «Получите по-настоящему удобное автоматизированное решение для взаимодействия с поставщиками»", "заголовок"),
    ("Форма «Заказать аудит и расчет проекта», кнопка «Отправить»", "форма"),
    ("«Компании, занятые в интернет-торговле, сталкиваются со сложностью получения актуальных цен…»", "Zero Block"),
    ("«Цены на интеграцию 1С с поставщиками и дистрибьютерами», «Оплата однократная. Без ежегодного продления!»", "карточки цен"),
    ("Кнопка «Заказать консультацию» (вторая)", "кнопка"),
    ("Заголовок «Что дает интеграция 1С с поставщиками по API?»", "заголовок"),
    ("Шесть пунктов «Загрузка номенклатуры», «Загрузка изображений и характеристик»… «Аналитика заказов»", "Zero Block"),
    ("Кнопка «Заказать услугу»", "Zero Block"),
    ("«Отзывы о работе Аллан Интеграция» (с опечаткой в названии), письма клиентов", "отзывы"),
    ("«Отзывы», второй ряд тех же писем", "отзывы"),
    ("Видео «Игорь Роганков рассказал про проекты, с которых началась совместная работа…» (X-COM)", "видео"),
    ("Четыре блока без текста сразу под видео X-COM", "Zero Block ×4"),
    ("Кнопка «Посмотреть клиентов»", "Zero Block"),
]
OLD = ("<table>\n<tr><th>#</th><th>Что на экране сейчас (сверху вниз)</th><th>Тип блока</th></tr>\n"
       + "\n".join(f"<tr><td>{i}</td><td>{html.escape(t, quote=False)}</td><td>{k}</td></tr>" for i, (t, k) in enumerate(OLD_ROWS, 1))
       + "\n</table>")
N_OFF = 22
EXTRA_CSS = ""

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый дизайн страницы «Интеграция 1С с поставщиками» - 30.09.2026</title>
<style>{b.BRIEF_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый дизайн страницы «Интеграция 1С с поставщиками»</h1>
<p class="muted">Страница: «Интеграция 1С с поставщиками телеком- и IT-оборудования» (<a href="{URL}">{URL}</a>, в списке Тильды <code>ecom</code>) · оформление как у «Интеграция 1С с Ozon», первый экран в рамке · блоки сверены с живой страницей 30.09.2026 · каждый шаг после письменного «да» · «Опубликовать» один раз в конце (Е-7)</p>
<div class="pills"><span class="pill ok">макет готов</span><span class="pill ok">картинки загружены</span><span class="pill warn">7 шагов, старое выключаем, не удаляем</span></div>

<div class="callout danger"><strong>Сейчас на живой странице видна галерея из 9 картинок</strong> (фото Павла, обложка X-COM, экраны 1С) сразу под хлебными крошками: её опубликовали вместе с загрузкой. Выключить её - шаг Е-0, первым.</div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-ecom-v3.html">макет страницы</a> (открыть в браузере). Меню сайта, хлебные крошки, форма «Отправьте заявку на расчет», блок «У нас есть решение для:», «Наши клиенты», «Сертификаты», подвал и всплывающие формы остаются как есть. Новое меню сайта делается отдельной инструкцией, здесь его нет.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать: там данные компании, название для превью и счётчики. Меняем только HEAD этой страницы. Старые блоки выключаем, а не удаляем. robots.txt, Bing, Twitter не трогаем. Telegram-бот на сайте остаётся.</div>

<div class="callout warn"><strong>Уже сделано - не трогать:</strong> 30.09.2026 загружены 9 картинок нового дизайна (галерея внизу страницы, адреса уже стоят в коде шагов Е-2 и Е-3, файлы сверены); хлебные крошки T123 «дом / Интеграция с поставщиками» (серый текст на белом, подходят к новому первому экрану); картинка превью для Telegram; ссылки на 13 страниц поставщиков. Задачи T3-1, T3-2, T3-3 из <code>tier3-ecom-postavshiki-2026-09-30.html</code> (частые вопросы на /ecom) перенесены сюда: вопросы теперь внутри блока Е-3, служебный код в Е-1.</div>

<div class="toc"><strong>Шаги</strong><ol start="0">
<li><a href="#e0">Е-0. Выключить галерею с загруженными картинками</a></li>
<li><a href="#e1">Е-1. HEAD страницы целиком одной вставкой</a></li>
<li><a href="#e2">Е-2. Первый экран с фото Павла и лентой дня</a></li>
<li><a href="#e3">Е-3. Основная часть: паспорт и разделы 01-08</a></li>
<li><a href="#e4">Е-4. Последний экран с призывом</a></li>
<li><a href="#e5">Е-5. Выключить {N_OFF} блока прошлой версии</a></li>
<li><a href="#e6">Е-6. Заголовок вкладки и описание: длинное тире на дефис</a></li>
<li><a href="#e7">Е-7. Опубликовать</a></li>
</ol></div>

<section class="task" id="e0">
<h2><span class="num">Е-0</span> Выключить галерею с загруженными картинками</h2>
<span class="lbl">Что сделать</span><p>Выключить блок-галерею с 9 картинками нового дизайна. Не удалять.</p>
<span class="lbl">Зачем</span><p>Галерея опубликована и стоит на самом верху страницы, над старым первым экраном: гости видят подряд фото Павла, обложку видео и скриншоты 1С без подписей. Картинки нужны только как файлы, код нового дизайна берёт их по адресу. Если галерею удалить, Тильда может стереть и файлы, тогда на новой странице будет пусто.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Интеграция 1С с поставщиками телеком- и IT-оборудования» (https://alsn.ru/ecom). Самый верх холста: меню, блок T123 «дом / Интеграция с поставщиками», сразу под ним галерея (в коде сайта {GALLERY_REC}) с фото Павла и экранами 1С. Ниже - старый первый экран «Однократная оплата без ежегодного продления!».</div>
<ol class="steps">
<li>Навести мышь на галерею → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
<li>Чтобы гости перестали видеть галерею сразу, можно опубликовать страницу отдельным шагом прямо сейчас: остальное на странице ещё не менялось. Или дождаться общей публикации в Е-7.</li>
</ol>
</section>

<section class="task" id="e1">
<h2><span class="num">Е-1</span> HEAD страницы целиком одной вставкой</h2>
<span class="lbl">Что сделать</span><p>Стереть всё, что сейчас лежит в HEAD страницы /ecom, и вставить один готовый код.</p>
<span class="lbl">Зачем</span><p>В коде всё оформление нового дизайна и служебные описания для поиска: услуга, страница, хлебные крошки и семь частых вопросов ровно как на экране. Вопросы могут попасть в выдачу под ссылкой, нейросети берут их как готовый ответ. Стили начинаются с <code>.v3</code> и не задевают меню, подвал и формы.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Список страниц → <code>ecom</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопировать старое содержимое поля в блокнот (Ctrl+A, Ctrl+C) и сохранить файл. Это откат. Сейчас там служебный код Service, WebPage и BreadcrumbList: они есть и в новом коде.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{box('e1a', HEAD)}
<p class="muted">Если публикуете не 30.09.2026, в строке <code>"dateModified": "{DATE_ISO}"</code> поставьте дату дня публикации в том же виде ГГГГ-ММ-ДД.</p>
</section>

<section class="task" id="e2">
<h2><span class="num">Е-2</span> Первый экран с фото Павла и лентой дня</h2>
<span class="lbl">Что сделать</span><p>Поставить под хлебными крошками новый первый экран в рамке: заголовок «Интеграция 1С с поставщиками телеком- и IT-оборудования», абзац, кнопки «Получить консультацию» и «От 103 950 ₽», справа фото Павла Агеева с подписью «Павел Агеев · ведущий аналитик 1С, эксперт по интеграциям». Под рамкой серая лента «Как выглядит день с интеграцией» из пяти пунктов.</p>
<span class="lbl">Зачем</span><p>Человек за пять секунд видит, что это за решение, сколько стоит и что оно даёт каждый день. Живой специалист на фото вызывает больше доверия, чем картинка-схема. Кнопка «Получить консультацию» открывает ту же форму, что и сейчас.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Интеграция 1С с поставщиками телеком- и IT-оборудования» (https://alsn.ru/ecom). Самый верх холста: меню, под ним блок T123 со строкой «дом / Интеграция с поставщиками». Новый блок ставим сразу под крошками, выше выключенной галереи из шага Е-0 и старого первого экрана «Однократная оплата без ежегодного продления!».</div>
<ol class="steps">
<li>Навести мышь на нижний край блока крошек → «+» → «Другое» → <strong>T123 «HTML-код»</strong>. Адреса картинок уже стоят в коде, ничего подставлять не нужно.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
{box('e2a', B1)}
</section>

<section class="task" id="e3">
<h2><span class="num">Е-3</span> Основная часть: паспорт и разделы 01-08</h2>
<span class="lbl">Что сделать</span><p>Одним блоком поставить всё остальное: паспорт интеграции сбоку (цена, что загружается, кнопки) и разделы «На какие вопросы отвечает интеграция», «Как идут данные», «Что видно в 1С» (вкладки и отчёты с экранами из инструкции модуля), «Какие поставщики уже подключены» (таблица, 13 поставщиков со своими страницами сверху, остальные под кнопкой), «Результаты клиентов» (кейс ООО «СЦ» и видеоотзыв X-COM), «Кому подходит», «Сколько стоит», «Частые вопросы».</p>
<span class="lbl">Зачем</span><p>Паспорт с ценой едет рядом, пока человек листает страницу, поэтому все разделы должны быть в одном блоке с ним. Экраны 1С открываются во весь экран по клику. Видео открывается в новой вкладке VK Видео, плеер на странице не встраиваем.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага Е-2 → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть». Код длинный, это нормально.</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box('e3a', B2)}
</section>

<section class="task" id="e4">
<h2><span class="num">Е-4</span> Последний экран с призывом</h2>
<span class="lbl">Что сделать</span><p>Поставить серый экран «Подключим ваших поставщиков к 1С»: одна строка пояснения, телефон и кнопка «Получить консультацию».</p>
<span class="lbl">Зачем</span><p>Кто дочитал до конца, получает понятный следующий шаг: прислать список своих поставщиков и узнать цену.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага Е-3 → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box('e4a', B3)}
</section>

<section class="task" id="e5">
<h2><span class="num">Е-5</span> Выключить {N_OFF} блока прошлой версии</h2>
<span class="lbl">Что сделать</span><p>Выключить старые блоки между новым последним экраном из шага Е-4 и формой «Отправьте заявку на расчет».</p>
<span class="lbl">Зачем</span><p>Всё их содержимое теперь есть в новых блоках. Если оставить, на странице будет два главных заголовка, две таблицы поставщиков и два списка цен. Выключенный блок не виден на сайте, но остаётся в редакторе на случай отката.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с поставщиками телеком- и IT-оборудования» (https://alsn.ru/ecom). Первый блок - старый первый экран «Однократная оплата без ежегодного продления!» под новыми блоками и выключенной галереей. Последний - кнопка «Посмотреть клиентов». Сразу под ней форма «Отправьте заявку на расчет. Мы свяжемся с вами в течение 15 минут…» и блок «У нас есть решение для:»: их <strong>не выключать</strong>.</div>
<ol class="steps">
<li>У каждого блока из таблицы → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
<li>Меню, крошки, форму «Отправьте заявку на расчет», «У нас есть решение для:», «Наши клиенты», «Сертификаты», подвал, всплывающие формы и выключенную галерею из шага Е-0 не трогать.</li>
</ol>
{OLD}
</section>

<section class="task" id="e6">
<h2><span class="num">Е-6</span> Заголовок вкладки и описание: длинное тире на дефис</h2>
<span class="lbl">Что сделать</span><p>В заголовке вкладки и в описании страницы заменить длинное тире на обычный дефис. Слова не меняются.</p>
<span class="lbl">Зачем</span><p>Эти строки видны в выдаче Яндекса и Google и под ссылкой в Telegram. Длинное тире выглядит как текст нейросети, дефис читается проще.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Список страниц → <code>ecom</code> → «Настройки» → вкладка «Главное» (или «SEO») → поле «Заголовок» → заменить строку целиком → поле «Описание» → заменить → «Сохранить изменения».</li>
<li>Вкладка «Соцсети» (или «Facebook &amp; SEO») → если там те же строки, заменить так же. Картинку превью не трогать → «Сохранить изменения».</li>
</ol>
<span class="lbl">Заголовок</span>
{swap('e6t', TITLE_OLD, TITLE_NEW)}
<span class="lbl">Описание</span>
{swap('e6d', DESC_OLD, DESC_NEW)}
</section>

<section class="task" id="e7">
<h2><span class="num">Е-7</span> Опубликовать</h2>
<span class="lbl">Что сделать</span><p>Опубликовать страницу «Интеграция 1С с поставщиками телеком- и IT-оборудования».</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Вверху редактора страницы <code>ecom</code> → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано»: проверю живую страницу (один главный заголовок, фото и подпись, вкладки и экраны, таблица поставщиков, видео, кнопки, телефонная версия, служебный код и частые вопросы).</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-ecom-v3-2026-09-30.html</code> · собирает <code>seo-data/scripts/build_ecom_v3_brief.py</code> из макета <code>seo-data/competitors/screens/preview-ecom-v3.html</code> · HEAD отдельно: <code>seo-data/tilda-briefs/_head-ecom-2026-09-30.txt</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

assert "\u2014" not in doc.replace(TITLE_OLD, "").replace(DESC_OLD, "").replace(html.escape(TITLE_OLD, quote=False), "").replace(html.escape(DESC_OLD, quote=False), "")
assert "\u2013" not in doc
open(OUT, "w", encoding="utf-8").write(doc)
open(HEAD_TXT, "w", encoding="utf-8").write(HEAD)
print("ok", OUT, "HEAD", len(HEAD), "B1", len(B1), "B2", len(B2), "B3", len(B3), "FAQ", len(FAQ))
