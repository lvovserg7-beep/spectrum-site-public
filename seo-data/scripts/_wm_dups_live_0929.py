import json, re, html, urllib.request, urllib.error

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
d = json.load(open('_wm-dups-2026-09-29.json', encoding='utf-8'))


def get(p):
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://alsn.ru' + p, headers={'User-Agent': UA}))
        return r.status, r.geturl(), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, '', ''


def one(rx, h):
    m = re.search(rx, h, re.S | re.I)
    return html.unescape(re.sub(r'<[^>]+>|\s+', ' ', m.group(1))).strip() if m else ''


res = {}
seen = set()
for kind in ('title', 'description'):
    for g in d[kind]:
        for u, _ in g['urls']:
            if u in seen:
                continue
            seen.add(u)
            st, final, h = get(u)
            r = {
                'status': st,
                'final': final,
                'title': one(r'<title>(.*?)</title>', h),
                'desc': one(r'<meta name="description" content="([^"]*)"', h),
                'h1': one(r'<h1[^>]*>(.*?)</h1>', h),
                'name': one(r'itemprop="name"[^>]*>(.*?)<', h),
                'sku': one(r'itemprop="sku"[^>]*>(.*?)<', h) or one(r'"sku"\s*:\s*"([^"]+)"', h),
                'price': one(r'itemprop="price"[^>]*content="([^"]+)"', h),
                'canonical': one(r'<link rel="canonical" href="([^"]+)"', h),
                'robots': one(r'<meta name="robots" content="([^"]+)"', h),
            }
            res[u] = r
            print(u)
            print('   ', r)
json.dump(res, open('_wm-dups-live-2026-09-29.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
