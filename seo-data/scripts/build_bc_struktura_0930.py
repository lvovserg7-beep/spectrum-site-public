# -*- coding: utf-8 -*-
"""Хлебные крошки под новую структуру alsn.ru (Тильда), 30.09.2026.

Берёт свежий срез _bc-struct-2026-09-30.json (_bc_struct_probe_0930.py) и собирает инструкцию
seo-data/tilda-briefs/tier2-breadcrumbs-struktura-2026-09-30.html.
В цепочку крошек идут только страницы, которые уже открываются. Разводящие /uslugi, /produkty, /licenzii
и /dorabotka-1c ещё не созданы - после их публикации крошки дополняются отдельной волной.
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
OUT = ROOT / "seo-data/tilda-briefs/tier2-breadcrumbs-struktura-2026-09-30.html"
TPL = ROOT / "seo-data/tilda-briefs/tier2-breadcrumbs-wave-2026-09-28.html"
LIVE = {r["path"]: r for r in json.loads((HERE / "_bc-struct-2026-09-30.json").read_text(encoding="utf-8"))}

tpl = TPL.read_text(encoding="utf-8")
STYLE = tpl[tpl.index("<style>"):tpl.index("</style>") + len("</style>")]
SCRIPT = tpl[tpl.rindex("<script>"):tpl.rindex("</script>") + len("</script>")]

LIGHT, DARK = "#8a8a8a", "#cfcfcf"
HOME_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" '
            'aria-hidden="true"><path d="M12 3.2 3 10.8V21h6.2v-6.5h5.6V21H21V10.8L12 3.2z"/></svg>')
SEP = '  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>'
HEAD_PATH = ('Список страниц → страница → <strong>Настройки</strong> (шестерёнка) → <strong>Дополнительно</strong> → '
             'поле «HTML-код для вставки внутрь head»')

DEV = ("Внедрение 1С", "development1c")
PROG = ("Программы 1С", "products")
B24 = ("Интеграция Битрикс24 и 1С", "1cbitrix")
ECOM = ("Интеграция с поставщиками", "ecom")
MP = ("Модуль 1С для маркетплейсов", "casemarketplace")
OZON = ("Интеграция 1С с Ozon", "1c-ozon")

_id = [0]


def nid(p):
    _id[0] += 1
    return f"{p}-{_id[0]}"


def esc(s):
    return html.escape(s, quote=False)


def nav(color, parents, name):
    lines = [f'<nav aria-label="Хлебные крошки" style="display:flex;align-items:center;flex-wrap:nowrap;font-size:14px;'
             f'line-height:1.2;color:{color};padding:12px 20px 8px;">',
             '  <a href="https://alsn.ru/" aria-label="Главная" title="Главная" style="display:inline-flex;color:inherit;text-decoration:none;">',
             f"    {HOME_SVG}", "  </a>", SEP]
    for pname, slug in parents:
        lines += [f'  <a href="https://alsn.ru/{slug}" style="color:inherit;text-decoration:none;white-space:nowrap;">{pname}</a>', SEP]
    lines += [f'  <span style="opacity:.75;white-space:nowrap;">{name}</span>', "</nav>"]
    return "\n".join(lines)


def ld(slug, parents, name):
    items = ['    { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/" }']
    for i, (pname, pslug) in enumerate(parents, 2):
        items.append(f'    {{ "@type": "ListItem", "position": {i}, "name": "{pname}", "item": "https://alsn.ru/{pslug}" }}')
    items.append(f'    {{ "@type": "ListItem", "position": {len(parents) + 2}, "name": "{name}", "item": "https://alsn.ru/{slug}" }}')
    return ('<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n'
            f'  "@id": "https://alsn.ru/{slug}#breadcrumb",\n  "itemListElement": [\n' + ",\n".join(items) + "\n  ]\n}\n</script>")


def copybox(text, p="c"):
    i = nid(p)
    return f'<div class="copybox"><pre id="{i}">{esc(text)}</pre><button type="button" data-copy="{i}">Копировать</button></div>'


def swatch(c):
    return f'<span class="swatch" style="background:{c}"></span><code>{c}</code>'


def now_str(path):
    r = LIVE.get(path, {})
    if not r.get("navs"):
        return "нет крошек"
    return "дом / " + " / ".join(r["navs"][0]["names"])


def new_str(parents, name):
    return "дом / " + " / ".join([p for p, _ in parents] + [name])


# (path, parents, name, режим, первый экран / ориентир)
# режим: showcase - витрина каталога: путь переносим из HEAD в T123 (HEAD витрины копируется на карточки товаров)
#        page     - обычная страница: T123 на экране, путь в HEAD
#        new_dark - крошек нет: новый T123 на тёмном первом экране
GROUPS = [
    ("С-1", "Конфигурации 1С: встают под «Внедрение 1С»",
     "Страницы конфигураций переходят в раздел «Внедрение 1С под ключ» (в новом меню это третий уровень под ним). "
     "В крошках добавляется звено «Внедрение 1С» со ссылкой на <code>/development1c</code>, как уже сделано на «Стоимость 1С:ERP» и «1С:Комплексная автоматизация».",
     "Гость видит, что конфигурация - часть услуги внедрения, и в один клик переходит к общей странице. Поисковик связывает страницы в один раздел.",
     [("/upt8", [DEV], "1С:УТ", "showcase"),
      ("/buhv8", [DEV], "1С:Бухгалтерия", "showcase"),
      ("/zup8", [DEV], "1С:ЗУП", "showcase"),
      ("/upravlenie_nashei_firmoi", [DEV], "1С:УНФ", "showcase")]),
    ("С-2", "«Продукты» переименовать в «Программы 1С»",
     "На странице <code>/products</code> в крошках написано «Продукты». В новом меню «Продукты» - это модуль для маркетплейсов, интеграция с поставщиками и боты, "
     "а <code>/products</code> стоит в «Лицензиях» под именем «Программы 1С». Имя в крошках меняем на «Программы 1С».",
     "Иначе в меню и в крошках одно слово «Продукты» ведёт в разные места. Под этим же именем витрина встанет родителем у 1С:КП, 1С:Фреш и других (задача С-3).",
     [("/products", [], "Программы 1С", "showcase")]),
    ("С-3", "Витрины лицензий: встают под «Программы 1С»",
     "В крошки витрин добавляется звено «Программы 1С» со ссылкой на <code>/products</code>. Для «Фастфуд и Общепит» крошек нет совсем - ставим новые.",
     "Так устроены «Лицензии» в новом меню: «Программы 1С», под ними витрины. Гость с витрины 1С:КП в один клик попадает на все программы 1С.",
     [("/its", [PROG], "1С:КП", "showcase"),
      ("/1cfresh", [PROG], "1С:Фреш", "showcase"),
      ("/dokumentooborot8", [PROG], "1С:Документооборот", "showcase"),
      ("/dopolnitelnie_licenzii", [PROG], "Лицензии 1С", "showcase"),
      ("/1_obschepit_fastfood", [PROG], "Фастфуд и Общепит", "new_dark",
       "обложка T1065 на тёмном фоне <code>#212121</code> с заголовком «1C:Предприятие 8. Фастфуд и Общепит»", "#212121")]),
    ("С-4", "Остальные страницы с новым родителем",
     "Три страницы получают родителя по новой структуре: «Интеграция с сайтом» - под «Интеграция Битрикс24 и 1С», "
     "страница для продавцов компьютерной техники - под «Интеграция с поставщиками», перевыставление последней мили - под «Интеграция 1С с Ozon».",
     "Путь повторяет новое меню: из крошек гость попадает на страницу продукта, к которому относится эта страница.",
     [("/integrationsite", [B24], "Интеграция с сайтом", "page"),
      ("/integraciya-1c-dlya-prodavcov-kompyuternoy-tehniki", [ECOM], "Для продавцов компьютерной техники", "new_page",
       "Zero-блок T396 на чёрном фоне, заголовок «Интеграция 1C для продавцов компьютерной техники»", "#000000"),
      ("/perevystavlenie-uslug-posledney-mili-ozon-v-1s", [MP, OZON], "Последняя миля Ozon", "new_page",
       "обложка T1065 на фото с тёмной вуалью, заголовок «Перевыставление услуг последней мили ОЗОН с НДС за три клика в 1С»", "#000000")]),
]


def page_head(path, parents, name):
    r = LIVE[path]
    A(f'<h3>{esc(r.get("h1", ""))}</h3>')
    A(f'<p class="muted"><a href="https://alsn.ru{path}">https://alsn.ru{path}</a> · адрес в Тильде <code>{path.lstrip("/")}</code> · '
      f'было: {esc(now_str(path))} · станет: <strong>{esc(new_str(parents, name))}</strong></p>')


def task_showcase(path, parents, name):
    r = LIVE[path]
    n = r["navs"][0]
    slug = path.lstrip("/")
    has_ld = bool(r.get("lds"))
    bg = n["bg"] or "не задан (белая полоса)"
    A(f'<p>Где: самый верх, сразу под меню, блок T123 <code>rec{n["rec"]}</code> со строкой «{esc(" / ".join(n["names"]))}». '
      f'Фон блока {swatch(n["bg"]) if n["bg"] else bg} не меняем.</p>')
    A('<ol class="steps"><li>Список страниц → <code>' + slug + '</code> → <strong>Редактировать</strong>.</li>'
      '<li>Блок крошек под меню → <strong>Контент</strong>. Сейчас в блоке такой код:</li></ol>')
    A('<p class="cap find">Найти (весь код блока)</p>' + copybox(n["raw"].replace("> <", ">\n<"), "f"))
    A('<ol class="steps" start="3"><li>Выделить весь код в поле (Ctrl+A) и заменить на:</li></ol>')
    A('<p class="cap put">Заменить на</p>' + copybox(nav(n["color"] or LIGHT, parents, name) + "\n" + ld(slug, parents, name), "p"))
    A('<ol class="steps" start="4"><li><strong>Сохранить</strong>.</li></ol>')
    if has_ld:
        l = r["lds"][0]
        A(f'<p>В HEAD страницы: удалить старый служебный путь. Он уже перенесён в блок выше, а из HEAD витрины Тильда копирует его на все карточки товаров.</p>'
          f'<ol class="steps"><li>{HEAD_PATH} (<code>{slug}</code>).</li><li>Найти (Ctrl+F):</li></ol>')
        A('<p class="cap find">Найти</p>' + copybox(l["id"] or f"https://alsn.ru/{slug}#breadcrumb", "f"))
        A('<ol class="steps" start="3"><li>Выделить весь блок, в котором стоит эта строка: от ближайшего сверху <code>&lt;script type="application/ld+json"&gt;</code> '
          f'до ближайшего снизу <code>&lt;/script&gt;</code> (путь «{esc(" / ".join(a for a, _ in l["items"]))}»). Вот он целиком:</li></ol>')
        A('<p class="cap find">Удалить</p>' + copybox(l["raw"], "f"))
        A('<ol class="steps" start="4"><li>Остальное в HEAD не трогать, скрипт карточек товаров (если есть) оставить. <strong>Сохранить</strong>.</li></ol>')
    else:
        A('<p class="muted">В HEAD этой страницы служебного пути нет, трогать HEAD не нужно.</p>')


def task_page(path, parents, name):
    r = LIVE[path]
    n = r["navs"][0]
    slug = path.lstrip("/")
    l = r["lds"][0]
    A(f'<p>Где: самый верх, сразу под меню, блок T123 <code>rec{n["rec"]}</code> со строкой «{esc(" / ".join(n["names"]))}». Фон {swatch(n["bg"])} не меняем.</p>')
    A('<ol class="steps"><li>Список страниц → <code>' + slug + '</code> → <strong>Редактировать</strong>.</li>'
      '<li>Блок крошек под меню → <strong>Контент</strong> → найти:</li></ol>')
    A('<p class="cap find">Найти</p>' + copybox(f'<span style="opacity:.75;white-space:nowrap;">{n["names"][-1]}</span>', "f"))
    rep = "\n".join(
        [f'<a href="https://alsn.ru/{s}" style="color:inherit;text-decoration:none;white-space:nowrap;">{p}</a>\n{SEP}' for p, s in parents]
        + [f'  <span style="opacity:.75;white-space:nowrap;">{name}</span>'])
    A('<p class="cap put">Заменить на</p>' + copybox(rep, "p"))
    A('<ol class="steps" start="3"><li><strong>Сохранить</strong>.</li></ol>')
    A(f'<ol class="steps"><li>{HEAD_PATH} (<code>{slug}</code>).</li><li>Найти (Ctrl+F):</li></ol>')
    A('<p class="cap find">Найти</p>' + copybox(l["id"], "f"))
    A('<ol class="steps" start="3"><li>Выделить весь этот блок от <code>&lt;script type="application/ld+json"&gt;</code> до <code>&lt;/script&gt;</code> и заменить на:</li></ol>')
    A('<p class="cap put">Заменить на</p>' + copybox(ld(slug, parents, name), "p"))
    A('<ol class="steps" start="4"><li><strong>Сохранить</strong>.</li></ol>')


def task_new(path, parents, name, where, bg, in_t123):
    slug = path.lstrip("/")
    A(f'<p>Где: крошек на странице нет, старого блока со стрелкой тоже нет. Первый экран - {where}. Фон нового T123: {swatch(bg)}, текст светло-серый.</p>')
    A('<ol class="steps"><li>Список страниц → <code>' + slug + '</code> → <strong>Редактировать</strong>.</li>'
      '<li>Навести на первый экран с заголовком → «+» <strong>сверху</strong> → Библиотека блоков → <strong>Другое</strong> → <strong>T123 «HTML-код»</strong>.</li>'
      '<li>Контент T123 → вставить:</li></ol>')
    code = nav(DARK, parents, name) + ("\n" + ld(slug, parents, name) if in_t123 else "")
    A('<p class="cap put">В T123</p>' + copybox(code, "p"))
    A(f'<ol class="steps" start="4"><li>Настройки T123 → «Цвет фона» <code>{bg}</code>, отступы сверху и снизу 0. <strong>Сохранить</strong>.</li></ol>')
    if in_t123:
        A('<p class="muted">Это витрина каталога: служебный путь положен в сам T123, в HEAD страницы его не ставим, иначе Тильда скопирует его на карточки товаров. '
          'Скрипт для карточек этой витрины - задача В-5 в <code>tier2-breadcrumbs-wave-2026-09-28.html</code>, она остаётся.</p>')
    else:
        A(f'<ol class="steps"><li>{HEAD_PATH} (<code>{slug}</code>) → в конец, ничего не стирая, вставить:</li></ol>')
        A('<p class="cap put">В HEAD страницы</p>' + copybox(ld(slug, parents, name), "p"))
        A('<ol class="steps" start="2"><li><strong>Сохранить</strong>.</li></ol>')


parts = []
A = parts.append
all_pages = [x for g in GROUPS for x in g[4]]

A('<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
  '  <title>Хлебные крошки под новую структуру - alsn.ru - 30.09.2026</title>\n  ' + STYLE + '\n</head>\n<body>\n  <div class="wrap">')
A('<h1>Хлебные крошки под новую структуру сайта</h1>')
A('<p class="muted">Сверка с живым alsn.ru 30.09.2026 · только Тильда, не Битрикс · вид как в каталоге: иконка дома и <code>/</code> · '
  'структура: <code>struktura-karta-2026-09-30.html</code></p>')
A(f'<div class="pills"><span class="pill warn">{len(all_pages)} страниц с новым путём</span>'
  '<span class="pill info">8 витрин: путь переезжает из HEAD в блок крошек</span><span class="pill danger">3 страницы без крошек</span></div>')
A('<div class="callout danger">Каждый шаг - только после письменного «да». «Опубликовать» - отдельным шагом по каждой странице. '
  'robots.txt, Twitter и Bing не трогаем. HEAD сайта (Organization, WebSite) не трогаем. Адреса страниц не меняем.</div>')
A('<div class="callout info"><strong>Как считали.</strong> Путь строится по новому меню, но в него попадают только страницы, которые уже открываются. '
  'Разводящих «Услуги» (<code>/uslugi</code>), «Продукты» (<code>/produkty</code>), «Лицензии» (<code>/licenzii</code>) и страницы «Разработка и доработка 1С» '
  '(<code>/dorabotka-1c</code>) пока нет, поэтому в крошках их тоже нет. Когда они выйдут, крошки дополним отдельной короткой волной (список внизу).</div>')
A('<div class="callout warn"><strong>Витрины каталога.</strong> На восьми страницах с товарами служебный путь сейчас лежит в HEAD страницы. '
  'Тильда копирует HEAD витрины на все карточки товаров, поэтому у каждой карточки поисковик видит путь самой витрины, например «Главная / 1С:КП» на карточке '
  'отраслевого 1С:КП (проверено 30.09.2026). Раз путь всё равно меняем, переносим его внутрь блока крошек T123: на карточки он больше не попадёт. '
  'Так требует и правило каталога (<code>tilda-catalog-jsonld.mdc</code>).</div>')

rows = "".join(
    f'<tr><td>{esc(LIVE[p].get("h1", ""))}<br><a href="https://alsn.ru{p}">https://alsn.ru{p}</a></td>'
    f'<td>{esc(now_str(p))}</td><td><strong>{esc(new_str(par, nm))}</strong></td><td>{g[0]}</td></tr>'
    for g in GROUPS for (p, par, nm, *_rest) in g[4])
A('<section class="task" id="list"><h2>Список страниц</h2>'
  '<table><tr><th>Страница</th><th>Сейчас на экране</th><th>Станет</th><th>Задача</th></tr>' + rows + '</table></section>')

toc = "".join(f'<li><a href="#{g[0].lower().replace("-", "")}">{g[0]}. {g[1]}</a></li>' for g in GROUPS)
A(f'<div class="toc"><strong>Задачи</strong><ol>{toc}<li><a href="#pub">Опубликовать</a></li><li><a href="#wait">Ждут новых страниц</a></li>'
  '<li><a href="#skip">Что не делать</a></li></ol></div>')

for tid, title, what, why, pages in GROUPS:
    A(f'<section class="task" id="{tid.lower().replace("-", "")}"><h2><span class="num">{tid}</span> {title}</h2>')
    A(f'<span class="lbl">Что сделать</span><p>{what}</p><span class="lbl">Зачем</span><p>{why}</p>')
    A('<span class="lbl">Как в Тильде</span>')
    for item in pages:
        path, parents, name, mode = item[:4]
        page_head(path, parents, name)
        if mode == "showcase":
            task_showcase(path, parents, name)
        elif mode == "page":
            task_page(path, parents, name)
        else:
            task_new(path, parents, name, item[4], item[5], mode == "new_dark")
        if path == "/products":
            A('<p><strong>Проверить карточки.</strong> На витрине <code>products</code> клик по блоку каталога → <strong>Контент</strong> → вкладка «Хлебные крошки». '
              'Если там вручную написано «Продукты» - заменить на «Программы 1С». Если имя берётся само и поля нет - ничего не делать.</p>')
        if path == "/perevystavlenie-uslug-posledney-mili-ozon-v-1s":
            A('<p class="muted">Раньше эта страница стояла в задаче В-8 инструкции <code>tier2-breadcrumbs-wave-2026-09-28.html</code> с путём '
              '«дом / Модуль 1С для маркетплейсов / Последняя миля Ozon». Там пункт снят с пометкой «перенесено», делать по этой инструкции.</p>')
    A('</section>')

pub = ", ".join(f"<code>{p.lstrip('/')}</code>" for p, *_ in all_pages)
A('<section class="task" id="pub"><h2><span class="num">P</span> Опубликовать</h2><ol class="steps">'
  f'<li>После «да» по задаче нажать <strong>«Опубликовать»</strong> на каждой затронутой странице: {pub}.</li>'
  '<li>«Опубликовать все страницы» не нужно: HEAD сайта не меняли.</li></ol></section>')

A('<section class="task" id="wait"><h2>Ждут новых страниц - сейчас не трогать</h2><table><tr><th>Страницы</th><th>Что изменится</th><th>Когда</th></tr>'
  '<tr><td>«Внедрение 1С», «Техподдержка 1С», «Битрикс24», «Интеграция Битрикс24 и 1С»</td><td>звено «Услуги» между домом и страницей</td><td>после выхода <code>/uslugi</code></td></tr>'
  '<tr><td>«Модуль 1С для маркетплейсов», «Интеграция с поставщиками», «Telegram-бот 1С»</td><td>звено «Продукты»</td><td>после выхода <code>/produkty</code></td></tr>'
  '<tr><td>«Программы 1С», «Битрикс24» в лицензиях, «Подбор и установка 1С за день» (<code>/utp</code>)</td><td>звено «Лицензии»</td><td>после выхода <code>/licenzii</code></td></tr>'
  '<tr><td>Синхронизации БП, УТ, ЗУП и «Интеграция с экосистемой» (<code>/integrationeco</code>)</td><td>родитель «Разработка и доработка 1С». До выхода страницы синхронизации делаются по В-8 под «Техподдержка 1С»</td><td>после выхода <code>/dorabotka-1c</code></td></tr>'
  '<tr><td>Страницы Telegram-бота <code>/tb*</code> (11 шт.)</td><td>«дом / Telegram-бот 1С / …» - родитель по новой структуре тот же</td><td>третья волна крошек</td></tr>'
  '<tr><td>WhatsApp-бот (<code>/whatsapp</code>)</td><td>крошки не правим: страницу убираем</td><td>отдельная задача</td></tr>'
  '</table></section>')

A('<section class="task" id="skip"><h2>Что не делать</h2><ul class="tight">'
  '<li>Не вставлять в крошки «Услуги», «Продукты», «Лицензии», «Разработка и доработка 1С», пока этих страниц нет: ссылка вела бы на 404.</li>'
  '<li>Не оставлять служебный путь витрины и в HEAD, и в T123 одновременно: на странице будет два пути.</li>'
  '<li>Не класть служебный путь витрины в карточки товаров, во вкладку SEO товара и в HEAD сайта.</li>'
  '<li>Не менять фон существующих блоков крошек и не удалять скрипт карточек товаров в HEAD витрин.</li>'
  '<li>Не писать на экране «Главная →». Только иконка дома и <code>/</code>.</li>'
  '<li>Не править robots.txt, Twitter, Bing. Не смешивать с Битрикс. Telegram-бот не снимаем.</li></ul></section>')

A('<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-breadcrumbs-struktura-2026-09-30.html</code> · сборщик: <code>seo-data/scripts/build_bc_struktura_0930.py</code> · '
  'срез сайта: <code>seo-data/scripts/_bc-struct-2026-09-30.json</code> (<code>_bc_struct_probe_0930.py</code>)</p>')
A('  </div>\n  ' + SCRIPT + '\n</body>\n</html>\n')

text = "\n".join(parts).replace("\u2014", "-").replace("\u2013", "-")
if __name__ == "__main__":
    OUT.write_text(text, encoding="utf-8")
    print(OUT, len(text), "страниц:", len(all_pages))
