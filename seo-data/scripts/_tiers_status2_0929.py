import json, re, os
B = r'C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-transcripts'
JOBS = [('0aa1355f-3bcd-4a0d-9ea6-3b0d1e62f682', r'[Тт]ир\s?[1-4]|T[1-4]-|Т[1-4]-|осталось|не сделано|хвост', 7),
        ('2c6917f1-e100-489b-ab07-45a1ab55e50a', r'крошк|[Aa]lt|альт|подпис[иь] к картин', 5)]


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


for i, pat, n in JOBS:
    turns, cur = [], None
    for ln in open(os.path.join(B, i, i + '.jsonl'), encoding='utf-8'):
        o = json.loads(ln)
        t = '\n'.join(texts(o.get('message', o)))
        if o.get('role') == 'user':
            q = re.search(r'<user_query>(.*?)</user_query>', t, re.S)
            if q:
                ts = re.search(r'<timestamp>(.*?)</timestamp>', t)
                cur = {'q': q.group(1).strip()[:160], 'ts': ts.group(1) if ts else '', 'a': ''}
                turns.append(cur)
        elif o.get('role') == 'assistant' and cur is not None and len(t.strip()) > 150:
            cur['a'] = t.strip()
    hits = [tr for tr in turns if re.search(pat, tr['a']) and '<summary>' not in tr['a']]
    print('#' * 20, i)
    for tr in hits[-n:]:
        print('\n>>>', tr['ts'], '|', tr['q'].replace('\n', ' '))
        print(tr['a'][:2200])
