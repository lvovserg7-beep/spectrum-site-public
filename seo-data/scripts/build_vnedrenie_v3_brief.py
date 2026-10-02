# -*- coding: utf-8 -*-
"""Инструкция для Тильды: новый дизайн страницы «Внедрение 1С» (alsn.ru/development1c) на стилях v3.

Код блоков - из макета preview-development1c-v3.html, стили - из эталона 1c-ozon
с префиксом .v3, первый экран в рамке - HERO_CSS. Выход:
  seo-data/tilda-briefs/tier4-development1c-v3-2026-09-30.html
  seo-data/tilda-briefs/_head-development1c-2026-09-30.txt
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_vnedrenie_v3_preview as p  # noqa: E402
from mp_hero_frame import HERO_CSS  # noqa: E402

p.main()
BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
OUT = os.path.join(BR, "tier4-development1c-v3-2026-09-30.html")
HEAD_TXT = os.path.join(BR, "_head-development1c-2026-09-30.txt")
URL = "https://alsn.ru/development1c"
DATE_ISO = "2026-09-30"
PH_PHOTO = "ВСТАВЬТЕ_ССЫЛКУ_ФОТО_СОФЬИ"
PHOTO_FILE = "seo-data/brand-images/allsun-hero-vnedrenie-sofia-maznitsina.jpg"

src = open(os.path.join(p.SCR, "preview-development1c-v3.html"), encoding="utf-8").read()


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
assert ".v3 .hf{" in CSS and ".v3 .hf.wide" in CSS and ".v3 .prices.three .pc{" in CSS and ".lb{" in CSS
assert ".v3 .v3" not in CSS and ".mh" not in CSS
assert ".v3 .pass .trust a{" in CSS


def cut(start, end, keep_end=False):
    i = src.index(start)
    j = src.index(end, i)
    return src[i + len(start):j + (len(end) if keep_end else 0)].strip()


hero = cut("<!-- HERO -->", "<!-- BODY -->")
body = cut("<!-- BODY -->", "<!-- FINAL -->")
final = cut("<!-- FINAL -->", "</section>", keep_end=True)
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
for a, c in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
             ("'[data-zoom]'", "'.v3 [data-zoom]'"), ("'a[data-tab]'", "'.v3 a[data-tab]'")):
    script = script.replace(a, c)

hero = hero.replace(p.PHOTO, PH_PHOTO)
assert PH_PHOTO in hero
assert "../../" not in hero + body + final
assert "Софья Мазницына" in hero and "Софья Мазницина" not in hero
assert "Софья Мазницина" not in body and "Софья Мазницына" not in body

B1 = f'<div class="v3">\n{hero}\n</div>'
B2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'
B3 = f'<div class="v3">\n{final}\n</div>'


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


FAQ = [(strip_tags(q), strip_tags(a)) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body)]
assert len(FAQ) == 8, len(FAQ)

HOWTO = [
    ("Обращение", "Разбираем цели и процессы, не продаём коробку."),
    ("Техническое задание", "Фиксируем контур, сроки и этапы."),
    ("Оплата и работы", "Сдаём и принимаем каждый этап отдельно."),
    ("Тестирование", "Проверяете с руководителем проекта Аллсан."),
    ("Приёмка", "Акт по этапу, дальше следующий контур или запуск."),
]


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


NAME = "Внедрение 1С"
PAGE_NAME = "Внедрение 1С под ключ - УТ, КА, ERP"
DESC = (
    "Внедрение 1С под ключ: обследование, настройка УТ, КА и ERP, обучение и запуск. "
    "Для торговли и производства от 500 млн ₽/год. Консультация - Аллсан."
)
LD_DESC = (
    "Внедрение 1С под ключ: обследование процессов, подбор УТ, КА или ERP, "
    "настройка, обучение и запуск. Для торговли и производства."
)

HEAD = "\n".join([
    '<meta name="robots" content="index, follow">',
    ld({
        "@context": "https://schema.org", "@type": "Service", "@id": URL + "#service",
        "name": NAME, "serviceType": "Внедрение 1С", "url": URL,
        "description": LD_DESC,
        "provider": {"@id": "https://alsn.ru/#organization"},
        "areaServed": {"@type": "Country", "name": "RU"},
        "audience": {
            "@type": "Audience",
            "audienceType": "Торговые и производственные компании с выручкой от 500 млн рублей в год",
        },
    }),
    ld({
        "@context": "https://schema.org", "@type": "WebPage", "@id": URL + "#webpage",
        "name": PAGE_NAME, "description": LD_DESC, "url": URL, "inLanguage": "ru-RU",
        "dateModified": DATE_ISO,
        "isPartOf": {"@type": "WebSite", "@id": "https://alsn.ru/#website"},
        "about": {"@id": URL + "#service"},
    }),
    ld({
        "@context": "https://schema.org", "@type": "BreadcrumbList", "@id": URL + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/"},
            {"@type": "ListItem", "position": 2, "name": "Внедрение 1С", "item": URL},
        ],
    }),
    ld({
        "@context": "https://schema.org", "@type": "HowTo", "@id": URL + "#howto",
        "name": "Этапы внедрения 1С",
        "step": [{"@type": "HowToStep", "name": n, "text": t} for n, t in HOWTO],
    }),
    ld({
        "@context": "https://schema.org", "@type": "FAQPage", "@id": URL + "#faq",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    }),
    '<link rel="preconnect" href="https://fonts.googleapis.com">',
    '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">',
    "<style>\n" + CSS + "\n</style>",
])

for s in (HEAD, B1.replace(PH_PHOTO, "https://static.tildacdn.com/x.jpg"), B2, B3, DESC, LD_DESC):
    assert "\u2014" not in s and "\u2013" not in s
assert "депортамент" not in HEAD + B1 + B2 + B3


def box(cid, text, tpl=False):
    cls = ' class="tpl"' if tpl else ""
    return (f'<div class="copybox"><pre id="{cid}"{cls}>{html.escape(text, quote=False)}</pre>'
            f'<button type="button" data-copy="{cid}">Копировать</button></div>')


OLD_ROWS = [
    ('Обложка «"Под ключ". Без головной боли и стресса», заголовок «Внедрение 1С под ключ - УТ, КА, ERP»', "обложка T180"),
    ("«Внедрение 1С под ключ на платформе 1С:Предприятие», абзац про запуск учёта и гарантию 90 дней", "заголовок + текст T508"),
    ("«Кто внедряет 1С», карточки Сергея Львова, Павла Агеева, Никиты Соколова и остальных", "карточки команды T923"),
    ("Кнопка «Оставить заявку» сразу под карточками команды (первая на странице)", "кнопка T191"),
    ("«Стоимость внедрения 1С», подзаголовок про тарифы внедрения и сопровождения", "заголовок T65"),
    ("Таблица «Особенности тарифа / Разовое обращение / Техподдержка / Внедрение / Сопровождение»", "HTML-код T131"),
    ("«* В зависимости от величины проекта рассчитывается индивидуальная скидка!»", "текст T56"),
    ("«Над вашим проектом работают три специалиста:» менеджер проекта, аналитик, программист", "колонки T510"),
    ("«Наши клиенты» сразу после трёх специалистов (не нижняя лента логотипов над подвалом)", "заголовок T795"),
    ("Пустой блок сразу под этой надписью «Наши клиенты»", "блок T3"),
    ("«Благодарности за внедрение»", "блок T670"),
    ('«Почему выбирают "Аллсан Интеграция"?», «Более 15 лет занимаемся 1С»', "карточки T503"),
    ("«Этапы внедрения 1С», семь шагов от обращения до приёмки", "этапы T576"),
    ("«Каждый клиент получает доступ в свой Личный Кабинет»", "текст с картинкой T509"),
    ("«Примеры работ по сопровождению 1С»", "заголовок T65"),
    ("Карточки «Переход с УТ 10.3 на 11.5», «Переход с 1С:Документооборот 2.1 на 3.0» и соседние", "карточки T959"),
    ("Кнопка «Заказать консультацию» под примерами работ", "кнопка T121"),
    ("«Преимущества сотрудничества с Аллсан Интеграция», «Экономим до 50% вашего бюджета»", "текст T121"),
    ("Заголовок «Частые вопросы по внедрению 1С»", "заголовок T60"),
    ("Аккордеон из четырёх вопросов, первый пункт «Что если, я оплачу, но ваше решение меня не устроит?»", "аккордеон T849"),
    ("Заголовок «Полезные страницы по внедрению 1С»", "заголовок T60"),
    ("Пять ссылок: КА, ERP, техподдержка, 1С:КП, кейсы", "колонки T106"),
    ("«Внедряем конфигурации 1С:Предприятие под ваши процессы. Отправьте заявку на расчет…»", "заголовок T60"),
    ("Кнопка «Оставить заявку» под этим текстом (вторая на странице)", "кнопка T191"),
    ("«Какие конфигурации 1С внедряем»", "заголовок T65"),
    ("Аккордеон конфигураций, первый пункт «Внедрение и сопровождение 1С Документооборот 8»", "аккордеон T585"),
]
N_OFF = len(OLD_ROWS)
OLD = ("<table>\n<tr><th>#</th><th>Что на экране сейчас (сверху вниз)</th><th>Тип блока</th></tr>\n"
       + "\n".join(f"<tr><td>{i}</td><td>{html.escape(t, quote=False)}</td><td>{k}</td></tr>"
                   for i, (t, k) in enumerate(OLD_ROWS, 1))
       + "\n</table>")

EXTRA_CSS = """
.urlrow{display:grid;grid-template-columns:190px 1fr;gap:10px;align-items:center;margin:8px 0}
.urlrow input{width:100%;padding:9px 11px;border:1px solid #cfcfca;border-radius:8px;font:14px ui-monospace,Consolas,monospace}
.urlrow input.ok{border-color:#1a7f4b;background:#e8f6ee}
.urlstate{font-size:13px;margin-top:6px}
"""

TPL_JS = """<script>
(function(){
var P=%s;
var pres=[].slice.call(document.querySelectorAll('pre.tpl'));
pres.forEach(function(p){p._tpl=p.textContent;});
function upd(){
  var ph=document.getElementById('u-photo').value.trim();
  document.getElementById('u-photo').classList.toggle('ok',/^https:\\/\\/static\\.tildacdn\\.com\\//.test(ph));
  pres.forEach(function(p){p.textContent=p._tpl.split(P).join(ph||P);});
  var s=document.getElementById('u-state');
  s.textContent=ph?'Ссылка подставлена в код шага Д-3.':'Пока в коде стоит заглушка. Вставьте адрес фото.';
}
document.getElementById('u-photo').addEventListener('input',upd);
upd();
})();
</script>""" % json.dumps(PH_PHOTO, ensure_ascii=False)

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый дизайн страницы «Внедрение 1С» - 30.09.2026</title>
<style>{b.BRIEF_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый дизайн страницы «Внедрение 1С»</h1>
<p class="muted">Страница: «Внедрение 1С» (<a href="{URL}">{URL}</a>, в списке Тильды <code>development1c</code>) · оформление как у «Интеграция 1С с Ozon», первый экран в рамке · блоки сверены с живой страницей 30.09.2026 · каждый шаг после письменного «да» · «Опубликовать» один раз в конце (Д-7)</p>
<div class="pills"><span class="pill ok">макет готов</span><span class="pill warn">8 шагов, старое выключаем, не удаляем</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-development1c-v3.html">макет страницы</a> (открыть в браузере). Меню сайта, хлебные крошки, блок «Услуги» / «Продукты 1С», «Отзывы клиентов», нижняя лента «Наши клиенты», «Сертификаты», подвал и всплывающие формы остаются как есть. Новое меню сайта делается отдельной инструкцией, здесь его нет.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать: там данные компании, название для превью и счётчики. Меняем только HEAD этой страницы. Старые блоки выключаем, а не удаляем. robots.txt, Bing, Twitter не трогаем. Telegram-бот на сайте остаётся. Страницы «Внедрение 1С:Комплексная автоматизация» и «Стоимость внедрения 1С:ERP» этой инструкцией не трогаем.</div>

<div class="callout warn"><strong>Уже сделано - не трогать:</strong> хлебные крошки T123 «дом / Внедрение 1С» (серый текст, код не менять, только белый фон в шаге Д-2); заголовок вкладки и описание страницы (дефис, без длинного тире); фото команды в новом блоке «Кто внедряет 1С» уже с сайта, Софью Мазницыну туда не ставить; новые портреты команды загрузите отдельной задачей, когда будут готовы.</div>

<div class="toc"><strong>Шаги</strong><ol start="0">
<li><a href="#d0">Д-0. Загрузить фото Софьи Мазницыной</a></li>
<li><a href="#d1">Д-1. HEAD страницы целиком одной вставкой</a></li>
<li><a href="#d2">Д-2. Белый фон у хлебных крошек</a></li>
<li><a href="#d3">Д-3. Первый экран с фото Софьи и лентой этапов</a></li>
<li><a href="#d4">Д-4. Основная часть: паспорт услуги и разделы 01-08</a></li>
<li><a href="#d5">Д-5. Последний экран с призывом</a></li>
<li><a href="#d6">Д-6. Выключить {N_OFF} блока прошлой версии</a></li>
<li><a href="#d7">Д-7. Опубликовать</a></li>
</ol></div>

<section class="task" id="d0">
<h2><span class="num">Д-0</span> Загрузить фото Софьи Мазницыной</h2>
<span class="lbl">Что сделать</span><p>Загрузить в Тильду одно фото для первого экрана и получить его адрес. Фото команды не загружать.</p>
<span class="lbl">Зачем</span><p>Код страницы берёт картинку по адресу. Пока фото нет в Тильде, справа в рамке будет пустота.</p>
<span class="lbl">Файл на компьютере</span>
<table>
<tr><th>Что</th><th>Файл в папке проекта</th></tr>
<tr><td>Софья Мазницына у стеклянной доски с процессами «Продажи / Клиенты / Планирование / Производство / Склад / Отчетность». Координатор департамента разработки и интеграции информационных систем.</td><td><code>{PHOTO_FILE}</code></td></tr>
</table>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Внедрение 1С» (https://alsn.ru/development1c). Низ холста, над подвалом, выше блоков «Наши клиенты» и «Сертификаты».</div>
<ol class="steps">
<li>Список страниц → <code>development1c</code> → открыть на редактирование.</li>
<li>Прокрутить в самый низ холста, над подвалом → «+» → «Изображение» → блок <strong>T107</strong> («Картинка на всю ширину» или просто «Картинка»).</li>
<li>«Контент» → «Загрузить файл» → выбрать файл из таблицы → «Сохранить и закрыть».</li>
<li>Вверху редактора «Предпросмотр». На открывшейся странице внизу правой кнопкой по фото → «Открыть изображение в новой вкладке». Скопировать адрес из строки браузера. Он должен начинаться с <code>https://static.tildacdn.com/</code>. Если адрес начинается с <code>thb.tildacdn.com</code> или в нём есть <code>/-/resize/</code>, пришлите его в чат, поправлю.</li>
<li>Вставить адрес в поле ниже. Код шага Д-3 подставится сам.</li>
<li>Блок T107 → «Ещё» / три точки → «Выключить блок». <strong>Не удалять</strong>, иначе Тильда может убрать файл.</li>
</ol>
<div class="urlrow"><label for="u-photo">Адрес фото Софьи</label><input id="u-photo" placeholder="https://static.tildacdn.com/tild..../....jpg"></div>
<div class="urlstate" id="u-state"></div>
</section>

<section class="task" id="d1">
<h2><span class="num">Д-1</span> HEAD страницы целиком одной вставкой</h2>
<span class="lbl">Что сделать</span><p>Стереть всё, что сейчас лежит в HEAD страницы /development1c, и вставить один готовый код.</p>
<span class="lbl">Зачем</span><p>В коде всё оформление нового дизайна и служебные описания для поиска: услуга, страница, хлебные крошки, этапы внедрения и восемь частых вопросов ровно как на экране. Вопросы могут попасть в выдачу под ссылкой. Стили начинаются с <code>.v3</code> и не задевают меню, подвал и формы.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Список страниц → <code>development1c</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопировать старое содержимое поля в блокнот (Ctrl+A, Ctrl+C) и сохранить файл. Это откат. Сейчас там служебный код Service, WebPage, BreadcrumbList, FAQPage и HowTo: они есть и в новом коде, вопросы и этапы обновлены под новый экран.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{box('d1a', HEAD)}
<p class="muted">Если публикуете не 30.09.2026, в строке <code>"dateModified": "{DATE_ISO}"</code> поставьте дату дня публикации в том же виде ГГГГ-ММ-ДД.</p>
</section>

<section class="task" id="d2">
<h2><span class="num">Д-2</span> Белый фон у хлебных крошек</h2>
<span class="lbl">Что сделать</span><p>Поставить белый фон у блока крошек. Код крошек не менять.</p>
<span class="lbl">Зачем</span><p>Новый первый экран белый. Если у крошек другой цвет, над рамкой будет лишняя полоса.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Внедрение 1С» (https://alsn.ru/development1c). Самый верх холста, сразу под меню. Блок T123 со строкой «дом / Внедрение 1С» (в коде сайта rec3989707201). Ниже сейчас обложка «Под ключ».</div>
<ol class="steps">
<li>Блок крошек → «Настройки» / кисточка → «Цвет фона» / «Фон блока» → вставить цвет ниже.</li>
<li>Отступ сверху и снизу - 0 или около 15, чтобы не отодвигать первый экран → «Сохранить и закрыть». Сам HTML крошек не трогать.</li>
</ol>
{box('d2a', '#FFFFFF')}
</section>

<section class="task" id="d3">
<h2><span class="num">Д-3</span> Первый экран с фото Софьи и лентой этапов</h2>
<span class="lbl">Что сделать</span><p>Поставить под хлебными крошками новый первый экран в рамке: заголовок «Внедрение 1С под ключ», абзац, кнопки «Записаться на консультацию» и «Стоимость после звонка», справа фото Софьи Мазницыной с подписью «координатор департамента разработки и интеграции». Под рамкой серая лента «Как идёт внедрение» из пяти пунктов.</p>
<span class="lbl">Зачем</span><p>Человек сразу видит, что это запуск учёта под процессы, а не коробка и не техподдержка. Живой человек на фото вызывает больше доверия, чем схема. Кнопка открывает ту же форму «konsultacia», что и сейчас.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Внедрение 1С» (https://alsn.ru/development1c). Самый верх холста: меню, под ним блок T123 «дом / Внедрение 1С». Новый блок ставим сразу под крошками, выше старой обложки «Под ключ».</div>
<ol class="steps">
<li>Сначала шаг Д-0: в коде ниже должен стоять адрес фото, а не слово «ВСТАВЬТЕ_ССЫЛКУ_ФОТО_СОФЬИ».</li>
<li>Навести мышь на нижний край блока крошек → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
<div class="callout warn">Сначала сделайте шаг Д-0: в коде должен стоять адрес фото, а не заглушка.</div>
{box('d3a', B1, tpl=True)}
</section>

<section class="task" id="d4">
<h2><span class="num">Д-4</span> Основная часть: паспорт услуги и разделы 01-08</h2>
<span class="lbl">Что сделать</span><p>Одним блоком поставить всё остальное: паспорт услуги сбоку (цена после звонка, УТ / УНФ / КА / ERP, гарантия 90 дней) и разделы «На какие вопросы отвечает внедрение», «Как идут работы», «Какие конфигурации внедряем», «Как принимаем работу», «Кому подходит», «Кто внедряет 1С», «Сколько стоит», «Частые вопросы».</p>
<span class="lbl">Зачем</span><p>Паспорт с ориентиром по цене едет рядом, пока человек листает страницу, поэтому все разделы должны быть в одном блоке с ним. Вопросы на экране совпадают со служебным кодом из шага Д-1. Софьи в блоке команды нет: её фото только на первом экране.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага Д-3 → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть». Код длинный, это нормально.</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box('d4a', B2)}
</section>

<section class="task" id="d5">
<h2><span class="num">Д-5</span> Последний экран с призывом</h2>
<span class="lbl">Что сделать</span><p>Поставить серый экран «Разберём, какой контур 1С вам нужен»: одна строка пояснения, телефон +7 495 260-04-03 и кнопка «Записаться на консультацию».</p>
<span class="lbl">Зачем</span><p>Кто дочитал до конца, получает понятный следующий шаг: созвониться и понять, это УТ, КА или ERP.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага Д-4 → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box('d5a', B3)}
</section>

<section class="task" id="d6">
<h2><span class="num">Д-6</span> Выключить {N_OFF} блока прошлой версии</h2>
<span class="lbl">Что сделать</span><p>Выключить старые блоки между новым последним экраном из шага Д-5 и сеткой «Услуги» / «Продукты 1С».</p>
<span class="lbl">Зачем</span><p>Всё их содержимое теперь есть в новых блоках. Если оставить, на странице будет два главных заголовка, две команды и два списка вопросов. Выключенный блок не виден на сайте, но остаётся в редакторе на случай отката.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Внедрение 1С» (https://alsn.ru/development1c). Первый блок - старая обложка «Под ключ» под новыми блоками. Последний - аккордеон «Какие конфигурации 1С внедряем», пункт «Внедрение и сопровождение 1С Документооборот 8». Сразу под ним сетка «Услуги» и «Продукты 1С»: их <strong>не выключать</strong>.</div>
<ol class="steps">
<li>У каждого блока из таблицы → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
<li>Меню, крошки, три формы «Заказать услугу / техподдержку» между командой и тарифами (это всплывающие окна), сетку «Услуги» и «Продукты 1С», «Отзывы клиентов», нижнюю ленту «Наши клиенты», «Сертификаты», подвал, поиск, выключенный T107 из шага Д-0 и всплывающие формы внизу холста не трогать.</li>
</ol>
{OLD}
</section>

<section class="task" id="d7">
<h2><span class="num">Д-7</span> Опубликовать</h2>
<span class="lbl">Что сделать</span><p>Опубликовать страницу «Внедрение 1С».</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Вверху редактора страницы <code>development1c</code> → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано»: проверю живую страницу (один главный заголовок, фото и подпись Софьи, Софьи нет в блоке команды, паспорт, этапы, ссылки на КА и ERP, частые вопросы, кнопки, телефонная версия).</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-development1c-v3-2026-09-30.html</code> · собирает <code>seo-data/scripts/build_vnedrenie_v3_brief.py</code> из макета <code>seo-data/competitors/screens/preview-development1c-v3.html</code> · HEAD отдельно: <code>seo-data/tilda-briefs/_head-development1c-2026-09-30.txt</code></p>
</div>
{b.COPY_JS}
{TPL_JS}
</body>
</html>"""

assert "\u2014" not in doc
assert "\u2013" not in doc
assert "хаб" not in doc.lower()
open(OUT, "w", encoding="utf-8").write(doc)
open(HEAD_TXT, "w", encoding="utf-8").write(HEAD)
print("ok", OUT, "HEAD", len(HEAD), "B1", len(B1), "B2", len(B2), "B3", len(B3), "FAQ", len(FAQ), "off", N_OFF)


if __name__ == "__main__":
    pass
