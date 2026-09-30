# -*- coding: utf-8 -*-
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"
PAGES = ["/", "/development1c", "/casemarketplace", "/its", "/bitrix24", "/whatsapp", "/internship", "/persons", "/amo_crm", "/vacancy", "/telegram1c"]


def fetch(p):
    req = urllib.request.Request("https://alsn.ru" + ("" if p == "/" else p) + "?r=2809", headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


for p in PAGES:
    h = fetch(p)
    footer_at = h.find('id="t-footer"')
    recs = {}
    for m in re.finditer(r"<img\b[^>]*>", h, re.I):
        tag = m.group(0)
        src = re.search(r"""(?:data-original|src)=["']([^"']+)["']""", tag)
        if not src or re.search(r"(?i)\.svg|/resize/20x/|mc\.yandex|/empty/", src.group(1)):
            continue
        alt = re.search(r"""\balt=(["'])(.*?)\1""", tag, re.S)
        if alt and alt.group(2).strip():
            continue
        before = h[: m.start()]
        rid = re.findall(r'id="rec(\d+)"', before)
        rid = rid[-1] if rid else "?"
        typ = re.findall(r'data-record-type="(\d+)"', before)
        where = "FOOTER" if 0 <= footer_at < m.start() else "page"
        recs.setdefault((rid, typ[-1] if typ else "?", where), []).append(src.group(1).rsplit("/", 1)[-1])
    print("==", p)
    for (rid, typ, where), files in recs.items():
        pos = h.find(f'id="rec{rid}"')
        chunk = h[pos: pos + 60000]
        heads = [text(x) for x in re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", chunk, re.S)[:1]]
        tn = [text(x) for x in re.findall(r"""class=['"]tn-atom['"][^>]*>(.*?)</div>""", chunk, re.S)[:3]]
        print(f"  rec{rid} T{typ} {where} n={len(files)} head={heads} tn={[t[:50] for t in tn if t]} files={sorted(set(files))[:6]}")
