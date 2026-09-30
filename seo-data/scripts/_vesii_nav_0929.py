import re, time, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
h = urllib.request.urlopen(urllib.request.Request('https://alsn.ru/vesii?x=%d' % time.time(), headers={'User-Agent': UA})).read().decode()
b = h.split('</head>')[1]
i = b.find('aria-label="Хлебные крошки"')
j = b.rfind('<div id="rec', 0, i)
print(b[j:j + 160])
print(re.sub(r'<svg.*?</svg>', '[дом]', b[i - 5:b.find('</nav>', i) + 6]))
print(re.findall(r'<div id="rec(\d+)"[^>]*data-record-type="(\d+)"', b)[:6])
