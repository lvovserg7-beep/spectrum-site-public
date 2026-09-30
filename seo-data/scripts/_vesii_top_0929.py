import io, re, time, urllib.request
from PIL import Image

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def raw(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA})).read()


h = raw('https://alsn.ru/vesii?x=%d' % time.time()).decode('utf-8')
body = h.split('</head>')[1]
recs = list(re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"([^>]*)data-record-type="(\d+)"', body))
for i, m in enumerate(recs[:8]):
    end = recs[i + 1].start() if i + 1 < len(recs) else m.start() + 20000
    seg = body[m.start():end]
    filt = re.findall(r't-cover__filter[^>]*style="([^"]*)"', seg)
    bgimg = re.findall(r'data-original="([^"]+)"', seg)[:1]
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', seg, flags=re.S))).strip()[:120]
    print(m.group(1), 'T' + m.group(3), m.group(2).strip()[:90], '| filter', filt[:1], '| img', bgimg, '|', txt)

img = 'https://static.tildacdn.com/lib/unsplash/1d7fbb63-e781-828e-4769-5b75cdb16048/photo.jpg'
im = Image.open(io.BytesIO(raw(img))).convert('RGB')
w, hh = im.size
top = im.crop((0, 0, w, max(1, hh // 30))).resize((1, 1)).getpixel((0, 0))
print('photo', im.size, 'top #%02x%02x%02x' % top)
