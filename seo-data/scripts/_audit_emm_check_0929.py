import urllib.request, re, time, html
from concurrent.futures import ThreadPoolExecutor
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
sm = urllib.request.urlopen(urllib.request.Request('https://alsn.ru/sitemap.xml?x=%d' % time.time(), headers={'User-Agent': UA})).read().decode()
urls = re.findall(r'<loc>\s*(.*?)\s*</loc>', sm)
PAT = {
    '15+ лет': r'15\+?\s*лет',
    'с 2015': r'с 2015',
    'более 10 лет / больше 10 лет': r'(?:более|больше)\s+10\s+лет',
    'TOP 5 / ТОП 5 / 5 место': r'(?:TOP|ТОП)[ -]?5\b|5\s*мест[оа]',
    '2 место': r'2\s*место',
    'до 50 %': r'до\s*50\s*%',
    'от 30 %': r'от\s*30\s*%',
    '9 из 10': r'9\s*из\s*10',
    'экспресс-аудит': r'[Ээ]кспресс[- ]аудит',
    'за 0 руб': r'за\s*0\s*руб',
    'ПЭК': r'ПЭК',
    'гарантия 90 дней': r'90\s*дней',
    'Начальный 10 800': r'10\s*800',
    'КП в течение 1 дня': r'КП в течени[ие] 1 дня',
}


def txt(u):
    try:
        h = urllib.request.urlopen(urllib.request.Request(u + '?x=%d' % time.time(), headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'replace')
    except Exception:
        return u, ''
    h = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', h, flags=re.S)
    return u, html.unescape(re.sub(r'<[^>]+>', ' ', h)).replace('\xa0', ' ')


with ThreadPoolExecutor(12) as ex:
    pages = list(ex.map(txt, urls))
for k, p in PAT.items():
    hits = []
    for u, t in pages:
        for m in re.finditer(p, t):
            s = re.sub(r'\s+', ' ', t[max(0, m.start() - 70):m.end() + 70])
            hits.append((u.replace('https://alsn.ru', ''), s))
            break
    print('\n##', k, '- страниц:', len(hits))
    for u, s in hits[:8]:
        print('  ', u or '/', '|', s)
