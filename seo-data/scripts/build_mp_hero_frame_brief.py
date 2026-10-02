# -*- coding: utf-8 -*-
"""Инструкция для Тильды: первый экран «в рамке» на трёх страницах модуля для маркетплейсов.

Берёт живой блок B1 (первый экран + лента дня) с alsn.ru, меняет только <section class="hero"> на .hf,
тексты заголовка, абзаца и кнопок оставляет как на сайте. CSS - из mp_hero_frame.py.
"""
import html
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import mp_hero_frame as hf  # noqa: E402

DATE = "2026-09-30"
OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", f"tier4-mp-hero-frame-{DATE}.html")
CHECK_DIR = os.environ.get("HERO_CHECK_DIR", r"C:\tmp_hub")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36"

PAGES = [
    ("casemarketplace", "Модуль 1С для маркетплейсов"),
    ("1c-ozon", "Интеграция 1С с Ozon"),
    ("1c-wildberries", "Интеграция 1С с Wildberries"),
]
HEADS = {
    "casemarketplace": "_head-casemarketplace-2026-09-28.txt",
    "1c-ozon": "_head-1c-ozon-2026-09-28.txt",
    "1c-wildberries": "_head-1c-wildberries-2026-09-28.txt",
}


def fetch(slug):
    url = f"https://alsn.ru/{slug}?nc={int(time.time())}"
    return subprocess.run(["curl.exe", "-s", "-A", UA, url], capture_output=True, check=True).stdout.decode("utf-8")


def block_b1(page):
    """Содержимое T123 с героем: от <!-- nominify begin --> до <!-- nominify end -->."""
    i = page.index('<section class="hero"')
    s = page.rindex("<!-- nominify begin -->", 0, i) + len("<!-- nominify begin -->")
    e = page.index("<!-- nominify end -->", i)
    rec = re.findall(r'<div id="rec(\d+)"', page[:i])[-1]
    return page[s:e].strip(), rec


def new_hero(sec):
    grab = lambda rx: re.search(rx, sec, re.S).group(0)  # noqa: E731
    eyebrow = grab(r'<div class="eyebrow">.*?</div>')
    h1 = grab(r"<h1>.*?</h1>").replace("<h1>Модуль 1С <br>для ", "<h1>Модуль 1С для <br>")
    lead = grab(r'<p class="lead">.*?</p>')
    btns = grab(r'<div class="btns">.*?</a>\s*</div>')
    alt = re.search(r'<div class="photo">\s*<img[^>]*alt="([^"]*)"', sec).group(1)
    name = re.search(r'<div class="tag"><b>(.*?)</b>', sec).group(1)
    return hf.hero_html(eyebrow, h1, lead, btns, alt, f"<b>{name}</b> · ведущий разработчик модуля"), h1


def check_page(slug, page, sec, hero):
    """Локальная копия живой страницы с новым первым экраном - для скриншотов."""
    p = page.replace(sec, hero, 1)
    p = re.sub(r'(<div id="rec\d+" class="r t-rec" style=")background-color:#[0-9a-fA-F]{6}; ("[^>]*>\s*<!-- T123 -->\s*<div class="t123">\s*<div[^>]*>\s*<div[^>]*>\s*<!-- nominify begin -->\s*<nav aria-label="Хлебные крошки")', r'\1background-color:#ffffff; \2', p)
    k = p.find(".v3 .hero{")
    k = p.index("</style>", k)
    p = p[:k] + "\n" + hf.HERO_CSS + "\n" + p[k:]
    os.makedirs(CHECK_DIR, exist_ok=True)
    open(os.path.join(CHECK_DIR, f"live-{slug}.html"), "w", encoding="utf-8").write(p)


def update_head_txt(slug):
    path = os.path.join(b.ROOT, "seo-data", "tilda-briefs", HEADS[slug])
    t = open(path, encoding="utf-8").read()
    if ".v3 .hf{" in t:
        return
    k = t.rindex("</style>")
    open(path, "w", encoding="utf-8").write(t[:k].rstrip("\n") + "\n" + hf.HERO_CSS + "\n" + t[k:])


data, pages = [], {}
for slug, name in PAGES:
    page = fetch(slug)
    pages[slug] = page
    b1, rec = block_b1(page)
    sec = re.search(r'<section class="hero">.*?</section>', b1, re.S).group(0)
    hero, h1 = new_hero(sec)
    b1_new = b1.replace(sec, hero, 1)
    assert b1_new.count('<section class="hf">') == 1 and '<section class="hero"' not in b1_new
    assert "\u2014" not in hero and "\u2013" not in hero
    check_page(slug, page, sec, hero)
    update_head_txt(slug)
    h1_text = html.unescape(re.sub(r"<[^>]+>", "", h1)).replace("\xa0", " ").strip()
    data.append((slug, name, rec, b1_new, re.sub(r"\s+", " ", h1_text)))

assert "\u2014" not in hf.HERO_CSS and "\u2013" not in hf.HERO_CSS

steps, toc = [], []
n = 0
for slug, name, rec, b1_new, h1_text in data:
    url = f"https://alsn.ru/{slug}"
    n += 1
    toc.append(f'<li><a href="#p{n}">П-{n}. «{name}»: стили первого экрана в HEAD страницы</a></li>')
    steps.append(f"""
<section class="task" id="p{n}">
<h2><span class="num">П-{n}</span> «{name}»: стили первого экрана в HEAD страницы</h2>
<span class="lbl">Что сделать</span><p>Дописать в конец стилей страницы оформление нового первого экрана. Больше в HEAD ничего не менять.</p>
<span class="lbl">Зачем</span><p>Без этих строк новый первый экран из следующего шага развалится: фото не встанет справа, текст не уйдёт влево. Все строки начинаются с <code>.v3 .hf</code> и касаются только первого экрана.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница «{name}» (<a href="{url}">{url}</a>, в списке Тильды <code>{slug}</code>) → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопируйте всё содержимое поля в блокнот (Ctrl+A, Ctrl+C). Это откат.</li>
<li>Прокрутите поле в самый конец. Последняя строка там <code>&lt;/style&gt;</code>. Поставьте курсор <strong>перед</strong> ней, в начало этой строки, нажмите Enter.</li>
<li>В пустую строку над <code>&lt;/style&gt;</code> вставьте код ниже. Строка <code>&lt;/style&gt;</code> должна остаться последней → «Сохранить изменения».</li>
</ol>
{b.copybox(f'p{n}css', hf.HERO_CSS)}
</section>""")
    n += 1
    toc.append(f'<li><a href="#p{n}">П-{n}. «{name}»: новый код первого экрана</a></li>')
    steps.append(f"""
<section class="task" id="p{n}">
<h2><span class="num">П-{n}</span> «{name}»: новый код первого экрана</h2>
<span class="lbl">Что сделать</span><p>Заменить код в блоке первого экрана целиком. Заголовок «{h1_text}», абзац, кнопки и лента «Как выглядит день с модулем» остаются теми же словами, меняется только расположение: текст слева на белом, фото Сергея Никешина справа на всю высоту рамки.</p>
<span class="lbl">Зачем</span><p>Первый экран становится одной рамкой по ширине сайта, как карточка модуля ниже. Фото видно целиком со всеми мониторами, текст его не перекрывает.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «{name}» (<a href="{url}">{url}</a>). Самый верх холста: меню, под ним блок T123 со строкой «дом / {name}». Сразу под ним блок T123 с заголовком «{h1_text}» и кнопкой «Показать на моём кабинете», внизу этого же блока лента «Как выглядит день с модулем». Номер блока на сайте <code>rec{rec}</code>.</div>
<ol class="steps">
<li>Навести мышь на этот блок → «Контент».</li>
<li>Скопируйте старый код в блокнот (Ctrl+A, Ctrl+C). Это откат.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить и закрыть».</li>
<li>Отступы блока не трогать (0 сверху и снизу).</li>
</ol>
{b.copybox(f'p{n}b1', b1_new)}
</section>""")
    crumb = re.search(r'<div id="rec(\d+)"[^>]*data-bg-color="(#[0-9a-fA-F]{6})"[^>]*>\s*<!-- T123 -->(?:(?!<div id="rec).)*?'
                      r'aria-label="Хлебные крошки"', pages[slug], re.S)
    if crumb and crumb.group(2).lower() != "#ffffff":
        n += 1
        toc.append(f'<li><a href="#p{n}">П-{n}. «{name}»: белый фон у хлебных крошек</a></li>')
        steps.append(f"""
<section class="task" id="p{n}">
<h2><span class="num">П-{n}</span> «{name}»: белый фон у хлебных крошек</h2>
<span class="lbl">Что сделать</span><p>Сменить цвет фона блока с хлебными крошками с тёмного <code>{crumb.group(2)}</code> на белый <code>#ffffff</code>. Код блока не трогать.</p>
<span class="lbl">Зачем</span><p>Фон остался от старой тёмной обложки. Под крошками теперь белый первый экран, и тёмная полоса между меню и рамкой выглядит как ошибка вёрстки. Серый текст крошек на белом читается как на страницах Ozon и Wildberries.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «{name}» (<a href="{url}">{url}</a>). Первый блок под меню: T123 со строкой «дом / {name}», номер на сайте <code>rec{crumb.group(1)}</code>.</div>
<ol class="steps">
<li>Навести мышь на блок → «Настройки».</li>
<li>Поле «Цвет фона»: стереть <code>{crumb.group(2)}</code>, вставить значение ниже → «Сохранить и закрыть».</li>
</ol>
{b.copybox(f'p{n}bg', '#ffffff')}
</section>""")

n += 1
toc.append(f'<li><a href="#p{n}">П-{n}. Опубликовать три страницы</a></li>')
steps.append(f"""
<section class="task" id="p{n}">
<h2><span class="num">П-{n}</span> Опубликовать три страницы</h2>
<span class="lbl">Что сделать</span><p>Опубликовать «Модуль 1С для маркетплейсов», «Интеграция 1С с Ozon» и «Интеграция 1С с Wildberries».</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>На каждой из трёх страниц вверху редактора → «Опубликовать».</li>
<li>Написать в чат «опубликовано»: проверю первый экран на компьютере и телефоне.</li>
</ol>
</section>""")

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый первый экран на трёх страницах модуля для маркетплейсов - {DATE[8:10]}.{DATE[5:7]}.{DATE[:4]}</title>
<style>{b.BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый первый экран на трёх страницах модуля для маркетплейсов</h1>
<p class="muted">Страницы: <a href="https://alsn.ru/casemarketplace">«Модуль 1С для маркетплейсов»</a>, <a href="https://alsn.ru/1c-ozon">«Интеграция 1С с Ozon»</a>, <a href="https://alsn.ru/1c-wildberries">«Интеграция 1С с Wildberries»</a> · код собран с живых страниц {DATE[8:10]}.{DATE[5:7]}.{DATE[:4]} · каждый шаг после письменного «да» · «Опубликовать» один раз в конце</p>
<div class="pills"><span class="pill ok">макет согласован</span><span class="pill warn">{n} шагов</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-casemarketplace-hero-e.html">макет первого экрана</a> (открыть в браузере). На каждой странице два действия: дописать стили в HEAD страницы и заменить код одного блока. Картинки загружать не надо, фото уже на сайте. Хлебные крошки, карточка модуля, разделы, витрина, меню и подвал не меняются.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать. В HEAD страницы ничего не стирать, только дописать строки перед последней <code>&lt;/style&gt;</code>. robots.txt, Bing, Twitter не трогаем.</div>

<div class="toc"><strong>Шаги</strong><ol>
{chr(10).join(toc)}
</ol></div>
{''.join(steps)}

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-mp-hero-frame-{DATE}.html</code> · собирает <code>seo-data/scripts/build_mp_hero_frame_brief.py</code>, стили и разметка в <code>seo-data/scripts/mp_hero_frame.py</code> · правило <code>.cursor/rules/tilda-hero-frame.mdc</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

for s in steps:
    assert "\u2014" not in s and "\u2013" not in s
open(OUT, "w", encoding="utf-8").write(doc)
for slug, name, rec, b1_new, h1_text in data:
    print("ok", slug, rec, len(b1_new), h1_text)
print(OUT)
