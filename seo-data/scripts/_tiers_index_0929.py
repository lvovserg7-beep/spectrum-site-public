import json, re, os, glob
B = r'C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-transcripts'


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


for d in sorted(glob.glob(os.path.join(B, '*')), key=os.path.getmtime):
    i = os.path.basename(d)
    p = os.path.join(d, i + '.jsonl')
    if not os.path.exists(p):
        continue
    users, first_ts, last_ts, tiers = [], None, None, 0
    for ln in open(p, encoding='utf-8'):
        try:
            o = json.loads(ln)
        except Exception:
            continue
        if o.get('role') != 'user':
            continue
        t = '\n'.join(texts(o.get('message', o)))
        q = re.search(r'<user_query>(.*?)</user_query>', t, re.S)
        ts = re.search(r'<timestamp>(.*?)</timestamp>', t)
        if q:
            qq = q.group(1).strip()
            users.append(qq)
            if ts:
                first_ts = first_ts or ts.group(1)
                last_ts = ts.group(1)
            if re.search(r'\b[тtТT]\s?-?[1-5]\b|тир|tier', qq, re.I):
                tiers += 1
    if not users:
        continue
    print('%s | %d сообщ | тиры:%d | %s .. %s\n   1: %s\n   last: %s' % (i, len(users), tiers, first_ts, last_ts,
          users[0][:150].replace('\n', ' '), users[-1][:150].replace('\n', ' ')))
