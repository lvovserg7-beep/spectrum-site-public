import json, re, html, urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'replace')


def locs(u):
    return re.findall(r'<loc>([^<]+)</loc>', get(u))


urls = []
for sm in locs('https://alsn.ru/sitemap.xml') or []:
    if sm.endswith('.xml'):
        urls += locs(sm)
    else:
        urls.append(sm)
if not urls:
    urls = locs('https://alsn.ru/sitemap.xml')
urls = sorted(set(u for u in urls if not u.endswith('.xml')))
print('urls', len(urls))


def meta(u):
    try:
        h = get(u)
    except Exception as e:
        return u, None, None, str(e)
    t = re.search(r'<title[^>]*>(.*?)</title>', h, re.S)
    d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', h)
    rob = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', h)
    can = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', h)
    f = lambda m: html.unescape(m.group(1)).strip() if m else ''
    return u, f(t), f(d), {'robots': f(rob), 'canonical': f(can)}


with ThreadPoolExecutor(12) as ex:
    rows = list(ex.map(meta, urls))

bt, bd = defaultdict(list), defaultdict(list)
for u, t, d, x in rows:
    if t is None:
        continue
    if 'noindex' in (x.get('robots') or ''):
        continue
    bt[t].append(u)
    if d:
        bd[d].append(u)

dt = {k: v for k, v in bt.items() if len(v) > 1}
dd = {k: v for k, v in bd.items() if len(v) > 1}
print('dup titles groups', len(dt), 'pages', sum(len(v) for v in dt.values()))
for k, v in dt.items():
    print('T:', k)
    for u in v: print('   ', u)
print('dup desc groups', len(dd), 'pages', sum(len(v) for v in dd.values()))
for k, v in dd.items():
    print('D:', k[:150])
    for u in v: print('   ', u)
errs = [r for r in rows if r[1] is None]
print('errors', len(errs), [e[0] for e in errs][:10])
json.dump({'rows': rows, 'dup_titles': dt, 'dup_desc': dd}, open('_dup-meta-2026-09-29.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
