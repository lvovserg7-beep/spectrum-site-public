import json, re, os
B = r'C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-transcripts'
i = '2c6917f1-e100-489b-ab07-45a1ab55e50a'


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
for tr in turns:
    if re.search(r'Sep (2[2-8]), 2026', tr['ts']):
        print('\n>>>', tr['ts'], '|', tr['q'].replace('\n', ' '))
        print(tr['a'][:1500])
