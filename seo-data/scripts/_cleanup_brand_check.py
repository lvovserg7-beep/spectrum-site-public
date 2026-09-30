import re, json, html, sys, urllib.request, pathlib

BR = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\tilda-briefs")
OUT = pathlib.Path(__file__).with_name("_cleanup_brand_pages")
OUT.mkdir(exist_ok=True)


import time
CACHE = len(sys.argv) > 1 and sys.argv[1] == "cache"


def get(url):
    sep = "&" if "?" in url else "?"
    last = ""
    for i in range(4):
        req = urllib.request.Request(url + sep + "chk=2909c%d" % i, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                h = r.read().decode("utf-8", "replace")
                if "<title>" in h:
                    return h
                last = "NO TITLE len=%d" % len(h)
        except Exception as e:
            last = "ERR " + str(e)
        time.sleep(3)
    print("FETCH FAIL", url, last)
    return last


def meta(h, name):
    m = re.search(r'<meta[^>]+(?:name|property)="%s"[^>]*content="([^"]*)"' % re.escape(name), h)
    return html.unescape(m.group(1)) if m else None


def metas(h, name):
    return [html.unescape(x) for x in re.findall(r'<meta[^>]+(?:name|property)="%s"[^>]*content="([^"]*)"' % re.escape(name), h)]


def title(h):
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    return html.unescape(m.group(1)) if m else None


def tags(h, t):
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip() for x in re.findall(r"<%s[^>]*>(.*?)</%s>" % (t, t), h, re.S)]


def ld(h):
    res = []
    for s in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try:
            res.append(("ok", json.loads(s)))
        except Exception as e:
            res.append(("BROKEN", s[:200]))
    return res


def types(h):
    out = []
    for st, d in ld(h):
        if st != "ok":
            out.append("BROKEN")
            continue
        items = d.get("@graph", [d]) if isinstance(d, dict) else d
        for it in items:
            if isinstance(it, dict):
                out.append(str(it.get("@type")) + ":" + str(it.get("@id", "")))
    return out


def has(h, s):
    return s in h or html.escape(s, quote=False) in h or html.escape(s) in h


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


pages = {}
URLS = {
    "home": "https://alsn.ru/",
    "about": "https://alsn.ru/about_us",
    "contacts": "https://alsn.ru/contacts",
    "vacancy": "https://alsn.ru/vacancy",
    "ecom": "https://alsn.ru/ecom",
    "etm": "https://alsn.ru/etm-ipro",
    "sc": "https://alsn.ru/caseecomsc",
    "xitsad": "https://alsn.ru/xitsadmarketplace",
    "hub": "https://alsn.ru/dopolnitelnie_licenzii",
    "its": "https://alsn.ru/its",
    "fresh": "https://alsn.ru/1cfresh",
    "p5": "https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-368525678472-1s-predpriyatie-8-prof-klientskaya-litse",
    "p10": "https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-359060596292-1s-predpriyatie-8-prof-klientskaya-litse",
    "p20": "https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-729293580752-1s-predpriyatie-8-prof-klientskaya-litse",
    "psrv": "https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-905369310501-1s-predpriyatie-83-prof-litsenziya-na-se",
    "vesii": "https://alsn.ru/vesii",
    "support": "https://alsn.ru/support1c",
}
for k, u in URLS.items():
    f = OUT / (k + ".html")
    h = f.read_text(encoding="utf-8") if CACHE and f.exists() else get(u)
    pages[k] = h
    (OUT / (k + ".html")).write_text(h, encoding="utf-8")

for k, h in pages.items():
    print("=" * 20, k, URLS[k])
    print(" title:", title(h))
    print(" descr:", meta(h, "description"))
    print(" robots:", metas(h, "robots"))
    print(" og:title:", meta(h, "og:title"))
    print(" og:descr:", meta(h, "og:description"))
    print(" og:image:", meta(h, "og:image"))
    print(" og:site_name:", metas(h, "og:site_name"))
    print(" h1:", tags(h, "h1")[:3])
    print(" ld:", types(h))
    print(" #organization count:", h.count('"@id": "https://alsn.ru/#organization"'), "| Organization objs:", sum(1 for t in types(h) if t.startswith("Organization:")))
    print(" alsn-bc-jsonld:", "alsn-bc-jsonld" in h, "| t-catalog__breadcrumbs:", "t-catalog__breadcrumbs" in h)

T = {k: text(v) for k, v in pages.items()}
chk = [
    ("home", "Аллсан Интеграция — франчайзи"), ("home", "Аллсан Интеграция - франчайзи"),
    ("home", "Аллсан Интеграция — официальный"), ("home", "Аллсан Интеграция - официальный"),
    ("home", "Наши специалисты — это"), ("home", "Наши специалисты - это"),
    ("home", "Аллсан Интеграция — внедрение"), ("home", "Аллсан Интеграция - внедрение"),
    ("home", "комната 503"), ("home", "TOP 5"), ("home", "ТОП 10"), ("home", "5 место"), ("home", "(Алсан"),
    ("home", "помещ. 1/5"), ("home", "telegram1c"), ("home", "Кто мы"),
    ("about", "Частые вопросы"), ("about", "Контакты Аллсан Интеграции"), ("about", "Аллсан Интеграция - главная"),
    ("about", "Генеральный директор - Львов"), ("about", "Генеральный директор — Львов"),
    ("about", "Аллсан Интеграция - партнёр 1С?"), ("about", "Аллсан Интеграция — партнёр 1С?"),
    ("about", "20,000"), ("about", "10,000"), ("about", "Allsun Integration"), ("about", "Сергей Львов"),
    ("vacancy", "Семь лет"), ("vacancy", "С 2015 года"), ("vacancy", "Allsun всегда"), ("vacancy", "Аллсан всегда"),
    ("vacancy", "100 проектов по разработке чат"), ("vacancy", "2000 успешно"),
    ("ecom", "Интеграция 1С с поставщиками телеком- и IT-оборудования"), ("ecom", "любых B2B"),
    ("ecom", "Интеграция 1С с поставщиками — это обмен"), ("ecom", "Интеграция 1С с поставщиками - это обмен"),
    ("ecom", "по API"), ("ecom", "Главная →"), ("ecom", "50+ крупнейшими"),
    ("sc", "Достигнутые результаты(экономический"), ("sc", "Достигнутые результаты (экономический"),
    ("sc", "Все кейсы →"), ("sc", "Интеграция 1С с поставщиками — ООО «СЦ»"),
    ("sc", "Кейс: интеграция 1С с поставщиками телеком- и IT-оборудования для ООО «СЦ»"),
    ("xitsad", "Кейс: интеграция 1С с маркетплейсами для ООО «ХИТСАД»"), ("xitsad", "Хлебные крошки"),
    ("hub", "Купить лицензии 1С ПРОФ"), ("its", "Купить 1С:КП ПРОФ"), ("fresh", "1С:Фреш"),
    ("hub", "Клиентская лицензия 1С ПРОФ — это"), ("hub", "Клиентская лицензия 1С ПРОФ - это"),
    ("its", "договор сопровождения"), ("fresh", "без своего сервера"),
]
print("=" * 20, "TEXT CHECKS (visible text)")
for k, s in chk:
    print(f" [{k}] {s!r}: text={s in T[k]} raw={has(pages[k], s)}")
    if s in ("TOP 5", "ТОП 10", "помещ. 1/5", "Allsun Integration", "Центр Реальной", "5 место") and s in T[k]:
        for m in re.finditer(re.escape(s), T[k]):
            print("    ctx:", T[k][max(0, m.start() - 120): m.end() + 120])
for k in ["home"]:
    for m in re.finditer("Реальной Автоматизации|реальной автоматизации|ЦРА", T[k]):
        print("  home CRA ctx:", T[k][max(0, m.start() - 150): m.end() + 80])

print("=" * 20, "breadcrumb nav snippets")
for k in ["home", "about", "ecom", "sc", "xitsad", "hub", "its", "fresh"]:
    m = re.search(r'<nav[^>]*aria-label="Хлебные крошки".*?</nav>', pages[k], re.S)
    print(k, ":", re.sub(r"\s+", " ", text(m.group(0))).strip() if m else None, "| arrow-t758:", "t758" in pages[k])

print("=" * 20, "ALT on case pages / ecom")
for k in ["sc", "xitsad", "ecom"]:
    imgs = re.findall(r"<img[^>]*>", pages[k])
    for tag in imgs:
        src = re.search(r'(?:data-original|src)="([^"]+)"', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        fn = src.group(1).rsplit("/", 1)[-1] if src else "?"
        print(f" [{k}] {fn[:45]:45} alt={html.unescape(alt.group(1)) if alt else None!r}")

# Catalog alts
print("=" * 20, "CATALOG ALTS")
cat = (BR / "tier2-catalog-alts-2026-09-16.html").read_text(encoding="utf-8")
arts = re.findall(r'<article class="prod".*?</article>', cat, re.S)
print(" products in brief:", len(arts))
for a in arts:
    sku = re.search(r'id="s-\d+">([^<]+)<', a)
    alt = re.search(r'id="a-\d+">([^<]+)<', a)
    link = re.search(r'href="(https://alsn\.ru/[^"]*tproduct[^"]*)"', a)
    name = re.search(r"<h3>.*?</span>\s*(.*?)</h3>", a, re.S)
    altt = html.unescape(alt.group(1)) if alt else None
    if not link:
        print(" NO LINK", name and name.group(1))
        continue
    h = get(link.group(1))
    ok = has(h, altt) if altt else None
    print(f" sku={sku and sku.group(1)} ok={ok} alt={altt!r} | {link.group(1)[-60:]}")
