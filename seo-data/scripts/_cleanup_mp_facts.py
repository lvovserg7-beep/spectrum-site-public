import re, html, pathlib, json
C = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_cleanup_mp_cache")

def meta(t, key):
    m = re.search(r'<meta[^>]+(?:name|property)="%s"[^>]+content="([^"]*)"' % re.escape(key), t)
    return html.unescape(m.group(1)) if m else None

def txt(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

for f in sorted(C.glob("*.html")):
    t = f.read_text(encoding="utf-8", errors="replace")
    print("=" * 20, f.stem)
    m = re.search(r"<title>(.*?)</title>", t, re.S)
    print("title:", html.unescape(m.group(1)) if m else None)
    for k in ["description", "og:title", "og:description", "og:image", "og:site_name", "robots"]:
        print(k + ":", meta(t, k))
    for tag in ["h1", "h2"]:
        for m in re.finditer(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), t, re.S):
            print(" ", tag, txt(m.group(1))[:120])
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    for ld in lds:
        types = re.findall(r'"@type"\s*:\s*"([^"]+)"', ld)
        dm = re.findall(r'"date(?:Modified|Published)"\s*:\s*"([^"]+)"', ld)
        print("  LD:", types[:6], dm)
    print("  .v3 in style:", ".v3" in t, "| breadcrumbs-like:", "Главная" in t)
    for kw in ["priceold", "Старая цена", "79 000", "79000", "40 700", "69 990", "НДС 5%", "НДС", "rFBS", "FBO", "DBS",
               "с 2015", "Принимаем любые предложения", "БЕСПЛАТНО", "+300%", "×4", "в 4 раза", "добавить в корзину",
               "Добавить в корзину", "t-store__prod-popup__btn", "t706", "tcart", "2026-09-1", "2026-09-2", "продлен"]:
        c = t.count(kw)
        if c:
            print(f"  [{kw}] x{c}")
