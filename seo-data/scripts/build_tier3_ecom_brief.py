# -*- coding: utf-8 -*-
"""Тир 3 по поставщикам (/ecom и карточки): инструкция для Тильды.

Тексты FAQ лежат в одном списке: из него собираются и блоки для холста,
и FAQPage для HEAD, чтобы совпадали буква в букву.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tilda-briefs" / "tier3-ecom-postavshiki-2026-09-30.html"
DATE = "30.09.2026"
DATE_ISO = "2026-09-30"

FAQ_H2 = "Частые вопросы об интеграции 1С с поставщиками"

FAQ = [
    (
        "Чем интеграция отличается от работы в личном кабинете поставщика?",
        "В личном кабинете (Мерлион B2B, OCS B2B, Treolan B2B) менеджер смотрит остатки и цены "
        "на сайте поставщика и переносит их в 1С вручную, часто через Excel. Интеграция подключает "
        "вашу 1С к API поставщика: остатки, цены и резерв приходят прямо в 1С, заходить в кабинет "
        "и скачивать прайс не нужно.",
    ),
    (
        "С какими поставщиками можно связать 1С?",
        "Готовые интеграции есть с дистрибьюторами телеком- и IT-оборудования: Мерлион, OCS, "
        "Treolan, Марвел, DIGIS, ЭЛКО Рус, 3logic, ЭТМ iPRO и другими. Полный список с функциями "
        "есть в таблице на этой странице. Если нужного поставщика в списке нет, сделаем новую "
        "интеграцию, стоимость от 208 950 ₽.",
    ),
    (
        "Чем это лучше загрузки прайса из Excel?",
        "Прайс из Excel устаревает сразу после выгрузки, а перенос вручную даёт ошибки. С интеграцией "
        "остатки и цены обновляются по расписанию. В кейсе ООО «СЦ» они приходят в 1С каждые "
        "5-10 минут, а заказ обрабатывается за 10-15 минут вместо нескольких часов.",
    ),
    (
        "Можно ли резервировать товар у поставщика прямо из 1С?",
        "Да, если поставщик поддерживает резерв по API. Резерв ставится из 1С вручную или "
        "автоматически по заказу клиента: модуль выбирает поставщика с лучшими условиями, номер и "
        "срок резерва приходят в 1С. Какие поставщики "
        "это умеют, видно в таблице, колонка «Резервирование».",
    ),
    (
        "Какие данные загружаются в 1С?",
        "Номенклатура, изображения и характеристики, штрих-коды, цены и остатки по расписанию. "
        "Остатки приходят с тех складов поставщика, которые выбраны при настройке. Есть резерв у "
        "поставщика и аналитика заказов. Если ваша 1С уже связана с сайтом, настроим автоматическую "
        "загрузку остатков поставщиков на виртуальные склады, связанные с сайтом. Набор зависит от "
        "того, что отдаёт API конкретного поставщика.",
    ),
    (
        "Сколько стоит интеграция и нужно ли её продлевать?",
        "Пакет из 5 поставщиков из нашего списка стоит 103 950 ₽ в год, каждый следующий поставщик "
        "из списка 15 645 ₽ в год. Интеграция с поставщиком не из списка от 208 950 ₽. Оплата "
        "ежегодная: год продления стоит столько же, сколько покупка. Если не продлить, модуль "
        "перестанет получать обновления, и когда поставщик изменит свой API, обмен с ним может "
        "остановиться. Цены с НДС 5%.",
    ),
    (
        "Сколько времени занимает подключение?",
        "Подключение одного поставщика занимает 2 недели.",
    ),
    (
        "Как получить доступ к API поставщика?",
        "Доступ к API выдаёт сам поставщик, обычно своим партнёрам. У Мерлион подключение к API "
        "бесплатное, по заявке на их сайте. Treolan даёт доступ партнёрам по запросу на email, "
        "а OCS открывает B2B-портал авторизованным партнёрам. Подскажем, что запросить у вашего "
        "поставщика.",
    ),
]

FAQ_LD = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "@id": "https://alsn.ru/ecom#faq",
    "mainEntity": [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in FAQ
    ],
}
FAQ_SCRIPT = (
    '<script type="application/ld+json">\n'
    + json.dumps(FAQ_LD, ensure_ascii=False, indent=2)
    + "\n</script>"
)

CARDS = [
    {
        "slug": "merlion",
        "brand": "Merlion",
        "h1_old": "Интеграция 1C с Merlion B2B по API",
        "h1_new": "Интеграция 1С с Merlion B2B по API",
        "t180": "rec1122990606",
        "t585": "rec1123096006",
        "t585_title": "Особенности интеграции с MERLION B2B",
        "t585_first": "Сервис MERLION B2B",
        "title_old": "Интеграция 1С с Merlion B2B по API недорого, прямой доступ к личному кабинету Мерлион B2B - Аллсан",
        "title_new": "Интеграция 1С с Merlion B2B по API - модуль обмена | Аллсан",
        "desc_old": "Интеграция с Мерлион B2B без ограничений по срокам. Цена - ниже конкурентов. Подключим вашу 1С быстро по API к личному кабинету Мерлион B2B - Аллсан Интеграция",
        "desc_new": "Модуль обмена 1С с Мерлион по API: остатки, закупочные цены и резерв в вашей 1С без выгрузки Excel из личного кабинета. Оплата однократная. Аллсан Интеграция",
        "item_title": "Чем модуль отличается от личного кабинета Merlion B2B",
        "item_text": "В личном кабинете Merlion B2B менеджер смотрит остатки и цены на сайте Мерлион и переносит их в 1С вручную или через Excel. Наш модуль подключает вашу 1С к MERLION API: остатки, закупочные цены и резерв приходят прямо в 1С, заходить в кабинет не нужно. Доступ к API Мерлион выдаёт бесплатно, по заявке.",
    },
    {
        "slug": "ocs",
        "brand": "OCS",
        "h1_old": "Интеграция 1C с OCS B2B по API",
        "h1_new": "Интеграция 1С с OCS B2B по API",
        "t180": "rec1129314406",
        "t585": "rec1129314496",
        "t585_title": "Особенности интеграции с OCS B2B",
        "t585_first": "Сервис OCS B2B",
        "title_old": "Интеграция 1С с OCS B2B по API недорого, прямой доступ к личному кабинету OCS B2B - Аллсан",
        "title_new": "Интеграция 1С с OCS B2B по API - модуль обмена | Аллсан",
        "desc_old": "Интеграция с OCS B2B без ограничений по срокам. Цена - ниже конкурентов. Подключим вашу 1С быстро по API к личному кабинету OCS B2B - Аллсан Интеграция",
        "desc_new": "Модуль обмена 1С с OCS по API: остатки, закупочные цены и резерв в вашей 1С без выгрузки Excel из личного кабинета. Оплата однократная. Аллсан Интеграция",
        "item_title": "Чем модуль отличается от личного кабинета OCS B2B",
        "item_text": "В личном кабинете OCS B2B менеджер смотрит остатки и цены на сайте OCS и переносит их в 1С вручную или через Excel. Наш модуль подключает вашу 1С к OCS API: остатки, закупочные цены и резерв приходят прямо в 1С, заходить в кабинет не нужно. Доступ к B2B и API OCS получают авторизованные партнёры OCS Distribution.",
    },
    {
        "slug": "treolan",
        "brand": "Treolan",
        "h1_old": "Интеграция 1C с Treolan B2B по API",
        "h1_new": "Интеграция 1С с Treolan B2B по API",
        "t180": "rec1129548106",
        "t585": "rec1129548196",
        "t585_title": "Особенности интеграции с Treolan B2B",
        "t585_first": "Что такое Treolan B2B",
        "title_old": "Интеграция 1С с Treolan B2B по API недорого, прямой доступ к личному кабинету Treolan B2B - Аллсан",
        "title_new": "Интеграция 1С с Treolan B2B по API - модуль обмена | Аллсан",
        "desc_old": "Интеграция с Treolan B2B без ограничений по срокам. Цена - ниже конкурентов. Подключим вашу 1С быстро по API к личному кабинету Treolan B2B - Аллсан Интеграция",
        "desc_new": "Модуль обмена 1С с Treolan по API: остатки, закупочные цены и резерв в вашей 1С без выгрузки Excel из личного кабинета. Оплата однократная. Аллсан Интеграция",
        "item_title": "Чем модуль отличается от личного кабинета Treolan B2B",
        "item_text": "В личном кабинете Treolan B2B менеджер смотрит остатки и цены на сайте Treolan и переносит их в 1С вручную или через Excel. Наш модуль подключает вашу 1С к Treolan API: остатки, закупочные цены и резерв приходят прямо в 1С, заходить в кабинет не нужно. Доступ к API Treolan даёт своим партнёрам по запросу на email.",
    },
]

ETM = {
    "h1_old": "Интеграция 1C с ЭТМ iPRO по API",
    "h1_new": "Интеграция 1С с ЭТМ iPRO по API",
    "title_old": "Интеграция iPRO ЭТМ с 1С — модуль обмена | Аллсан",
    "title_new": "Интеграция iPRO ЭТМ с 1С - модуль обмена | Аллсан",
    "desc_old": "Модуль обмена 1С с кабинетом ЭТМ iPRO: остатки, цены и резерв по API. Чем отличается от бесплатного модуля УТ 11 — объясним на консультации. Аллсан Интеграция.",
    "desc_new": "Модуль обмена 1С с кабинетом ЭТМ iPRO: остатки, цены и резерв по API. Чем отличается от бесплатного модуля УТ 11 - объясним на консультации. Аллсан Интеграция.",
}

_n = 0


def box(text: str, label: str = "") -> str:
    global _n
    _n += 1
    cid = f"c{_n}"
    lab = f'<span class="lbl">{html.escape(label)}</span>' if label else ""
    return (
        f'{lab}<div class="copybox"><pre id="{cid}">{html.escape(text)}</pre>'
        f'<button type="button" data-copy="{cid}">Копировать</button></div>'
    )


CSS = """
:root{--bg:#f4f3ef;--card:#fff;--text:#1a1a1a;--muted:#5c5c5c;--border:#e2e2de;--ok:#1a7f4b;--ok-bg:#e8f6ee;--warn:#9a6700;--warn-bg:#fff6e0;--danger:#b42318;--danger-bg:#fdecea;--info:#0b6e99;--info-bg:#e8f4fa;--code:#0f172a}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--text);background:var(--bg)}
.wrap{max-width:920px;margin:0 auto;padding:24px 18px 72px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:-.02em}h2{font-size:20px;margin:0 0 10px}h3{font-size:16px;margin:16px 0 6px}
p{margin:0 0 8px}a{color:#0b5cad}.muted{color:var(--muted);font-size:14px}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 16px}
.pill{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:650;border:1px solid var(--border);background:#fff}
.pill.ok{color:var(--ok);background:var(--ok-bg);border-color:#c6e6d3}.pill.warn{color:var(--warn);background:var(--warn-bg);border-color:#f0dfa0}
.pill.danger{color:var(--danger);background:var(--danger-bg);border-color:#f5c2c0}.pill.info{color:var(--info);background:var(--info-bg);border-color:#bddceb}
.callout{border-radius:10px;padding:12px 14px;margin:12px 0 18px;border:1px solid var(--border);background:var(--card);font-size:14px}
.callout.danger{background:var(--danger-bg);border-color:#f5c2c0}.callout.warn{background:var(--warn-bg);border-color:#f0dfa0}.callout.info{background:var(--info-bg);border-color:#bddceb}
.toc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 16px;margin:0 0 20px}
.toc ol{margin:6px 0 0;padding-left:22px}.toc li{margin:3px 0}.toc a{text-decoration:none}
.task{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px 18px;margin:0 0 18px}
.task .num{display:inline-block;background:#111;color:#fff;border-radius:999px;font-size:12px;font-weight:700;padding:2px 10px;margin-right:6px;vertical-align:middle}
.lbl{display:block;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:14px 0 4px}
ol.steps{margin:4px 0 0;padding-left:22px}ol.steps>li{margin:6px 0}
.path{font-family:ui-monospace,"Cascadia Mono",Consolas,monospace;font-size:12.5px;background:#111;color:#f5f5f4;border-radius:8px;padding:8px 10px;margin:6px 0 8px;overflow-x:auto}
.copybox{position:relative;margin:6px 0 10px}
.copybox pre{margin:0;background:var(--code);color:#e5e7eb;border-radius:10px;padding:12px 12px 40px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;font:13px/1.4 ui-monospace,"Cascadia Mono",Consolas,monospace}
.copybox button{position:absolute;right:8px;bottom:8px;background:#fff;border:1px solid #ccc;border-radius:8px;padding:4px 10px;font-size:12px;font-weight:650;cursor:pointer}
.copybox button:hover{background:#f3f4f6}.copybox button.ok{background:var(--ok-bg)}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 0;background:#fff}
th,td{border:1px solid var(--border);padding:7px 9px;text-align:left;vertical-align:top}th{background:#fafaf8;font-weight:650}
.faqitem{border-left:3px solid #111;padding-left:12px;margin:14px 0}
ul.tight{margin:4px 0 0;padding-left:18px}ul.tight li{margin:3px 0}
@media print{body{background:#fff}.copybox button{display:none}.task,.toc,.callout{break-inside:avoid}}
"""

JS = """
function flash(b){b.classList.add("ok");const t=b.textContent;b.textContent="Скопировано";setTimeout(()=>{b.textContent=t;b.classList.remove("ok")},1200)}
document.querySelectorAll(".copybox button[data-copy]").forEach(b=>{b.addEventListener("click",async()=>{const p=document.getElementById(b.getAttribute("data-copy"));if(!p)return;await navigator.clipboard.writeText(p.textContent);flash(b)})});
"""


def faq_items_html() -> str:
    parts = []
    for i, (q, a) in enumerate(FAQ, 1):
        parts.append(
            f'<div class="faqitem"><h3>Пункт {i}</h3>'
            + box(q, "Заголовок пункта")
            + box(a, "Текст пункта")
            + "</div>"
        )
    return "\n".join(parts)


def card_html(c: dict, idx: int) -> str:
    url = f"https://alsn.ru/{c['slug']}"
    return f"""
<section class="task" id="t3-5-{c['slug']}">
  <h2><span class="num">T3-5.{idx}</span> Карточка «{html.escape(c['h1_new'])}»</h2>
  <p class="muted">Страница: <a href="{url}">{url}</a> · в списке Тильды адрес <code>{c['slug']}</code></p>

  <span class="lbl">Что сделать</span>
  <p>Поменять заголовок вкладки и описание для поиска, исправить латинскую «C» в главном заголовке на русскую «С», добавить в аккордеон первым пунктом объяснение, чем модуль отличается от личного кабинета {html.escape(c['brand'])}.</p>

  <span class="lbl">Зачем</span>
  <p>Сейчас в поиске страница обещает «прямой доступ к личному кабинету» и «ниже конкурентов». Люди, которые ищут вход в кабинет {html.escape(c['brand'])}, кликают и уходят, а поисковик видит, что страница не отвечает на запрос. Новый заголовок честно говорит: это модуль для вашей 1С. Латинская «C» в «1C» мешает поиску по запросу «1С» русскими буквами.</p>

  <h3>Шаг 1. Заголовок вкладки и описание для поиска</h3>
  <ol class="steps">
    <li>Список страниц → <strong>{c['slug']}</strong> → <strong>шестерёнка</strong> (Настройки страницы).</li>
    <li>Вкладка <strong>Главное</strong>: поля «Заголовок» и «Описание». Если во вкладке <strong>Facebook &amp; SEO</strong> → «Как страница выглядит в поисковой выдаче» задан отдельный заголовок и описание, менять там же.</li>
    <li>Заменить заголовок:</li>
  </ol>
  {box(c['title_old'], 'Найти (заголовок)')}
  {box(c['title_new'], 'Заменить на')}
  <ol class="steps" start="4"><li>Заменить описание:</li></ol>
  {box(c['desc_old'], 'Найти (описание)')}
  {box(c['desc_new'], 'Заменить на')}
  <ol class="steps" start="5">
    <li>Если во вкладке <strong>Соцсети</strong> (Facebook &amp; SEO → заголовок и описание для соцсетей) стоят старые строки, поставить туда те же новые.</li>
    <li><strong>Сохранить</strong>.</li>
  </ol>

  <h3>Шаг 2. Главный заголовок: «1C» латиницей → «1С» по-русски</h3>
  <p>Где: первый экран страницы, баннер <strong>T180</strong> ({c['t180']}), над ним строка «Однократная оплата без ежегодного продления!», под ним «Возможности:» и цена «от 99 900 руб».</p>
  <ol class="steps">
    <li>Редактор страницы (карандаш) → блок T180 → <strong>Контент</strong> → поле «Заголовок».</li>
    <li>Стереть строку целиком и вставить новую из блока ниже. Буквы выглядят одинаково, поэтому не править одну букву вручную, а вставить копией.</li>
  </ol>
  {box(c['h1_old'], 'Найти')}
  {box(c['h1_new'], 'Заменить на')}
  <ol class="steps" start="3"><li><strong>Сохранить и закрыть</strong>. Цену и остальной текст баннера не трогать.</li></ol>

  <h3>Шаг 3. Новый первый пункт в аккордеоне</h3>
  <p>Где: ниже таблицы поставщиков и цен, аккордеон <strong>T585</strong> ({c['t585']}) с заголовком «{html.escape(c['t585_title'])}». Сейчас первый пункт «{html.escape(c['t585_first'])}».</p>
  <ol class="steps">
    <li>Блок T585 → <strong>Контент</strong> → внизу списка «Добавить элемент» (иногда «+ Элемент»).</li>
    <li>В новом элементе заполнить поля:</li>
  </ol>
  {box(c['item_title'], 'Заголовок пункта')}
  {box(c['item_text'], 'Текст пункта')}
  <ol class="steps" start="3">
    <li>Перетащить новый элемент за значок перетаскивания наверх, чтобы он стал первым, перед «{html.escape(c['t585_first'])}».</li>
    <li><strong>Сохранить и закрыть</strong>.</li>
  </ol>

  <h3>Шаг 4. Опубликовать</h3>
  <ol class="steps"><li>Кнопка <strong>Опубликовать</strong> вверху редактора страницы {c['slug']}. Отдельный шаг, после «да».</li></ol>
</section>
"""


def build() -> str:
    cards = "\n".join(card_html(c, i) for i, c in enumerate(CARDS, 1))
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TIER 3 - поставщики (/ecom и карточки) - инструкция Тильда - {DATE}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>TIER 3 - интеграция 1С с поставщиками. Инструкция Тильда</h1>
<p class="muted">Страницы: «Интеграция 1С с поставщиками телеком- и IT-оборудования» (<a href="https://alsn.ru/ecom">https://alsn.ru/ecom</a>), кейс ООО «СЦ» (<a href="https://alsn.ru/caseecomsc">https://alsn.ru/caseecomsc</a>), карточки Мерлион, OCS, Treolan, ЭТМ iPRO · дата: {DATE} · только живая Тильда, не Битрикс</p>
<div class="pills">
  <span class="pill info">ecom</span><span class="pill ok">T1 и T2 закрыты</span>
  <span class="pill warn">Twitter / X - SKIP</span><span class="pill danger">Bing - SKIP</span><span class="pill">robots.txt не трогать</span>
</div>

<div class="callout danger">Каждый шаг - только после письменного «да». «Опубликовать» - отдельный шаг в конце каждой страницы. Код в HEAD страницы только дописывать, ничего не стирать. Общий HEAD сайта (данные компании) не трогать. Telegram-бот на сайте не снимать.</div>

<div class="callout warn"><strong>Уже сделано - не трогать:</strong> заголовок вкладки, описание и главный заголовок страницы /ecom (Тир 2, 14.09.2026); картинка превью для Telegram (проверена 30.09.2026); служебный код Service, WebPage и BreadcrumbList в HEAD /ecom; крошки T123 на /ecom и карточках; ссылки из таблицы /ecom на 13 карточек поставщиков. Удаление старых крошек T758 на карточках - в <code>tier2-breadcrumbs-wave-2026-09-28.html</code>, здесь не повторять. T3-1, T3-2, T3-3 (частые вопросы и служебный код FAQ на /ecom, публикация) сделаны 30.09.2026 вместе с новым дизайном /ecom (проверено на сайте, форма T720 и блок «У нас есть решение для:» выключены намеренно). T3-5 (карточки Мерлион, OCS, Treolan) и T3-6 (карточка ЭТМ iPRO) 30.09.2026 перенесены в <code>tier4-postavshiki-v3-2026-09-30.html</code>: там новый дизайн всех 13 карточек вместе с заголовками и описаниями.</div>

<div class="toc"><strong>Задачи</strong><ol>
  <li><a href="#t3-4">T3-4. Кейс ООО «СЦ»: ссылка на страницу интеграции</a></li>
  <li><a href="#skip">Что не делать</a></li>
</ol></div>

<section class="task" id="t3-4">
  <h2><span class="num">T3-4</span> Кейс ООО «СЦ»: ссылка на страницу интеграции</h2>
  <p class="muted">Страница: «Кейс: интеграция 1С с поставщиками телеком- и IT-оборудования для ООО «СЦ»», <a href="https://alsn.ru/caseecomsc">https://alsn.ru/caseecomsc</a> · в списке Тильды адрес <code>caseecomsc</code></p>
  <span class="lbl">Что сделать</span>
  <p>В первом абзаце кейса поставить ссылку на страницу «Интеграция 1С с поставщиками телеком- и IT-оборудования».</p>
  <span class="lbl">Зачем</span>
  <p>Кейс убеждает, а купить можно на странице продукта. Сейчас из абзаца туда не перейти. Ссылка ведёт заинтересованного читателя к цене и списку поставщиков, а поисковику показывает связь кейса с продуктом.</p>
  <span class="lbl">Как в Тильде</span>
  <p>Где: первый экран кейса, блок <strong>T205</strong> (rec3384890201). Под главным заголовком абзац, который начинается словами «Для ООО «СЦ» мы настроили обмен 1С…», ниже кнопка «ЗАКАЗАТЬ КОНСУЛЬТАЦИЮ».</p>
  <ol class="steps">
    <li>Редактор страницы caseecomsc → клик в текст абзаца.</li>
    <li>Выделить слова из таблицы → иконка цепочки «Ссылка» → вставить адрес → Enter.</li>
  </ol>
  <table>
    <tr><th>Что выделить</th><th>Какой адрес</th></tr>
    <tr><td>обмен 1С с личными кабинетами и API поставщиков телеком- и IT-оборудования</td><td>https://alsn.ru/ecom</td></tr>
  </table>
  <ol class="steps" start="3">
    <li>Текст абзаца не менять. <strong>Сохранить</strong>.</li>
    <li><strong>Опубликовать</strong> страницу caseecomsc. Отдельный шаг, после «да».</li>
  </ol>
</section>

<section class="task" id="skip">
  <h2>Что не делать</h2>
  <table>
    <tr><th>Пункт</th><th>Почему</th></tr>
    <tr><td>Служебный код HowTo, Person, Article на /ecom</td><td>Нет пошаговой инструкции и автора на странице, код без видимого текста поисковик считает накруткой</td></tr>
    <tr><td>Снимать промо Telegram-бота с /ecom</td><td>На живом сайте бота не снимаем</td></tr>
    <tr><td>Старые крошки T758 на карточках</td><td>Уже в инструкции <code>tier2-breadcrumbs-wave-2026-09-28.html</code></td></tr>
    <tr><td>Писать срок подключения, SLA</td><td>Нет подтверждённых данных</td></tr>
    <tr><td>Bing, LinkedIn для Bing, Twitter / X</td><td>Не ведём</td></tr>
    <tr><td>Файл robots.txt</td><td>На Тильде не редактируется</td></tr>
    <tr><td>301 со старого /caseecom</td><td>Адрес освобождён специально</td></tr>
  </table>
</section>

<section class="task">
  <h2>Вопросы к заказчику (до следующего тира)</h2>
  <ul class="tight">
    <li>Срок подключения одного поставщика из списка: можно ли назвать цифру на странице?</li>
    <li>В таблице поставщиков есть непрофильные (Тайпит-Мебель, Делия, МаСт гидроизоляция и др.). Оставить или убрать в следующем тире?</li>
  </ul>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier3-ecom-postavshiki-2026-09-30.html</code>, собран <code>seo-data/scripts/build_tier3_ecom_brief.py</code>. Открывать локально в браузере, на alsn.ru не заливать.</p>
</div>
<script>{JS}</script>
</body>
</html>
"""


if __name__ == "__main__":
    text = build()
    assert "\u2014" not in text.replace(ETM["title_old"], "").replace(ETM["desc_old"], ""), "длинное тире"
    assert "\u2013" not in text, "среднее тире"
    OUT.write_text(text, encoding="utf-8")
    print(OUT)
