import re, time, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def req(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'}))


sm = req('https://alsn.ru/sitemap.xml?x=%d' % time.time()).read().decode()
print('sitemap event:', re.findall(r'<loc>([^<]*event[^<]*)</loc>', sm))
for p in ['/event-2025-06-----old1', '/event-2025-06', '/event-marketplaces']:
    for q in ['?x=%d' % time.time(), '']:
        r = req('https://alsn.ru' + p + q)
        head = r.read().decode().split('</head>')[0]
        print(p, 'nocache' if q else 'plain', r.status,
              re.findall(r'<meta[^>]*name="robots"[^>]*>', head),
              'X-Robots:', r.headers.get('X-Robots-Tag'),
              '| Last-Modified:', r.headers.get('Last-Modified'))
