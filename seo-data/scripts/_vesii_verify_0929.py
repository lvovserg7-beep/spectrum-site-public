import re, json, time, html, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
EXPECTED = open('../tilda-briefs/_head-vesii-2026-09-29.txt', encoding='utf-8').read()
EXP = json.loads(re.search(r'<script[^>]*>(.*)</script>', EXPECTED, re.S).group(1))

r = urllib.request.urlopen(urllib.request.Request('https://alsn.ru/vesii?x=%d' % time.time(), headers={'User-Agent': UA, 'Cache-Control': 'no-cache'}))
h = r.read().decode('utf-8')
print('Last-Modified:', r.headers.get('Last-Modified'))
head, body = h.split('</head>', 1)

lds = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', head, re.S)
print('LD blocks in HEAD:', len(lds))
for i, s in enumerate(lds):
    try:
        j = json.loads(s)
        g = j.get('@graph', [j])
        print(i, 'OK', [(n.get('@type'), n.get('@id')) for n in g])
        if any(n.get('@id') == 'https://alsn.ru/vesii#article' for n in g):
            print('   совпадает с эталоном:', j == EXP)
            if j != EXP:
                for a, b in zip(g, EXP['@graph']):
                    if a != b:
                        print('   diff in', a.get('@type'))
    except Exception as e:
        print(i, 'INVALID', e, s[:200])
print('caseecomsc в HEAD:', 'caseecomsc' in head)
print('description:', re.findall(r'<meta name="description" content="([^"]*)"', head))
print('og:description:', re.findall(r'property="og:description" content="([^"]*)"', head))
print('og:image:', re.findall(r'property="og:image" content="([^"]*)"', head))
print('og:title:', re.findall(r'property="og:title" content="([^"]*)"', head))
print('title:', re.findall(r'<title>(.*?)</title>', head))

print('T758 блоков:', len(re.findall(r'data-record-type="758"', body)))
vis = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', body, flags=re.S)
vis = html.unescape(re.sub(r'<[^>]+>', ' ', vis))
print('«СЦ» в видимом тексте:', [m.group(0) for m in re.finditer(r'.{0,60}«СЦ».{0,20}', vis)])
print('стрелка →:', [m.group(0).strip() for m in re.finditer(r'.{0,50}→.{0,50}', vis)])
print('Хлебные крошки T123:', 'aria-label="Хлебные крошки"' in body)
