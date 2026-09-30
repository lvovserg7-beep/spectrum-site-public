import re, time, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def get(p):
    return urllib.request.urlopen(urllib.request.Request('https://alsn.ru' + p + '?x=%d' % time.time(), headers={'User-Agent': UA})).read().decode('utf-8')


h = get('/vesii')
body = h.split('</head>')[1]
for m in re.finditer(r'<div id="rec(\d+)"[^>]*data-record-type="(\d+)"', body):
    seg = body[m.start():m.start() + 6000]
    imgs = set(re.findall(r'(https://(?:static|optim)\.tildacdn\.com/[^"\'\s)]+\.(?:jpg|jpeg|png|webp))', seg))
    imgs = [i for i in imgs if 'Tilda_Icons' not in i and '_5.png' not in i and 'noroot' not in i]
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', seg))[:80]
    if imgs:
        print(m.group(1), m.group(2), imgs[:4], '|', txt)

d = get('/development1c').split('</head>')[0]
print('dev ids', sorted(set(re.findall(r'"@id"\s*:\s*"([^"]+)"', d))))
print('dev types', sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', d))))
c = get('/cases').split('</head>')[0]
print('cases ids', sorted(set(re.findall(r'"@id"\s*:\s*"([^"]+)"', c))))
