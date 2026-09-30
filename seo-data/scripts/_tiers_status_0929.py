import json, re, os
B = r'C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-transcripts'
IDS = ['221c1001-de82-40f1-a4a3-52914540cc46', 'e63ab8cf-bc45-4540-b655-6d63703ae8b9', 'c9a67249-e662-438a-b432-2f166ef508a7',
       '51afc82f-f2e2-4e52-899a-5e19fff5d41d', '2b64b9ba-e869-49be-a421-652be76aa203', '0aa1355f-3bcd-4a0d-9ea6-3b0d1e62f682',
       'db635a50-75a0-4090-a501-a23edef749c5', '2c6917f1-e100-489b-ab07-45a1ab55e50a']
N = 3


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ('input', 'arguments'):
                continue
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


for i in IDS:
    p = os.path.join(B, i, i + '.jsonl')
    prod, turns, cur = None, [], None
    for ln in open(p, encoding='utf-8'):
        o = json.loads(ln)
        t = '\n'.join(texts(o.get('message', o)))
        if o.get('role') == 'user':
            q = re.search(r'<user_query>(.*?)</user_query>', t, re.S)
            if not q:
                continue
            m = re.search(r'разбираем\s+(?:продукт\s+)?(.{0,80})', q.group(1))
            if m and not prod:
                prod = m.group(1)
            ts = re.search(r'<timestamp>(.*?)</timestamp>', t)
            cur = {'q': q.group(1).strip()[:200], 'ts': ts.group(1) if ts else '', 'a': ''}
            turns.append(cur)
        elif o.get('role') == 'assistant' and cur is not None and len(t.strip()) > 150:
            cur['a'] = t.strip()
    print('#' * 20, i, '| продукт:', prod)
    for tr in turns[-N:]:
        print('\n>>>', tr['ts'], '|', tr['q'].replace('\n', ' '))
        print(tr['a'][:2800])
    print()
