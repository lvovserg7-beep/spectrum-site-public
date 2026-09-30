import json, re, glob, os
from collections import Counter
B = r'C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-transcripts'
IDS = ['51afc82f-f2e2-4e52-899a-5e19fff5d41d', '9839cc4a-86e3-4fb0-859a-26cd974f014a',
       'agent-4a9b9c13-6c20-4128-b6b9-4eb94cc3037c', 'cf5fdc38-f68f-4023-9a8f-62fdb1d8c845',
       'e63ab8cf-bc45-4540-b655-6d63703ae8b9']


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


for i in IDS:
    p = os.path.join(B, i, i + '.jsonl')
    print('=' * 20, i)
    urls = Counter()
    for ln in open(p, encoding='utf-8'):
        try:
            o = json.loads(ln)
        except Exception:
            continue
        role = o.get('role') or o.get('type')
        t = '\n'.join(texts(o.get('message', o)))
        for u in re.findall(r'https?://alsn\.ru/[A-Za-z0-9_\-/]*', t):
            urls[u.rstrip('/')] += 1
        if role == 'user':
            q = re.search(r'<user_query>(.*?)</user_query>', t, re.S)
            q = (q.group(1) if q else t).strip()
            ts = re.search(r'<timestamp>(.*?)</timestamp>', t)
            print('USER', ts.group(1) if ts else '', '|', q[:260].replace('\n', ' '))
    print('URLS', urls.most_common(40))
