# -*- coding: utf-8 -*-
"""Макеты страниц «Интеграция 1С с поставщиками» на стилях v3 (эталон 1c-ozon) с первым экраном в рамке.

Страницы: /ecom (каталог поставщиков) и шаблон карточки поставщика на примере /merlion.
Стили - из preview-1c-ozon-v3.html как есть, первый экран - HERO_CSS из mp_hero_frame.py,
шапка - меню вариант C из build_menu_preview_0930.py.
Выход: seo-data/competitors/screens/preview-ecom-v3.html, preview-ecom-card-merlion-v3.html,
       seo-data/competitors/ecom-design-options-2026-09-30.html
"""
import io
import os
import re

import build_menu_preview_0930 as menu
from build_tier3_ecom_brief import FAQ
from mp_hero_frame import HERO_CSS
from sup_new_data import DROP_ROWS, NEW_CARDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCR = os.path.join(ROOT, "competitors", "screens")
SRC = os.path.join(SCR, "preview-1c-ozon-v3.html")

PHOTO = "../../brand-images/allsun-hero-ecom-suppliers.jpg"
PHOTO_ALT = ("Павел Агеев, ведущий аналитик 1С и эксперт по интеграциям Аллсан Интеграция, "
             "с коммутатором у стола с сетевым оборудованием поставщиков")
WHO = '<div class="who"><b>Павел Агеев</b> · ведущий аналитик 1С, эксперт по интеграциям</div>'
VID_XCOM = "https://vkvideo.ru/video-181185386_456239049"
IMG_XCOM = "../../brand-images/case-xcom-video-cover.jpg"
PLAY = '<span class="play"><svg viewBox="0 0 24 24" width="30" height="30"><path d="M8 5v14l11-7z" fill="#fff"/></svg></span>'
EYEBROW = '<div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>{}</div>'

# Таблица поставщиков с живой /ecom (T131 rec880605118), 30.09.2026
TABLE_RAW = (
    "Марвел ✔ ✔ ✔ &nbsp; OCS Distribution ✔ ✔ ✔ &nbsp; Мерлион ✔ ✔ ✔ ✔ Русский Свет ✔ ✔ &nbsp; &nbsp; "
    "Ресурс-Медиа ✔ ✔ ✔ &nbsp; ProWay ✔ ✔ &nbsp; &nbsp; ТФН &nbsp; &nbsp; ✔ ✔ Treolan ✔ ✔ ✔ ✔ DIGIS ✔ ✔ ✔ &nbsp; "
    "Тайпит-Мебель ✔ ✔ &nbsp; &nbsp; ЭТМ iPRO ✔ ✔ ✔ ✔ АК Системс ✔ ✔ ✔ &nbsp; AUVIX ✔ ✔ ✔ &nbsp; Асбис &nbsp; &nbsp; ✔ &nbsp; "
    "BION ✔ ✔ ✔ &nbsp; Вектор (Металлообработка) ✔ ✔ ✔ &nbsp; ВТТ ✔ ✔ ✔ &nbsp; Делия (Стамотологическая компания) ✔ ✔ ✔ &nbsp; "
    "diHouse ✔ ✔ ✔ ✔ ДССЛ ✔ ✔ &nbsp; &nbsp; KARIN ✔ ✔ ✔ &nbsp; Макспрофит ✔ ✔ ✔ &nbsp; MICS distribution company ✔ ✔ ✔ &nbsp; "
    "MONT &nbsp; &nbsp; ✔ &nbsp; Ниеншанц-Автоматика ✔ ✔ &nbsp; &nbsp; ГК НОВЫЕ ТЕХНОЛОГИИ ✔ ✔ ✔ &nbsp; 3logic group ✔ ✔ ✔ ✔ "
    "Русско-Китайский Центр Содействия Бизнесу ✔ ✔ ✔ &nbsp; KVK ✔ ✔ &nbsp; &nbsp; RM-Company ✔ ✔ &nbsp; &nbsp; "
    "СвязьКомплект ✔ ✔ ✔ &nbsp; НДК (наладочно-диагностическая компания) ✔ ✔ &nbsp; &nbsp; SDS LLC ✔ ✔ &nbsp; &nbsp; "
    "Superwave group ✔ ✔ ✔ ✔ Тайле ✔ ✔ &nbsp; &nbsp; ТД В1 Электроникс ✔ ✔ &nbsp; &nbsp; Клавторг ✔ ✔ ✔ ✔ TFN &nbsp; &nbsp; ✔ ✔ "
    "ЭЛКО Рус ✔ ✔ ✔ &nbsp; F5it ✔ ✔ &nbsp; &nbsp; МаСт гидроизоляция ✔ ✔ ✔ ✔ НАГ ✔ ✔ &nbsp; ✔ Distribution Center ✔ ✔ ✔ &nbsp; "
    "Landata &nbsp; &nbsp; &nbsp; &nbsp; Emilink &nbsp; &nbsp; ✔ ✔ Форум электро ✔ ✔ &nbsp; &nbsp; legion project ✔ ✔ &nbsp; &nbsp; "
    "DKC.MARKET ✔ &nbsp; &nbsp; &nbsp; ergolux &nbsp; &nbsp; &nbsp; &nbsp; IT PROEKT &nbsp; ✔ &nbsp; &nbsp; Zitrek &nbsp; &nbsp; &nbsp; &nbsp; "
    "Hyperline ✔ ✔ &nbsp; ✔ NARMAK ✔ ✔ ✔ ✔ Учебный центр ЭМИЛИНК МСК ✔ ✔ &nbsp; &nbsp; ENERGON ✔ ✔ &nbsp; &nbsp; "
    "Office kit (офисное оборудование) &nbsp; &nbsp; &nbsp; &nbsp; Зазеркалье дистрибуция &nbsp; &nbsp; &nbsp; &nbsp; "
    "Русклимат &nbsp; &nbsp; &nbsp; &nbsp; ЮМП (ЮНИТ МАРК ПРО) &nbsp; &nbsp; &nbsp; &nbsp; ВИМАРКЕТ &nbsp; &nbsp; &nbsp; &nbsp; "
    "КОМПЭЛ &nbsp; &nbsp; &nbsp; &nbsp;"
)
CARDS = {
    "Марвел": "marvel", "OCS Distribution": "ocs", "Мерлион": "merlion", "Русский Свет": "russkiy-svet",
    "Ресурс-Медиа": "resurs-media", "Treolan": "treolan", "DIGIS": "digis", "ЭТМ iPRO": "etm-ipro",
    "AUVIX": "auvix", "ВТТ": "vtt", "ДССЛ": "dssl", "3logic group": "3logic", "ЭЛКО Рус": "elko",
}
CARDS13 = dict(CARDS)
CARDS.update(NEW_CARDS)


def parse_table():
    rows, name = [], []
    toks = TABLE_RAW.split()
    i = 0
    while i < len(toks):
        if toks[i] in ("✔", "&nbsp;"):
            cells = [t == "✔" for t in toks[i:i + 4]]
            rows.append((" ".join(name), cells))
            name, i = [], i + 4
        else:
            name.append(toks[i])
            i += 1
    return [r for r in rows if r[0] not in DROP_ROWS]


def sup_table(rows):
    y, n = '<span class="y">✓</span>', '<span class="n">-</span>'
    tr = []
    for nm, c in rows:
        show = {"DKC.MARKET": "ДКС", "IT PROEKT": "IT Partner"}.get(nm, nm)
        label = f'<a href="https://alsn.ru/{CARDS[nm]}">{show}</a>' if nm in CARDS else show
        tr.append("<tr><td>" + label + "</td>" + "".join(f"<td>{y if v else n}</td>" for v in c) + "</tr>")
    return ('<div class="cmpw"><table class="cmp sup"><thead><tr><th>Поставщик</th><th>Остатки</th><th>Цены</th>'
            '<th>Резерв</th><th>Сайт*</th></tr></thead><tbody>' + "".join(tr) + "</tbody></table></div>")


def hero(eyebrow, h1, lead, btns):
    return (f'<section class="hf wide"><div class="in"><div class="frame">'
            f'<div class="txt">{EYEBROW.format(eyebrow)}{h1}{lead}{btns}</div>'
            f'<div class="ph"><img src="{PHOTO}" alt="{PHOTO_ALT}" fetchpriority="high"><div class="veil"></div>'
            f'{WHO}</div></div></div></section>')


def prices():
    return """
    <div class="prices three">
     <div class="pc a"><span class="badge">Основной пакет</span><div class="nm">5 поставщиков из списка</div><div class="p">103 950 ₽</div><div class="s">в год, продление по той же цене</div>
      <ul><li>Любые 5 поставщиков из таблицы</li><li>Остатки, цены, резерв</li><li>Настройка в вашей 1С</li></ul>
      <a class="btn m" href="#popup:konsultacia">Получить консультацию</a></div>
     <div class="pc"><div class="nm">+1 поставщик из списка</div><div class="p">15 645 ₽</div><div class="s">в год, к основному пакету</div>
      <ul><li>Любой следующий поставщик из таблицы</li><li>Подключаем, когда нужно</li></ul>
      <a class="btn g" href="#popup:konsultacia">Добавить поставщика</a></div>
     <div class="pc"><div class="nm">Новый поставщик</div><div class="p">208 950 ₽</div><div class="s">стартовая цена, если поставщика нет в списке</div>
      <ul><li>Интеграция под API или кабинет поставщика</li><li>Потом он появляется в списке</li></ul>
      <a class="btn g" href="#popup:konsultacia">Обсудить поставщика</a></div>
    </div>
    <p class="note">Оплата ежегодная: год продления стоит столько же, сколько покупка. Без продления модуль перестаёт получать обновления, и если поставщик изменит свой API, обмен с ним может остановиться. Цены с НДС 5%.</p>"""


def faq_html(items):
    return "\n".join(
        f'    <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(items))


TRUST = '<div class="trust"><span>с 2015 года</span><span>ТОП 10 ЦРА</span><span>1С:Франчайзи</span></div>'


def num(n):
    return f'<div class="num"><span class="n">{n:02d}</span><span class="ln"></span></div>'


SHOTS = "../../brand-images/ecom-screens/"
# экраны и описания - по инструкции seo-data/ecom-manual/manual.md
TABS = [
    ("Наличие", "ecom-1c-podbor-nalichie-postavshchik.png",
     "Колонка «Поставщик» в подборе товаров в заказ клиента 1С: остаток у подключённых поставщиков",
     "Остаток поставщика виден прямо в заказе клиента",
     "При подборе товаров в заказ клиента появляется колонка «Поставщик»: сколько штук есть у подключённых поставщиков. "
     "Менеджер отвечает клиенту из 1С.",
     "Не нужно открывать кабинеты дистрибьюторов"),
    ("Резерв", "ecom-1c-rezerv-u-postavshchika.png",
     "Документ «Резервирование у поставщиков» в 1С: номер резерва, срок действия и цена по каждой позиции",
     "Резерв по заказу клиента ставится сам",
     "На основании заказа клиента создаётся документ «Резерв у поставщика». Модуль сам резервирует товар у подходящего "
     "поставщика по самым выгодным условиям. Номер резерва, срок его действия и цена возвращаются в 1С.",
     "Номер и срок резерва видны в документе"),
    ("Сопоставление", "ecom-1c-sopostavlenie-nomenklatury.png",
     "Обработка сопоставления номенклатуры поставщика с товарами 1С по артикулу",
     "Товары поставщика связаны с вашими",
     "Каждый день модуль сам сопоставляет номенклатуру поставщика с вашей по идентификатору. "
     "Что не связалось само, менеджер сопоставляет по артикулу в одной обработке или вручную.",
     "Прайс поставщика ложится на ваши карточки"),
]
EXTRA_SHOTS = [
    ("ecom-1c-ostatki-po-praysam.png", "Отчёт «Остатки по прайсам поставщиков» в 1С: количество, цена, валюта и время обновления",
     "Остатки и цены всех поставщиков в одном отчёте",
     "По каждому поставщику: количество, цена, валюта прайса и время последнего обновления."),
    ("ecom-1c-monitor-zagruzki.png", "Отчёт «Монитор загрузки остатков поставщиков» в 1С",
     "Монитор загрузки",
     "Сколько позиций отдал поставщик, сколько попало в прайс 1С, отклонение и ошибки. Сбой видно сразу, а не когда спросит клиент."),
    ("ecom-1c-monitoring-avtorezerva.png", "Отчёт «Мониторинг авторезервирования» в 1С: резервы и запросы по поставщикам",
     "Мониторинг автоматического резерва",
     "Сколько позиций зарезервировано и сколько запросов не прошло, по каждому поставщику за период."),
    ("ecom-1c-otchet-rezervirovanie.png", "«Отчёт по резервированию» в 1С: данные заказа и данные резерва у поставщика",
     "Отчёт по резервированию",
     "Что заказал клиент и что зарезервировано: количество, цена заказа и резерва, поставщик, номер и срок резерва."),
]


def zoom(file, alt, cls, lazy=True):
    lz = ' loading="lazy"' if lazy else ""
    return (f'<a class="{cls}" href="{SHOTS}{file}" data-zoom aria-label="Открыть экран: {alt}">'
            f'<img src="{SHOTS}{file}" alt="{alt}"{lz}><span class="zoom">Открыть экран</span></a>')


def screens_hub():
    on = ' class="on"'
    btns = "".join(f'<button{on if i == 0 else ""} data-t="{i}">{t[0]}</button>' for i, t in enumerate(TABS))
    panes = "".join(
        f'<div class="pane{" on" if i == 0 else ""}"><div class="shot">{zoom(f, alt, "shotz")}</div>'
        f'<div class="txt"><b>{b}</b><p>{p}</p><div class="res">{r}</div></div></div>'
        for i, (_, f, alt, b, p, r) in enumerate(TABS))
    ex = "".join(f'<div class="ex">{zoom(f, alt, "exshot")}<b>{b}</b><p>{p}</p></div>' for f, alt, b, p in EXTRA_SHOTS)
    return f"""   <div class="sec" id="reports">
    {num(3)}
    <h2>Что видно в 1С</h2>
    <p class="sub">Настоящие экраны модуля. Нажмите на картинку, чтобы открыть её целиком.</p>
    <div class="tabs">{btns}</div>
    {panes}
    <div class="extra-h">Контроль, что всё загрузилось</div>
    <div class="extra">{ex}</div>
   </div>"""


# ---------------------------------------------------------------- /ecom
def body_hub():
    rows = parse_table()
    main = [r for r in rows if r[0] in CARDS]
    rest = [r for r in rows if r[0] not in CARDS]
    h1 = '<h1 class="long">Интеграция 1С <br>с <span>поставщиками</span><small>телеком- и IT-оборудования</small></h1>'
    lead = ('<p class="lead">Остатки, закупочные цены и резерв дистрибьюторов приходят прямо в вашу 1С. '
            'Прайс из Excel больше не нужен.</p>')
    btns = ('<div class="btns"><a class="btn m" href="#popup:konsultacia">Получить консультацию <span class="ar">→</span></a>'
            '<a class="btn g" href="#price">От 103 950 ₽</a></div>')
    return f"""
<div class="crumb-bar"><div class="in crumb">⌂ / Интеграция с поставщиками</div></div>

<!-- HERO -->
{hero("B2B-поставщики · телеком и IT", h1, lead, btns)}

<!-- DAY -->
<div class="day">
 <div class="in"><div class="box">
  <div class="lbl">Как выглядит день с интеграцией</div>
  <div class="track">
   <div class="it"><span class="t mono">по расписанию</span><b>Остатки поставщиков</b>с настроенных складов, прямо в вашей 1С</div>
   <div class="it"><span class="t mono">по расписанию</span><b>Закупочные цены</b>актуальные, без скачивания прайса</div>
   <div class="it"><span class="t mono">при заказе</span><b>Резерв у поставщика</b>модуль сам выбирает поставщика с лучшими условиями<a class="more" href="#reports" data-tab="1">Как это выглядит →</a></div>
   <div class="it"><span class="t mono">сразу</span><b>Прайс на сайте</b>если 1С уже связана с вашим сайтом, остатки поставщиков сами попадают на виртуальные склады, связанные с сайтом<a class="more" href="#suppliers">Где работает →</a></div>
   <div class="it"><span class="t mono">10-15 минут</span><b>Заказ обработан</b>вместо нескольких часов в кейсе ООО «СЦ»<a class="more" href="#case">Кейс →</a></div>
  </div>
 </div></div>
</div>

<!-- BODY -->
<section class="body">
 <div class="in">
  <aside class="pass">
   <div class="ttl">Паспорт интеграции</div>
   <div class="price">103 950 ₽</div>
   <div class="per">в год за 5 поставщиков из списка</div>
   <dl>
    <dt>Данные</dt><dd>остатки, цены, резерв</dd>
    <dt>Откуда</dt><dd>API и кабинеты поставщиков</dd>
    <dt>Доступ к API</dt><dd>логин, код или токен</dd>
    <dt>Поставщики</dt><dd>телеком и IT</dd>
    <dt>+1 поставщик</dt><dd>15 645 ₽ в год</dd>
    <dt>Новый поставщик</dt><dd>от 208 950 ₽</dd>
    <dt>Подключение</dt><dd>2 недели</dd>
    <dt>Оплата</dt><dd>ежегодно</dd>
   </dl>
   <a class="btn m" href="#popup:konsultacia">Получить консультацию</a>
   <a class="btn g" href="#suppliers">Список поставщиков</a>
   <div class="small">Цены с НДС 5%. Год продления стоит столько же, сколько покупка.</div>
   {TRUST}
  </aside>

  <div>
   <div class="sec">
    {num(1)}
    <h2>На какие вопросы отвечает интеграция</h2>
    <p class="sub">Менеджер отвечает клиенту из 1С и не открывает кабинет каждого дистрибьютора.</p>
    <div class="qpanel">
     <div class="q big">
      <b>Есть ли товар у поставщика прямо сейчас?</b>
      Остатки и цены всех подключённых поставщиков лежат в вашей 1С и обновляются по расписанию.
      <div class="mini">
       <div><span>Остатки</span><span>с настроенных складов</span></div>
       <div><span>Цены</span><span>закупочные</span></div>
       <div><span>Резерв</span><span>из 1С</span></div>
       <div><span>Прайс в Excel</span><span>не нужен</span></div>
       <div><span>Заказ в кейсе СЦ</span><span>10-15 минут</span></div>
      </div>
      <a class="go" href="#suppliers">Кто подключён →</a>
     </div>
     <div class="q"><b>У кого дешевле эта позиция?</b>Закупочные цены разных поставщиков приходят в одну базу, сравнить их можно без выгрузок.<a class="go" href="#route">Как идут данные →</a></div>
     <div class="q"><b>Как не продать то, чего нет?</b>Резерв у поставщика ставится из 1С сразу при заказе клиента, номер и срок резерва приходят в 1С.<a class="go" href="#suppliers">Где работает →</a></div>
    </div>
   </div>

   <div class="sec" id="route">
    {num(2)}
    <h2>Как идут данные</h2>
    <p class="sub">Модуль забирает данные у поставщиков через их API. Обмен идёт через отдельную транзитную базу, поэтому рабочая 1С не тормозит, даже когда поставщиков много.</p>
    <div class="route">
     <div class="node"><div class="k">Поставщики</div><b>API и кабинеты</b><ul><li>Мерлион, OCS, Treolan и другие</li><li>остатки на складах</li><li>закупочные цены</li></ul></div>
     <div class="pipe"><div>остатки и цены</div><div class="back">резерв</div></div>
     <div class="node mid"><div class="k">Модуль Аллсан</div><b>Обмен по расписанию</b><ul><li>транзитная база</li><li>сопоставление товаров</li><li>резерв у поставщика</li></ul></div>
     <div class="pipe"><div>в учёт</div><div class="back">заказы</div></div>
     <div class="node"><div class="k">Ваша 1С и сайт</div><b>Учёт и прайс</b><ul><li>остатки поставщиков</li><li>цены для прайса</li><li>остатки для сайта</li></ul></div>
    </div>
   </div>

{screens_hub()}

   <div class="sec" id="suppliers">
    {num(4)}
    <h2>Какие поставщики уже подключены</h2>
    <p class="sub">Готовые интеграции. По названию поставщика откроется страница с подробностями.</p>
    {sup_table(main)}
    <details class="cmpmore"><summary>Показать ещё {len(rest)} поставщиков</summary>
    {sup_table(rest)}
    </details>
    <p class="cmpnote">* Сайт: если ваша 1С уже связана с сайтом, настроим автоматическую загрузку остатков поставщика на виртуальные склады, связанные с сайтом. Остатки везде приходят с тех складов поставщика, которые выбраны при настройке. Штрих-коды загружаем у всех поставщиков, которые их отдают. Нужного поставщика нет в списке? Сделаем новую интеграцию.</p>

    <div class="extra-h">Что загружается в 1С</div>
    <div class="fit six">
     <div><b>Номенклатура</b><p>Карточки товаров поставщика в вашей базе.</p></div>
     <div><b>Фото и характеристики</b><p>Для карточек на сайте и в 1С.</p></div>
     <div><b>Штрих-коды</b><p>Если поставщик их отдаёт.</p></div>
     <div><b>Остатки по расписанию</b><p>С настроенных складов поставщика, без ручной загрузки.</p></div>
     <div><b>Резерв у поставщика</b><p>Вручную или сам, по заказу клиента в 1С.</p></div>
     <div><b>Аналитика заказов</b><p>Что и у кого заказывали.</p></div>
    </div>
   </div>

   <div class="sec" id="case">
    {num(5)}
    <h2>Результаты клиентов</h2>
    <p class="sub">Кейс ООО «СЦ»: 5 поставщиков телеком и IT подключены к 1С.</p>
    <div class="case solo">
     <div class="l">
      <div class="big">×3</div>
      <div class="cap">выросла производительность менеджеров ООО «СЦ»</div>
      <a class="go" href="https://alsn.ru/caseecomsc">Читать кейс ООО «СЦ» полностью →</a>
     </div>
     <div class="r">
      <blockquote>«Хотим выразить благодарность команде ООО «Аллсан Интеграция» за профессиональную реализацию проекта по интеграции 1С с B2B-поставщиками. Рекомендуем их как надежного партнера для автоматизации учета!»</blockquote>
      <div class="who"><b>Мельник О.И.</b>генеральный директор ООО «СЦ»</div>
     </div>
    </div>
    <div class="fit" style="margin-top:26px">
     <div><b>−40% трудозатрат</b><p>на работу с поставщиками: со 100% рабочего дня до 60%.</p></div>
     <div><b>10-15 минут</b><p>на обработку заказа вместо нескольких часов.</p></div>
     <div><b>2 месяца</b><p>окупаемость проекта. Остатки и цены приходят каждые 5-10 минут.</p></div>
    </div>
    <h3 class="vh">Видеоотзыв X-COM о работе с Аллсан</h3>
    <div class="letter vid">
     <a class="video" href="{VID_XCOM}" target="_blank" rel="noopener" aria-label="Смотреть видеоотзыв X-COM в новом окне">
      <img src="{IMG_XCOM}" alt="Видеоотзыв Игоря Роганкова, соучредителя X-COM, о сотрудничестве с Аллсан" loading="lazy">
      {PLAY}
      <span class="vcap">Смотреть видеоотзыв</span>
     </a>
     <div>
      <b>Игорь Роганков</b>
      <div class="vnote" style="margin:0 0 14px">соучредитель X-COM</div>
      <p>Рассказывает, как с Аллсан ускорили обработку заказов на 20%.</p>
      <a class="go" href="{VID_XCOM}" target="_blank" rel="noopener">Смотреть на VK Видео →</a>
     </div>
    </div>
   </div>

   <div class="sec">
    {num(6)}
    <h2>Кому подходит</h2>
    <div class="fit">
     <div><b>Торгуете телеком и IT-железом</b><p>Компьютеры, коммутаторы, сетевое оборудование. Закупаете у нескольких дистрибьюторов.</p></div>
     <div><b>Прайсы вручную уже не успеваете</b><p>Менеджеры каждый день скачивают Excel из кабинетов и загружают в 1С, а остатки всё равно устаревают.</p></div>
     <div><b>Продаёте через сайт</b><p>1С уже связана с сайтом, и нужно, чтобы остатки поставщиков попадали туда сами, а резерв ставился из 1С.</p></div>
    </div>
    <p class="cmpnote">Нужен обмен с Ozon и Wildberries, а не с поставщиками? Это другой продукт: <a href="https://alsn.ru/casemarketplace" style="color:var(--acc)">модуль 1С для маркетплейсов</a>.</p>
   </div>

   <div class="sec" id="price">
    {num(7)}
    <h2>Сколько стоит</h2>
    <p class="sub">Оплата раз в год. Чем больше поставщиков из списка, тем дешевле каждый.</p>
    {prices()}
   </div>

   <div class="sec faq" style="margin-bottom:40px">
    {num(8)}
    <h2>Частые вопросы об интеграции 1С с поставщиками</h2>
{faq_html(FAQ)}
   </div>
  </div>
 </div>
</section>

<section class="final">
 <div class="in">
  <div><h2>Подключим ваших поставщиков к 1С</h2><p>Пришлите список поставщиков. Скажем, кто уже есть в готовых интеграциях и сколько это будет стоить.</p><div class="ph">+7 (495) 260-04-03</div></div>
  <a class="btn m" href="#popup:konsultacia">Получить консультацию <span class="ar">→</span></a>
 </div>
</section>
"""


# ---------------------------------------------------------------- карточка
CARD_FAQ = [
    ("Чем модуль отличается от личного кабинета Merlion B2B?",
     "В кабинете Merlion B2B менеджер смотрит остатки и цены на сайте Мерлион и переносит их в 1С вручную или через Excel. "
     "Модуль подключает вашу 1С к MERLION API: остатки, закупочные цены и резерв приходят прямо в 1С."),
    ("Нужен ли доступ к API Мерлион?",
     "Да. Использование MERLION API бесплатное. Для подключения заполните заявку у Мерлион: сначала дают тестовую учётную запись, "
     "после проверки переходят на боевую."),
    ("Можно подключить других поставщиков?",
     "Да. Мерлион входит в пакет из 5 любых поставщиков из нашего списка за 103 950 ₽. Каждый следующий из списка стоит 15 645 ₽."),
    ("Нужно ли продлевать интеграцию?",
     "Да, оплата ежегодная. Год продления стоит столько же, сколько покупка. Без продления модуль перестаёт получать обновления. Цены с НДС 5%."),
]
OTHER = [("OCS", "ocs"), ("Treolan", "treolan"), ("Марвел", "marvel"), ("DIGIS", "digis"), ("ЭЛКО Рус", "elko"),
         ("3logic", "3logic"), ("ЭТМ iPRO", "etm-ipro"), ("Ресурс-Медиа", "resurs-media"), ("AUVIX", "auvix"),
         ("ВТТ", "vtt"), ("ДССЛ", "dssl"), ("Русский Свет", "russkiy-svet")]


def body_card():
    h1 = "<h1>Интеграция 1С <br>с <span>Merlion B2B</span><small>по API</small></h1>"
    lead = ('<p class="lead">Остатки и закупочные цены со складов Мерлион приходят в вашу 1С, резерв ставится из 1С. '
            'Это модуль для вашей базы, а не вход в личный кабинет Merlion B2B.</p>')
    btns = ('<div class="btns"><a class="btn m" href="#popup:konsultacia">Получить консультацию <span class="ar">→</span></a>'
            '<a class="btn g" href="#price">Сколько стоит</a></div>')
    chips = "".join(f'<a href="https://alsn.ru/{s}">{n}</a>' for n, s in OTHER)
    return f"""
<div class="crumb-bar"><div class="in crumb">⌂ / <a href="https://alsn.ru/ecom">Интеграция с поставщиками</a> / Мерлион</div></div>

<!-- HERO -->
{hero("Поставщики · Мерлион", h1, lead, btns)}

<!-- BODY -->
<section class="body" style="padding-top:56px">
 <div class="in">
  <aside class="pass">
   <div class="ttl">Паспорт интеграции</div>
   <div class="price">103 950 ₽</div>
   <div class="per">пакет из 5 поставщиков, Мерлион входит</div>
   <dl>
    <dt>Поставщик</dt><dd>Мерлион (MERLION)</dd>
    <dt>Данные</dt><dd>остатки, цены, резерв</dd>
    <dt>Сайт</dt><dd>снять и вернуть товар</dd>
    <dt>Доступ к API</dt><dd>бесплатно, по заявке</dd>
    <dt>Продление</dt><dd>не нужно</dd>
   </dl>
   <a class="btn m" href="#popup:konsultacia">Получить консультацию</a>
   <a class="btn g" href="https://alsn.ru/ecom#suppliers">Все поставщики</a>
   <div class="small">Цены с НДС 5%. +1 поставщик из списка 15 645 ₽.</div>
   {TRUST}
  </aside>

  <div>
   <div class="sec">
    {num(1)}
    <h2>Что приходит из Мерлион в 1С</h2>
    <p class="sub">Модуль забирает данные по MERLION API и кладёт их в вашу базу.</p>
    <div class="fit">
     <div><b>Остатки</b><p>Товары на складах Мерлион в вашей 1С, по расписанию.</p></div>
     <div><b>Закупочные цены</b><p>Актуальные цены Мерлион без скачивания Excel.</p></div>
     <div><b>Резерв онлайн</b><p>Товар на складе Мерлион резервируется из 1С, в том числе при заказе на вашем сайте.</p></div>
    </div>
   </div>

   <div class="sec">
    {num(2)}
    <h2>Модуль или личный кабинет</h2>
    <p class="sub">Кабинет Merlion B2B остаётся у вас. Модуль убирает ручной перенос данных из него в 1С.</p>
    <div class="extra">
     <div class="ex"><b>Личный кабинет Merlion B2B</b><p>Остатки и цены видны на сайте Мерлион. Чтобы они попали в 1С, менеджер скачивает Excel и загружает вручную. Резерв ставят в кабинете.</p><span class="need">Каждый день руками</span></div>
     <div class="ex"><b>Модуль Аллсан в 1С</b><p>Остатки и цены приходят в 1С сами. Резерв ставится из 1С, и рядом лежат данные других ваших поставщиков.</p><span class="need">Автоматически</span></div>
    </div>
   </div>

   <div class="sec">
    {num(3)}
    <h2>Как идут данные</h2>
    <div class="route">
     <div class="node"><div class="k">Мерлион</div><b>MERLION API</b><ul><li>склад и транзит</li><li>закупочные цены</li><li>заказы и резерв</li></ul></div>
     <div class="pipe"><div>остатки и цены</div><div class="back">резерв</div></div>
     <div class="node mid"><div class="k">Модуль Аллсан</div><b>Обмен по расписанию</b><ul><li>загрузка в 1С</li><li>резерв у Мерлион</li><li>другие поставщики</li></ul></div>
     <div class="pipe"><div>в учёт</div><div class="back">заказы</div></div>
     <div class="node"><div class="k">Ваша 1С и сайт</div><b>Учёт и прайс</b><ul><li>остатки Мерлион</li><li>цены для прайса</li><li>товар на сайте вкл/выкл</li></ul></div>
    </div>
   </div>

   <div class="sec">
    {num(4)}
    <h2>Как получить доступ к MERLION API</h2>
    <div class="extra">
     <div class="ex"><b>Заявка у Мерлион</b><p>Заполните форму заявки на сайте Мерлион, укажите сервис и цель: тестовая учётная запись или боевое подключение.</p><span class="need">API бесплатный</span></div>
     <div class="ex"><b>Сначала тест</b><p>Боевое использование открывают только после тестирования. Ключи вставляем в модуль и проверяем обмен на вашей базе.</p><span class="need">Поможем с настройкой</span></div>
    </div>
   </div>

   <div class="sec" id="price">
    {num(5)}
    <h2>Сколько стоит</h2>
    <p class="sub">Мерлион входит в пакет из 5 любых поставщиков из списка.</p>
    {prices()}
   </div>

   <div class="sec faq">
    {num(6)}
    <h2>Частые вопросы</h2>
{faq_html(CARD_FAQ)}
   </div>

   <div class="sec" style="margin-bottom:40px">
    <div class="extra-h" style="margin-top:0">Другие поставщики</div>
    <div class="chips">{chips}<a class="all" href="https://alsn.ru/ecom#suppliers">Весь список →</a></div>
   </div>
  </div>
 </div>
</section>

<section class="final">
 <div class="in">
  <div><h2>Подключим Мерлион к вашей 1С</h2><p>Скажите, какие ещё поставщики у вас есть. Посчитаем пакет целиком.</p><div class="ph">+7 (495) 260-04-03</div></div>
  <a class="btn m" href="#popup:konsultacia">Получить консультацию <span class="ar">→</span></a>
 </div>
</section>
"""


EXTRA_CSS = """
@media(min-width:1141px){.v3 .hf.wide .txt{width:470px}.v3 .hf.wide .ph{aspect-ratio:auto;width:calc(100% - 448px)}.v3 .hf.wide .ph img{object-position:100% 50%}}
@media(max-width:1000px){.v3 .hf h1.long{font-size:37px}}
.prices.three .pc{display:flex;flex-direction:column;padding:26px 22px}
.prices.three .pc ul{flex:1 1 auto}
.prices.three .pc .btn{margin-top:auto;padding:15px 12px;font-size:15px;white-space:nowrap;text-align:center}
.q.big .mini div{gap:14px}.q.big .mini div span+span{text-align:right}
.v3 .hf h1 small{display:block;font-size:.5em;line-height:1.2;font-weight:700;letter-spacing:-.01em;color:var(--ink);margin-top:8px}
.crumb-bar .crumb a{color:inherit}
.crumb-bar .crumb a:hover{color:var(--acc)}
.cmp.sup td:first-child a{color:var(--ink);text-decoration:none;font-weight:600;border-bottom:1px solid var(--line)}
.cmp.sup td:first-child a:hover{color:var(--acc);border-color:var(--acc)}
.cmp.sup th+th,.cmp.sup td+td{width:84px}
.fit.six{grid-template-columns:repeat(3,minmax(0,1fr));gap:22px 14px}
.pane .shotz{position:relative;display:block}
.tabs+.pane .shot img,.pane .shot img{aspect-ratio:auto;object-fit:contain}
.pane .zoom{position:absolute;right:10px;bottom:10px;background:rgba(33,33,33,.86);color:#fff;font-size:13px;font-weight:600;padding:7px 10px;border-radius:8px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips a{font-size:14px;font-weight:600;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:8px 12px}
.chips a:hover{border-color:var(--acc);color:var(--acc)}
.chips a.all{background:#fff;color:var(--acc);border-color:var(--acc)}
.mh .btn,.mm .btn{display:inline-flex;align-items:center;gap:10px;padding:12px 20px;border-radius:12px;font-weight:600;font-size:15px;white-space:nowrap;border:0;cursor:pointer;font-family:inherit}
.mh .btn.m,.mm .btn.m{background:var(--acc);color:#fff}
@media(max-width:1000px){.fit.six{grid-template-columns:minmax(0,1fr)}.cmp.sup th+th,.cmp.sup td+td{width:48px}.cmp.sup th{font-size:10.5px;letter-spacing:0}}
"""

CASE_CSS = """
.case.solo .r{padding:38px;justify-content:center}
.case.solo blockquote{margin:0}
.go{display:inline-block;margin-top:auto;padding-top:22px;color:var(--acc);font-weight:600;font-size:15px;text-decoration:none}
.go:hover{text-decoration:underline}
.vh{margin:56px 0 0;font-size:24px;font-weight:800;letter-spacing:-.02em;line-height:1.25}
.letter.vid{grid-template-columns:minmax(0,400px) minmax(0,1fr);align-items:center}
.letter.vid b{display:block;font-size:18px;margin-bottom:4px}
.letter.vid p{margin:0;font-size:15.5px;line-height:1.55;color:#3d4247}
.letter.vid .go{padding-top:14px}
@media(max-width:1000px){.letter.vid{grid-template-columns:minmax(0,1fr)}.case.solo .r{padding:28px}.vh{font-size:21px;margin-top:40px}}
"""


def page(title, body, note):
    src = io.open(SRC, encoding="utf-8").read()
    head = src[: src.index("</style>")]
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head)
    head += menu.CSS_C + "\n" + HERO_CSS + "\n" + EXTRA_CSS + CASE_CSS + "</style>\n</head>\n<body>\n"
    script = src[src.index("<script>"): src.index("</script>") + len("</script>")]
    demo = (f'<div style="background:#F7F8FA;border-bottom:1px solid #D7DADD;font:13px Onest,sans-serif;color:#6b7075;padding:8px 0">'
            f'<div class="in"><b style="color:#212121">Макет.</b> {note} '
            f'<a href="../ecom-design-options-2026-09-30.html" style="color:#F55823">Все макеты</a></div></div>')
    html = (head + demo + menu.header_a(menu.LOGO_WHITE_TEXT) + menu.mobile() + '\n<div class="v3">' + body + "</div>\n"
            + script + f"\n<script>{menu.JS}</script>\n</body>\n</html>\n")
    assert "\u2014" not in html and "\u2013" not in html, title
    return html


def index():
    doc = """<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Страницы «Интеграция 1С с поставщиками» - оформление v3 - 30.09.2026</title>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;600;800&display=swap" rel="stylesheet">
<style>
body{margin:0;font-family:'Onest',Arial,sans-serif;background:#F7F8FA;color:#212121}
.w{max-width:1100px;margin:0 auto;padding:48px 28px}
h1{font-size:40px;font-weight:800;letter-spacing:-.02em;margin:0 0 10px}
.s{color:#6b7075;font-size:16px;line-height:1.55;margin:0 0 30px;max-width:780px}
.g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
.c{display:block;background:#fff;border:1px solid #D7DADD;border-radius:20px;padding:24px 24px 22px;color:inherit;text-decoration:none}
.c:hover{border-color:#F55823}
.k{font-family:monospace;color:#F55823;font-size:13px;margin-bottom:8px}
.c b{font-size:20px}.c p{color:#3d4247;font-size:15px;line-height:1.5}.c span{color:#F55823;font-weight:600}
.n{margin-top:26px;font-size:14.5px;color:#3d4247;line-height:1.6;background:#fff;border:1px solid #D7DADD;border-radius:16px;padding:18px 22px}
.n b{color:#212121}
@media(max-width:800px){.g{grid-template-columns:1fr}}
</style></head><body><div class="w">
<h1>Страницы поставщиков в стиле v3</h1>
<p class="s">Оформление как у «Интеграции 1С с Ozon»: те же шрифты, цвета, паспорт слева, разделы с номерами. Первый экран в рамке, как на страницах модуля для маркетплейсов, с новым фото. Сверху новое меню сайта.</p>
<div class="g">
<a class="c" href="screens/preview-ecom-v3.html"><div class="k">Страница 1</div><b>Интеграция 1С с поставщиками телеком- и IT-оборудования</b>
<p>https://alsn.ru/ecom. Лента дня, паспорт с ценой, 7 разделов: вопросы, схема данных, таблица поставщиков (13 со своими страницами сверху, остальные под кнопкой), кейс ООО «СЦ» и видео X-COM, кому подходит, цены, частые вопросы из Тир 3.</p><span>Открыть макет →</span></a>
<a class="c" href="screens/preview-ecom-card-merlion-v3.html"><div class="k">Страница 2 · шаблон</div><b>Карточка поставщика на примере Мерлион</b>
<p>https://alsn.ru/merlion. Тот же первый экран, паспорт, «что приходит в 1С», «модуль или личный кабинет», как получить доступ к API, цены, вопросы и ссылки на других поставщиков. По этому шаблону собираются все 13 карточек.</p><span>Открыть макет →</span></a>
</div>
<div class="n">
<b>Что проверить до переноса в Тильду</b><br>
1. Фото: Павел Агеев, ведущий аналитик 1С, эксперт по интеграциям. Подпись на фото справа внизу, как у Сергея Никешина на странице маркетплейсов.<br>
2. Заголовок /ecom оставлен словами с сайта, вторая строка «телеком- и IT-оборудования» набрана мельче, чтобы первый экран не разъехался. Лид и кнопки переписаны под новый вид.<br>
3. Цена на карточках: в макете 103 950 ₽ за пакет из 5 поставщиков, как в таблице. Сейчас на карточках «от 99 900 руб».<br>
4. Новый раздел «Что видно в 1С» на /ecom: настоящие экраны модуля из инструкции (наличие у поставщика в заказе клиента, автоматический резерв, сопоставление товаров, отчёты контроля загрузки). Имя склада клиента на первом экране размыто.<br>
5. В таблице есть непрофильные поставщики (мебель, стоматология, гидроизоляция). В макете они под кнопкой «Показать ещё», решение за вами.<br>
Проверить телефон: открыть макет и сузить окно или F12 → значок телефона, ширина 390 px.
</div>
</div></body></html>"""
    out = os.path.join(ROOT, "competitors", "ecom-design-options-2026-09-30.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    return out


def main():
    for name, title, body, note in [
        ("preview-ecom-v3.html", "Интеграция 1С с поставщиками - макет v3", body_hub(),
         "Страница «Интеграция 1С с поставщиками телеком- и IT-оборудования» (https://alsn.ru/ecom) в стиле v3."),
        ("preview-ecom-card-merlion-v3.html", "Интеграция 1С с Merlion B2B - макет v3", body_card(),
         "Карточка поставщика на примере Мерлион (https://alsn.ru/merlion). Шаблон для всех 13 карточек."),
    ]:
        out = os.path.join(SCR, name)
        io.open(out, "w", encoding="utf-8").write(page(title, body, note))
        print("ok", out)
    print("ok", index())


if __name__ == "__main__":
    main()
