import re, time, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def get(p):
    return urllib.request.urlopen(urllib.request.Request('https://alsn.ru' + p + '?x=%d' % time.time(), headers={'User-Agent': UA})).read().decode('utf-8')


for p in ['/vesii', '/caseecomsc']:
    h = get(p)
    head = h.split('</head>')[0]
    print('=====', p)
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', head, re.S):
        print('--- LD at', m.start(), 'len', len(m.group(1)))
        print(m.group(1))
    for m in re.finditer(r'<meta (?:name|property)="(og:[^"]+|description|robots)" content="([^"]*)"', head):
        print(m.group(1), '=', m.group(2)[:200])
    print('og:image', re.findall(r'property="og:image" content="([^"]+)"', head))
    body = h.split('</head>')[1]
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', body, re.S):
        print('--- BODY LD len', len(m.group(1)), m.group(1)[:300])
    imgs = re.findall(r'(?:data-original|src)="(https://static\.tildacdn\.com/[^"]+\.(?:jpg|jpeg|png|webp))"', body)
    print('imgs', imgs[:8])
