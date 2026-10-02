# -*- coding: utf-8 -*-
"""13 страниц поставщиков (alsn.ru/merlion, /ocs ...) на стилях v3: макеты и инструкция для Тильды.

Шаблон - карточка Мерлион из build_ecom_v3_preview.py, стили - как в build_ecom_v3_brief.py.
Факты о доступе к API - из аккордеонов «Особенности интеграции с ...» на живых страницах (30.09.2026),
отметки остатки / цены / резерв / сайт - из таблицы на https://alsn.ru/ecom.
Выход:
  seo-data/competitors/screens/preview-sup-{slug}-v3.html (13 шт.)
  seo-data/competitors/sup-cards-design-options-2026-09-30.html
  seo-data/tilda-briefs/tier4-postavshiki-v3-2026-09-30.html
  seo-data/tilda-briefs/_head-{slug}-2026-09-30.txt (13 шт.)
"""
import html
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_ecom_v3_preview as p  # noqa: E402
import build_mp_ozon_blocks as b  # noqa: E402
from mp_hero_frame import HERO_CSS  # noqa: E402

BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
OUT = os.path.join(BR, "tier4-postavshiki-v3-2026-09-30.html")
INDEX = os.path.join(p.ROOT, "competitors", "sup-cards-design-options-2026-09-30.html")
LIVE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_sup_cards_live_0930.json"), encoding="utf-8"))
DATE_ISO = "2026-10-02"
PHOTO_CDN = "https://static.tildacdn.com/tild6664-3537-4661-b433-666437613864/allsun-hero-ecom-sup.jpg"

# name - в тексте, gen - «на складах ...», ins - «с ...», crumb - имя в крошках (как в tier2-breadcrumbs-wave)
SUP = [
    dict(slug="merlion", crumb="Мерлион", h1b="Merlion B2B", name="Мерлион", gen="Мерлион", ins="Мерлион",
         full="Мерлион (MERLION)", cab="Merlion B2B", api="MERLION API", flags=(1, 1, 1, 1),
         items=("склад и транзит", "закупочные цены", "заказы и резерв"), short="бесплатно, по заявке",
         acc=[("Заявка у Мерлион", "Заполните форму заявки на сайте Мерлион, укажите сервис и цель: тестовая учётная запись или боевое подключение.", "API бесплатный"),
              ("Сначала тест", "Боевое использование открывают только после проверки на тестовой учётной записи.", "Тест, потом работа")],
         faq="Да. Использование MERLION API бесплатное. Для подключения заполните заявку у Мерлион: сначала дают тестовую учётную запись, после проверки переходят на боевую."),
    dict(slug="ocs", crumb="OCS", h1b="OCS B2B", name="OCS", gen="OCS", ins="OCS",
         full="OCS Distribution", cab="OCS B2B", api="OCS API", flags=(1, 1, 1, 0),
         items=("склад и транзит", "цены OCS", "заказы из учётной системы"), short="для партнёров OCS",
         acc=[("Партнёрство с OCS", "B2B-портал и API OCS доступны авторизованным партнёрам OCS Distribution. Вопросы по доступу решает ваш менеджер OCS.", "Для партнёров"),
              ("Документы для доступа", "OCS просит письмо-соглашение об использовании информации с подписью директора и печатью и список сотрудников с ролями. Если вы их уже отправляли, второй раз не нужно.", "Один раз")],
         faq="Да. Доступ к B2B и API дают авторизованным партнёрам OCS Distribution. Для этого OCS просит подписанное соглашение об использовании информации и список сотрудников с ролями."),
    dict(slug="treolan", crumb="Treolan", h1b="Treolan B2B", name="Treolan", gen="Treolan", ins="Treolan",
         full="Treolan", cab="Treolan B2B", api="Treolan API", flags=(1, 1, 1, 1),
         items=("состояние склада", "каталог и карточки товаров", "счета и накладные"), short="партнёрам, по запросу",
         acc=[("Партнёрство с Treolan", "Доступ к API получают партнёры компании Treolan.", "Для партнёров"),
              ("Запрос на email", "Партнёр отправляет в Treolan письмо с запросом доступа к API.", "По запросу")],
         faq="Да. Доступ к API Treolan дают партнёрам компании по запросу на email."),
    dict(slug="marvel", crumb="Марвел", h1b="Marvel B2B", name="Марвел", gen="Марвел", ins="Марвел",
         full="Марвел-Дистрибуция", cab="Marvel B2B", api="Marvel API", flags=(1, 1, 1, 0),
         items=("склад с ценами партнёра", "характеристики и фото", "резервы и заказы"), short="через менеджера Марвел",
         acc=[("Через менеджера", "Все партнёры Марвел подключены к B2B-порталу. Для API зарегистрированному партнёру достаточно обратиться к своему менеджеру.", "Для партнёров"),
              ("Что есть в API", "Склад с ценами партнёра, характеристики, фото и описания товаров, резервы и заказы.", "Резерв есть")],
         faq="Да. Зарегистрированному партнёру Марвел достаточно обратиться к своему менеджеру."),
    dict(slug="digis", crumb="DIGIS", h1b="DIGIS B2B", name="DIGIS", gen="DIGIS", ins="DIGIS",
         full="DIGIS", cab="DIGIS B2B", api="DIGIS API", flags=(1, 1, 1, 0),
         items=("каталог", "наличие и цены", "новые и изменённые товары"), short="через менеджера DIGIS",
         acc=[("Через менеджера", "Доступ к DIGIS API выдаёт ваш менеджер DIGIS.", "Через менеджера"),
              ("Что есть в API", "Каталог, наличие и цены, обновление изменившихся и новых товаров. Характеристик и описаний товаров в DIGIS API нет.", "Без описаний")],
         faq="Да. Доступ к DIGIS API выдаёт ваш менеджер DIGIS. Характеристик и описаний товаров в этом API нет."),
    dict(slug="elko", crumb="Элко Рус", h1b="ELKO Rus B2B", name="ЭЛКО", gen="ЭЛКО", ins="ЭЛКО",
         full="ЭЛКО Рус, сейчас АБСОЛЮТ ТРЕЙД", cab="ELKO B2B", api="ELKO API", flags=(1, 1, 1, 0),
         items=("остатки и цены", "свойства и фото", "структура каталога"), short="выдаёт поставщик",
         acc=[("Доступ у поставщика", "ELKO Rus теперь работает под брендом «АБСОЛЮТ ТРЕЙД». Доступ к API выдаёт сам поставщик, спросите у своего менеджера.", "Через менеджера"),
              ("Что есть в API", "Цены и остатки, свойства и изображения товаров, структура каталога.", "Остатки и цены")],
         faq="Да. Доступ к ELKO API выдаёт сам поставщик, он теперь работает под брендом «АБСОЛЮТ ТРЕЙД». Подскажем, что у него запросить."),
    dict(slug="3logic", crumb="3logic", h1b="3Logic B2B", name="3Logic", gen="3Logic", ins="3Logic",
         full="3Logic Group", cab="3Logic B2B", api="3Logic API", flags=(1, 1, 1, 1),
         items=("наличие на складе", "товары в транзите", "заказы"), short="по договору поставки",
         acc=[("Договор поставки", "Для подключения к API 3Logic нужен заключённый договор поставки с 3Logic Group.", "Обязательно"),
              ("Правило поставщика", "Списки товаров и цен API 3Logic просит запрашивать не чаще раза в 10 минут.", "Раз в 10 минут")],
         faq="Да. Для подключения к API 3Logic нужен заключённый договор поставки с 3Logic Group."),
    dict(slug="etm-ipro", crumb="ЭТМ iPRO", h1b="ЭТМ iPRO", name="ЭТМ iPRO", gen="ЭТМ", ins="ЭТМ iPRO",
         full="ЭТМ, сервис iPRO", cab="ЭТМ iPRO", api="ЭТМ iPRO API", flags=(1, 1, 1, 1),
         items=("товары и цены", "остатки ЭТМ и поставщиков", "заказы"), short="по анкете ЭТМ",
         acc=[("Анкета ЭТМ", "Для подключения к API ЭТМ iPRO заполните анкету: выберите способ обмена данными и перечень данных.", "По анкете"),
              ("Что есть в API", "Список товаров, цены, остатки на складах ЭТМ и поставщиков, характеристики и фото, размещение и подтверждение заказов.", "Заказы есть")],
         faq="Да. Для подключения к API ЭТМ iPRO заполните анкету ЭТМ: выберите способ обмена и перечень данных.",
         extra=("Чем модуль отличается от бесплатного модуля ЭТМ?",
                "ЭТМ iPRO встроен в наш модуль интеграции с поставщиками и работает одновременно с другими вашими поставщиками: "
                "остатки, цены и резерв по всем приходят в одну 1С. Настраивать отдельную интеграцию под ЭТМ не нужно.")),
    dict(slug="resurs-media", crumb="Ресурс-Медиа", h1b="Ресурс-Медиа B2B", name="Ресурс-Медиа", gen="Ресурс-Медиа", ins="Ресурс-Медиа",
         full="Ресурс-Медиа", cab="Ресурс-Медиа B2B", api="Ресурс-Медиа API", flags=(1, 1, 1, 0),
         items=("весь ассортимент", "цены и наличие", "электронные документы"), short="через менеджера",
         acc=[("Через менеджера", "Подробности по API даёт ваш менеджер в Ресурс-Медиа. Если вы ещё не партнёр, оставьте заявку на их сайте.", "Через менеджера"),
              ("Что есть в API", "Весь ассортимент, цены и наличие на складе, электронные документы.", "Цены и наличие")],
         faq="Да. Подробности по API даёт ваш менеджер в Ресурс-Медиа. Если вы ещё не партнёр, оставьте заявку на их сайте."),
    dict(slug="auvix", crumb="AUVIX", h1b="AUVIX B2B", name="AUVIX", gen="AUVIX", ins="AUVIX",
         full="AUVIX", cab="AUVIX B2B", api="AUVIX API", flags=(1, 1, 1, 0),
         items=("каталог", "остатки и цены", "фото и характеристики"), short="выдаёт поставщик",
         acc=[("Доступ у поставщика", "Доступ к AUVIX API выдаёт сам поставщик, спросите у своего менеджера.", "Через менеджера"),
              ("Что есть в API", "Каталог, изображения и характеристики, остатки и цены с автоматическим обновлением.", "Остатки и цены")],
         faq="Да. Доступ к AUVIX API выдаёт сам поставщик. Подскажем, что у него запросить."),
    dict(slug="vtt", crumb="ВТТ", h1b="ВТТ B2B", name="ВТТ", gen="ВТТ", ins="ВТТ",
         full="ВТТ (Высокие технологии тонера)", cab="ВТТ B2B", api="ВТТ API", flags=(1, 1, 1, 0),
         items=("наличие на складе", "цены", "резервы и заказы"), short="через менеджера ВТТ",
         acc=[("Портал ВТТ", "Доступ к B2B-порталу ВТТ дают через менеджера по продажам или после самостоятельной регистрации на портале. Про API уточните у менеджера.", "Менеджер или регистрация"),
              ("Что есть в API", "Наличие на складе вашего подразделения ВТТ, цены, фото и EAN, резервы и заказы.", "Резерв есть")],
         faq="Да. Доступ к порталу ВТТ дают через менеджера по продажам или после самостоятельной регистрации. Про API уточните у менеджера."),
    dict(slug="dssl", crumb="DSSL", h1b="ДССЛ B2B", name="ДССЛ", gen="ДССЛ", ins="ДССЛ",
         full="DSSL (ДССЛ)", cab="DSSL B2B", api="API ДССЛ", flags=(1, 1, 0, 0),
         items=("каталог", "наличие", "цены"), short="выдаёт поставщик",
         acc=[("Доступ у поставщика", "Доступ к данным для обмена выдаёт сам ДССЛ, спросите у своего менеджера.", "Через менеджера"),
              ("Что загружаем", "По ДССЛ модуль загружает остатки и цены. Резерва из 1С нет.", "Остатки и цены")],
         faq="Да. Доступ к данным выдаёт сам ДССЛ. Подскажем, что у него запросить."),
    dict(slug="russkiy-svet", crumb="Русский Свет", h1b="Русский Свет B2B", name="Русский Свет", gen="Русского Света", ins="Русским Светом", po="Русскому Свету",
         full="Русский Свет", cab="RS24", api="API Русского Света", flags=(1, 1, 0, 0),
         items=("склады и ассортимент", "остатки и цены", "характеристики"), short="логин и пароль RS24",
         acc=[("Логин RS24", "Для API Русского Света нужен логин и пароль от RS24, личного кабинета для юрлиц.", "Логин и пароль"),
              ("Что есть в API", "Склады и ассортимент, остатки, цены и характеристики в формате JSON.", "Остатки и цены")],
         faq="Да. Для авторизации в API Русского Света нужен логин и пароль от RS24."),
]
assert [s["slug"] for s in SUP] == list(LIVE), "порядок и состав как на сайте"

# сверка отметок с таблицей /ecom
_tab = {p.CARDS[n]: tuple(int(v) for v in c) for n, c in p.parse_table() if n in p.CARDS}
for s in SUP:
    assert _tab[s["slug"]] == s["flags"], s["slug"]

import sup_profile as prof  # noqa: E402
from sup_new_data import NEW  # noqa: E402

_tab_all = {n: tuple(int(v) for v in c) for n, c in p.parse_table()}


def _finish_new(d):
    s = dict(d)
    fl = {_tab_all[t] for t in s.pop("tab")}
    assert len(fl) == 1, (s["slug"], fl)
    s["flags"] = fl.pop()
    st, pr, rs, _ = s["flags"]
    assert st or pr or rs, s["slug"]
    s["cab"], s["api"] = s["name"], f"API {s['gen']}"
    s["items"] = tuple(w for w, f in (("остатки на складах", st), ("закупочные цены", pr), ("резерв товара", rs)) if f)
    s["short"] = "выдаёт поставщик"
    dsh = data_short(s)
    s["acc"] = [("Доступ у поставщика", f"Доступ к API выдаёт сам {s['name']}, обычно своим партнёрам. Спросите у своего менеджера, "
                 "а мы подскажем, что запросить.", "Через менеджера"),
                ("Что загружаем", f"По {s['po']} модуль работает с данными: {dsh}. Набор зависит от того, что отдаёт API поставщика.",
                 dsh[0].upper() + dsh[1:])]
    s["faq"] = f"Да. Доступ к API выдаёт сам {s['name']}. Подскажем, что у него запросить."
    return s


NEW_SUP = []  # заполняется после определения data_short


RENEW_A = ("Да, оплата ежегодная. Год продления стоит столько же, сколько покупка: 103 950 ₽ за пакет из 5 поставщиков, "
           "15 645 ₽ за каждого следующего из списка. Если не продлить, модуль перестанет получать обновления, "
           "и когда поставщик изменит свой API, обмен с ним может остановиться. Цены с НДС 5%.")


def _join(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " и " + xs[-1]


def data_words(s):
    """Что приходит в 1С без резерва: «остатки и закупочные цены» / «остатки» / «закупочные цены» / ""."""
    st, pr = s["flags"][0], s["flags"][1]
    return _join([w for w, f in (("остатки", st), ("закупочные цены", pr)) if f]) if (st or pr) else ""


def data_full(s):
    st, pr, rs = s["flags"][:3]
    return _join([w for w, f in (("остатки", st), ("закупочные цены", pr), ("резерв", rs)) if f])


def data_short(s):
    st, pr, rs = s["flags"][:3]
    return ", ".join(w for w, f in (("остатки", st), ("цены", pr), ("резерв", rs)) if f)


NEW_SUP = [_finish_new(d) for d in NEW]
ALL_SUP = SUP + NEW_SUP


def into_1c(s):
    dw, rs = data_words(s), s["flags"][2]
    if dw:
        return f"{dw} приходят прямо в 1С" + (", резерв ставится из 1С" if rs else "")
    return "резерв ставится прямо из 1С по заказу клиента"


def card_faq(s):
    st, pr, rs, site = s["flags"]
    v = prof.voice(s["slug"])
    cab_q = (
        f"Чем модуль отличается от личного кабинета {s['cab']}?",
        f"Зачем модуль, если кабинет {s['cab']} уже есть?",
        f"Что меняется для менеджера после подключения {s['gen']}?",
        f"Можно работать только в кабинете {s['cab']}?",
    )[v]
    cab_a = (
        f"В кабинете {s['cab']} менеджер смотрит данные на сайте {s['gen']} и переносит их в 1С вручную или через Excel. Модуль подключает вашу 1С к {s['api']}: {into_1c(s)}.",
        f"Кабинет {s['cab']} остаётся. Модуль нужен, чтобы не переносить данные руками: {into_1c(s)}.",
        f"Менеджер перестаёт скачивать прайс {s['gen']}. {into_1c(s)[0].upper() + into_1c(s)[1:]} через {s['api']}.",
        f"В кабинете {s['cab']} всё видно, но в учёт это попадает только после ручной загрузки. С модулем {into_1c(s)}.",
    )[v]
    items = [
        (cab_q, cab_a),
        (f"Нужен ли доступ к {s['api']}?", s["faq"]),
    ]
    if s.get("extra"):
        items.insert(1, s["extra"])
    if not rs:
        items.append((f"Можно ли резервировать товар у {s['gen']} из 1С?",
                      f"Нет. По {s.get('po', s['name'])} модуль загружает {data_words(s)}. Резерв из 1С работает у поставщиков, "
                      "где он отмечен в таблице на странице «Интеграция с поставщиками»."))
    if site and st:
        items.append((f"Можно ли выгружать остатки {s['gen']} на ваш сайт?",
                      f"Да, если ваша 1С уже связана с сайтом. Настроим автоматическую загрузку остатков {s['gen']} "
                      "на виртуальные склады в 1С, которые связаны с сайтом."))
    items += [
        (f"Сколько времени занимает подключение {s['gen']}?",
         "Подключение одного поставщика занимает 2 недели."),
        ("Можно подключить других поставщиков?",
         f"Да. {s['name']} входит в пакет из 5 любых поставщиков из нашего списка за 103 950 ₽ в год. Каждый следующий из списка стоит 15 645 ₽ в год."),
        ("Нужно ли продлевать интеграцию?", RENEW_A),
    ]
    return prof.faq_extra(s, data_full(s) or "номер и срок резерва") + items


def fit_cards(s):
    st, pr, rs, site = s["flags"]
    g = s["gen"]
    v = prof.voice(s["slug"])
    stock = (
        f"Товары на настроенных складах {g} в вашей 1С, по расписанию.",
        f"В учёт попадает наличие только с тех складов {g}, которые выбраны при настройке.",
        f"Остаток {g} обновляется в 1С сам. Склады, которые вы не включили, в обмен не входят.",
        f"Менеджер видит наличие {g} в 1С и не открывает для этого кабинет.",
    )[v]
    price = (
        f"Актуальные цены {g} без скачивания Excel.",
        f"Закупочная цена {g} лежит в 1С рядом с вашим товаром.",
        f"Прайс {g} больше не загружают файлом: цена приходит вместе с обменом.",
        f"Сравнить цену {g} с другими поставщиками можно в той же базе.",
    )[v]
    reserve = (
        f"Товар у {g} резервируется из 1С по заказу клиента, номер и срок резерва приходят в 1С.",
        f"По заказу клиента модуль ставит резерв у {g} и записывает номер и срок в документ.",
        f"Резерв {g} не ставят в кабинете: его создаёт 1С, а ответ поставщика возвращается в заказ.",
        f"Когда клиент заказывает товар {g}, резерв уходит из 1С, обратно приходят номер и срок.",
    )[v]
    pool = [
        (st, "Остатки", stock),
        (pr, "Закупочные цены", price),
        (rs, "Резерв онлайн", reserve),
        (st or pr, "Сопоставление товаров", f"Товары {g} связываются с вашими по идентификатору раз в день, остальные по артикулу."),
        (st, "Наличие в заказе клиента", f"Остаток {g} виден в колонке «Поставщик» при подборе товаров в заказ клиента."),
        (rs, "Отчёт по резервированию", f"Что заказал клиент и что зарезервировано у {g}: количество, цена, номер и срок резерва."),
        (rs, "Мониторинг авторезервирования", "Сколько позиций зарезервировано и сколько запросов не прошло, за любой период."),
    ]
    return [(t, x) for f, t, x in pool if f][:3]


def body(s):
    st, pr, rs, site = s["flags"]
    g, api, cab, nm = s["gen"], s["api"], s["cab"], s["name"]
    long_ = ' class="long"' if len(s["h1b"]) > 12 else ""
    h1 = f"<h1{long_}>Интеграция 1С <br>с <span>{s['h1b']}</span><small>по API</small></h1>"
    if st and pr:
        head_ = f"Остатки с настроенных складов {g} и закупочные цены приходят в вашу 1С"
    elif st:
        head_ = f"Остатки с настроенных складов {g} приходят в вашу 1С"
    elif pr:
        head_ = f"Закупочные цены {g} приходят в вашу 1С"
    else:
        head_ = f"Резерв у {g} ставится прямо из 1С по заказу клиента"
    v = prof.voice(s["slug"])
    tail_ = ((", резерв ставится из 1С. " if rs else " без выгрузки Excel. ") if (st or pr) else ". ")
    tail2 = (
        f"Это обмен с вашей базой, а не вход в кабинет {cab}.",
        f"Менеджер остаётся в 1С и не выгружает прайс {g} руками.",
        f"Кабинет {cab} при этом не отменяем: модуль забирает из него рутину.",
        f"Подключаем {nm} к той 1С, в которой вы уже ведёте учёт.",
    )[v]
    lead = f'<p class="lead">{head_}{tail_}{tail2}</p>'
    btns = ('<div class="btns"><a class="btn m" href="#popup:konsultacia">Получить консультацию <span class="ar">→</span></a>'
            '<a class="btn g" href="#price">Сколько стоит</a></div>')
    others = [o for o in ALL_SUP if o["slug"] != s["slug"]]
    start = sum(ord(ch) for ch in s["slug"]) % len(others)
    near = [others[(start + i * 7) % len(others)] for i in range(6)]
    chips = "".join(f'<a href="https://alsn.ru/{o["slug"]}">{o["crumb"]}</a>' for o in near)
    site_dd = "<dt>Сайт</dt><dd>через виртуальные склады</dd>\n    " if (site and st) else ""
    fits = "\n     ".join(f"<div><b>{t}</b><p>{x}</p></div>" for t, x in fit_cards(s))
    dw = data_words(s)
    if dw:
        cab_txt = (f"{dw[0].upper() + dw[1:]} видны на сайте {g}. Чтобы они попали в 1С, менеджер скачивает Excel и загружает вручную."
                   + (" Резерв ставят в кабинете." if rs else ""))
        mod_txt = (f"{dw[0].upper() + dw[1:]} приходят в 1С сами. " + ("Резерв ставится из 1С, рядом" if rs else "Рядом")
                   + " лежат данные других ваших поставщиков.")
    else:
        cab_txt = f"Резерв менеджер ставит в кабинете {cab} вручную и переносит номер резерва в 1С."
        mod_txt = "Резерв ставится из 1С по заказу клиента, номер и срок резерва приходят в 1С сами."
    pipe1 = {(1, 1): "остатки и цены", (1, 0): "остатки", (0, 1): "цены", (0, 0): "номер резерва"}[(st, pr)]
    mid2 = f"резерв у {g}" if rs else "сопоставление товаров"
    end_items = ([f"остатки {g}"] if st else []) + (["цены для прайса"] if pr else []) + ([f"резервы у {g}"] if rs else [])
    end_items.append("остатки для сайта" if (site and st) else "заказы клиентов")
    end_li = "".join(f"<li>{x}</li>" for x in end_items[:3])
    end_k = "Ваша 1С и сайт" if (site and st) else "Ваша 1С"
    acc = "\n".join(f'     <div class="ex"><b>{t}</b><p>{x}</p><span class="need">{n}</span></div>' for t, x, n in s["acc"])
    it = "".join(f"<li>{i}</li>" for i in s["items"])
    about = prof.about_html(s)
    off = 1 if about else 0
    about_sec = ""
    if about:
        about_sec = f"""
   <div class="sec">
    {p.num(1)}
    <h2>{about[0]}</h2>
    {about[1]}
   </div>
"""
    h_in = (
        f"Что приходит из {g} в 1С",
        f"Какие данные {g} попадают в учёт",
        f"Что модуль забирает у {g}",
        f"Что вы увидите в 1С по {g}",
    )[v]
    h_cab = (
        "Модуль или личный кабинет",
        f"Кабинет {cab} и модуль",
        "Что остаётся ручным",
        f"Где менеджер работает с {s['ins']}",
    )[v]
    fin_h, fin_p = (
        (f"Подключим {nm} к вашей 1С", "Скажите, какие ещё поставщики у вас есть. Посчитаем пакет целиком."),
        (f"Запустим обмен с {s['ins']}", "Напишите, кто ещё у вас в закупках. Соберём пакет из списка."),
        (f"{nm} в вашей 1С", "Посчитаем, сколько поставщиков из списка вам нужно."),
        (f"Обсудим подключение {s['gen']}", "Пакет из 5 поставщиков считаем вместе, не по одному."),
    )[v]
    return f"""
<div class="crumb-bar"><div class="in crumb">⌂ / <a href="https://alsn.ru/ecom">Интеграция с поставщиками</a> / {s['crumb']}</div></div>

<!-- HERO -->
{p.hero("Поставщики · " + s['crumb'], h1, lead, btns)}

<!-- BODY -->
<section class="body" style="padding-top:56px">
 <div class="in">
  <aside class="pass">
   <div class="ttl">Паспорт интеграции</div>
   <div class="price">103 950 ₽</div>
   <div class="per">в год за пакет из 5 поставщиков, {nm} входит</div>
   <dl>
    <dt>Поставщик</dt><dd>{s['full']}</dd>
    <dt>Данные</dt><dd>{data_short(s)}</dd>
    {site_dd}<dt>Доступ к API</dt><dd>{s['short']}</dd>
    <dt>Подключение</dt><dd>2 недели</dd>
    <dt>Оплата</dt><dd>ежегодно</dd>
   </dl>
   <a class="btn m" href="#popup:konsultacia">Получить консультацию</a>
   <a class="btn g" href="https://alsn.ru/ecom#suppliers">Все поставщики</a>
   <div class="small">Цены с НДС 5%. +1 поставщик из списка 15 645 ₽ в год. Год продления стоит столько же, сколько покупка.</div>
   {p.TRUST}
  </aside>

  <div>
{about_sec}
   <div class="sec">
    {p.num(1 + off)}
    <h2>{h_in}</h2>
    <p class="sub">Модуль забирает данные по {api} и кладёт их в вашу базу.</p>
    <div class="fit">
     {fits}
    </div>
   </div>

   <div class="sec">
    {p.num(2 + off)}
    <h2>{h_cab}</h2>
    <p class="sub">Кабинет {cab} остаётся у вас. Модуль убирает ручной перенос данных из него в 1С.</p>
    <div class="extra">
     <div class="ex"><b>Личный кабинет {cab}</b><p>{cab_txt}</p><span class="need">Каждый день руками</span></div>
     <div class="ex"><b>Модуль Аллсан в 1С</b><p>{mod_txt}</p><span class="need">Автоматически</span></div>
    </div>
   </div>

   <div class="sec">
    {p.num(3 + off)}
    <h2>Как идут данные</h2>
    <div class="route">
     <div class="node"><div class="k">{s['crumb']}</div><b>{api}</b><ul>{it}</ul></div>
     <div class="pipe"><div>{pipe1}</div><div class="back">{"резерв" if rs else "запросы"}</div></div>
     <div class="node mid"><div class="k">Модуль Аллсан</div><b>Обмен по расписанию</b><ul><li>загрузка в 1С</li><li>{mid2}</li><li>другие поставщики</li></ul></div>
     <div class="pipe"><div>в учёт</div><div class="back">заказы</div></div>
     <div class="node"><div class="k">{end_k}</div><b>Учёт и прайс</b><ul>{end_li}</ul></div>
    </div>
   </div>

   <div class="sec">
    {p.num(4 + off)}
    <h2>Как получить доступ к {api}</h2>
    <p class="sub">Доступ выдаёт сам поставщик. Логин и пароль, код доступа или токен мы вставляем в модуль и проверяем обмен на вашей базе.</p>
    <div class="extra">
{acc}
    </div>
   </div>

   <div class="sec" id="price">
    {p.num(5 + off)}
    <h2>Сколько стоит</h2>
    <p class="sub">{nm} входит в пакет из 5 любых поставщиков из списка.</p>
    {p.prices()}
   </div>

   <div class="sec faq">
    {p.num(6 + off)}
    <h2>Частые вопросы</h2>
{p.faq_html(card_faq(s))}
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
  <div><h2>{fin_h}</h2><p>{fin_p}</p><div class="ph">+7 (495) 260-04-03</div></div>
  <a class="btn m" href="#popup:konsultacia">Получить консультацию <span class="ar">→</span></a>
 </div>
</section>
"""


def h1_text(s):
    return f"Интеграция 1С с {s['h1b']} по API"


# ---------------------------------------------------------------- макеты
def build_previews():
    for s in ALL_SUP:
        html_ = p.page(f"{h1_text(s)} - макет v3", body(s),
                       f"Страница «{h1_text(s)}» (https://alsn.ru/{s['slug']}) в стиле v3.")
        html_ = html_.replace("../ecom-design-options-2026-09-30.html", "../sup-cards-design-options-2026-09-30.html")
        html_ = html_.replace("</style>", LONG_CSS + "\n</style>", 1)
        io.open(os.path.join(p.SCR, f"preview-sup-{s['slug']}-v3.html"), "w", encoding="utf-8").write(html_)
    cards = "\n".join(
        f'<a class="c" href="screens/preview-sup-{s["slug"]}-v3.html"><div class="k">{i:02d} · alsn.ru/{s["slug"]}'
        f'{" · новая" if s in NEW_SUP else ""}</div>'
        f'<b>{h1_text(s)}</b><p>Данные: {data_short(s)}'
        f'{", сайт через виртуальные склады" if (s["flags"][3] and s["flags"][0]) else ""}. Доступ к API: {s["short"]}.</p><span>Открыть макет →</span></a>'
        for i, s in enumerate(ALL_SUP, 1))
    doc = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Страницы поставщиков в стиле v3 - 30.09.2026</title>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;600;800&display=swap" rel="stylesheet">
<style>
body{{margin:0;font-family:'Onest',Arial,sans-serif;background:#F7F8FA;color:#212121}}
.w{{max-width:1100px;margin:0 auto;padding:48px 28px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.02em;margin:0 0 10px}}
.s{{color:#6b7075;font-size:16px;line-height:1.55;margin:0 0 30px;max-width:780px}}
.g{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.c{{display:block;background:#fff;border:1px solid #D7DADD;border-radius:20px;padding:22px;color:inherit;text-decoration:none}}
.c:hover{{border-color:#F55823}}
.k{{font-family:monospace;color:#F55823;font-size:13px;margin-bottom:8px}}
.c b{{font-size:18px;line-height:1.3}}.c p{{color:#3d4247;font-size:14.5px;line-height:1.5}}.c span{{color:#F55823;font-weight:600}}
.n{{margin-top:26px;font-size:14.5px;color:#3d4247;line-height:1.6;background:#fff;border:1px solid #D7DADD;border-radius:16px;padding:18px 22px}}
.n b{{color:#212121}}
@media(max-width:900px){{.g{{grid-template-columns:1fr}}}}
</style></head><body><div class="w">
<h1>{len(ALL_SUP)} страниц поставщиков в стиле v3</h1>
<p class="s">13 действующих страниц с исправленными текстами и {len(NEW_SUP)} новых. Все по шаблону карточки Мерлион: первый экран в рамке с фото Павла Агеева (на телефоне подпись под фото), паспорт, «что приходит в 1С», «модуль или личный кабинет», схема данных, доступ к API, цены, вопросы, ссылки на других поставщиков. Разделы собираются по отметкам из таблицы /ecom: остатки, цены, резерв, сайт.</p>
<div class="g">
{cards}
</div>
<div class="n">
<b>Что проверить</b><br>
1. Оплата ежегодная: 103 950 ₽ в год за пакет из 5 поставщиков, 15 645 ₽ в год за каждого следующего, продление по цене покупки (02.10.2026).<br>
2. Остатки - только с настроенных складов поставщика. Сайт - через виртуальные склады, если 1С уже связана с сайтом. Срок подключения 2 недели.<br>
3. Где в таблице /ecom нет резерва, резерв не обещаем. Где только резерв (Асбис, MONT, TFN, Emilink), не обещаем остатки и цены и не пишем про сайт.<br>
4. У новых поставщиков и у ЭЛКО, AUVIX, ДССЛ доступ к API описан нейтрально: «выдаёт сам поставщик, спросите у менеджера».<br>
Проверить телефон: сузить окно или F12 → значок телефона, ширина 390 px.
</div>
</div></body></html>"""
    io.open(INDEX, "w", encoding="utf-8").write(doc)


# ---------------------------------------------------------------- стили (как в build_ecom_v3_brief.py)
def prefix_selectors(sel):
    out = []
    for x in (y.strip() for y in sel.split(",")):
        if not x:
            continue
        if x.startswith(".lb"):
            out.append(x)
        elif x in (":root", "body"):
            out.append(".v3")
        elif x == "*":
            out.append(".v3 *")
        else:
            out.append(".v3 " + x)
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


LONG_CSS = ("@media(min-width:1241px){.v3 .hf h1.long{font-size:clamp(34px,2.8vw,40px)}}\n"
            "@media(min-width:1001px) and (max-width:1240px){.v3 .hf h1.long{font-size:30px}}")


def build_css():
    ozon_raw = re.search(r"<style>(.*?)</style>", open(p.SRC, encoding="utf-8").read(), re.S).group(1)
    plain, v3 = [], []
    for line in p.EXTRA_CSS.strip().split("\n"):
        if line.startswith((".mh", ".crumb-bar")):
            continue
        (v3 if ".v3 " in line else plain).append(line)
    css = "\n".join(
        line for line in prefix_css(ozon_raw + "\n" + "\n".join(plain)).split("\n")
        if not line.startswith((".v3 .head{", ".v3 .head .in{", ".v3 .crumb{"))
    )
    css += "\n" + re.sub(r"/\*.*?\*/", "", HERO_CSS).strip() + "\n" + "\n".join(v3) + "\n" + LONG_CSS
    assert ".v3 .hf{" in css and ".v3 .chips{" in css and ".v3 .prices.three .pc{" in css
    assert ".v3 .v3" not in css and ".mh" not in css
    return css


def cut(src, start, end, keep_end=False):
    i = src.index(start)
    j = src.index(end, i)
    return src[i:j + (len(end) if keep_end else 0)].strip()


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def strip_tags(x):
    return html.unescape(re.sub(r"<[^>]+>", "", x)).strip()


def page_code(s, css):
    src = open(os.path.join(p.SCR, f"preview-sup-{s['slug']}-v3.html"), encoding="utf-8").read()
    hero = cut(src, "<!-- HERO -->", "<!-- BODY -->").replace(p.PHOTO, PHOTO_CDN)
    bod = cut(src, "<!-- BODY -->", '<section class="final">')
    final = cut(src, '<section class="final">', "</section>", keep_end=True)
    assert "../../" not in hero + bod + final
    url = f"https://alsn.ru/{s['slug']}"
    faq = [(strip_tags(q), strip_tags(a)) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", bod)]
    assert len(faq) == len(card_faq(s))
    name = h1_text(s)
    desc = desc_new(s)
    head = "\n".join([
        '<meta name="robots" content="index, follow">',
        ld({"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": name,
            "serviceType": "Интеграция 1С с API поставщика", "url": url, "description": desc,
            "provider": {"@id": "https://alsn.ru/#organization"}, "areaServed": {"@type": "Country", "name": "RU"},
            "isRelatedTo": {"@id": "https://alsn.ru/ecom#service"},
            "offers": {"@type": "AggregateOffer", "lowPrice": "15645", "highPrice": "208950", "priceCurrency": "RUB", "offerCount": "3"}}),
        ld({"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage", "name": name, "description": desc,
            "url": url, "inLanguage": "ru-RU", "dateModified": DATE_ISO,
            "isPartOf": {"@type": "WebSite", "@id": "https://alsn.ru/#website"}, "about": {"@id": url + "#service"}}),
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/"},
            {"@type": "ListItem", "position": 2, "name": "Интеграция с поставщиками", "item": "https://alsn.ru/ecom"},
            {"@type": "ListItem", "position": 3, "name": s["crumb"], "item": url}]}),
        ld({"@context": "https://schema.org", "@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}),
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">',
        "<style>\n" + css + "\n</style>",
    ])
    b1 = f'<div class="v3">\n{hero}\n</div>'
    b2 = f'<div class="v3">\n{bod}\n</div>'
    b3 = f'<div class="v3">\n{final}\n</div>'
    for x in (head, b1, b2, b3):
        assert "\u2014" not in x and "\u2013" not in x
    return head, b1, b2, b3, len(faq)


def title_new(s):
    return f"{h1_text(s)} - модуль обмена | Аллсан"


def desc_new(s):
    what = (f"{data_full(s)} в вашей 1С без выгрузки Excel из личного кабинета" if data_words(s)
            else "резерв товара прямо из 1С по заказу клиента")
    return f"Модуль обмена 1С с {s['ins']} по API: {what}. Подключение за 2 недели. Аллсан Интеграция"


# ---------------------------------------------------------------- старые блоки (с живой страницы 30.09.2026)
KIND = {"180": "обложка", "1033": "карточки", "65": "заголовок", "191": "кнопка", "316": "форма",
        "121": "HTML-код", "585": "аккордеон"}


def old_blocks(slug):
    bl = LIVE[slug]["blocks"]
    i = next(k for k, x in enumerate(bl) if x["type"] == "180")
    j = next(k for k, x in enumerate(bl) if x["type"] == "795")
    rows = []
    for x in bl[i:j]:
        t = re.sub(r"\s+", " ", x["text"]).strip()
        t = re.sub(r"\s*[\u2013\u2014]\s*", " - ", t)
        if x["type"] == "121" and t.startswith(("Отзывы", "#rec")):
            t = t[:60]
        t = (t[:95] + "…") if len(t) > 95 else t
        rows.append((x["type"], x["rec"], t or "без текста (пустой блок)"))
    assert rows[0][0] == "180" and any(r[0] == "585" for r in rows)
    return rows


# ---------------------------------------------------------------- инструкция
def box(cid, text):
    return (f'<div class="copybox"><pre id="{cid}">{html.escape(text, quote=False)}</pre>'
            f'<button type="button" data-copy="{cid}">Копировать</button></div>')


def swap(cid, old, new):
    return f'<span class="lbl">Найти</span>\n{box(cid + "f", old)}\n<span class="lbl">Заменить на</span>\n{box(cid + "r", new)}'


# проверено на живом alsn.ru (_sup_ecom_done_check_0930.py): шаги, которые уже на сайте
DONE = {"merlion": {1, 2, 4}}
DONE_NOTE = {"merlion": "30.09.2026 на Мерлионе (/merlion) уже стоят и опубликованы: HEAD страницы из шага 1, "
                        "первый экран в рамке из шага 2, последний экран «Подключим Мерлион к вашей 1С» из шага 4"}
# блок уже стоит на холсте, но старой версии: вставить код поверх
REPASTE = {"merlion": {3: "Блок стоит старой версии: в паспорте нет строки «Подключение 2 недели», в частых вопросах нет "
                          "«Сколько времени занимает подключение Мерлион?», а в HEAD этот вопрос уже есть."}}


def has_crumbs(slug):
    return any(x["type"] == "131" and "Интеграция с поставщиками" in x["text"] for x in LIVE[slug]["blocks"])


def page_section(n, s, css):
    head, b1, b2, b3, nfaq = page_code(s, css)
    open(os.path.join(BR, f"_head-{s['slug']}-2026-09-30.txt"), "w", encoding="utf-8").write(head)
    url, slug, name = f"https://alsn.ru/{s['slug']}", s["slug"], h1_text(s)
    live = LIVE[slug]
    rows = old_blocks(slug)
    old = ("<table>\n<tr><th>#</th><th>Тип</th><th>Номер в коде</th><th>Что на экране сейчас (сверху вниз)</th></tr>\n"
           + "\n".join(f"<tr><td>{i}</td><td>T{t} {KIND.get(t, '')}</td><td><code>rec{r}</code></td><td>{html.escape(x, quote=False)}</td></tr>"
                       for i, (t, r, x) in enumerate(rows, 1)) + "\n</table>")
    old_h1 = re.sub(r"\s+", " ", live["h1"][0]) if live.get("h1") else ""
    crumbs = (f"блок T123 «дом / Интеграция с поставщиками / {s['crumb']}»" if has_crumbs(slug) else
              "старые крошки «Интеграция 1C по API с B2B поставщиками и дистрибьютерами → …» (новые T123 здесь ещё не стоят, "
              "их ставят по инструкции <code>tier2-breadcrumbs-wave-2026-09-28.html</code>)")
    head_now = ("служебный код BreadcrumbList (он есть и в новом коде)" if live.get("ld") else "пусто или посторонний код")
    rs, site = s["flags"][2], s["flags"][3]
    p_ = f"p{n}"
    sec = _page_html(n, s, p_, url, slug, name, live, rows, old, old_h1, crumbs, head_now, rs, site, head, b1, b2, b3, nfaq)
    done, rep = DONE.get(slug, set()), REPASTE.get(slug, {})
    for k in done:
        sec, cnt = re.subn(rf'<section class="task" id="{p_}-{k}">.*?</section>\n\n?', "", sec, flags=re.S)
        assert cnt == 1
    for k, why in rep.items():
        old_ol = re.search(rf'(<section class="task" id="{p_}-{k}">.*?)(<ol class="steps">.*?</ol>)', sec, re.S)
        new_ol = (f'<div class="where"><strong>Сейчас на сайте.</strong> {why} Новый блок не добавлять: заменить код в этом.</div>\n'
                  '<ol class="steps">\n<li>Блок T123 под первым экраном в рамке (слева паспорт с ценой «103 950 ₽», справа разделы 01-06) '
                  '→ «Контент» → Ctrl+A → Delete → вставить код ниже целиком → «Сохранить и закрыть».</li>\n'
                  '<li>Отступы блока не менять.</li>\n</ol>')
        sec = sec[:old_ol.start(2)] + new_ol + sec[old_ol.end(2):]
    if 4 in done:
        sec = sec.replace(f"Под новым последним экраном из шага {n}.4.",
                          f"Под последним экраном «Подключим {s['name']} к вашей 1С», он уже стоит.")
    if done:
        left = 7 - len(done)
        sec = sec.replace(f'<span class="muted">· alsn.ru/{slug}</span></summary>',
                          f'<span class="muted">· alsn.ru/{slug} · осталось {left} шага</span></summary>', 1)
    return sec


def _page_html(n, s, p_, url, slug, name, live, rows, old, old_h1, crumbs, head_now, rs, site, head, b1, b2, b3, nfaq):
    return f"""
<details class="page" id="{p_}"{" open" if n == 1 else ""}>
<summary><span class="num">{n:02d}</span> {name} <span class="muted">· alsn.ru/{slug}</span></summary>
<div class="pbody">
<p class="muted">Страница «{html.escape(old_h1)}» (<a href="{url}">{url}</a>, в списке Тильды <code>{slug}</code>) · макет: <a href="../competitors/screens/preview-sup-{slug}-v3.html">preview-sup-{slug}-v3.html</a> · данные: {"остатки, цены, резерв" if rs else "остатки и цены, без резерва"}{", снять товар с сайта" if site else ""}</p>

<section class="task" id="{p_}-1">
<h3><span class="num">{n}.1</span> HEAD страницы целиком одной вставкой</h3>
<ol class="steps">
<li>Список страниц → <code>{slug}</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопировать старое содержимое в блокнот и сохранить файл, это откат. Сейчас там: {head_now}.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{box(p_ + "h", head)}
<p class="muted">Внутри: стили нового дизайна, услуга, страница, крошки «Главная / Интеграция с поставщиками / {s['crumb']}» и {nfaq} частых вопросов ровно как на экране. Тот же код лежит в файле <code>_head-{slug}-2026-09-30.txt</code>.</p>
</section>

<section class="task" id="{p_}-2">
<h3><span class="num">{n}.2</span> Первый экран в рамке</h3>
<p>Заголовок «{name}», абзац, кнопки «Получить консультацию» и «Сколько стоит», справа фото Павла Агеева с подписью. Адрес фото уже стоит в коде.</p>
<div class="where"><strong>Где.</strong> Страница «{html.escape(old_h1)}» ({url}). Верх холста: меню, под ним {crumbs}. Новый блок ставим сразу под крошками, выше старого первого экрана «Однократная оплата без ежегодного продления!».</div>
<ol class="steps">
<li>Нижний край блока крошек → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
{box(p_ + "a", b1)}
</section>

<section class="task" id="{p_}-3">
<h3><span class="num">{n}.3</span> Основная часть: паспорт и разделы 01-06</h3>
<p>Паспорт с ценой сбоку и разделы «Что приходит из {s['gen']} в 1С», «Модуль или личный кабинет», «Как идут данные», «Как получить доступ к {s['api']}», «Сколько стоит», «Частые вопросы», ссылки на других поставщиков.</p>
<ol class="steps">
<li>Под блоком из шага {n}.2 → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box(p_ + "b", b2)}
</section>

<section class="task" id="{p_}-4">
<h3><span class="num">{n}.4</span> Последний экран с призывом</h3>
<p>Серый экран «Подключим {s['name']} к вашей 1С», телефон и кнопка «Получить консультацию».</p>
<ol class="steps">
<li>Под блоком из шага {n}.3 → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box(p_ + "c", b3)}
</section>

<section class="task" id="{p_}-5">
<h3><span class="num">{n}.5</span> Выключить {len(rows)} блоков прошлой версии</h3>
<p>Всё их содержимое теперь в новых блоках: иначе на странице будет два главных заголовка и два списка цен. Выключенный блок не виден на сайте и остаётся в редакторе для отката.</p>
<div class="where"><strong>Где искать.</strong> Под новым последним экраном из шага {n}.4. Первый - старый первый экран «Однократная оплата без ежегодного продления!» (T180, <code>rec{rows[0][1]}</code>), последний - пустой блок сразу над «Наши клиенты». «Наши клиенты», «Сертификаты», поиск, подвал, всплывающие формы, меню и крошки <strong>не выключать</strong>.</div>
<ol class="steps">
<li>У каждого блока из таблицы → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
</ol>
{old}
</section>

<section class="task" id="{p_}-6">
<h3><span class="num">{n}.6</span> Заголовок вкладки и описание для поиска</h3>
<p>Сейчас в выдаче страница обещает «прямой доступ к личному кабинету» и «недорого». Человек, который ищет вход в кабинет поставщика, кликает и уходит. Новые строки говорят, что это модуль для вашей 1С.</p>
<ol class="steps">
<li>Список страниц → <code>{slug}</code> → «Настройки» → вкладка «Главное» (или «SEO») → поле «Заголовок» → заменить → поле «Описание» → заменить → «Сохранить изменения».</li>
<li>Вкладка «Соцсети» (или «Facebook &amp; SEO»): если там стоят те же старые строки, заменить так же. Картинку превью не трогать → «Сохранить изменения».</li>
</ol>
<span class="lbl">Заголовок</span>
{swap(p_ + "t", live["title"], title_new(s))}
<span class="lbl">Описание</span>
{swap(p_ + "d", live["desc"], desc_new(s))}
</section>

<section class="task" id="{p_}-7">
<h3><span class="num">{n}.7</span> Опубликовать</h3>
<ol class="steps">
<li>Вверху редактора страницы <code>{slug}</code> → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано {slug}»: проверю живую страницу (один главный заголовок, фото, паспорт, вопросы, телефонная версия, служебный код).</li>
</ol>
</section>
</div>
</details>"""


BRIEF_EXTRA = """
details.page{background:#fff;border:1px solid var(--border,#e2e2de);border-radius:12px;margin:0 0 14px}
details.page>summary{cursor:pointer;list-style:none;padding:14px 18px;font-weight:700;font-size:17px}
details.page>summary::-webkit-details-marker{display:none}
details.page>summary::after{content:"+";float:right;font-weight:400;font-size:22px;line-height:1}
details.page[open]>summary::after{content:"−"}
details.page>summary .num{display:inline-block;background:#111;color:#fff;border-radius:999px;font-size:12px;font-weight:700;padding:2px 10px;margin-right:6px;vertical-align:middle}
details.page>summary .muted{font-weight:400;font-size:14px}
.pbody{padding:0 18px 6px}
.pbody .task h3{margin:0 0 8px}
"""


def build_brief():
    css = build_css()
    pages = "\n".join(page_section(i, s, css) for i, s in enumerate(SUP, 1))
    toc = "\n".join(f'<li><a href="#p{i}">{h1_text(s)}</a> · <code>{s["slug"]}</code>'
                    + (f' · <span class="muted">осталось {7 - len(DONE[s["slug"]])} шага из 7</span>' if s["slug"] in DONE else "")
                    + "</li>" for i, s in enumerate(SUP, 1))
    left_steps = sum(7 - len(DONE.get(s["slug"], ())) for s in SUP)
    done_lines = "".join(f" {DONE_NOTE[k]}." for k in DONE)
    no_crumbs = ", ".join(s["crumb"] for s in SUP if not has_crumbs(s["slug"]))
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый дизайн 13 страниц поставщиков - 30.09.2026</title>
<style>{b.BRIEF_CSS}{BRIEF_EXTRA}</style>
</head>
<body>
<div class="wrap">
<h1>Новый дизайн 13 страниц поставщиков</h1>
<p class="muted">Страницы «Интеграция 1С с … по API» (Мерлион, OCS, Treolan, Марвел, DIGIS, ЭЛКО, 3Logic, ЭТМ iPRO, Ресурс-Медиа, AUVIX, ВТТ, ДССЛ, Русский Свет) · оформление как у «Интеграция 1С с поставщиками» (<a href="https://alsn.ru/ecom">https://alsn.ru/ecom</a>), первый экран в рамке · блоки сверены с живыми страницами 30.09.2026 · обновлено 30.09.2026 после проверки сайта: открыто {left_steps} шагов на 13 страницах · каждый шаг после письменного «да» · «Опубликовать» отдельным шагом в конце каждой страницы</p>
<div class="pills"><span class="pill ok">13 макетов готовы</span><span class="pill ok">фото уже загружено</span><span class="pill warn">7 шагов на страницу (на Мерлионе осталось 4), старое выключаем, не удаляем</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/sup-cards-design-options-2026-09-30.html">все 13 макетов</a> (открыть в браузере). Устройство то же, что у /ecom: один код в HEAD страницы и три блока T123 (первый экран, основная часть, последний экран). Меню, крошки, «Наши клиенты», «Сертификаты», подвал и всплывающие формы остаются.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать. Меняем только HEAD каждой страницы. Старые блоки выключаем, а не удаляем. robots.txt, Bing, Twitter не трогаем. Telegram-бот на сайте остаётся.</div>

<div class="callout warn"><strong>Порядок.</strong> Страницы независимы, можно делать по одной: шаги 1-7 одной страницы, публикация, проверка, потом следующая. Сначала закончить Мерлион: новый код там уже частично стоит, осталось заменить основной блок, выключить старое, поменять заголовок и опубликовать. Внутри страницы шаги по порядку: сначала новый код (1-4), потом выключение старого (5), чтобы страница ни минуты не была пустой.</div>

<div class="callout"><strong>Хлебные крошки.</strong> На 6 страницах (Мерлион, OCS, Treolan, Марвел, 3logic, ЭТМ iPRO) новые крошки T123 уже стоят: серый текст на белом, подходят к новому первому экрану. На 7 страницах ({no_crumbs}) их ещё нет, они и удаление старых крошек T758 - в <code>tier2-breadcrumbs-wave-2026-09-28.html</code>. Служебный код крошек для всех 13 страниц уже входит в HEAD из шага 1 этой инструкции: при работе по той инструкции на этих страницах код в HEAD второй раз не вставлять, только T123 на холст и удаление T758.</div>

<div class="callout warn"><strong>Уже сделано - не трогать:</strong> фото Павла Агеева загружено 30.09.2026 вместе с дизайном /ecom (адрес уже стоит в коде шагов 2); новое меню сайта на всех 13 страницах; ссылки из таблицы /ecom на эти страницы. Задачи T3-5 (Мерлион, OCS, Treolan) и T3-6 (ЭТМ iPRO) из <code>tier3-ecom-postavshiki-2026-09-30.html</code> перенесены сюда: заголовки и описания меняются в шагах 6, главный заголовок с латинской «C» уходит вместе со старым первым экраном в шагах 5.{done_lines}</div>

<div class="toc"><strong>Страницы</strong><ol>
{toc}
</ol></div>

{pages}

<section class="task">
<h2>Что решено без вас и что не пишем</h2>
<ul class="tight">
<li>Цена на всех карточках 103 950 ₽ за пакет из 5 поставщиков, как на /ecom. На старых карточках было «от 99 900 руб».</li>
<li>У Русского Света и ДССЛ в таблице /ecom нет резерва: на их страницах резерв не обещаем.</li>
<li>ЭЛКО, AUVIX, ДССЛ: как получить доступ к API, на сайте не написано. Пишем «доступ выдаёт сам поставщик, спросите у менеджера».</li>
<li>Срок подключения пишем только «2 недели» (ответ заказчика 30.09.2026). Не пишем SLA и «каждые 15 минут». Про бесплатный модуль ЭТМ - только то, что в частом вопросе на странице ЭТМ iPRO (ответ заказчика 30.09.2026), без сравнения функций.</li>
</ul>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-postavshiki-v3-2026-09-30.html</code> · собирает <code>seo-data/scripts/build_sup_cards_v3.py</code> · HEAD по страницам: <code>seo-data/tilda-briefs/_head-{{slug}}-2026-09-30.txt</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""
    olds = "".join(html.escape(LIVE[s["slug"]]["title"], quote=False) + html.escape(LIVE[s["slug"]]["desc"], quote=False) for s in SUP)
    check = doc
    for s in SUP:
        for x in (LIVE[s["slug"]]["title"], LIVE[s["slug"]]["desc"]):
            check = check.replace(html.escape(x, quote=False), "")
    assert "\u2014" not in check and "\u2013" not in check, "тире в новом тексте"
    assert olds
    open(OUT, "w", encoding="utf-8").write(doc)
    return len(doc)


if __name__ == "__main__":
    build_previews()
    print("ok previews", INDEX)
    # дизайн на 13 страницах опубликован 30.09.2026, инструкцию с остатком пишет build_sup_srok_brief.py
    if "--full-brief" in sys.argv:
        print("ok brief", OUT, build_brief())
