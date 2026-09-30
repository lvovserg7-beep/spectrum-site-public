import re, pathlib, collections
C = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_cleanup_mp_cache")
import sys
t = (C / f"{sys.argv[1] if len(sys.argv) > 1 else 'xitsad'}.html").read_text(encoding="utf-8", errors="replace")
recs = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r'<div id="(rec\d+)"[^>]*data-record-type="(\d+)"', t)]
def rec_of(pos):
    r = None
    for s, rid, typ in recs:
        if s <= pos:
            r = (rid, typ)
    return r
cnt = collections.Counter()
alts = collections.Counter()
for m in re.finditer(r'<img[^>]*>', t):
    tag = m.group(0)
    a = re.search(r'alt="([^"]*)"', tag)
    r = rec_of(m.start())
    if a is not None and a.group(1) == "":
        cnt[r] += 1
    elif a:
        alts[(r, a.group(1)[:40])] += 1
print("EMPTY:", cnt)
for k, v in list(alts.items())[:40]:
    print(k, v)
