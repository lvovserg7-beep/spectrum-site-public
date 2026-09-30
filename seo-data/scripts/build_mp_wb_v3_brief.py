# -*- coding: utf-8 -*-
"""Инструкция для Тильды: новый дизайн страницы «Интеграция 1С с Wildberries» на стилях эталона 1c-ozon."""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_mp_ozon_v3_brief as v  # noqa: E402
import build_mp_wb_v3_preview as p  # noqa: E402

p.main()
SRC = p.OUT
OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-1c-wildberries-v3-2026-09-28.html")
HEAD_TXT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "_head-1c-wildberries-2026-09-28.txt")

src = open(SRC, encoding="utf-8").read()

PH_MARGIN = "ВСТАВЬТЕ_ССЫЛКУ_НА_ОТЧЁТ_WB"
IMG_PHOTO = "https://optim.tildacdn.com/tild3632-3333-4139-b730-663861323430/-/format/webp/allsun-hero-mp-emplo.jpg.webp"
IMG_SEO = "https://optim.tildacdn.com/tild6461-3632-4530-b166-373838343431/-/format/webp/ozon-1c-seo-generato.png.webp"
IMG_REVIEWS = "https://static.tildacdn.com/tild3131-6336-4633-b430-376264643262/__.jpg"
IMG_FORECAST = "https://static.tildacdn.com/tild3133-6532-4734-b437-653163333835/noroot.png"
IMG_BARCODE = "https://static.tildacdn.com/tild3736-3964-4631-b164-616539623664/_-01.jpg"
IMG_V_BARCODE = "https://static.tildacdn.com/tild3536-6565-4562-b435-383364353737/______Wildberries__1.jpg"
IMG_V_REVIEWS = "https://static.tildacdn.com/tild3530-3961-4365-b936-323035313561/__-____Wildberries__.jpg"

LOCAL = {
    "../../brand-images/allsun-hero-mp-employee-module.jpg": IMG_PHOTO,
    "../../brand-images/wb-screens/wb-1c-marzha.jpg": PH_MARGIN,
    "../../brand-images/wb-screens/wb-1c-otzyvy-ii.jpg": IMG_REVIEWS,
    "../../brand-images/wb-screens/wb-1c-prognoz-zakupok.png": IMG_FORECAST,
    "../../brand-images/wb-screens/wb-1c-shtrihkody.jpg": IMG_BARCODE,
    "../../brand-images/ozon-screens/ozon-1c-seo-generator.png": IMG_SEO,
    "../../brand-images/case-wb-barcodes-video-cover.jpg": IMG_V_BARCODE,
    "../../brand-images/case-wb-reviews-video-cover.jpg": IMG_V_REVIEWS,
}

css_raw = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
CSS = "\n".join(
    line for line in v.prefix_css(css_raw).split("\n")
    if not line.startswith((".v3 .head{", ".v3 .head .in{", ".v3 .crumb{"))
)
assert ".v3 .vids{" in CSS and ".v3 .pane .shot img.wbm{" in CSS and ".lb{" in CSS


def cut(start, end):
    i = src.index(start)
    return src[i:src.index(end, i)].strip()


hero = cut("<!-- HERO -->", "<!-- BODY -->")
body = cut("<!-- BODY -->", '<section class="final">')
final = cut('<section class="final">', "<script>")
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
for a, c in LOCAL.items():
    hero, body = hero.replace(a, c), body.replace(a, c)
assert "../../" not in hero + body + final, "остались локальные пути"
for a, c in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
             ("'[data-zoom]'", "'.v3 [data-zoom]'"), ("'a[data-tab]'", "'.v3 a[data-tab]'")):
    script = script.replace(a, c)

B1 = f'<div class="v3">\n{hero}\n</div>'
B2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'
B3 = f'<div class="v3">\n{final}\n</div>'


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


FAQ = [(strip_tags(q), strip_tags(a)) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body)]
assert len(FAQ) == 5


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


DESC_OLD = "Модуль Аллсан связывает 1С с Wildberries: остатки и цены, заказы и поставки, отчёты и маржа в 1С. От 40 700 ₽/год. Запишитесь на звонок."
DESC_NEW = "Модуль Аллсан связывает 1С с Wildberries: остатки и цены онлайн, заказы FBO, FBS и DBS в 1С, маржа и ответы на отзывы. От 40 700 ₽/год. Запишитесь на звонок."
LD_DESC = DESC_NEW.replace(" Запишитесь на звонок.", "")
assert len(DESC_NEW) <= 170, len(DESC_NEW)

HEAD = "\n".join([
    '<meta name="robots" content="index, follow">',
    ld({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "dateModified": "2026-09-28",
        "name": "Интеграция 1С с Wildberries",
        "description": LD_DESC,
        "url": "https://alsn.ru/1c-wildberries",
        "inLanguage": "ru-RU",
        "isPartOf": {"@id": "https://alsn.ru/#website"},
    }),
    ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/"},
            {"@type": "ListItem", "position": 2, "name": "Модуль 1С для маркетплейсов", "item": "https://alsn.ru/casemarketplace"},
            {"@type": "ListItem", "position": 3, "name": "Интеграция 1С с Wildberries", "item": "https://alsn.ru/1c-wildberries"},
        ],
    }),
    ld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    }),
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">',
    "<style>\n" + CSS + "\n</style>",
])

for s in (HEAD, B1, B2, B3, DESC_NEW):
    assert "\u2014" not in s and "\u2013" not in s


def tpl_box(cid, text):
    return b.copybox(cid, text).replace(f'<pre id="{cid}"', f'<pre id="{cid}" class="tpl"', 1)


def swap(cid, old, new):
    return (f'<span class="lbl">Найти</span>\n{b.copybox(cid + "f", old)}\n'
            f'<span class="lbl">Заменить на</span>\n{b.copybox(cid + "r", new)}')


EXTRA_CSS = """
.urlrow{display:grid;grid-template-columns:170px 1fr;gap:10px;align-items:center;margin:8px 0}
.urlrow input{width:100%;padding:9px 11px;border:1px solid #cfcfca;border-radius:8px;font:14px ui-monospace,Consolas,monospace}
.urlrow input.ok{border-color:#1a7f4b;background:#e8f6ee}
.urlstate{font-size:13px;margin-top:6px}
"""

TPL_JS = """<script>
(function(){
var A=%s;
var pres=[].slice.call(document.querySelectorAll('pre.tpl'));
pres.forEach(function(p){p._tpl=p.textContent;});
var re=/^https:\\/\\/(static|optim)\\.tildacdn\\.com\\//;
function upd(){
  var a=document.getElementById('u-m').value.trim();
  document.getElementById('u-m').classList.toggle('ok',re.test(a));
  pres.forEach(function(p){p.textContent=p._tpl.split(A).join(a||A);});
  document.getElementById('u-state').textContent=a?'Адрес подставлен в код шага W-3.':'Пока в коде стоит заглушка. Вставьте адрес.';
}
document.getElementById('u-m').addEventListener('input',upd);
upd();
})();
</script>""" % json.dumps(PH_MARGIN, ensure_ascii=False)

OLD = """<table>
<tr><th>Что на экране сейчас (сверху вниз)</th><th>Тип блока</th></tr>
<tr><td>Заголовок «Интеграция 1С с Wildberries» и абзац «Модуль Аллсан синхронизирует вашу 1С с кабинетом Wildberries…»</td><td>заголовок с текстом</td></tr>
<tr><td>Заголовок «Что синхронизируется с Wildberries»</td><td>заголовок</td></tr>
<tr><td>Пять строк «Остатки и цены из 1С в кабинет Wildberries…», «Заказы и подготовка отправлений…»</td><td>текст</td></tr>
<tr><td>Заголовок «Кому подходит»</td><td>заголовок</td></tr>
<tr><td>Абзац «Компаниям с учётом в 1С, которые продают или выходят на Wildberries…»</td><td>текст</td></tr>
<tr><td>Заголовок «Сколько стоит»</td><td>заголовок</td></tr>
<tr><td>Абзац «Подписка на модуль только для Wildberries - от 40 700 ₽…» и кнопка «Купить модуль 1С для Wildberries»</td><td>текст с кнопкой</td></tr>
</table>"""

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый дизайн страницы «Интеграция 1С с Wildberries» - 28.09.2026</title>
<style>{b.BRIEF_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый дизайн страницы «Интеграция 1С с Wildberries»</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-wildberries">https://alsn.ru/1c-wildberries</a> (в списке Тильды <code>1c-wildberries</code>) · оформление как у «Интеграция 1С с Ozon» · блоки сверены с живой страницей 28.09.2026 · каждый шаг после письменного «да» · «Опубликовать» один раз в конце (W-7)</p>
<div class="pills"><span class="pill ok">макет согласован</span><span class="pill warn">8 шагов, старое выключаем, не удаляем</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-1c-wildberries-v3.html">макет страницы</a> (открыть в браузере). Меню сайта, хлебные крошки, «Наши клиенты», сертификаты и подвал остаются как есть.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать: там название компании для превью, счётчики и данные организации. Меняем только HEAD этой страницы. Старые блоки выключаем, а не удаляем: так можно откатиться за минуту. robots.txt, Bing, Twitter не трогаем.</div>

<div class="toc"><strong>Шаги</strong><ol>
<li><a href="#w0">W-0. Загрузить экран отчёта по марже WB</a></li>
<li><a href="#w1">W-1. HEAD страницы целиком одной вставкой</a></li>
<li><a href="#w2">W-2. Первый экран с фото и лентой дня</a></li>
<li><a href="#w3">W-3. Основная часть: паспорт модуля и разделы 01-07</a></li>
<li><a href="#w4">W-4. Заявка внизу страницы</a></li>
<li><a href="#w5">W-5. Выключить семь блоков прошлой версии</a></li>
<li><a href="#w6">W-6. Описание страницы для поиска и для соцсетей</a></li>
<li><a href="#w7">W-7. Опубликовать</a></li>
</ol></div>

<section class="task" id="w0">
<h2><span class="num">W-0</span> Загрузить экран отчёта по марже WB</h2>
<span class="lbl">Что сделать</span><p>Загрузить в Тильду одну картинку и получить её адрес. Остальные картинки (фото Сергея, экраны отзывов, прогноза закупок, штрихкодов, SEO-описаний, обложки двух видео) уже есть на сайте, их грузить не надо.</p>
<span class="lbl">Зачем</span><p>На сайте отчёт по марже лежит одной картинкой вместе с отчётом Ozon. Для страницы Wildberries я вырезал только отчёт WB, чтобы гость не видел чужую площадку.</p>
<table>
<tr><th>Что</th><th>Файл в папке проекта</th></tr>
<tr><td>Экран «Рассчёт рентабельности WB» с оранжевой надписью WB справа</td><td><code>seo-data/brand-images/wb-screens/wb-1c-marzha.jpg</code></td></tr>
</table>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Открыть страницу <code>1c-wildberries</code> на редактирование. В самом низу холста, над подвалом → «+» → «Изображение» → блок <strong>T107</strong>.</li>
<li>В блоке → «Контент» → «Загрузить файл» → выбрать файл → «Сохранить и закрыть».</li>
<li>«Предпросмотр» → правой кнопкой по картинке → «Открыть изображение в новой вкладке» → скопировать адрес. Подойдёт адрес с <code>static.tildacdn.com</code> или <code>optim.tildacdn.com</code>.</li>
<li>Вставить адрес в поле ниже. Он сам подставится в код шага W-3.</li>
<li>Блок T107 → три точки → «Выключить блок». Не удалять, иначе Тильда может убрать файл.</li>
</ol>
<div class="urlrow"><label for="u-m">Адрес отчёта WB</label><input id="u-m" placeholder="https://static.tildacdn.com/tild..../....jpg"></div>
<div class="urlstate" id="u-state"></div>
</section>

<section class="task" id="w1">
<h2><span class="num">W-1</span> HEAD страницы целиком одной вставкой</h2>
<span class="lbl">Что сделать</span><p>Стереть всё, что сейчас лежит в HEAD этой страницы, и вставить один готовый код.</p>
<span class="lbl">Зачем</span><p>Сейчас в HEAD страницы только служебные описания для поисковиков. Новый код содержит их же (с обновлённым описанием, где названы схемы FBO, FBS и DBS), частые вопросы для поисковиков и все стили нового дизайна. Всё в одном месте, как на странице про Ozon. Стили начинаются с <code>.v3</code> и не задевают меню, подвал и другие блоки.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-wildberries</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопируйте старое содержимое поля в блокнот (Ctrl+A, Ctrl+C). Это откат, если что-то пойдёт не так.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{b.copybox('w1a', HEAD)}
</section>

<section class="task" id="w2">
<h2><span class="num">W-2</span> Первый экран с фото и лентой дня</h2>
<span class="lbl">Что сделать</span><p>Поставить под хлебными крошками новый первый экран: заголовок «Интеграция 1С с Wildberries», две кнопки, фото Сергея Никешина с подписью и светлая лента «Как выглядит день с модулем» из пяти пунктов.</p>
<span class="lbl">Зачем</span><p>Первое, что видит человек: о чём страница, что модуль делает каждый день и живой разработчик модуля за работой. Кнопка «Показать на моём кабинете» сразу открывает форму заявки.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Интеграция 1С с Wildberries» (https://alsn.ru/1c-wildberries). Самый верх холста: меню, под ним блок T123 со строкой «дом / Модуль 1С для маркетплейсов / Интеграция 1С с Wildberries». Новый блок ставим сразу под ним, над старым заголовком.</div>
<ol class="steps">
<li>Навести мышь между блоком крошек и старым заголовком «Интеграция 1С с Wildberries» → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
{b.copybox('w2a', B1)}
</section>

<section class="task" id="w3">
<h2><span class="num">W-3</span> Основная часть: паспорт модуля и разделы 01-07</h2>
<span class="lbl">Что сделать</span><p>Одним блоком поставить всё остальное: карточку модуля сбоку (цена, схемы FBO, FBS, DBS, кнопки) и разделы «На какие вопросы отвечает модуль», «Как идут данные», вкладки с экранами 1С и карточки «Ещё в модуле для Wildberries», «Модуль в работе» с двумя видео, «Кому подходит», «Сколько стоит», частые вопросы.</p>
<span class="lbl">Зачем</span><p>Карточка с ценой едет рядом, пока человек листает страницу, поэтому все разделы должны быть в одном блоке с ней. Экраны открываются во весь экран по клику, видео открываются в новом окне VK Видео. Функции, которые для WB ещё в разработке, честно помечены плашкой.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага W-2 → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть». Код длинный, это нормально.</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
<div class="callout warn">Сначала сделайте шаг W-0: в коде должен стоять адрес отчёта, а не слово «ВСТАВЬТЕ_ССЫЛКУ_НА_ОТЧЁТ_WB».</div>
{tpl_box('w3a', B2)}
</section>

<section class="task" id="w4">
<h2><span class="num">W-4</span> Заявка внизу страницы</h2>
<span class="lbl">Что сделать</span><p>Поставить последний экран: «Покажем модуль на вашем кабинете Wildberries», телефон и кнопка «Записаться на демонстрацию».</p>
<span class="lbl">Зачем</span><p>Кто дочитал до конца, получает понятный следующий шаг, не прокручивая наверх.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага W-3 → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{b.copybox('w4a', B3)}
</section>

<section class="task" id="w5">
<h2><span class="num">W-5</span> Выключить семь блоков прошлой версии</h2>
<span class="lbl">Что сделать</span><p>Выключить старые блоки, которые теперь повторяют новые.</p>
<span class="lbl">Зачем</span><p>Иначе на странице будет два заголовка «Интеграция 1С с Wildberries» и всё содержимое дважды. Выключенный блок не виден на сайте, но остаётся в редакторе на случай отката.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Wildberries» (https://alsn.ru/1c-wildberries). Семь блоков подряд сразу под новым блоком из шага W-4, до блока «Наши клиенты».</div>
<ol class="steps">
<li>У каждого блока из таблицы → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
<li>Меню, крошки, «Наши клиенты», «Сертификаты», подвал и выключенный T107 из шага W-0 не трогать.</li>
</ol>
{OLD}
</section>

<section class="task" id="w6">
<h2><span class="num">W-6</span> Описание страницы для поиска и для соцсетей</h2>
<span class="lbl">Что сделать</span><p>Заменить текст описания в двух полях настроек страницы.</p>
<span class="lbl">Зачем</span><p>Это описание Яндекс и Google показывают под заголовком в выдаче, а Telegram и ВКонтакте под картинкой ссылки. В новом тексте названы схемы FBO, FBS и DBS и ответы на отзывы, как на самой странице.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-wildberries</code> → «Настройки» → вкладка «SEO» → поле «Описание» → найти текст и заменить целиком → «Сохранить изменения».</li>
<li>Там же вкладка «Соцсети» (или «Facebook &amp; SEO» / «Социальные сети») → поле «Описание» → тот же текст → «Сохранить изменения». Картинку и заголовок для соцсетей не трогать.</li>
</ol>
{swap('w6', DESC_OLD, DESC_NEW)}
</section>

<section class="task" id="w7">
<h2><span class="num">W-7</span> Опубликовать</h2>
<span class="lbl">Что сделать</span><p>Опубликовать страницу.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Вверху редактора → «Опубликовать».</li>
<li>Написать в чат «опубликовано»: проверю живую страницу (один заголовок, вкладки, экраны, видео, телефонная версия, служебная разметка).</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-wildberries-v3-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_wb_v3_brief.py</code> из макета <code>seo-data/competitors/screens/preview-1c-wildberries-v3.html</code></p>
</div>
{b.COPY_JS}
{TPL_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
open(HEAD_TXT, "w", encoding="utf-8").write(HEAD)
print("ok", OUT, len(HEAD), len(B1), len(B2), len(B3), len(DESC_NEW))
