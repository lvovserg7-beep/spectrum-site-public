import re, html, urllib.request, urllib.error, time, importlib.util
from collections import Counter

spec = importlib.util.spec_from_file_location('b', '_build_dups_html_0929.py')
src = open('_build_dups_html_0929.py', encoding='utf-8').read()
ns = {'__file__': __file__}
exec(src.split('P = []')[0].replace("live = json.load(open(ROOT / '_wm-dups-live-2026-09-29.json', encoding='utf-8'))", ''), ns)
PRODUCTS, VESII_DESC = ns['PRODUCTS'], ns['VESII_DESC']

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def get(p):
    u = 'https://alsn.ru' + p + ('&' if '?' in p else '?') + 'nc=' + str(int(time.time()))
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'}))
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''


def one(rx, h):
    m = re.search(rx, h, re.S | re.I)
    return html.unescape(m.group(1)).strip() if m else ''


titles = []
print('=== Д-3 карточки')
for _, _, items in PRODUCTS:
    for u, new in items:
        st, h = get(u)
        t = one(r'<title>(.*?)</title>', h)
        titles.append(t)
        ok = 'OK ' if t == new else 'ERR'
        print(ok, st, u.split('/tproduct/')[1][:40], '|', t, '' if t == new else f'  <> ждали: {new}')
dup = [t for t, c in Counter(titles).items() if c > 1]
print('дубли среди карточек:', dup)

print('=== Д-1 vesii')
st, h = get('/vesii')
d = one(r'<meta name="description" content="([^"]*)"', h)
og = one(r'property="og:description" content="([^"]*)"', h)
print('desc', 'OK' if d == VESII_DESC else 'ERR', '|', d)
print('og  ', 'OK' if og == VESII_DESC else 'ERR', '|', og)
print('T758 на странице:', 'data-record-type="758"' in h, '| текст СЦ в видимом:', 'поставщиками в ООО «СЦ»' in re.sub(r'<script.*?</script>', '', h, flags=re.S))
print('код caseecomsc в HEAD:', 'caseecomsc' in h.split('</head>')[0])

print('=== Д-2 вебинары')
sm = get('/sitemap.xml')[1]
for p in ['/event-2025-06-----old1', '/event-2025-06', '/event-marketplaces']:
    st, h = get(p)
    rb = re.findall(r'<meta name="robots" content="([^"]+)"', h)
    print(p, st, 'robots', rb, '| в sitemap:', ('alsn.ru' + p + '<') in sm, '| title', one(r'<title>(.*?)</title>', h)[:60])
