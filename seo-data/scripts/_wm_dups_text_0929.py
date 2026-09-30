import re, html, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def get(p):
    return urllib.request.urlopen(urllib.request.Request('https://alsn.ru' + p, headers={'User-Agent': UA})).read().decode('utf-8', 'replace')


def text(h):
    h = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<header.*?</header>|<footer.*?</footer>', ' ', h, flags=re.S | re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


for p, n in [('/vesii', 3500), ('/event-2025-06-----old1', 1500), ('/event-2025-06', 1500), ('/event-marketplaces', 1500)]:
    h = get(p)
    print('=====', p)
    print('og:title', re.findall(r'property="og:title" content="([^"]*)"', h))
    print(text(h)[:n])
    dates = sorted(set(re.findall(r'\d{1,2}\s+(?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)(?:\s+20\d\d)?', text(h))))
    print('dates', dates)

sm = get('/sitemap.xml')
print('sitemap has', [u for u in ['event-2025-06-----old1', 'event-2025-06<', 'event-marketplaces', 'vesii'] if u in sm])
for p in ['/', '/casemarketplace', '/1c-ozon', '/1c-wildberries', '/cases']:
    h = get(p)
    print(p, sorted(set(re.findall(r'href="(?:https://alsn\.ru)?(/event[^"#?]*|/vesii)"', h))))
