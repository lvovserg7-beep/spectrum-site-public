# -*- coding: utf-8 -*-
"""Инструкция для Тильды: новый дизайн страницы «Модуль 1С для маркетплейсов» (casemarketplace) на стилях эталона 1c-ozon."""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_mp_ozon_v3_brief as v  # noqa: E402
import build_mp_hub_v3_preview as p  # noqa: E402

p.main()
SRC = p.OUT
OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-casemarketplace-v3-2026-09-28.html")
HEAD_TXT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "_head-casemarketplace-2026-09-28.txt")

src = open(SRC, encoding="utf-8").read()

css_raw = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
CSS = "\n".join(
    line for line in v.prefix_css(css_raw).split("\n")
    if not line.startswith((".v3 .head{", ".v3 .head .in{", ".v3 .crumb{"))
)
assert ".v3 .team{" in CSS and ".v3 .cmp{" in CSS and ".v3 .prices.three{" in CSS and ".lb{" in CSS


def cut(start, end):
    i = src.index(start)
    return src[i:src.index(end, i)].strip()


hero = cut("<!-- HERO -->", "<!-- BODY -->")
body = cut("<!-- BODY -->", "<!-- SHOWCASE -->")
final = cut('<section class="final">', "<script>")
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
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
assert len(FAQ) == 8, len(FAQ)


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


URL = "https://alsn.ru/casemarketplace"
DESC_OLD = "Модуль Аллсан связывает 1С с Wildberries: остатки и цены, заказы и поставки, отчёты и маржа в 1С. От 40 700 ₽/год. Запишитесь на звонок."
DESC_NEW = "Модуль Аллсан связывает 1С с Ozon и Wildberries: остатки и цены, заказы по всем схемам, маржа за каждый день и ответы на отзывы. От 40 700 ₽/год."
LD_DESC = DESC_NEW
assert len(DESC_NEW) <= 170, len(DESC_NEW)

HEAD = "\n".join([
    '<meta name="robots" content="index, follow">',
    ld({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "dateModified": "2026-09-28",
        "name": "Модуль 1С для маркетплейсов",
        "description": LD_DESC,
        "url": URL,
        "inLanguage": "ru-RU",
        "isPartOf": {"@id": "https://alsn.ru/#website"},
        "about": {"@id": URL + "#module"},
    }),
    ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/"},
            {"@type": "ListItem", "position": 2, "name": "Модуль 1С для маркетплейсов", "item": URL},
        ],
    }),
    ld({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "@id": URL + "#module",
        "name": "Модуль интеграции 1С с маркетплейсами Ozon и Wildberries",
        "description": "Обмен остатками, ценами и заказами между 1С и Ozon, Wildberries. Схемы Ozon FBO, FBS, rFBS, DBS, схемы Wildberries FBO, FBS, DBS. Ежедневная маржа, кластеры, прогноз закупок, ответы на отзывы с ИИ.",
        "url": URL,
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "1C:Enterprise 8.3",
        "offers": {"@type": "AggregateOffer", "lowPrice": "40700", "highPrice": "69990", "priceCurrency": "RUB", "offerCount": "3"},
        "provider": {"@id": "https://alsn.ru/#organization"},
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

NDS_OLD = "Цены с НДС за год. Стоимость внедрения уточняем на звонке: она зависит от доработок вашей 1С."
NDS_NEW = "Цены с НДС 5% за год. Стоимость внедрения уточняем на звонке: она зависит от доработок вашей 1С."

for s in (HEAD, B1, B2, B3, DESC_NEW, NDS_NEW):
    assert "\u2014" not in s and "\u2013" not in s


def swap(cid, old, new):
    return (f'<span class="lbl">Найти</span>\n{b.copybox(cid + "f", old)}\n'
            f'<span class="lbl">Заменить на</span>\n{b.copybox(cid + "r", new)}')


OLD = """<table>
<tr><th>#</th><th>Что на экране сейчас (сверху вниз)</th><th>Тип блока</th></tr>
<tr><td>1</td><td>Заголовок «Модуль интеграции 1С с маркетплейсами Ozon и Wildberries»</td><td>заголовок</td></tr>
<tr><td>2</td><td>Обложка «Совместимо с 1С:УТ, УНФ (1.6,3.0), КА, ERP» и абзац «Интеграция 1С с Ozon и Wildberries: остатки, заказы и юнит-экономика…»</td><td>обложка</td></tr>
<tr><td>3</td><td>Кнопка «Хочу демонстрацию» (первая из трёх)</td><td>кнопка</td></tr>
<tr><td>4</td><td>Заголовок «Возможности модуля интеграции 1С с OZON и Wildberries» с подписью «…БЕСПЛАТНО!»</td><td>заголовок</td></tr>
<tr><td>5</td><td>Таблица «Функция модуля / OZON / WB» с галочками</td><td>таблица</td></tr>
<tr><td>6</td><td>Строка «Примечание: Модуль интеграции маркетплейсов совместим с конфигурациями…»</td><td>текст</td></tr>
<tr><td>7</td><td>Заголовок «Частые вопросы о модуле интеграции 1С с маркетплейсами»</td><td>заголовок</td></tr>
<tr><td>8</td><td>Вопросы и ответы «Вопрос: С какими конфигурациями 1С совместим модуль…»</td><td>вопросы-ответы</td></tr>
<tr><td>9</td><td>Кнопка «Хочу демонстрацию» (вторая)</td><td>кнопка</td></tr>
<tr><td>10</td><td>Заголовок «Обзор уникальных функций модуля интеграции 1С с маркетплейсами»</td><td>заголовок</td></tr>
<tr><td>11</td><td>Аккордеон, первый пункт «Бесплатное добавление новых функций»</td><td>аккордеон T585</td></tr>
<tr><td>12</td><td>«Кто внедряет модуль» с семью фото (Сергей Львов, Павел Агеев…)</td><td>команда</td></tr>
<tr><td>13</td><td>Заголовок «Стоимость модуля интеграции 1С с маркетплейсами»</td><td>заголовок</td></tr>
<tr><td>14</td><td>Три карточки «40 700 р/год OZON», «40 700 р/год WB», «69 990 р/год» с зачёркнутыми 49 000 и 79 000</td><td>карточки цен</td></tr>
<tr><td>15</td><td>Текст «Цены представлены с учётом 5% НДС. * После окончания годовой подписки…»</td><td>текст</td></tr>
<tr><td>16</td><td>«Реализованные проекты» (ПЭК, «Как сократить ФОТ на 1 млн руб. в год?»…)</td><td>карточки кейсов</td></tr>
<tr><td>17</td><td>Заголовок «У вас ещё нет 1С? Тогда выбирайте решение "под ключ"»</td><td>заголовок</td></tr>
<tr><td>18</td><td>Блок «Тариф "под ключ"» с текстом «Для выхода на маркетплейсы "с нуля"…»</td><td>текст с картинкой</td></tr>
<tr><td>19</td><td>Пустой блок сразу под ним (на сайте без текста)</td><td>T126 / разделитель</td></tr>
<tr><td>20</td><td>«Что вы ещё получите»: «Бесплатная техподдержка», «Будет работать всегда»…</td><td>преимущества</td></tr>
<tr><td>21</td><td>Заголовок «Варианты техподдержки интеграции 1С с маркетплейсами»</td><td>заголовок</td></tr>
<tr><td>22</td><td>Аккордеон, первый пункт «Бесплатная техподдержка»</td><td>аккордеон T585</td></tr>
<tr><td>23</td><td>Кнопка «Хочу демонстрацию» (третья)</td><td>кнопка</td></tr>
<tr><td>24</td><td>Галерея «Благодарности за внедрение»</td><td>галерея</td></tr>
<tr><td>25</td><td>Заголовок «Видеоотзыв о внедрении»</td><td>заголовок</td></tr>
<tr><td>26</td><td>«Внедрение модуля в магазине ЭкоТайди: с 0 до 20 000 000 за 6 месяцев»</td><td>видео с текстом</td></tr>
<tr><td>27</td><td>Галерея «Видеоинструкции»</td><td>галерея</td></tr>
<tr><td>28</td><td>Заголовок «Тарифы "Под ключ" для выхода на маркетплейсы "с нуля": 1С + модуль»</td><td>заголовок</td></tr>
<tr><td>29</td><td>«Тариф СТАРТ. Идеально для ИП, малого и среднего бизнеса»</td><td>заголовок с текстом</td></tr>
<tr><td>30</td><td>Аккордеон, первый пункт «1С:УНФ или 1С:УТ»</td><td>аккордеон T585</td></tr>
<tr><td>31</td><td>«Тариф ПРОФИ. Оптимальный тариф для тех, кто дорос…»</td><td>заголовок с текстом</td></tr>
<tr><td>32</td><td>Аккордеон, первый пункт «1С:Комплексная автоматизация 8»</td><td>аккордеон T585</td></tr>
<tr><td>33</td><td>Кнопка «Узнать цены»</td><td>кнопка</td></tr>
</table>"""

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый дизайн страницы «Модуль 1С для маркетплейсов» - 28.09.2026</title>
<style>{b.BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый дизайн страницы «Модуль 1С для маркетплейсов»</h1>
<p class="muted">Страница: <a href="https://alsn.ru/casemarketplace">https://alsn.ru/casemarketplace</a> (в списке Тильды <code>casemarketplace</code>) · оформление как у «Интеграция 1С с Ozon» · блоки сверены с живой страницей 28.09.2026 · каждый шаг после письменного «да» · «Опубликовать» один раз в конце (М-9)</p>
<div class="pills"><span class="pill ok">макет согласован</span><span class="pill warn">9 шагов, старое выключаем, не удаляем</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-casemarketplace-v3.html">макет страницы</a> (открыть в браузере). Меню сайта, хлебные крошки, витрина с корзиной «Цены на модули интеграции 1С с маркетплейсами», «Полезные страницы по модулю», форма «Остались вопросы?», «Наши клиенты», сертификаты и подвал остаются как есть. Картинки загружать не надо: все фото и экраны уже лежат на сайте.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать: там название компании для превью, счётчики и данные организации. Меняем только HEAD этой страницы. Витрину с корзиной не трогать: от неё зависят карточки товаров. Старые блоки выключаем, а не удаляем. robots.txt, Bing, Twitter не трогаем.</div>

<div class="toc"><strong>Шаги</strong><ol>
<li><a href="#m1">М-1. HEAD страницы целиком одной вставкой</a></li>
<li><a href="#m2">М-2. Первый экран с фото и лентой дня</a></li>
<li><a href="#m3">М-3. Основная часть: паспорт модуля и разделы 01-08</a></li>
<li><a href="#m4">М-4. Выключить 33 блока прошлой версии</a></li>
<li><a href="#m5">М-5. Заявка под витриной</a></li>
<li><a href="#m6">М-6. Описание страницы для поиска и для соцсетей</a></li>
<li><a href="#m7">М-7. НДС 5% на странице «Интеграция 1С с Ozon»</a></li>
<li><a href="#m8">М-8. НДС 5% на странице «Интеграция 1С с Wildberries»</a></li>
<li><a href="#m9">М-9. Опубликовать три страницы</a></li>
</ol></div>

<section class="task" id="m1">
<h2><span class="num">М-1</span> HEAD страницы целиком одной вставкой</h2>
<span class="lbl">Что сделать</span><p>Стереть всё, что сейчас лежит в HEAD этой страницы, и вставить один готовый код.</p>
<span class="lbl">Зачем</span><p>Сейчас в HEAD страницы старые частые вопросы, которые не совпадают с новыми, и описание модуля без схем продаж. Новый код содержит служебные описания страницы и модуля, восемь частых вопросов ровно как на экране и все стили нового дизайна. Стили начинаются с <code>.v3</code> и не задевают меню, подвал, витрину и другие блоки.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>casemarketplace</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопируйте старое содержимое поля в блокнот (Ctrl+A, Ctrl+C). Это откат, если что-то пойдёт не так.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{b.copybox('m1a', HEAD)}
</section>

<section class="task" id="m2">
<h2><span class="num">М-2</span> Первый экран с фото и лентой дня</h2>
<span class="lbl">Что сделать</span><p>Поставить под хлебными крошками новый первый экран: заголовок «Модуль 1С для маркетплейсов», две кнопки, фото Сергея Никешина с подписью и светлая лента «Как выглядит день с модулем» из пяти пунктов.</p>
<span class="lbl">Зачем</span><p>Человек сразу видит, что модуль работает с обеими площадками и что он даёт каждый день. Кнопка «Показать на моём кабинете» открывает форму заявки.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Модуль 1С для маркетплейсов» (https://alsn.ru/casemarketplace). Самый верх холста: меню, под ним блок T123 со строкой «дом / Модуль 1С для маркетплейсов». Новый блок ставим сразу под ним, над старым заголовком «Модуль интеграции 1С с маркетплейсами Ozon и Wildberries».</div>
<ol class="steps">
<li>Навести мышь между блоком крошек и старым заголовком → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
{b.copybox('m2a', B1)}
</section>

<section class="task" id="m3">
<h2><span class="num">М-3</span> Основная часть: паспорт модуля и разделы 01-08</h2>
<span class="lbl">Что сделать</span><p>Одним блоком поставить всё остальное: карточку модуля сбоку (цена, схемы Ozon и WB, кнопки) и разделы «На какие вопросы отвечает модуль», «Как идут данные», «Что умеет модуль» (вкладки с экранами и таблица функций Ozon / WB), «Отзывы клиентов» с видео и письмом, «Кому подходит», «Кто внедряет модуль» с фото команды, «Сколько стоит» с техподдержкой и тарифами «под ключ», частые вопросы.</p>
<span class="lbl">Зачем</span><p>Карточка с ценой едет рядом, пока человек листает страницу, поэтому все разделы должны быть в одном блоке с ней. Кнопки «Купить» прокручивают к витрине с корзиной ниже. Со страницы убраны обещания «добавим БЕСПЛАТНО», «продление со скидкой» и зачёркнутые цены.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага М-2 → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть». Код длинный, это нормально.</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{b.copybox('m3a', B2)}
</section>

<section class="task" id="m4">
<h2><span class="num">М-4</span> Выключить 33 блока прошлой версии</h2>
<span class="lbl">Что сделать</span><p>Выключить старые блоки между новым блоком из шага М-3 и витриной.</p>
<span class="lbl">Зачем</span><p>Всё их содержимое теперь есть в новых блоках. Если оставить, на странице будет два заголовка H1, два списка цен и противоречия: старые блоки обещают бесплатные функции и показывают зачёркнутые цены. Выключенный блок не виден на сайте, но остаётся в редакторе на случай отката.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Модуль 1С для маркетплейсов» (https://alsn.ru/casemarketplace). Первый блок - заголовок «Модуль интеграции 1С с маркетплейсами Ozon и Wildberries» сразу под новым блоком из шага М-3. Последний - кнопка «Узнать цены». Сразу под ней заголовок «Цены на модули интеграции 1С с маркетплейсами» и витрина с кнопками «Добавить в корзину»: их <strong>не выключать</strong>.</div>
<ol class="steps">
<li>У каждого блока из таблицы → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
<li>Меню, крошки, витрину, «Полезные страницы по модулю», «Услуги», форму «Остались вопросы?», «Наши клиенты», «Сертификаты», подвал и всплывающие формы не трогать.</li>
</ol>
{OLD}
</section>

<section class="task" id="m5">
<h2><span class="num">М-5</span> Заявка под витриной</h2>
<span class="lbl">Что сделать</span><p>Поставить последний экран: «Покажем модуль на вашем кабинете», телефон и кнопка «Записаться на демонстрацию».</p>
<span class="lbl">Зачем</span><p>Кто посмотрел цены и не готов купить сразу, получает понятный следующий шаг.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Под витриной с кнопками «Добавить в корзину» и «Load more», над блоком «Полезные страницы по модулю».</div>
<ol class="steps">
<li>Навести мышь между витриной и «Полезные страницы по модулю» → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{b.copybox('m5a', B3)}
</section>

<section class="task" id="m6">
<h2><span class="num">М-6</span> Описание страницы для поиска и для соцсетей</h2>
<span class="lbl">Что сделать</span><p>Заменить текст описания в двух полях настроек страницы. Заголовок и картинку для соцсетей не трогать.</p>
<span class="lbl">Зачем</span><p>Сейчас у общей страницы стоит описание со страницы Wildberries. Яндекс и Google показывают его в выдаче, Telegram и ВКонтакте под картинкой ссылки. Человек ищет модуль для обеих площадок и видит только WB.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>casemarketplace</code> → «Настройки» → вкладка «SEO» → поле «Описание» → найти текст и заменить целиком → «Сохранить изменения».</li>
<li>Там же вкладка «Соцсети» (или «Facebook &amp; SEO» / «Социальные сети») → поле «Описание» → тот же текст → «Сохранить изменения».</li>
</ol>
{swap('m6', DESC_OLD, DESC_NEW)}
</section>

<section class="task" id="m7">
<h2><span class="num">М-7</span> НДС 5% на странице «Интеграция 1С с Ozon»</h2>
<span class="lbl">Что сделать</span><p>Дописать ставку НДС в подзаголовке раздела с ценами.</p>
<span class="lbl">Зачем</span><p>На всех трёх страницах модуля цена должна читаться одинаково: «с НДС 5%». Иначе покупатель может решить, что в цену заложен НДС 20%.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon), в Тильде <code>1c-ozon</code>. Блок T123 с паспортом модуля и разделами: третий HTML-блок сверху (после крошек и первого экрана с фото). Строка стоит в разделе «06 Сколько стоит», сразу под заголовком H2 «Сколько стоит», над карточками цен.</div>
<ol class="steps">
<li>Открыть страницу на редактирование → блок T123 сразу под первым экраном с фото → «Контент».</li>
<li>Щёлкнуть в поле с кодом → Ctrl+F → вставить текст из «Найти» → заменить его строкой из «Заменить на». Остальной код не трогать.</li>
<li>«Сохранить и закрыть».</li>
</ol>
{swap('m7', NDS_OLD, NDS_NEW)}
</section>

<section class="task" id="m8">
<h2><span class="num">М-8</span> НДС 5% на странице «Интеграция 1С с Wildberries»</h2>
<span class="lbl">Что сделать</span><p>Та же правка, что в М-7, на странице Wildberries.</p>
<span class="lbl">Зачем</span><p>Одинаковая формулировка цены на всех страницах модуля.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Интеграция 1С с Wildberries» (https://alsn.ru/1c-wildberries), в Тильде <code>1c-wildberries</code>. Блок T123 с паспортом модуля: третий HTML-блок сверху (после крошек и первого экрана с фото). Раздел «06 Сколько стоит», строка сразу под H2 «Сколько стоит», над карточками цен.</div>
<ol class="steps">
<li>Открыть страницу на редактирование → блок T123 сразу под первым экраном с фото → «Контент».</li>
<li>Щёлкнуть в поле с кодом → Ctrl+F → найти строку → заменить. Остальной код не трогать.</li>
<li>«Сохранить и закрыть».</li>
</ol>
{swap('m8', NDS_OLD, NDS_NEW)}
</section>

<section class="task" id="m9">
<h2><span class="num">М-9</span> Опубликовать три страницы</h2>
<span class="lbl">Что сделать</span><p>Опубликовать «Модуль 1С для маркетплейсов», «Интеграция 1С с Ozon» и «Интеграция 1С с Wildberries».</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>На каждой из трёх страниц вверху редактора → «Опубликовать».</li>
<li>Написать в чат «опубликовано»: проверю живые страницы (один заголовок, вкладки, таблица, экраны, видео, кнопки «Купить» к витрине, телефонная версия, служебная разметка, НДС 5%).</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-casemarketplace-v3-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_hub_v3_brief.py</code> из макета <code>seo-data/competitors/screens/preview-casemarketplace-v3.html</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
open(HEAD_TXT, "w", encoding="utf-8").write(HEAD)
print("ok", OUT, len(HEAD), len(B1), len(B2), len(B3), len(DESC_NEW))
