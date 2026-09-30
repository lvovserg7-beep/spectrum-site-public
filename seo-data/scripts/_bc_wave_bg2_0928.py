import io, re, urllib.request
from PIL import Image

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def raw(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA})).read()


for u in ['https://static.tildacdn.com/tild3838-6433-4730-b866-306261396130/Merlion-API-01.jpg',
          'https://static.tildacdn.com/tild6331-3736-4963-b866-623866656333/perehod-s-ut-na-unf-.png']:
    im = Image.open(io.BytesIO(raw(u))).convert('RGB')
    w, h = im.size
    strip = im.crop((0, 0, w, max(1, h // 30))).resize((1, 1))
    print(u.rsplit('/', 1)[1], im.size, '#%02x%02x%02x' % strip.getpixel((0, 0)))

h = raw('https://alsn.ru/perehod-s-upp-na-ka-unf-ut').decode('utf-8')
for m in re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"([^>]*)data-record-type="(\d+)"', h):
    print(m.group(1), m.group(3), m.group(2)[:150])
    if m.start() > 200000:
        break
i = h.find('Хлебные крошки')
print(h[i - 900:i + 200])
