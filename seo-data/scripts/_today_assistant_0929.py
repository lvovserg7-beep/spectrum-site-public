import json, re, os, sys
B = r'C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-transcripts'
JOBS = [('e63ab8cf-bc45-4540-b655-6d63703ae8b9', 'Sep 28, 2026, 5:'), ('51afc82f-f2e2-4e52-899a-5e19fff5d41d', 'Sep 29, 2026')]


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


for i, mark in JOBS:
    print('#' * 30, i)
    on = False
    for ln in open(os.path.join(B, i, i + '.jsonl'), encoding='utf-8'):
        o = json.loads(ln)
        role = o.get('role')
        t = '\n'.join(texts(o.get('message', o)))
        if role == 'user' and mark in t:
            on = True
            q = re.search(r'<user_query>(.*?)</user_query>', t, re.S)
            print('\n>>> USER:', (q.group(1) if q else '')[:200].strip())
        elif on and role == 'assistant' and len(t.strip()) > 200:
            print('\n<<< ASSISTANT:\n', t.strip()[:3500])
