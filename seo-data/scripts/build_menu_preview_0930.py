# -*- coding: utf-8 -*-
"""Макеты верхнего меню alsn.ru кодом (T123 в Header) в стиле страниц v3.

Вариант A - светлая шапка и мега-панель. Вариант B - тёмная шапка и каскадные списки.
Выход: seo-data/competitors/screens/preview-menu-v3-{a,b}.html и сводная страница вариантов.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "seo-data/competitors/screens"
OPTIONS = ROOT / "seo-data/competitors/mp-menu-design-options-2026-09-30.html"

LOGO_DARK_TEXT = "../../logo/Аллсан_6.png"
LOGO_WHITE_TEXT = "https://static.tildacdn.com/tild6634-3863-4731-a232-653239393635/_5.png"
PHONE, PHONE_HREF = "+7 495 260-04-03", "tel:+74952600403"
CONSULT_HREF = "#popup:consult"
SEARCH_HREF = "#opensearch"

# Раздел: (название, ссылка «Все ...», промо, колонки)
# Колонка: (заголовок, ссылка, описание, [(пункт, ссылка, пометка)])
MENU = [
    ("Услуги", ("Все услуги", "/uslugi"),
     ("Реакция от 15 минут", "Программист, аналитик и руководитель проекта на связи по вашей 1С.",
      "Получить консультацию", CONSULT_HREF),
     [
         ("Внедрение 1С под ключ", "/development1c", "Запуск учёта с нуля или переход на новую конфигурацию", [
             ("1С:ERP", "/erp-time-price", ""),
             ("1С:Управление торговлей", "/upt8", ""),
             ("1С:Комплексная автоматизация", "/kompleksnaya_avtomatizaciya", ""),
             ("1С:Бухгалтерия", "/buhv8", ""),
             ("1С:ЗУП", "/zup8", ""),
             ("1С:УНФ", "/upravlenie_nashei_firmoi", ""),
         ]),
         ("Разработка и доработка 1С", "/dorabotka-1c", "Отчёты, печатные формы, обмены, исправление чужих правок", []),
         ("Техническая поддержка 1С", "/support1c", "Внешний отдел 1С вместо штатного программиста", []),
         ("Битрикс24", "/bitrix24", "Готовые решения и быстрое внедрение", [
             ("Внедрение Битрикс24", "/bitrix24", ""),
             ("Интеграция сайта с 1С и Битрикс24", "/1cbitrix", ""),
         ]),
     ]),
    ("Продукты", ("Все продукты", "/produkty"),
     ("Модуль 1С для Ozon и WB", "40 700 ₽ за площадку, 69 990 ₽ за обе, с НДС 5%. Остатки, заказы и юнит-экономика в вашей 1С.",
      "Смотреть решение", "/casemarketplace"),
     [
         ("Интеграция 1С с маркетплейсами", "/casemarketplace", "Остатки, заказы и финансы Ozon и WB в 1С", [
             ("Ozon", "/1c-ozon", "FBO, FBS, rFBS, DBS"),
             ("Wildberries", "/1c-wildberries", "FBO, FBS, DBS"),
         ]),
         ("Интеграция 1С с поставщиками B2B", "/ecom", "Цены, остатки, резерв и заказы телеком и IT-поставщиков", [
             ("Все поставщики", "/b2b-postavshiki", ""),
         ]),
         ("Чат-боты 1С для мессенджеров", "/telegram1c", "Данные 1С в мессенджере сотрудника", [
             ("Телеграм-бот 1С", "/telegram1c", ""),
             ("Бот 1С для MAX", "/max1c", "новое"),
         ]),
     ]),
    ("Лицензии", ("Все лицензии", "/licenzii"),
     ("Официальный партнёр 1С", "ТОП 10 ЦРА. Подберём лицензию под задачу и сразу поможем с установкой и внедрением.",
      "Подобрать лицензию", "/licenzii"),
     [
         ("Программы 1С", "/products", "Коробки, облако и договор поддержки", [
             ("1С:Бухгалтерия", "/licenzii-1c-buhgalteriya", ""),
             ("1С:Управление торговлей", "/licenzii-1c-ut", ""),
             ("1С:Комплексная автоматизация", "/licenzii-1c-ka", ""),
             ("1С:ЗУП", "/licenzii-1c-zup", ""),
             ("1С:УНФ", "/licenzii-1c-unf", ""),
             ("1С:КП (ИТС)", "/its", ""),
             ("1С:Fresh", "/1cfresh", ""),
             ("1С:Документооборот", "/dokumentooborot8", ""),
             ("Лицензии 1С", "/dopolnitelnie_licenzii", ""),
         ]),
         ("Битрикс24", "/bitrix24", "Лицензии и тарифы Битрикс24", []),
     ]),
    ("Наш опыт", None, None, [
        ("Кейсы", "/cases", "Задача, решение и результат по проектам", []),
        ("Отзывы", "/clients", "Письма и видеоотзывы клиентов", []),
        ("СМИ о нас", "/publication", "Публикации и интервью", []),
    ]),
    ("О компании", None, None, [
        ("О компании", "/about_us", "", []),
        ("Реальная автоматизация", "/cra", "", []),
        ("Команда", "/persons", "", []),
        ("Блог", "/blog", "", []),
        ("Вакансии", "/vacancy", "", []),
        ("Для стажёров", "/internship", "", []),
        ("Контакты", "/contacts", "", []),
    ]),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

BASE_CSS = """
:root{--bg:#F7F8FA;--acc:#F55823;--ink:#212121;--line:#D7DADD;--soft:#FDE7DE;--mut:#6b7075}
*{box-sizing:border-box}
body{margin:0;font-family:Onest,system-ui,sans-serif;color:var(--ink);background:#fff}
a{color:inherit;text-decoration:none}
.in{max-width:1240px;margin:0 auto;padding:0 28px}
.demo-note{background:var(--bg);border-bottom:1px solid var(--line);font-size:13px;color:var(--mut);padding:8px 0}
.demo-note b{color:var(--ink)}
.page{padding:28px 0 120px}
.crumbs{font-size:14px;color:#8a8a8a;display:flex;gap:8px;align-items:center;margin-bottom:34px}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--acc);margin-bottom:22px}
.rails{display:flex;flex-direction:column;gap:4px}.rails i{display:block;height:2px;width:22px;background:var(--acc);border-radius:2px}
.page h1{font-size:68px;line-height:1.02;font-weight:800;letter-spacing:-.03em;margin:0 0 22px;max-width:900px}
.page h1 span{color:var(--acc)}
.page .lead{font-size:20px;line-height:1.5;color:#3d4247;max-width:720px}
.btn{display:inline-flex;align-items:center;gap:10px;padding:12px 20px;border-radius:12px;font-weight:600;font-size:15px;white-space:nowrap;border:0;cursor:pointer;font-family:inherit}
.btn.m{background:var(--acc);color:#fff}
.btn.m:hover{background:#e04c1a}
@media(max-width:1000px){.in{padding:0 18px}.page h1{font-size:44px}}
"""

# ---------- Вариант A: светлая шапка + мега-панель ----------
CSS_A = """
.mh{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.96);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.mh .bar{display:flex;align-items:center;gap:28px;height:76px}
.mh .logo{display:flex;align-items:center;flex:0 0 auto}
.mh .logo img{height:54px;width:auto;display:block}
.mh nav{flex:1 1 auto}
.mh .top{display:flex;gap:4px;margin:0;padding:0;list-style:none}
.mh .top>li>button,.mh .top>li>a{display:flex;align-items:center;gap:7px;height:76px;padding:0 14px;background:none;border:0;font:600 15.5px Onest,sans-serif;color:var(--ink);cursor:pointer;position:relative}
.mh .top>li>button::after{content:"";width:7px;height:7px;border-right:1.8px solid currentColor;border-bottom:1.8px solid currentColor;transform:rotate(45deg) translateY(-3px);transition:transform .2s}
.mh .top>li>button::before{content:"";position:absolute;left:14px;right:14px;bottom:-1px;height:2px;background:var(--acc);transform:scaleX(0);transition:transform .2s}
.mh .top>li.open>button,.mh .top>li>button:hover{color:var(--acc)}
.mh .top>li.open>button::before{transform:scaleX(1)}
.mh .top>li.open>button::after{transform:rotate(-135deg) translateY(-1px)}
.mh .tools{display:flex;align-items:center;gap:14px;flex:0 0 auto}
.mh .ph{font-weight:700;font-size:15.5px;white-space:nowrap}
.mh .ph small{display:block;font-weight:400;font-size:12px;color:var(--mut)}
.mh .ic{width:40px;height:40px;border-radius:12px;border:1px solid var(--line);display:grid;place-items:center;background:#fff;cursor:pointer}
.mh .ic:hover{border-color:var(--acc);color:var(--acc)}
.mh .ic svg{width:18px;height:18px}
.mh .burger{display:none}
/* мега-панель */
.mh .panel{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 24px 48px rgba(33,33,33,.10);opacity:0;visibility:hidden;transform:translateY(-6px);transition:opacity .18s,transform .18s,visibility .18s}
.mh li.open>.panel{opacity:1;visibility:visible;transform:none}
.mh .pin{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:40px;padding:32px 28px 36px;max-width:1240px;margin:0 auto}
.mh .cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 32px;align-content:start}
.mh .cols.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.mh .cols.c2{grid-template-columns:repeat(2,minmax(0,1fr))}
.mh .promo{align-self:start}
.mh .col h4{margin:0 0 4px;font-size:16px;font-weight:700;line-height:1.3}
.mh .col h4 a{display:inline-flex;gap:8px;align-items:baseline}
.mh .col h4 a:hover{color:var(--acc)}
.mh .col h4 a::before{content:"";flex:0 0 14px;height:2px;background:var(--acc);transform:translateY(-4px)}
.mh .col p{margin:0 0 12px 22px;font-size:13.5px;line-height:1.45;color:var(--mut)}
.mh .col ul{list-style:none;margin:0 0 0 22px;padding:0;display:grid;gap:2px}
.mh .col ul a{display:flex;justify-content:space-between;gap:10px;padding:6px 10px;margin-left:-10px;border-radius:8px;font-size:14.5px;color:#3d4247}
.mh .col ul a:hover{background:var(--bg);color:var(--ink)}
.mh .col ul em{font-style:normal;font-size:12px;color:var(--mut);white-space:nowrap}
.mh .col ul em.new{color:var(--acc);background:var(--soft);border-radius:6px;padding:1px 7px}
.mh .all{grid-column:1/-1;display:flex;align-items:center;gap:10px;padding-top:18px;border-top:1px solid var(--line);font-weight:600;font-size:14.5px;color:var(--acc)}
.mh .all::after{content:"→"}
.mh .promo{background:var(--bg);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:10px;border:1px solid var(--line)}
.mh .promo .k{font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--acc)}
.mh .promo b{font-size:20px;line-height:1.25}
.mh .promo p{margin:0;font-size:14px;line-height:1.5;color:#3d4247}
.mh .promo .btn{margin-top:auto;align-self:flex-start}
.mh .simple{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px 24px;padding:24px 28px 28px;max-width:1240px;margin:0 auto}
.mh .simple a{padding:10px 12px;border-radius:10px;font-weight:600;font-size:15px}
.mh .simple a span{display:block;font-weight:400;font-size:13px;color:var(--mut);margin-top:2px}
.mh .simple a:hover{background:var(--bg);color:var(--acc)}
.mh-shade{position:fixed;inset:76px 0 0;background:rgba(33,33,33,.18);opacity:0;visibility:hidden;transition:.18s;z-index:90}
.mh-shade.on{opacity:1;visibility:visible}
@media(max-width:1180px){.mh .ph small{display:none}.mh .top>li>button,.mh .top>li>a{padding:0 10px;font-size:15px}}
@media(max-width:1000px){
 .mh .bar{height:64px;gap:12px}.mh .logo img{height:44px}
 .mh nav,.mh .tools .btn,.mh .ph{display:none}
 .mh .tools{margin-left:auto}
 .mh .burger{display:grid}
 .mh-shade{display:none}
}
/* мобильное меню */
.mm{position:fixed;inset:64px 0 0;background:#fff;z-index:120;overflow:auto;transform:translateX(100%);transition:transform .25s;padding:8px 18px 28px;display:flex;flex-direction:column}
.mm.on{transform:none}
.mm details{border-bottom:1px solid var(--line)}
.mm summary{list-style:none;display:flex;justify-content:space-between;align-items:center;padding:16px 0;font-weight:700;font-size:18px;cursor:pointer}
.mm summary::-webkit-details-marker{display:none}
.mm summary::after{content:"+";font-weight:400;font-size:24px;color:var(--acc);line-height:1}
.mm details[open]>summary::after{content:"−"}
.mm details details{border:0;margin-left:14px}
.mm details details summary{font-size:16px;font-weight:600;padding:10px 0}
.mm .lnk{display:block;padding:10px 0 10px 14px;font-size:15.5px;color:#3d4247}
.mm .lnk.all{color:var(--acc);font-weight:600}
.mm .foot{margin-top:auto;padding-top:22px;display:grid;gap:12px}
.mm .foot .btn{justify-content:center;padding:15px}
.mm .foot .ph{font-weight:700;font-size:18px;text-align:center}
"""

# ---------- Вариант B: тёмная шапка + каскад ----------
CSS_B = """
.mh{position:sticky;top:0;z-index:100;background:#111214;color:#fff}
.mh .bar{display:flex;align-items:center;gap:26px;height:80px}
.mh .logo img{height:58px;width:auto;display:block}
.mh nav{flex:1 1 auto}
.mh .top{display:flex;gap:2px;margin:0;padding:0;list-style:none}
.mh .top>li{position:relative}
.mh .top>li>button,.mh .top>li>a{display:flex;align-items:center;gap:7px;height:80px;padding:0 14px;background:none;border:0;font:500 15.5px Onest,sans-serif;color:#e9eaec;cursor:pointer}
.mh .top>li>button::after{content:"";width:6px;height:6px;border-right:1.6px solid currentColor;border-bottom:1.6px solid currentColor;transform:rotate(45deg) translateY(-3px);opacity:.7}
.mh .top>li.open>button,.mh .top>li>button:hover{color:var(--acc)}
.mh .tools{display:flex;align-items:center;gap:14px;flex:0 0 auto}
.mh .ph{font-weight:600;font-size:15.5px;white-space:nowrap}
.mh .ic{width:40px;height:40px;border-radius:12px;border:1px solid #3a3d42;display:grid;place-items:center;background:transparent;color:#fff;cursor:pointer}
.mh .ic:hover{border-color:var(--acc);color:var(--acc)}
.mh .ic svg{width:18px;height:18px}
.mh .burger{display:none}
.mh .dd{position:absolute;left:0;top:calc(100% - 8px);min-width:300px;background:#fff;color:var(--ink);border-radius:18px;padding:10px;box-shadow:0 22px 48px rgba(0,0,0,.28);opacity:0;visibility:hidden;transform:translateY(6px);transition:.16s}
.mh li.open>.dd{opacity:1;visibility:visible;transform:none}
.mh .dd{min-width:330px}
.mh .dd>a,.mh .dd .row>a{display:block;position:relative;padding:11px 34px 11px 14px;border-radius:10px;font-size:15px;font-weight:600;line-height:1.3}
.mh .dd>a:hover,.mh .dd .row:hover>a,.mh .dd .row.open>a{background:var(--bg);color:var(--acc)}
.mh .dd .row{position:relative}
.mh .dd .row.has>a::after{content:"";position:absolute;right:16px;top:50%;width:6px;height:6px;margin-top:-3px;border-right:1.6px solid var(--mut);border-top:1.6px solid var(--mut);transform:rotate(45deg)}
.mh .dd .row>a span{display:block;font-size:12.5px;font-weight:400;color:var(--mut);margin-top:3px}
.mh .dd .all{color:var(--acc);font-weight:600;border-bottom:1px solid var(--line);border-radius:10px 10px 0 0;margin-bottom:6px}
.mh .sub{position:absolute;left:calc(100% + 6px);top:-10px;min-width:280px;background:#fff;border-radius:18px;padding:10px;box-shadow:0 22px 48px rgba(0,0,0,.22);opacity:0;visibility:hidden;transform:translateX(-4px);transition:.14s}
.mh .row:hover>.sub,.mh .row.open>.sub{opacity:1;visibility:visible;transform:none}
.mh .sub a{display:flex;justify-content:space-between;gap:10px;padding:9px 14px;border-radius:10px;font-size:14.5px;color:#3d4247}
.mh .sub a:hover{background:var(--bg);color:var(--ink)}
.mh .sub a.head{font-weight:700;color:var(--ink)}
.mh .sub em{font-style:normal;font-size:12px;color:var(--mut)}
.mh .sub em.new{color:var(--acc);background:var(--soft);border-radius:6px;padding:1px 7px}
@media(max-width:1180px){.mh .top>li>button,.mh .top>li>a{padding:0 9px;font-size:15px}}
@media(max-width:1000px){
 .mh .bar{height:64px;gap:12px}.mh .logo img{height:46px}
 .mh nav,.mh .tools .btn,.mh .ph{display:none}
 .mh .tools{margin-left:auto}.mh .burger{display:grid}
}
.mm{position:fixed;inset:64px 0 0;background:#111214;color:#fff;z-index:120;overflow:auto;transform:translateX(100%);transition:transform .25s;padding:8px 18px 28px;display:flex;flex-direction:column}
.mm.on{transform:none}
.mm details{border-bottom:1px solid #2a2d31}
.mm summary{list-style:none;display:flex;justify-content:space-between;align-items:center;padding:16px 0;font-weight:700;font-size:18px;cursor:pointer}
.mm summary::-webkit-details-marker{display:none}
.mm summary::after{content:"+";font-weight:400;font-size:24px;color:var(--acc);line-height:1}
.mm details[open]>summary::after{content:"−"}
.mm details details{border:0;margin-left:14px}
.mm details details summary{font-size:16px;font-weight:600;padding:10px 0}
.mm .lnk{display:block;padding:10px 0 10px 14px;font-size:15.5px;color:#cfd2d6}
.mm .lnk.all{color:var(--acc);font-weight:600}
.mm .foot{margin-top:auto;padding-top:22px;display:grid;gap:12px}
.mm .foot .btn{justify-content:center;padding:15px}
.mm .foot .ph{font-weight:700;font-size:18px;text-align:center}
"""

ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
ICON_BURGER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h10"/></svg>'


def e(s):
    return html.escape(s or "")


def a(href, inner, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{e(href)}"{c}>{inner}</a>'


def em(note):
    if not note:
        return ""
    cls = ' class="new"' if note == "новое" else ""
    return f"<em{cls}>{e(note)}</em>"


# ---------- разметка A ----------
def panel_a(sec, pid):
    name, allink, promo, cols = sec
    if not promo:
        items = "".join(
            a(href, e(t) + (f"<span>{e(d)}</span>" if d else "")) for t, href, d, _ in cols)
        return f'<div id="{pid}" class="panel" role="region" aria-label="{e(name)}"><div class="simple">{items}</div></div>'
    col_html = []
    for t, href, d, kids in cols:
        lis = "".join(f"<li>{a(h, e(k) + em(n))}</li>" for k, h, n in kids)
        col_html.append(
            f'<div class="col"><h4>{a(href, e(t))}</h4>'
            + (f"<p>{e(d)}</p>" if d else "")
            + (f"<ul>{lis}</ul>" if lis else "") + "</div>")
    all_html = a(allink[1], e(allink[0]), "all") if allink else ""
    k, text, btn, bhref = promo
    promo_html = (f'<aside class="promo"><span class="k">{e(name)}</span><b>{e(k)}</b><p>{e(text)}</p>'
                  f'{a(bhref, e(btn), "btn m")}</aside>')
    return (f'<div id="{pid}" class="panel" role="region" aria-label="{e(name)}"><div class="pin">'
            f'<div class="cols c{len(cols)}">{"".join(col_html)}{all_html}</div>{promo_html}</div></div>')


def header_a():
    lis = []
    for i, sec in enumerate(MENU):
        lis.append(f'<li><button type="button" aria-expanded="false" aria-controls="p{i}">{e(sec[0])}</button>'
                   f'{panel_a(sec, "p" + str(i))}</li>')
    return f"""<header class="mh" id="mh">
<div class="in bar">
 <a class="logo" href="https://alsn.ru/" aria-label="Аллсан Интеграция, на главную"><img src="{LOGO_DARK_TEXT}" alt="Аллсан"></a>
 <nav aria-label="Основное меню"><ul class="top">{''.join(lis)}</ul></nav>
 <div class="tools">
  <a class="ph" href="{PHONE_HREF}">{PHONE}<small>Пн-Пт 9:00-18:00</small></a>
  <a class="ic" href="{SEARCH_HREF}" aria-label="Поиск по сайту">{ICON_SEARCH}</a>
  <a class="btn m" href="{CONSULT_HREF}">Получить консультацию</a>
  <button class="ic burger" type="button" aria-label="Открыть меню" aria-expanded="false">{ICON_BURGER}</button>
 </div>
</div>
</header>
<div class="mh-shade" id="mhShade"></div>"""


# ---------- разметка B ----------
def dd_b(sec):
    name, allink, promo, cols = sec
    rows = [a(allink[1], e(allink[0]), "all")] if allink else []
    for t, href, d, kids in cols:
        if kids:
            sub = a(href, e(t), "head") + "".join(a(h, e(k) + em(n)) for k, h, n in kids)
            rows.append(f'<div class="row has">{a(href, e(t) + (f"<span>{e(d)}</span>" if d else ""))}'
                        f'<div class="sub">{sub}</div></div>')
        else:
            rows.append(f'<div class="row">{a(href, e(t) + (f"<span>{e(d)}</span>" if d else ""))}</div>')
    return f'<div class="dd">{"".join(rows)}</div>'


def header_b():
    lis = [f'<li><button type="button" aria-expanded="false">{e(s[0])}</button>{dd_b(s)}</li>' for s in MENU]
    return f"""<header class="mh" id="mh">
<div class="in bar">
 <a class="logo" href="https://alsn.ru/" aria-label="Аллсан Интеграция, на главную"><img src="{LOGO_WHITE_TEXT}" alt="Аллсан"></a>
 <nav aria-label="Основное меню"><ul class="top">{''.join(lis)}</ul></nav>
 <div class="tools">
  <a class="ph" href="{PHONE_HREF}">{PHONE}</a>
  <a class="ic" href="{SEARCH_HREF}" aria-label="Поиск по сайту">{ICON_SEARCH}</a>
  <a class="btn m" href="{CONSULT_HREF}">Получить консультацию</a>
  <button class="ic burger" type="button" aria-label="Открыть меню" aria-expanded="false">{ICON_BURGER}</button>
 </div>
</div>
</header>"""


# ---------- мобильное меню (общее) ----------
def mobile():
    parts = []
    for name, allink, _promo, cols in MENU:
        inner = [a(allink[1], e(allink[0]), "lnk all")] if allink else []
        for t, href, _d, kids in cols:
            if kids:
                k = a(href, "Обзор", "lnk all") + "".join(a(h, e(x), "lnk") for x, h, _ in kids)
                inner.append(f"<details><summary>{e(t)}</summary>{k}</details>")
            else:
                inner.append(a(href, e(t), "lnk"))
        parts.append(f"<details><summary>{e(name)}</summary>{''.join(inner)}</details>")
    return (f'<div class="mm" id="mm" aria-hidden="true">{"".join(parts)}'
            f'<div class="foot"><a class="ph" href="{PHONE_HREF}">{PHONE}</a>'
            f'<a class="btn m" href="{CONSULT_HREF}">Получить консультацию</a></div></div>')


JS = """
(function(){
 var mh=document.getElementById('mh'),shade=document.getElementById('mhShade'),mm=document.getElementById('mm');
 var items=[].slice.call(mh.querySelectorAll('.top>li')),t=null,desk=matchMedia('(min-width:1001px)');
 function close(){items.forEach(function(li){li.classList.remove('open');var b=li.querySelector('button');if(b)b.setAttribute('aria-expanded','false')});if(shade)shade.classList.remove('on')}
 function open(li){close();li.classList.add('open');li.querySelector('button').setAttribute('aria-expanded','true');if(shade)shade.classList.add('on')}
 items.forEach(function(li){
  var b=li.querySelector('button');if(!b)return;
  b.addEventListener('click',function(){li.classList.contains('open')?close():open(li)});
  li.addEventListener('mouseenter',function(){if(!desk.matches)return;clearTimeout(t);t=setTimeout(function(){open(li)},120)});
  li.addEventListener('mouseleave',function(){if(!desk.matches)return;clearTimeout(t);t=setTimeout(close,220)});
 });
 [].slice.call(mh.querySelectorAll('.row.has>a')).forEach(function(x){x.addEventListener('focus',function(){x.parentNode.classList.add('open')});x.parentNode.addEventListener('focusout',function(ev){if(!x.parentNode.contains(ev.relatedTarget))x.parentNode.classList.remove('open')})});
 document.addEventListener('keydown',function(ev){if(ev.key==='Escape'){close();mm.classList.remove('on')}});
 document.addEventListener('click',function(ev){if(!mh.contains(ev.target))close()});
 if(shade)shade.addEventListener('click',close);
 var bg=mh.querySelector('.burger');
 bg.addEventListener('click',function(){mm.style.top=Math.max(0,mh.getBoundingClientRect().bottom)+'px';var on=mm.classList.toggle('on');bg.setAttribute('aria-expanded',on);mm.setAttribute('aria-hidden',!on);document.body.style.overflow=on?'hidden':''});
})();
"""

PAGE = """<main class="page"><div class="in">
<div class="crumbs"><span>⌂</span>/<span>Продукты</span>/<span>Интеграция 1С с маркетплейсами</span>/<span style="color:#3d4247">Ozon</span></div>
<div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>Модуль для селлеров</div>
<h1>Интеграция 1С <span>с Ozon</span></h1>
<p class="lead">Остатки, заказы и финансы Ozon в вашей 1С. Схемы FBO, FBS, rFBS и DBS. Страница-пример: так шапка выглядит над контентом в стиле v3.</p>
</div></main>"""


def build(variant):
    css, head = (CSS_A, header_a()) if variant == "a" else (CSS_B, header_b())
    title = "светлая шапка и мега-панель" if variant == "a" else "тёмная шапка и каскадные списки"
    note = ("Наведите на пункт меню или нажмите на него. На телефоне (уже 1000 px) - кнопка меню справа."
            " Ссылки на новые страницы (/uslugi, /max1c и т.п.) заработают после их публикации.")
    doc = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Макет меню alsn.ru, вариант {variant.upper()}: {title}</title>{FONTS}
<style>{BASE_CSS}{css}</style></head><body>
<div class="demo-note"><div class="in"><b>Вариант {variant.upper()}: {title}.</b> {note} <a href="../mp-menu-design-options-2026-09-30.html" style="color:#F55823">Все варианты</a></div></div>
{head}
{mobile()}
{PAGE}
<script>{JS}</script>
<script>/* только для макета: #open=N раскрывает раздел, #mobile открывает мобильное меню */
(function(){{var h=location.hash,m=h.match(/open=(\\d)/),li=document.querySelectorAll('#mh .top>li');
if(m&&li[m[1]])li[m[1]].querySelector('button').click();
var r=h.match(/row=(\\d)/);if(m&&r){{var rows=li[m[1]].querySelectorAll('.row.has');if(rows[r[1]])rows[r[1]].classList.add('open')}}
if(h.indexOf('mobile')>-1){{document.querySelector('#mh .burger').click();var d=document.querySelectorAll('#mm>details');if(d[1]){{d[1].open=true;var dd=d[1].querySelector('details');if(dd)dd.open=true}}}}}})();</script>
</body></html>"""
    out = SCREENS / f"preview-menu-v3-{variant}.html"
    out.write_text(doc, encoding="utf-8")
    return out


def options():
    doc = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Верхнее меню alsn.ru: варианты оформления, 30.09.2026</title>{FONTS}
<style>{BASE_CSS}
.w{{max-width:1040px;margin:0 auto;padding:40px 28px 80px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.02em;margin:0 0 10px}}
.sub{{font-size:18px;color:var(--mut);margin:0 0 30px}}
.g{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}
.c{{border:1px solid var(--line);border-radius:22px;padding:26px;background:#fff;display:flex;flex-direction:column;gap:10px}}
.c .k{{font-family:monospace;color:var(--acc);font-size:14px}}
.c h2{{margin:0;font-size:24px}}
.c ul{{margin:0;padding-left:18px;color:#3d4247;line-height:1.6}}
.c .btn{{align-self:flex-start;margin-top:8px}}
.box{{margin-top:28px;background:var(--bg);border-radius:22px;padding:24px 26px;line-height:1.6;color:#3d4247}}
.box b{{color:var(--ink)}}
@media(max-width:800px){{.g{{grid-template-columns:minmax(0,1fr)}}}}
</style></head><body><div class="w">
<h1>Верхнее меню кодом: два варианта</h1>
<p class="sub">Структура одна и та же: Услуги, Продукты, Лицензии, Наш опыт, О компании, до третьего уровня. Отличается только подача.</p>
<div class="g">
<div class="c"><span class="k">A</span><h2>Светлая шапка и мега-панель</h2>
<ul><li>Белая полоса в тон страницам v3, логотип с тёмным текстом.</li>
<li>По наведению раскрывается широкая панель: 2-й уровень заголовками с описанием, 3-й уровень ссылками, справа карточка с предложением раздела.</li>
<li>Все пункты раздела видны сразу, не надо вести мышь по цепочке.</li>
<li>Затемнение страницы под панелью, ссылка «Все услуги» внизу панели.</li></ul>
<a class="btn m" href="screens/preview-menu-v3-a.html">Открыть вариант A</a></div>
<div class="c"><span class="k">B</span><h2>Тёмная шапка и каскадные списки</h2>
<ul><li>Чёрная полоса, как на сайте сейчас: привычно для постоянных клиентов.</li>
<li>Белые карточки-списки со скруглением 18 px, 3-й уровень выезжает вправо.</li>
<li>Компактнее, но до 3-го уровня нужно вести мышь по цепочке.</li></ul>
<a class="btn m" href="screens/preview-menu-v3-b.html">Открыть вариант B</a></div>
</div>
<div class="box"><b>Как это встанет в Тильду.</b> Шапка - один блок T123 на странице Header (вместо текущего T228, его выключаем, не удаляем).
Стили с префиксом, чтобы не задеть страницы. Поиск открывает стандартный поиск Тильды, кнопка «Получить консультацию» - существующую всплывающую форму.
На телефоне своя кнопка меню и раскрывающиеся списки. Перед боевой шапкой - проверка на копии Header.<br><br>
<b>Мой выбор - A.</b> Он продолжает дизайн новых страниц, третий уровень в нём виден без «охоты» мышью, а карточка справа продаёт главный продукт раздела.</div>
</div></body></html>"""
    OPTIONS.write_text(doc, encoding="utf-8")
    return OPTIONS


if __name__ == "__main__":
    for v in ("a", "b"):
        print(build(v))
    print(options())
