# -*- coding: utf-8 -*-
"""Страница «Интеграция 1С с Ozon»: HEAD целиком одной вставкой и мелкие правки текста. 28.09.2026."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_mp_ozon_v3_brief as v  # noqa: E402

OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-1c-ozon-v3-day-2026-09-28.html")

CSS = "\n".join(
    line for line in v.CSS_V3.split("\n")
    if not line.startswith((".v3 .head{", ".v3 .head .in{", ".v3 .crumb{"))
)
assert ".v3 .day .more{" in CSS and "1121/515" in CSS and "minmax(0,1fr)" in CSS and ".lb" in CSS


DESC_OLD = "Модуль Аллсан связывает 1С с Ozon Seller: остатки и цены онлайн, заказы FBS в 1С, отчёты и юнит-экономика. От 40 700 ₽/год. Запишитесь на звонок."
DESC_NEW = "Модуль Аллсан связывает 1С с Ozon Seller: остатки и цены онлайн, заказы FBO, FBS, rFBS и DBS в 1С, юнит-экономика. От 40 700 ₽/год. Запишитесь на звонок."
LD_DESC_OLD = "Модуль Аллсан связывает 1С с Ozon Seller: остатки и цены онлайн, заказы FBS в 1С, отчёты и юнит-экономика. От 40 700 ₽/год."
LD_DESC_NEW = "Модуль Аллсан связывает 1С с Ozon Seller: остатки и цены онлайн, заказы FBO, FBS, rFBS и DBS в 1С, юнит-экономика. От 40 700 ₽/год."
assert len(DESC_NEW) <= 160, len(DESC_NEW)


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


WEBPAGE = ld({
    "@context": "https://schema.org",
    "@type": "WebPage",
    "dateModified": "2026-09-28",
    "name": "Интеграция 1С с Ozon",
    "description": LD_DESC_NEW,
    "url": "https://alsn.ru/1c-ozon",
    "inLanguage": "ru-RU",
    "isPartOf": {"@id": "https://alsn.ru/#website"},
})
CRUMBS = ld({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/"},
        {"@type": "ListItem", "position": 2, "name": "Модуль 1С для маркетплейсов", "item": "https://alsn.ru/casemarketplace"},
        {"@type": "ListItem", "position": 3, "name": "Интеграция 1С с Ozon", "item": "https://alsn.ru/1c-ozon"},
    ],
})

HEAD = "\n".join([
    '<meta name="robots" content="index, follow">',
    WEBPAGE,
    CRUMBS,
    v.FAQ_LD,
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">',
    "<style>\n" + CSS + "\n</style>",
])

LIVE_PHOTO = "https://optim.tildacdn.com/tild3632-3333-4139-b730-663861323430/-/format/webp/allsun-hero-mp-emplo.jpg.webp"
LIVE_COVER = "https://optim.tildacdn.com/tild3363-3664-4966-b837-393439303735/-/resize/800x/-/format/webp/case-ecotide-video-c.jpg.webp"
B1_LIVE = v.B1.replace(v.PH_PHOTO, LIVE_PHOTO)
B2_LIVE = v.B2.replace(v.PH_COVER, LIVE_COVER)
assert v.PH_PHOTO not in B1_LIVE and v.PH_COVER not in B2_LIVE

TRUST_OLD = '<div class="trust"><span>ТОП 10 ЦРА</span><span>с 2015 года</span><span>1С:Франчайзи</span></div>'
TRUST_NEW = '<div class="trust"><span>с 2015 года</span><span>ТОП 10 ЦРА</span><span>1С:Франчайзи</span></div>'
STOCK_OLD = "<b>Остатки и цены на Ozon</b>обновляются из 1С сами"
STOCK_NEW = "<b>Остатки на вашем складе</b>и цены уходят из 1С в Ozon сами"
ROUTE_OLD = "<li>заказы FBS, rFBS, DBS</li>"
ROUTE_NEW = "<li>заказы FBO, FBS, rFBS, DBS</li>"
assert TRUST_NEW in B2_LIVE and ROUTE_NEW in B2_LIVE and STOCK_NEW in B1_LIVE
DAY_STYLE_START = "<style>\n.v3 .tabs+.pane .shot img"


assert v.PH_SEO in B2_LIVE and v.PH_REEXP in B2_LIVE and "Premium Plus" in B2_LIVE


def tpl_box(cid, text):
    return b.copybox(cid, text).replace(f'<pre id="{cid}"', f'<pre id="{cid}" class="tpl"', 1)


EXTRA_CSS = """
.urlrow{display:grid;grid-template-columns:170px 1fr;gap:10px;align-items:center;margin:8px 0}
.urlrow input{width:100%;padding:9px 11px;border:1px solid #cfcfca;border-radius:8px;font:14px ui-monospace,Consolas,monospace}
.urlrow input.ok{border-color:#1a7f4b;background:#e8f6ee}
.urlstate{font-size:13px;margin-top:6px}
"""

TPL_JS = """<script>
(function(){
var A=%s, B=%s;
var pres=[].slice.call(document.querySelectorAll('pre.tpl'));
pres.forEach(function(p){p._tpl=p.textContent;});
var re=/^https:\\/\\/(static|optim)\\.tildacdn\\.com\\//;
function upd(){
  var a=document.getElementById('u-seo').value.trim(), c=document.getElementById('u-rx').value.trim();
  document.getElementById('u-seo').classList.toggle('ok',re.test(a));
  document.getElementById('u-rx').classList.toggle('ok',re.test(c));
  pres.forEach(function(p){p.textContent=p._tpl.split(A).join(a||A).split(B).join(c||B);});
  document.getElementById('u-state').textContent=(a&&c)?'Адреса подставлены в код шага Ф-1.':'Пока в коде стоят заглушки. Вставьте оба адреса.';
}
['u-seo','u-rx'].forEach(function(id){document.getElementById(id).addEventListener('input',upd);});
upd();
})();
</script>""" % (json.dumps(v.PH_SEO, ensure_ascii=False), json.dumps(v.PH_REEXP, ensure_ascii=False))


def swap(cid, old, new):
    return (f'<span class="lbl">Найти</span>\n{b.copybox(cid + "f", old)}\n'
            f'<span class="lbl">Заменить на</span>\n{b.copybox(cid + "r", new)}')


doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Интеграция 1С с Ozon - HEAD одной вставкой и правки текста - 28.09.2026</title>
<style>{b.BRIEF_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Интеграция 1С с Ozon - HEAD одной вставкой и правки текста</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-ozon">https://alsn.ru/1c-ozon</a> (в списке Тильды <code>1c-ozon</code>) · HEAD сверен с живой страницей 28.09.2026, 14:46 · каждый шаг после письменного «да», «Опубликовать» один раз в конце</p>

<div class="callout ok"><strong>Уже на сайте, не трогать:</strong> пять пунктов в ленте «Как выглядит день с модулем», FBO в строке «Схемы» паспорта. HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать: там название компании для превью, счётчики и разметка организации.</div>

<section class="task" id="g1">
<h2><span class="num">Г-1</span> HEAD страницы целиком одной вставкой</h2>
<span class="lbl">Что сделать</span><p>Стереть всё, что сейчас лежит в HEAD этой страницы, и вставить один готовый код.</p>
<span class="lbl">Зачем</span><p>Сейчас в HEAD страницы семь кусков, добавленных в разное время: старые стили прежнего дизайна (их блоки выключены), стили нового дизайна, отдельная правка для телефона и служебные описания для поисковиков. Разобраться, что за что отвечает, трудно. Новый код делает то же самое, но одним куском: сначала описания для поисковиков, потом шрифты и все стили страницы. В нём уже учтены правки для телефона, отчёт Ozon без WB во вкладке «Маржа по товарам» и оформление ленты дня.</p>
<p>Что в коде: метка «страница открыта для поиска»; описание страницы; хлебные крошки для поисковиков; частые вопросы для поисковиков; шрифт Onest; стили всех трёх новых блоков.</p>
<p>Старые стили прежнего дизайна в новый код не вошли. Если когда-нибудь понадобится включить старые блоки обратно, скажите: верну стили отдельно.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>На всякий случай скопируйте старое содержимое поля в блокнот (Ctrl+A, Ctrl+C). Это откат, если что-то пойдёт не так.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
<li>Если на шаге Д-1 вы вставляли стиль в начало первого блока T123 (заголовок, фото Сергея, лента), удалите его оттуда: блок → «Контент» → стереть в самом начале кода кусок от <code>&lt;style&gt;</code> до <code>&lt;/style&gt;</code>, который начинается так, как показано ниже. Дальше <code>&lt;div class="v3"&gt;</code> не трогать. Если не вставляли, пропустите.</li>
</ol>
{b.copybox('g1c', HEAD)}
<span class="lbl">Начало стиля, который надо убрать из первого блока (только если вставляли)</span>
{b.copybox('g1d', DAY_STYLE_START)}
</section>

<section class="task" id="d5">
<h2><span class="num">Д-5</span> Первый пункт ленты: «Остатки на вашем складе»</h2>
<span class="lbl">Что сделать</span><p>В ленте «Как выглядит день с модулем» поменять первый пункт.</p>
<span class="lbl">Зачем</span><p>Селлер думает о своём складе: сколько товара у него есть и видит ли это Ozon. Так понятнее, чем «остатки на Ozon».</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Первый блок T123 сразу под хлебными крошками: заголовок, фото Сергея, лента. Пункт с меткой «по расписанию», самый левый в ленте.</div>
<p>Блок → «Контент» → найти строку и заменить → «Сохранить и закрыть».</p>
{swap('d5', STOCK_OLD, STOCK_NEW)}
</section>

<section class="task" id="f0">
<h2><span class="num">Ф-0</span> Загрузить два экрана модуля</h2>
<span class="lbl">Что сделать</span><p>Загрузить в Тильду два скриншота 1С и получить их адреса.</p>
<span class="lbl">Зачем</span><p>В новом ряду «Ещё в модуле для Ozon» у карточек про SEO-описания и перевыставление услуг есть настоящие экраны модуля. Код берёт их по адресу, без загрузки на их месте будет пусто.</p>
<table>
<tr><th>Что</th><th>Файл в папке проекта</th></tr>
<tr><td>Экран «Генератор SEO текстов» (салфетка для монитора)</td><td><code>seo-data/brand-images/ozon-screens/ozon-1c-seo-generator.png</code></td></tr>
<tr><td>Экран «Загрузка отчёта о перевыставлении услуг»</td><td><code>seo-data/brand-images/ozon-screens/ozon-1c-perevystavlenie-uslug.png</code></td></tr>
</table>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> на редактирование. В самом низу холста, над подвалом → «+» → «Изображение» → блок <strong>T107</strong>.</li>
<li>В блоке → «Контент» → «Загрузить файл» → экран SEO → «Сохранить и закрыть». Второй блок T107 так же, с экраном перевыставления услуг.</li>
<li>«Предпросмотр» → правой кнопкой по картинке → «Открыть изображение в новой вкладке» → скопировать адрес. Подойдёт адрес с <code>static.tildacdn.com</code> или <code>optim.tildacdn.com</code>.</li>
<li>Вставить оба адреса в поля ниже. Они сами подставятся в код шага Ф-1.</li>
<li>Оба блока T107 → три точки → «Выключить блок». Не удалять, иначе Тильда может убрать файл.</li>
</ol>
<div class="urlrow"><label for="u-seo">Адрес экрана SEO</label><input id="u-seo" placeholder="https://static.tildacdn.com/tild..../....png"></div>
<div class="urlrow"><label for="u-rx">Адрес экрана услуг</label><input id="u-rx" placeholder="https://static.tildacdn.com/tild..../....png"></div>
<div class="urlstate" id="u-state"></div>
</section>

<section class="task" id="f1">
<h2><span class="num">Ф-1</span> Новый код второго блока: четыре функции, FBO и «с 2015 года»</h2>
<span class="lbl">Что сделать</span><p>Заменить код второго нового блока целиком.</p>
<span class="lbl">Зачем</span><p>В разделе «Отчёты, которых нет в типовом обмене» под вкладками появится ряд «Ещё в модуле для Ozon»: SEO-описания с помощью ИИ, перевыставление услуг последней мили с НДС, автоответы на отзывы (с пометкой, что для Ozon нужна подписка Premium Plus) и реестр продаж юрлицам. Экраны открываются крупно по клику. Заодно в этом коде уже есть FBO в схеме «Как идут данные» и значок «с 2015 года» первым в паспорте.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Второй новый блок T123, сразу под лентой «Как выглядит день с модулем». Начинается с карточки «Паспорт модуля 40 700 ₽», внутри разделы 01-07 до «Частые вопросы».</div>
<ol class="steps">
<li>Сначала шаг Ф-0: в коде ниже не должно остаться слов <code>ВСТАВЬТЕ_ССЫЛКУ</code>.</li>
<li>Блок → «Контент» → Ctrl+A → Delete → вставить код ниже → «Сохранить и закрыть». Настройки блока не менять.</li>
<li>После шагов Г-1, Д-5, Ф-0 и Ф-1 нажать «Опубликовать».</li>
</ol>
{tpl_box('f1c', B2_LIVE)}
</section>

<section class="task" id="s1">
<h2><span class="num">С-1</span> Описание страницы для Яндекса и Google: все четыре схемы</h2>
<span class="lbl">Что сделать</span><p>Заменить описание страницы в настройках SEO.</p>
<span class="lbl">Зачем</span><p>Это текст под заголовком в поиске. Сейчас в нём только FBS, и селлер, который торгует со склада Ozon (FBO), может решить, что модуль ему не подходит. Новый текст той же длины, в нём все четыре схемы, как в паспорте модуля.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> → «Настройки» (шестерёнка) → вкладка «SEO» (в старом интерфейсе «Facebook &amp; SEO» → «Поисковая выдача») → поле «Описание».</li>
<li>Стереть текст в поле и вставить новый → «Сохранить изменения». Заголовок страницы не трогать.</li>
</ol>
<span class="lbl">Было</span>
{b.copybox('s1f', DESC_OLD)}
<span class="lbl">Стало</span>
{b.copybox('s1r', DESC_NEW)}
</section>

<section class="task" id="s2">
<h2><span class="num">С-2</span> То же описание для превью в соцсетях и мессенджерах</h2>
<span class="lbl">Что сделать</span><p>Заменить описание во вкладке «Соцсети».</p>
<span class="lbl">Зачем</span><p>Этот текст виден под картинкой, когда ссылку пересылают в Telegram или ВКонтакте. Он должен совпадать с описанием для поиска.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Там же в настройках страницы → вкладка «Соцсети» (в старом интерфейсе «Facebook &amp; SEO» → «Соцсети») → поле «Описание».</li>
<li>Если поле пустое и стоит галочка «как в SEO», ничего делать не нужно. Если там старый текст, заменить на новый → «Сохранить изменения». Картинку превью не трогать.</li>
</ol>
{b.copybox('s2r', DESC_NEW)}
</section>

<section class="task" id="s3">
<h2><span class="num">С-3</span> Описание в служебной разметке HEAD</h2>
<span class="lbl">Что сделать</span><p>В HEAD страницы заменить одну строку описания в служебной разметке страницы.</p>
<span class="lbl">Зачем</span><p>Поисковики читают это описание вместе с видимым. Оно должно совпадать по смыслу, иначе на странице два разных рассказа о модуле.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Настройки страницы → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Это второй кусок в поле, сразу после строки <code>&lt;meta name="robots" ...&gt;</code>, со словами <code>"@type": "WebPage"</code>. Найти в нём текст и заменить. Кавычки вокруг текста не стирать. Остальное не трогать → «Сохранить изменения».</li>
<li>После С-1, С-2 и С-3 нажать «Опубликовать».</li>
</ol>
<span class="lbl">Найти</span>
{b.copybox('s3f', LD_DESC_OLD)}
<span class="lbl">Заменить на</span>
{b.copybox('s3r', LD_DESC_NEW)}
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-ozon-v3-day-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_ozon_v3_day.py</code> · стили берутся из макета <code>seo-data/competitors/screens/preview-1c-ozon-v3.html</code></p>
</div>
{b.COPY_JS}
{TPL_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
open(os.path.join(b.ROOT, "seo-data", "tilda-briefs", "_head-1c-ozon-2026-09-28.txt"), "w", encoding="utf-8").write(HEAD)
print("ok", OUT, len(HEAD))
