# -*- coding: utf-8 -*-
import html
import json
import re
from pathlib import Path

h = Path(__file__).with_name("_dev_v3_live_check_0930.html").read_text(encoding="utf-8")
# только блок паспорта
m = re.search(r'id="rec4363615101".*?(?=<div id="rec)', h, re.S)
chunk = m.group(0) if m else h
pairs = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", chunk, re.S)
pairs = [
    (
        html.unescape(re.sub(r"<[^>]+>", "", q)).strip(),
        html.unescape(re.sub(r"<[^>]+>", "", a)).strip(),
    )
    for q, a in pairs
]
head = h[: h.index("</head>")]
faq = None
for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
    d = json.loads(mm.group(1))
    if d.get("@type") == "FAQPage":
        faq = [(x["name"], x["acceptedAnswer"]["text"]) for x in d["mainEntity"]]
out = [f"vis {len(pairs)} ld {len(faq or [])}"]
okn = 0
for i, (q, a) in enumerate(faq or []):
    vq, va = pairs[i] if i < len(pairs) else ("", "")
    st = "OK" if (q == vq and a == va) else "FAIL"
    if st == "OK":
        okn += 1
    out.append(f"{st} {q}")
    if st == "FAIL":
        out.append(f"  q vis={vq!r}")
        if a != va:
            out.append(f"  a ld ={a!r}")
            out.append(f"  a vis={va!r}")
out.append(f"MATCH {okn}/{len(faq or [])}")
# scroll: look overflow
out.append("emdash body " + str("\u2014" in chunk or "\u2013" in chunk))
out.append("sofia in body block " + str("Софья" in chunk))
Path(__file__).with_name("_dev_v3_faq_0930.txt").write_text("\n".join(out), encoding="utf-8")
print("ok", okn)
