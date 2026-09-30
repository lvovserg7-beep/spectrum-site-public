import re, time, html, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
URLS = [
    '/products/tproduct/946953291-241626506282-1s-predpriyatie-8-proizvodstvennaya-bezo',
    '/products/tproduct/946953291-725353126612-1s-predpriyatie-8-proizvodstvennaya-bezo',
    '/products/tproduct/946953291-573152840912-1s-predpriyatie-8-proizvodstvennaya-bezo',
    '/products/tproduct/946953291-614846453552-1s-predpriyatie-8-proizvodstvennaya-bezo',
    '/products/tproduct/946953291-157999786462-1s-predpriyatie-8-proizvodstvennaya-bezo',
]


def req(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA, 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}))


r = req('https://alsn.ru/products?x=%d' % time.time())
print('/products витрина Last-Modified:', r.headers.get('Last-Modified'))
for u in URLS:
    for q in ['?x=%d' % time.time(), '']:
        r = req('https://alsn.ru' + u + q)
        h = r.read().decode('utf-8')
        t = html.unescape(re.search(r'<title>(.*?)</title>', h, re.S).group(1))
        og = re.findall(r'property="og:title" content="([^"]*)"', h)
        sku = re.findall(r'itemprop="sku"[^>]*>([^<]+)<', h) or re.findall(r'"sku"\s*:\s*"([^"]+)"', h)
        print(u.split('/tproduct/')[1][:22], 'nocache' if q else 'plain  ', r.headers.get('Last-Modified'), sku[:1], '|', t, '| og:', og[:1])

# product data from Tilda store API used by the catalog block
h = req('https://alsn.ru/products?x=%d' % time.time()).read().decode('utf-8')
print('storepart ids:', sorted(set(re.findall(r'data-storepart-uid="(\d+)"', h)))[:5], sorted(set(re.findall(r'storepart[^"]{0,20}"(\d{6,})', h)))[:5])
