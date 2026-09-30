import re, json, urllib.request, html as H, os

OUT = os.path.join(os.path.dirname(__file__), "_cleanup_impl_pages")
os.makedirs(OUT, exist_ok=True)
PAGES = {
    "dev": "https://alsn.ru/development1c?chk=2909b",
    "ka": "https://alsn.ru/kompleksnaya_avtomatizaciya?chk=2909b",
    "erp": "https://alsn.ru/erp-time-price?chk=2909b",
    "sup": "https://alsn.ru/support1c?chk=2909b",
    "robots": "https://alsn.ru/robots.txt",
}
src = {}
for k, u in PAGES.items():
    req = urllib.request.Request(u, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9",
    })
    try:
        t = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    except Exception as e:
        print("FETCH FAIL", k, u, e)
        t = ""
    src[k] = t
    open(os.path.join(OUT, k + ".html"), "w", encoding="utf-8").write(t)


def text(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    return re.sub(r"\s+", " ", s)


def meta(s):
    r = {}
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    r["title"] = H.unescape(m.group(1)) if m else None
    for n in ["description", "robots"]:
        m = re.search(r'<meta name="%s" content="([^"]*)"' % n, s)
        r[n] = H.unescape(m.group(1)) if m else None
    for p in ["og:title", "og:description", "og:image"]:
        m = re.search(r'<meta property="%s" content="([^"]*)"' % p, s)
        r[p] = H.unescape(m.group(1)) if m else None
    r["canonical"] = re.findall(r'rel="canonical" href="([^"]*)"', s)
    r["h1"] = [text(x).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)]
    r["h2"] = [text(x).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)]
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    types = []
    for l in lds:
        try:
            j = json.loads(l)
            if "@graph" in j:
                types += [g.get("@type") for g in j["@graph"]]
            else:
                types.append(j.get("@type"))
        except Exception as e:
            types.append("ERR:" + str(e)[:40])
    r["ld"] = types
    r["dateModified"] = re.findall(r'"dateModified":\s*"([^"]*)"', s)
    r["alts"] = sorted(set(re.findall(r'alt="([^"]*)"', s)))
    r["og_site_name"] = len(re.findall(r'og:site_name', s))
    r["http_src"] = len(re.findall(r'src="http://', s))
    return r


for k in ["dev", "ka", "erp", "sup"]:
    print("=" * 20, k)
    m = meta(src[k])
    for kk, v in m.items():
        print(kk, ":", v)

print("=" * 20, "robots")
print(src["robots"])


def has(k, s):
    return s in text(src[k]) or s in src[k]


CHECKS = {
    "dev": [
        "1С\" по Москве", "Если вы украдете данные", "Как вы защищаете данные клиента",
        "Мы осуществляем внедрение, обслуживание", "Внедряем конфигурации 1С:Предприятие под ваши процессы",
        "Анализ потребностей по доработке", "Анализ процессов и потребностей по интеграции 1С",
        "Тестирование доработок на стороне", "Тестирование на стороне клиента с руководителем проекта Аллсан",
        "Работы проводят программисты и аналитики", "Кто внедряет 1С",
        "Полезные страницы по внедрению 1С", "Реакция на задачи - 15 мин", "Обследование, настройка, обучение и запуск",
        "Настроим УТ, КА или ERP под ваши процессы", "ТОП 10 Центра реальной автоматизации",
        "Это не техподдержка и не продажа коробки", "Внедрение 1С под ключ на платформе 1С:Предприятие",
        "Гарантия на работы 90 дней", "Договор 1С:КП оформляем отдельно", "Стоимость внедрения 1С",
        "Этапы внедрения 1С", "Частые вопросы по внедрению 1С", "Какие конфигурации 1С внедряем",
        "Отдельный разбор внедрения 1С:Комплексная автоматизация",
        "Внедрение 1С:Комплексная автоматизация", "Стоимость и этапы внедрения 1С:ERP",
        "Техподдержка 1С после запуска", "1С:КП - подписка на сопровождение от 1С", "Кейсы внедрения и автоматизации",
        "HowTo", "FAQPage", "development1c#service", "development1c#breadcrumb", "development1c#webpage",
        "Внедрение 1С под ключ, Аллсан", "Внедрение 1С:ERP на производстве",
    ],
    "ka": [
        "доступен в только", "доступен только в 1С:ERP", "Внедрения проводят программисты", "Кто внедряет 1С:КА",
        "Полезные страницы по внедрению 1С", "Общий разбор внедрения 1С", "Реакция на задачи - 15 мин",
        "Обследование, настройка, обучение и запуск", "ТОП 10 Центра реальной автоматизации",
        "Цифры ниже - цена программы 1С:КА", "Это сопровождение уже работающей КА", "FAQPage",
        "kompleksnaya_avtomatizaciya#service", "kompleksnaya_avtomatizaciya#breadcrumb", "kompleksnaya_avtomatizaciya#webpage",
        "Интерфейс 1С:Комплексная автоматизация", "Клиенты Аллсан", "Стоимость — после консультации",
        "Стоимость - после консультации",
    ],
    "erp": [
        "Ввод в действие", "Ввод в действие", "автоматизированной системы", "автоматизированной системы",
        "собранной информации", "собранной информации", "программный продукт", "программный продукт",
        "консультационной и технической", "консультационной и технической",
        "Внедрение 1С:ERP проводят программисты", "Кто внедряет 1С:ERP", "Полезные страницы по внедрению 1С",
        "Общий разбор внедрения 1С", "Внедряем 1С:ERP на производстве по всей России",
        "Внедряем и дорабатываем 1С ЕРП", "Из чего складывается стоимость внедрения 1С:ERP",
        "Как проходит внедрение 1С:ERP под ключ", "Общий разбор внедрения - страница",
        "HowTo", "FAQPage", "erp-time-price#service", "erp-time-price#breadcrumb", "erp-time-price#webpage",
        "Консультация — Аллсан", "Консультация - Аллсан", "Реакция на задачи - 15 мин",
    ],
    "sup": [
        "Техподдержка / Внедрение / Сопровождение", "Пакет часов техподдержки", "Особенности тарифа",
        "Разовое обращение", "Корпоративный проект", "Это не 1С:КП и не внедрение с нуля",
        "База 1С у вас уже работает", "support1c#service", "support1c#webpage", "support1c#breadcrumb",
        "Клиенты Аллсан", "Сертификат Аллсан Интеграция", "Зеленоград", "rec3954909701", "rec1207704771",
        "t213", "Главная →", "#organization",
    ],
}
t_erp = text(src["erp"])
print("ERP combining breve count:", t_erp.count("\u0306"))
for w in ["Ввод в дей", "автоматизированно", "собранно", "программны", "консультационно"]:
    for m in re.finditer(re.escape(w), t_erp):
        frag = t_erp[m.start():m.start() + 30]
        print("  ", w, "->", repr(frag), "breve" if "\u0306" in frag else "ok")
        break
for k, lst in CHECKS.items():
    print("=" * 20, "CHECK", k)
    for s in lst:
        print(("YES " if has(k, s) else "no  ") + s, "| count:", src[k].count(s))
