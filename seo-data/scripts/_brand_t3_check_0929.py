import urllib.request, re, time, html
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
for p in ['/', '/about_us', '/vacancy']:
    h = urllib.request.urlopen(urllib.request.Request('https://alsn.ru' + p + '?x=%d' % time.time(), headers={'User-Agent': UA})).read().decode('utf-8', 'replace')
    t = re.search(r'<title>(.*?)</title>', h, re.S).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    rb = re.findall(r'<meta name="robots"[^>]*>', h)
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    faq = 'Частые вопросы' in h
    print(p, '\n title:', html.unescape(t), '\n desc:', html.unescape(d.group(1)) if d else None,
          '\n robots:', rb, '\n h1:', [re.sub('<[^>]+>', '', x)[:120] for x in h1], '\n "Частые вопросы":', faq,
          '\n длинное тире в title/desc:', '\u2014' in t or (d and '\u2014' in html.unescape(d.group(1))))
