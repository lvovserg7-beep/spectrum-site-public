# -*- coding: utf-8 -*-
"""Этап 0: карта соответствия схемы подрядчика и живых страниц alsn.ru (Тильда)."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVE = json.loads((ROOT / "seo-data/scripts/_tiers_live_0929.json").read_text(encoding="utf-8"))
OUT = ROOT / "seo-data/tilda-briefs/struktura-karta-2026-09-30.html"

PAGES = {p["path"]: p for p in LIVE}
SITE = "https://alsn.ru"


def h1(path):
    p = PAGES.get(path)
    return (p or {}).get("h1") or ""


def crumb_now(path):
    p = PAGES.get(path)
    if not p:
        return ""
    names = p.get("bc_names") or []
    if not names:
        return "нет" + (", старый блок со стрелкой" if p.get("t758") else "")
    tail = ", плюс старый блок со стрелкой" if p.get("t758") else ""
    return " / ".join(names) + tail


# Строки схемы: (уровень, имя в схеме, url или None, статус, родитель в крошках, в меню, примечание)
# статус: have / new / merge / fix
U, P, L = "Услуги", "Продукты", "Лицензии"
SCHEMA = [
    (1, U, "/uslugi", "new", "Главная", "1 уровень, первая строка списка «Все услуги»",
     "Разводящая страница в дизайне v3. Адрес предлагаемый."),
    (2, "Внедрение 1С под ключ", "/development1c", "have", "Главная / Услуги", "2 уровень",
     "Первая строка его подсписка - сама страница."),
    (3, "1С:ERP", "/erp-time-price", "fix", "Главная / Услуги / Внедрение 1С под ключ", "3 уровень",
     "H1 про стоимость. Страницу оставляем, расширение до «Внедрение 1С:ERP» - отдельной задачей."),
    (3, "1С:Управление торговлей", "/upt8", "have", "Главная / Услуги / Внедрение 1С под ключ", "3 уровень",
     "На странице и услуга, и витрина (4 товара). См. вопрос 1."),
    (3, "1С:Комплексная автоматизация", "/kompleksnaya_avtomatizaciya", "have",
     "Главная / Услуги / Внедрение 1С под ключ", "3 уровень", "Плюс 4 товара витрины."),
    (3, "1С:Бухгалтерия", "/buhv8", "have", "Главная / Услуги / Внедрение 1С под ключ", "3 уровень",
     "Плюс витрина 22 товара. См. вопрос 1."),
    (3, "1С:Зарплата и управление персоналом", "/zup8", "have",
     "Главная / Услуги / Внедрение 1С под ключ", "3 уровень", "Плюс витрина 8 товаров."),
    (3, "1С:УНФ (нет в схеме)", "/upravlenie_nashei_firmoi", "have",
     "Главная / Услуги / Внедрение 1С под ключ", "3 уровень", "Предлагаем добавить: УНФ есть в ЦА внедрения. См. вопрос 3."),
    (2, "Разработка и доработка 1С", "/dorabotka-1c", "new", "Главная / Услуги", "2 уровень",
     "Новая страница v3. Сейчас доработка описана внутри /development1c."),
    (2, "Техническая поддержка 1С", "/support1c", "have", "Главная / Услуги", "2 уровень", ""),
    (2, "Внедрение Битрикс24 и интеграция с 1С", "/bitrix24", "have", "Главная / Услуги", "2 уровень",
     "В схеме одна строка, на сайте две страницы. В меню обе, объединение не в этом плане."),
    (2, "Интеграция сайта с 1С и Битрикс24", "/1cbitrix", "have", "Главная / Услуги", "2 уровень",
     "Вторая страница Битрикс24."),
    (1, P, "/produkty", "new", "Главная", "1 уровень, первая строка «Все продукты»",
     "Разводящая страница v3."),
    (2, "Интеграция 1С с маркетплейсами", "/casemarketplace", "have", "Главная / Продукты", "2 уровень", ""),
    (3, "Ozon", "/1c-ozon", "have", "Главная / Продукты / Интеграция 1С с маркетплейсами", "3 уровень", ""),
    (4, "Ozon + 1С:УТ", "/1c-ozon-ut", "new", "... / Ozon", "нет, ссылка со страницы Ozon", "Нужны факты по конфигурации."),
    (4, "Ozon + 1С:КА", "/1c-ozon-ka", "new", "... / Ozon", "нет", ""),
    (4, "Ozon + 1С:ERP", "/1c-ozon-erp", "new", "... / Ozon", "нет", ""),
    (4, "Ozon + 1С:Бухгалтерия", "/1c-ozon-buh", "new", "... / Ozon", "нет", "Подтвердить, что модуль работает в БП."),
    (3, "Wildberries", "/1c-wildberries", "have", "Главная / Продукты / Интеграция 1С с маркетплейсами", "3 уровень", ""),
    (4, "Wildberries + 1С:УТ", "/1c-wildberries-ut", "new", "... / Wildberries", "нет, ссылка со страницы WB", ""),
    (4, "Wildberries + 1С:КА", "/1c-wildberries-ka", "new", "... / Wildberries", "нет", ""),
    (4, "Wildberries + 1С:ERP", "/1c-wildberries-erp", "new", "... / Wildberries", "нет", ""),
    (4, "Wildberries + 1С:Бухгалтерия", "/1c-wildberries-buh", "new", "... / Wildberries", "нет", ""),
    (2, "Интеграция 1С с поставщиками B2B", "/ecom", "have", "Главная / Продукты", "2 уровень", ""),
    (3, "Все поставщики", "/b2b-postavshiki", "new", "Главная / Продукты / Интеграция 1С с поставщиками B2B",
     "3 уровень", "Каталог карточек. Сейчас список 57 имён блоком на /ecom."),
    (2, "Чат-боты 1С для мессенджеров (нет в схеме)", None, "label", "", "2 уровень, заголовок списка",
     "Решение 30.09: боты остаются в «Продуктах» на Тильде. Пункт-заголовок без своей страницы."),
    (3, "Телеграм-бот 1С", "/telegram1c", "have", "Главная / Продукты / Телеграм-бот 1С", "3 уровень",
     "Переезжает из «Разработки» в «Продукты». Отраслевые /tb* встают под него."),
    (3, "Бот 1С для MAX", "/max1c", "new", "Главная / Продукты / Бот 1С для MAX", "3 уровень",
     "Решение 30.09: новая страница v3, бот уже работает. Адрес предлагаемый. Для текста нужны функции и цена, см. вопрос 8."),
    (3, "WhatsApp-бот 1С", "/whatsapp", "remove", "", "нет",
     "Решение 30.09: страницу убираем. Снять с публикации, затем 301 /whatsapp -> /telegram1c, после выхода /max1c перевести на /max1c. См. раздел 5."),
    (1, L, "/licenzii", "new", "Главная", "1 уровень, первая строка «Все лицензии»", "Разводящая страница v3."),
    (2, "Программы 1С", "/products", "have", "Главная / Лицензии", "2 уровень", "113 товаров."),
    (3, "1С:КП (ИТС)", "/its", "have", "Главная / Лицензии / Программы 1С", "3 уровень", "65 товаров."),
    (3, "1С:Fresh", "/1cfresh", "have", "Главная / Лицензии / Программы 1С", "3 уровень", "27 товаров."),
    (3, "1С:Документооборот", "/dokumentooborot8", "have", "Главная / Лицензии / Программы 1С", "3 уровень", "5 товаров."),
    (3, "Фастфуд и общепит", "/1_obschepit_fastfood", "have", "Главная / Лицензии / Программы 1С", "нет", "10 товаров."),
    (3, "1С:Бухгалтерия - лицензии", "/licenzii-1c-buhgalteriya", "new", "Главная / Лицензии / Программы 1С", "3 уровень",
     "Решение 30.09: отдельная витрина v3. Товары сейчас на /buhv8 (22). См. вопрос 1."),
    (3, "1С:Управление торговлей - лицензии", "/licenzii-1c-ut", "new", "Главная / Лицензии / Программы 1С", "3 уровень",
     "Товары сейчас на /upt8 (4)."),
    (3, "1С:Комплексная автоматизация - лицензии", "/licenzii-1c-ka", "new", "Главная / Лицензии / Программы 1С", "3 уровень",
     "Товары сейчас на /kompleksnaya_avtomatizaciya (4)."),
    (3, "1С:ЗУП - лицензии", "/licenzii-1c-zup", "new", "Главная / Лицензии / Программы 1С", "3 уровень",
     "Товары сейчас на /zup8 (8)."),
    (3, "1С:УНФ - лицензии", "/licenzii-1c-unf", "new", "Главная / Лицензии / Программы 1С", "3 уровень",
     "Товары сейчас на /upravlenie_nashei_firmoi (6)."),
    (3, "Лицензии 1С (было «Дополнительные лицензии»)", "/dopolnitelnie_licenzii", "fix",
     "Главная / Лицензии / Программы 1С", "3 уровень",
     "Решение 30.09: переименовать и увести в иерархию 1С. Адрес не меняем, 22 товара. Имя в крошках и меню - «Лицензии 1С»."),
    (2, "Битрикс24", "/bitrix24", "fix", "Главная / Лицензии", "2 уровень",
     "Решение 30.09: Битрикс24 в «Лицензиях». Своей витрины нет, пункт ведёт к блоку «Цены на лицензии Битрикс24» на /bitrix24. См. вопрос 7."),
    (2, "Карточки товаров", "/…/tproduct/…", "have", "ST340 карточки", "нет", "295 карточек, крошки ST340 уже по канону."),
    (2, "Корзина / оформление", None, "have", "", "иконка", "Всплывающая корзина Тильды (T706), отдельного адреса нет."),
]

OUTSIDE = [
    ("/perehod-s-upp-na-ka-unf-ut", "Внедрение 1С под ключ", "3 уровень в крошках, в меню нет"),
    ("/perehod-s-ut-10-3", "Внедрение 1С под ключ", "в крошках под внедрением"),
    ("/perehod-s-ut-na-unf", "Внедрение 1С под ключ", "в крошках под внедрением"),
    ("/moy-sklad-perenos-v-1s", "Внедрение 1С под ключ", "в крошках под внедрением"),
    ("/perehod-s-dokumentooborota-2-1-na-3-0", "Внедрение 1С под ключ", "в крошках под внедрением"),
    ("/sinhronizaciya-bp-i-bp", "Разработка и доработка 1С", "после публикации страницы доработки"),
    ("/sinhronizaciya-mezhdu-ut-i-ut", "Разработка и доработка 1С", "после публикации страницы доработки"),
    ("/sinhronizaciya-mezhdu-zup-i-zup", "Разработка и доработка 1С", "после публикации страницы доработки"),
    ("/integrationeco", "Разработка и доработка 1С", "после публикации страницы доработки"),
    ("/integrationsite", "Интеграция сайта с 1С и Битрикс24", "родитель /1cbitrix"),
    ("/utp", "Все лицензии", "подбор и установка 1С за день"),
    ("/perevystavlenie-uslug-posledney-mili-ozon-v-1s", "Ozon", "функция модуля Ozon"),
    ("/integraciya-1c-dlya-prodavcov-kompyuternoy-tehniki", "Интеграция 1С с поставщиками B2B", "та же тема, что /ecom"),
    ("/crmfurniture", "не переносим", "вне шести продуктов, оставляем как есть"),
    ("/amo_crm", "не переносим", "вне шести продуктов, оставляем как есть"),
    ("/tbstroit", "Телеграм-бот 1С", "отраслевая страница бота, в крошках под /telegram1c"),
    ("/tbtehpod", "Телеграм-бот 1С", "то же"),
    ("/tbintmag", "Телеграм-бот 1С", "то же"),
    ("/tbavtoservis", "Телеграм-бот 1С", "то же"),
    ("/tbhr", "Телеграм-бот 1С", "то же"),
    ("/tbdokument", "Телеграм-бот 1С", "то же"),
    ("/tbotdelprod", "Телеграм-бот 1С", "то же"),
    ("/tbsotrudniki", "Телеграм-бот 1С", "то же"),
    ("/tbfiksasotrud", "Телеграм-бот 1С", "то же"),
    ("/tbbot-parkovka-parking-garazh-stoyanka", "Телеграм-бот 1С", "то же"),
    ("/tbbot-restoran-kafe-kofeynya-bar", "Телеграм-бот 1С", "то же"),
]

SUPPLIERS = """Ак Системс|Асбис|AUVIX|BION|Вектор (Металлообработка)|ВИМАРКЕТ|ВТТ|ГК НОВЫЕ ТЕХНОЛОГИИ|Делия (Стоматологическая компания)|diHouse|Distribution Center|DKC.MARKET|DIGIS|ДССЛ|Emilink|ENERGON|ergolux|F5it|Форум электро|Hyperline|IT PROEKT|KARIN|Клавторг|КОМПЭЛ|KVK|Landata|legion project|Макспрофит|Марвел|Мерлион|MICS distribution company|MONT|НАГ|НДК (наладочно-диагностическая компания)|Ниеншанц-Автоматика|Office kit (офисное оборудование)|OCS Distribution|ProWay|Ресурс-Медиа|RM-Company|Русклимат|Русский Свет|Русско-Китайский Центр Содействия Бизнесу|СвязьКомплект|SDS LLC|Superwave group|Тайле|Тайпит-Мебель|ТД В1 Электроникс|TFN (ТФН)|Treolan|Учебный центр ЭМИЛИНК МСК|ЭЛКО Рус|ЭТМ iPRO|ЮМП (ЮНИТ МАРК ПРО)|3logic group|Zitrek""".split("|")

HAVE_SUP = {
    "AUVIX": "/auvix", "DIGIS": "/digis", "ДССЛ": "/dssl", "ЭЛКО Рус": "/elko", "ЭТМ iPRO": "/etm-ipro",
    "Марвел": "/marvel", "Мерлион": "/merlion", "OCS Distribution": "/ocs", "Ресурс-Медиа": "/resurs-media",
    "Русский Свет": "/russkiy-svet", "Treolan": "/treolan", "ВТТ": "/vtt", "3logic group": "/3logic",
}
DROP_SUP = {"Вектор (Металлообработка)", "Делия (Стоматологическая компания)", "Тайпит-Мебель",
            "Учебный центр ЭМИЛИНК МСК", "Русско-Китайский Центр Содействия Бизнесу"}
DOUBT_SUP = {"Русклимат", "Office kit (офисное оборудование)", "НДК (наладочно-диагностическая компания)",
             "Ниеншанц-Автоматика", "Форум электро", "ergolux", "KARIN"}

STATUS = {
    "have": ("ok", "есть"),
    "new": ("info", "новая"),
    "fix": ("warn", "есть, доработать"),
    "merge": ("warn", "решить"),
    "skip": ("muted", "не в плане"),
    "label": ("muted", "заголовок меню"),
    "remove": ("danger", "убрать"),
}


def e(s):
    return html.escape(s or "")


def link(path):
    if not path or "…" in path:
        return e(path or "-")
    if path in PAGES:
        return f'<a href="{SITE}{path}" target="_blank" rel="noopener"><code>{e(path)}</code></a>'
    return f"<code>{e(path)}</code>"


def schema_rows():
    out = []
    for lvl, name, path, st, parent, menu, note in SCHEMA:
        cls, label = STATUS[st]
        cur = h1(path) if path else ""
        now = crumb_now(path) if path else ""
        pad = (lvl - 1) * 18
        wt = "700" if lvl == 1 else ("600" if lvl == 2 else "400")
        out.append(
            f'<tr class="l{lvl}"><td style="padding-left:{8 + pad}px;font-weight:{wt}">{e(name)}</td>'
            f"<td>{link(path)}</td><td class=\"sm\">{e(cur) or '<span class=muted>-</span>'}</td>"
            f'<td><span class="pill {cls}">{label}</span></td>'
            f'<td class="sm">{e(parent)}</td><td class="sm">{e(menu)}</td>'
            f'<td class="sm">{e(now) or "<span class=muted>-</span>"}</td><td class="sm">{e(note)}</td></tr>'
        )
    return "\n".join(out)


def outside_rows():
    out = []
    for path, parent, note in OUTSIDE:
        out.append(
            f"<tr><td>{link(path)}</td><td class=\"sm\">{e(h1(path)) or '<span class=muted>нет в срезе</span>'}</td>"
            f"<td class=\"sm\">{e(parent)}</td><td class=\"sm\">{e(note)}</td></tr>"
        )
    return "\n".join(out)


def supplier_rows():
    out = []
    n_have = n_new = n_drop = n_doubt = 0
    for i, s in enumerate(SUPPLIERS, 1):
        if s in HAVE_SUP:
            st, cls, n_have = "есть страница", "ok", n_have + 1
            path = HAVE_SUP[s]
        elif s in DROP_SUP:
            st, cls, n_drop = "убрать (не телеком и IT)", "danger", n_drop + 1
            path = None
        elif s in DOUBT_SUP:
            st, cls, n_doubt = "уточнить профиль", "warn", n_doubt + 1
            path = None
        else:
            st, cls, n_new = "новая страница", "info", n_new + 1
            path = None
        crumb = crumb_now(path) if path else ""
        out.append(
            f"<tr><td>{i}</td><td>{e(s)}</td><td>{link(path) if path else '<span class=muted>-</span>'}</td>"
            f'<td><span class="pill {cls}">{st}</span></td><td class="sm">{e(crumb) or "<span class=muted>-</span>"}</td></tr>'
        )
    return "\n".join(out), n_have, n_new, n_drop, n_doubt


def count(st):
    return sum(1 for r in SCHEMA if r[3] == st)


sup_html, n_have, n_new, n_drop, n_doubt = supplier_rows()

MENU = """Услуги
  Все услуги  ->  /uslugi                      (новая)
  Внедрение 1С под ключ
    Внедрение 1С под ключ  ->  /development1c
    1С:ERP  ->  /erp-time-price
    1С:Управление торговлей  ->  /upt8
    1С:Комплексная автоматизация  ->  /kompleksnaya_avtomatizaciya
    1С:Бухгалтерия  ->  /buhv8
    1С:ЗУП  ->  /zup8
    1С:УНФ  ->  /upravlenie_nashei_firmoi      (вопрос 3)
  Разработка и доработка 1С  ->  /dorabotka-1c (новая)
  Техническая поддержка 1С  ->  /support1c
  Внедрение Битрикс24  ->  /bitrix24
  Интеграция сайта с 1С и Битрикс24  ->  /1cbitrix

Продукты
  Все продукты  ->  /produkty                  (новая)
  Интеграция 1С с маркетплейсами
    Модуль для маркетплейсов  ->  /casemarketplace
    Ozon  ->  /1c-ozon
    Wildberries  ->  /1c-wildberries
  Интеграция 1С с поставщиками B2B
    Интеграция с поставщиками  ->  /ecom
    Все поставщики  ->  /b2b-postavshiki       (новая)
  Чат-боты 1С для мессенджеров
    Телеграм-бот 1С  ->  /telegram1c
    Бот 1С для MAX  ->  /max1c                 (новая)

Лицензии
  Все лицензии  ->  /licenzii                  (новая)
  Программы 1С
    Все программы 1С  ->  /products
    1С:Бухгалтерия  ->  /licenzii-1c-buhgalteriya   (новая витрина)
    1С:Управление торговлей  ->  /licenzii-1c-ut    (новая витрина)
    1С:Комплексная автоматизация  ->  /licenzii-1c-ka   (новая витрина)
    1С:ЗУП  ->  /licenzii-1c-zup                    (новая витрина)
    1С:УНФ  ->  /licenzii-1c-unf                    (новая витрина)
    1С:КП (ИТС)  ->  /its
    1С:Fresh  ->  /1cfresh
    1С:Документооборот  ->  /dokumentooborot8
    Лицензии 1С  ->  /dopolnitelnie_licenzii   (было «Дополнительные лицензии»)
  Битрикс24  ->  /bitrix24, блок «Цены на лицензии Битрикс24»   (вопрос 7)

Наш опыт      (2 уровня, пункты из текущего меню: Кейсы, Отзывы)
О компании    (2 уровня, пункты из текущего меню)"""

QUESTIONS = [
    ("Отдельные витрины Бухгалтерии, УТ, КА, ЗУП, УНФ: что с товарами на старых страницах",
     "Решение 30.09: делаем 5 новых витрин лицензий в дизайне v3, старые /buhv8, /upt8, /kompleksnaya_avtomatizaciya, /zup8, "
     "/upravlenie_nashei_firmoi остаются страницами внедрения. Риск: у Тильды адрес карточки товара строится от страницы с блоком каталога "
     "(/buhv8/tproduct/...). Если блок товаров со старой страницы убрать, старые адреса карточек перестанут открываться, а они в индексе "
     "и в Товарном фиде. Предложение: на старых страницах блок товаров пока оставить ниже по странице (или свернуть) и перевести "
     "карточки на новые витрины отдельным шагом, когда новые адреса проиндексируются. Согласны?"),
    ("Адреса новых страниц",
     "/uslugi, /produkty, /licenzii, /dorabotka-1c, /b2b-postavshiki, /1c-ozon-ut, /1c-ozon-ka, /1c-ozon-erp, /1c-ozon-buh "
     "и такие же для Wildberries (/1c-wildberries-ut и т.д.). Если нужны другие - поправим до этапа 1."),
    ("УНФ во «Внедрении»",
     "В схеме подрядчика 1С:УНФ нет, но она есть в ЦА внедрения и на сайте есть страница. Предложение: 6-й пункт под «Внедрением 1С под ключ»."),
    ("Список поставщиков",
     f"Из 57 имён схемы убрать {n_drop} явно не телеком и IT (красные). Ещё {n_doubt} (жёлтые) - уточнить, продаёте ли им интеграцию. "
     f"Остальные {n_new} - новые страницы волнами по 10."),
    ("Страницы конфигураций маркетплейсов",
     "Нужны факты: работает ли модуль в 1С:Бухгалтерии и чем отличается работа в УТ, КА и ERP (документы, схема, настройки). "
     "Без них 8 страниц будут копиями /1c-ozon и /1c-wildberries."),
    ("1С:ERP",
     "Место ERP в схеме занимает /erp-time-price «Стоимость внедрения 1С:ERP…». Пока ставим его как есть, а расширение до полноценной страницы "
     "«Внедрение 1С:ERP» (со старым адресом) - отдельной задачей после структуры. Согласны?"),
    ("Битрикс24 в «Лицензиях»",
     "Товаров Битрикс24 в каталоге Тильды нет, цены лицензий стоят блоком на /bitrix24 (там же внедрение). Вариант А: пункт меню ведёт "
     "к этому блоку, ничего нового не делаем. Вариант Б: отдельная витрина «Лицензии Битрикс24» в каталоге (карточки тарифов, корзина) "
     "на новой странице, например /bitrix24-licenzii, в дизайне v3. Какой берём?"),
    ("Бот 1С для MAX: что писать на странице",
     "Бот уже работает (ответ 30.09). Для текста осталось: что он умеет - те же сценарии, что Telegram-бот на /telegram1c (заказы, остатки, "
     "документы, уведомления, отраслевые варианты) или другой набор; цена и условия; есть ли клиент, скриншоты или видео. "
     "Если функции совпадают с Telegram-ботом, скажите «как у Telegram» - возьмём список оттуда. Выдумывать не будем."),
]

REMOVE_WA = """<div class="card">
<b>Убрать страницу «WhatsApp-бот 1С» (/whatsapp).</b> Решение 30.09.2026. Это отдельные шаги в Тильде, каждый после вашего «да».
<ol>
<li>Убрать ссылки на /whatsapp с других страниц, из меню и подвала (список ссылок соберём перед шагом).</li>
<li>Снять страницу с публикации в Тильде (страницу в кабинете не удаляем - останется копия текста).</li>
<li>Настройки сайта → SEO → «Редиректы страниц (Code 301)»: старый адрес <code>/whatsapp</code>, новый <code>/telegram1c</code>. Сохранить, «Опубликовать все страницы».
По <a href="https://help-ru.tilda.cc/search-engine" target="_blank" rel="noopener">справке Тильды</a> 301 работает только с адреса, которого нет, поэтому сначала шаг 2.</li>
<li>Когда выйдет страница «Бот 1С для MAX», поменять цель редиректа на <code>/max1c</code>.</li>
<li>Отправить /whatsapp на переобход в Яндекс.Вебмастере, чтобы поиск быстрее увидел редирект.</li>
</ol>
</div>"""

q_html = "\n".join(
    f'<div class="q"><div class="qn">Вопрос {i}</div><b>{e(t)}</b><p>{e(d)}</p></div>'
    for i, (t, d) in enumerate(QUESTIONS, 1)
)

DOC = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Этап 0. Карта структуры alsn.ru по схеме подрядчика - 30.09.2026</title>
<style>
:root{{--bg:#f4f3ef;--card:#fff;--text:#1a1a1a;--muted:#5c5c5c;--border:#e2e2de;
--ok:#1a7f4b;--ok-bg:#e8f6ee;--warn:#9a6700;--warn-bg:#fff6e0;--danger:#b42318;--danger-bg:#fdecea;--info:#0b6e99;--info-bg:#e8f4fa}}
*{{box-sizing:border-box}}
body{{margin:0;font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--text);background:var(--bg)}}
.wrap{{max-width:1320px;margin:0 auto;padding:24px 18px 72px}}
h1{{font-size:26px;margin:0 0 6px;letter-spacing:-.02em}}
h2{{font-size:20px;margin:34px 0 10px}}
p{{margin:0 0 8px}} a{{color:#0b5cad}}
.muted{{color:var(--muted)}} .sm{{font-size:13px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin:12px 0}}
.pill{{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:650;border:1px solid var(--border);background:#fff;white-space:nowrap}}
.pill.ok{{color:var(--ok);background:var(--ok-bg);border-color:#c6e6d3}}
.pill.warn{{color:var(--warn);background:var(--warn-bg);border-color:#f0dfa0}}
.pill.danger{{color:var(--danger);background:var(--danger-bg);border-color:#f5c2c0}}
.pill.info{{color:var(--info);background:var(--info-bg);border-color:#bddceb}}
.pill.muted{{color:var(--muted)}}
.stats{{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}}
.stat{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:10px 14px;min-width:150px}}
.stat b{{display:block;font-size:24px}}
.tw{{overflow-x:auto;background:#fff;border:1px solid var(--border);border-radius:12px}}
table{{border-collapse:collapse;width:100%;min-width:900px}}
th,td{{text-align:left;vertical-align:top;padding:7px 8px;border-bottom:1px solid var(--border)}}
th{{background:#fafaf7;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);position:sticky;top:0}}
tr.l1 td{{background:#fbfaf6}}
code{{font:12.5px/1.4 ui-monospace,Consolas,monospace;background:#f1f1ee;padding:1px 5px;border-radius:5px}}
pre{{background:#0f172a;color:#e2e8f0;border-radius:12px;padding:16px;overflow:auto;font:13px/1.55 ui-monospace,Consolas,monospace}}
.q{{background:#fff;border:1px solid var(--border);border-left:4px solid #F55823;border-radius:10px;padding:12px 14px;margin:10px 0}}
.qn{{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
ul{{margin:6px 0 0 18px;padding:0}}
</style>
</head>
<body><div class="wrap">
<h1>Этап 0. Карта структуры alsn.ru по схеме подрядчика</h1>
<p class="muted">30.09.2026. Разделы «Услуги», «Продукты», «Лицензии». Источник схемы: <code>Предложеная структура/Схема_структуры_сайта_Аллсан_с_правками.xlsx</code>.
Живые страницы: срез alsn.ru от 29.09.2026 (138 страниц), карта сайта от 30.09.2026.</p>

<div class="card">
<b>Что это за документ.</b> Каждая строка схемы подрядчика сопоставлена со страницей живого сайта: есть она или нужна новая, где будет в меню и какой будет путь в хлебных крошках.
Это только карта, в Тильде по ней ничего не меняем. После вашего согласования (и ответов на вопросы внизу) идём на этап 1 - разводящие страницы.
<ul>
<li>Адреса существующих страниц не меняем, редиректов нет.</li>
<li>Все новые страницы - сразу в дизайне v3, как «Интеграция 1С с Ozon».</li>
<li>Меню - с 3-м уровнем, стандартными блоками Тильды (T228 или ME601B), без кода.</li>
</ul>
</div>

<div class="stats">
<div class="stat"><b>{count("have") + count("fix")}</b>строк схемы уже есть на сайте</div>
<div class="stat"><b>{count("new")}</b>новых страниц в разделах</div>
<div class="stat"><b>{n_have}</b>страниц поставщиков есть</div>
<div class="stat"><b>{n_new}</b>поставщиков - новые страницы</div>
<div class="stat"><b>{len(OUTSIDE)}</b>страниц вне схемы с решением</div>
</div>

<h2>1. Меню после перестройки</h2>
<p class="muted">Пункт, у которого есть подменю, в Тильде сам не кликается. Поэтому первая строка каждого списка ведёт на страницу самого пункта.
Пункты на новые страницы включаем только после их публикации.</p>
<pre>{e(MENU)}</pre>

<h2>2. Схема подрядчика и страницы сайта</h2>
<p class="muted">«Путь в крошках» - какой он будет. «Крошки сейчас» - что стоит на странице по срезу 29.09 («нет» - крошек нет).</p>
<div class="tw"><table>
<thead><tr><th>Строка схемы</th><th>Адрес</th><th>H1 сейчас</th><th>Статус</th><th>Путь в крошках</th><th>В меню</th><th>Крошки сейчас</th><th>Примечание</th></tr></thead>
<tbody>
{schema_rows()}
</tbody></table></div>

<h2>3. Страницы сайта, которых нет в схеме</h2>
<p class="muted">Схема подрядчика не учитывает переходы, синхронизации и часть посадочных с трафиком. Чтобы их не потерять, ставим их в иерархию через хлебные крошки и ссылки с родителя. В меню их нет.</p>
<div class="tw"><table>
<thead><tr><th>Адрес</th><th>H1 сейчас</th><th>Родитель</th><th>Решение</th></tr></thead>
<tbody>
{outside_rows()}
</tbody></table></div>
<p class="muted sm">Не входят в этот план и остаются как есть: «Наш опыт», «О компании», блог, СМИ, служебные страницы.</p>

<h2>4. Поставщики B2B (57 из схемы)</h2>
<p class="muted">Есть страница: {n_have}. Новые: {n_new}. Убрать: {n_drop}. Уточнить профиль: {n_doubt}. Все страницы поставщиков встают под «Все поставщики».</p>
<div class="tw"><table style="min-width:640px">
<thead><tr><th>№</th><th>Поставщик</th><th>Страница</th><th>Решение</th><th>Крошки сейчас</th></tr></thead>
<tbody>
{sup_html}
</tbody></table></div>

<h2>5. Что убираем</h2>
{REMOVE_WA}

<h2>6. Что нужно решить до этапа 1</h2>
{q_html}

<h2>7. Дальше</h2>
<div class="card">
<ul>
<li><b>Этап 1.</b> Макеты разводящих страниц «Услуги», «Продукты», «Лицензии» в дизайне v3, потом перенос в Тильду по шагам.</li>
<li><b>Этап 2.</b> Меню с 3-м уровнем на копии шапки, проверка на компьютере и телефоне, затем боевая шапка и подвал.</li>
<li><b>Этапы 3-5.</b> «Разработка и доработка 1С», 8 страниц конфигураций маркетплейсов, «Все поставщики» и страницы поставщиков.</li>
<li><b>Этап 6.</b> Хлебные крошки по путям из таблицы выше.</li>
</ul>
</div>
</div></body></html>
"""

OUT.write_text(DOC, encoding="utf-8")
print("OK", OUT, "have", count("have") + count("fix"), "new", count("new"), "sup", n_have, n_new, n_drop, n_doubt)
missing = [r[2] for r in SCHEMA if r[2] and r[3] in ("have", "fix") and r[2] not in PAGES and "…" not in r[2]]
missing += [p for p, _, _ in OUTSIDE if p not in PAGES]
print("not in live slice:", missing)
