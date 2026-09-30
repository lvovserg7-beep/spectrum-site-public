import urllib.request, re, time, json
from concurrent.futures import ThreadPoolExecutor
from email.utils import parsedate_to_datetime
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'


def get(u, head=False):
    r = urllib.request.Request(u, headers={'User-Agent': UA}, method='HEAD' if head else 'GET')
    return urllib.request.urlopen(r, timeout=30)


def locs(u):
    x = get(u + '?x=%d' % time.time()).read().decode('utf-8', 'replace')
    return re.findall(r'<loc>\s*(.*?)\s*</loc>', x)


urls = set()
todo = ['https://alsn.ru/sitemap.xml']
seen = set()
while todo:
    s = todo.pop()
    if s in seen:
        continue
    seen.add(s)
    for l in locs(s):
        (todo if l.endswith('.xml') else urls).__class__
        if l.endswith('.xml'):
            todo.append(l)
        else:
            urls.add(l)
print('карты:', sorted(seen))
extra = ['https://alsn.ru/event-marketplaces', 'https://alsn.ru/event-2025-06-----old1']
for e in extra:
    urls.add(e)
print('адресов:', len(urls))


def lm(u):
    try:
        r = get(u + ('&' if '?' in u else '?') + 'x=%d' % time.time(), head=True)
        v = r.headers.get('Last-Modified')
        return u, v, r.status
    except Exception as ex:
        return u, None, str(ex)[:60]


with ThreadPoolExecutor(12) as ex:
    res = list(ex.map(lm, sorted(urls)))
today = []
for u, v, st in res:
    if v:
        d = parsedate_to_datetime(v)
        if d.strftime('%Y-%m-%d') == '2026-09-29' or (d.strftime('%Y-%m-%d') == '2026-09-28' and d.hour >= 21):
            today.append((d.isoformat(), u))
bad = [(u, st) for u, v, st in res if not v]
today.sort()
for d, u in today:
    print(d, u)
print('сегодня:', len(today), '| без даты:', len(bad))
for b in bad[:20]:
    print('  нет даты', b)
json.dump({'today': today, 'nodate': bad}, open(r'c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_published_today_0929.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
