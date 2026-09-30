import csv, io, re
from collections import Counter

SRC = r'C:\Users\ALSN_LSA\Desktop\Спектр\store-163322-202609291141.csv'
OUT_FULL = r'C:\Users\ALSN_LSA\Desktop\Спектр\store-163322-202609291141-fixed.csv'
OUT_SHORT = r'C:\Users\ALSN_LSA\Desktop\Спектр\store-163322-202609291141-17-kartochek.csv'
GEN = r'c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_build_dups_html_0929.py'

src = open(GEN, encoding='utf-8').read()
body = re.search(r'^PRODUCTS\s*=.*?^\]', src, re.S | re.M).group(0)
PRODUCTS = eval(body.split('=', 1)[1], {'PB': 0, 'LIC': 0, 'KA': 0})
SEO = {}
for _, _, items in PRODUCTS:
    for url, t in items:
        SEO[re.search(r'tproduct/\d+-(\d+)-', url).group(1)] = t
assert len(SEO) == 17, len(SEO)

NAME = {
    '241626506282': '1С Предприятие 8 Производственная безопасность Промышленная безопасность Электронная поставка',
    '725353126612': '1С Предприятие 8 Производственная безопасность Пожарная безопасность Электронная поставка',
    '573152840912': '1С Предприятие 8 Производственная безопасность Комплексная Электронная поставка',
    '157999786462': '1С Предприятие 8 Производственная безопасность Охрана труда Электронная поставка',
    '697998222332': '1С Предприятие 8 ПРОФ Клиентская лицензия на 1 рабочее место Электронная поставка',
    '350780030942': '1С:Предприятие 8 ПРОФ. Клиентская лицензия на 1 рабочее место. Коробочная поставка (арт. 4601546080875)',
    '680601662821': '1С Комплексная автоматизация для 10 пользователей + клиент-сервер (x86-64) Электронная поставка',
    '282548349311': '1С Комплексная автоматизация для 10 пользователей + клиент-сервер (x86-64) Коробочная поставка',
}


def spans(line):
    """Границы полей в сырой строке (с кавычками), разделитель ';'."""
    out, i, n, start, q = [], 0, len(line), 0, False
    while i < n:
        c = line[i]
        if q:
            if c == '"':
                if i + 1 < n and line[i + 1] == '"':
                    i += 1
                else:
                    q = False
        elif c == '"':
            q = True
        elif c == ';':
            out.append((start, i)); start = i + 1
        i += 1
    out.append((start, n))
    return out


def enc(v):
    return '"' + v.replace('"', '""') + '"'


raw = open(SRC, 'rb').read().decode('utf-8')
lines = raw.split('\n')
head = lines[0]
hdr = next(csv.reader([head], delimiter=';'))
iT, iS = hdr.index('Title'), hdr.index('SEO title')
changed, short, log = [], [head], []
for k, ln in enumerate(lines[1:], 1):
    if not ln:
        continue
    r = next(csv.reader([ln], delimiter=';'))
    uid = r[0]
    if uid not in SEO:
        continue
    sp = spans(ln)
    assert len(sp) == len(hdr), (uid, len(sp))
    edits = [(iS, SEO[uid])]
    if uid in NAME:
        edits.append((iT, NAME[uid]))
    for idx, val in sorted(edits, key=lambda e: -sp[e[0]][0]):
        a, b = sp[idx]
        log.append((uid, r[2], hdr[idx], r[idx], val))
        ln = ln[:a] + enc(val) + ln[b:]
    r2 = next(csv.reader([ln], delimiter=';'))
    assert r2[iS] == SEO[uid] and r2[iT] == NAME.get(uid, r[iT])
    assert [x for j, x in enumerate(r2) if j not in (iT, iS)] == [x for j, x in enumerate(r) if j not in (iT, iS)]
    lines[k] = ln
    short.append(ln)
    changed.append(uid)
assert len(changed) == 17, changed

new = '\n'.join(lines)
open(OUT_FULL, 'wb').write(new.encode('utf-8'))
open(OUT_SHORT, 'wb').write(('\n'.join(short) + '\n').encode('utf-8'))

rows = list(csv.reader(io.StringIO(new, newline=''), delimiter=';'))[1:]
seo = Counter(x[iS] for x in rows if x[iS])
tit = Counter(x[iT] for x in rows)
print('дубли SEO title среди 17:', [s for s in SEO.values() if seo[s] > 1])
print('дубли названий среди 8:', [s for s in NAME.values() if tit[s] > 1])
print('строк отличается:', sum(1 for a, b in zip(raw.split('\n'), lines) if a != b))
print('тире:', new.count('\u2014') - raw.count('\u2014'))
for u, sku, f, old, val in log:
    print(sku, f, '|', old, '=>', val)
