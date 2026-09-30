import re, json, time, html, urllib.request
from collections import Counter

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
src = open('_build_dups_html_0929.py', encoding='utf-8').read()
ns = {'__file__': __file__}
exec(src.split('P = []')[0].replace("live = json.load(open(ROOT / '_wm-dups-live-2026-09-29.json', encoding='utf-8'))", ''), ns)
PRODUCTS = ns['PRODUCTS']
BEFORE = json.load(open('_wm-dups-live-2026-09-29.json', encoding='utf-8'))


def req(u, ref=None):
    hd = {'User-Agent': UA, 'Cache-Control': 'no-cache'}
    if ref:
        hd['Referer'] = ref
    return urllib.request.urlopen(urllib.request.Request(u, headers=hd))


def one(rx, h):
    m = re.search(rx, h, re.S | re.I)
    return html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip() if m else ''


for vitr, vurl, _ in PRODUCTS:
    r = req(vurl + '?x=%d' % time.time())
    print('ВИТРИНА', vurl, 'опубликована:', r.headers.get('Last-Modified'))

rows = []
for vitr, vurl, items in PRODUCTS:
    print('\n==', vitr)
    for u, new in items:
        h = req('https://alsn.ru' + u + '?x=%d' % time.time()).read().decode('utf-8')
        page_title = one(r'<title>(.*?)</title>', h)
        desc = one(r'<meta name="description" content="([^"]*)"', h)
        h1 = one(r'<h1[^>]*>(.*?)</h1>', h)
        uid = re.search(r'/tproduct/\d+-(\d+)-', u).group(1)
        api_title = api_seo = ''
        for sp in set(re.findall(r'storepart[a-z_]*["\':= ]+["\']?(\d{5,})', h, re.I)):
            d = req('https://store.tildaapi.com/api/getproduct/?storepartuid=%s&productuid=%s&c=%d' % (sp, uid, time.time()), 'https://alsn.ru/').read().decode()
            try:
                p = json.loads(d).get('product')
            except Exception:
                continue
            if isinstance(p, dict):
                api_title = p.get('title', '')
                api_seo = {k: v for k, v in p.items() if 'seo' in k.lower()}
                break
        orig = BEFORE[u]['h1']
        st_title = 'OK ' if page_title == new else 'ERR'
        st_name = 'OK ' if api_title.replace('.', '').replace(':', ' ').split() and api_title == orig or api_title.startswith('1С') else 'ERR'
        rows.append((u, page_title, desc))
        print(f'{st_title} title | {page_title}')
        if page_title != new:
            print(f'          ждали   | {new}')
        print(f'{st_name} название в каталоге | {api_title}')
        print(f'    h1 на странице | {h1}')
        print(f'    description    | {desc[:110]}')
        if api_seo:
            print(f'    seo в API      | {api_seo}')

print('\nдубли title:', [t for t, c in Counter(r[1] for r in rows).items() if c > 1])
print('дубли description:', [t for t, c in Counter(r[2] for r in rows).items() if c > 1])
