# -*- coding: utf-8 -*-
import re, urllib.request, json
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
OUT = Path(__file__).resolve().parent / "_case-pages-extra-2026-09-23.txt"

def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")

lines = []
for path in ["/caseecomsc", "/xitsadmarketplace"]:
    html = fetch("https://alsn.ru" + path)
    lines.append(f"\n==== {path} ====")
    # context around Все кейсы
    for m in re.finditer("Все кейсы", html):
        start = max(0, m.start() - 80)
        end = min(len(html), m.end() + 120)
        chunk = re.sub(r"\s+", " ", html[start:end])
        lines.append(f"  Все кейсы ctx: ...{chunk}...")
    # Article blocks
    for i, m in enumerate(re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, re.I | re.S)):
        body = m.group(1).strip()
        try:
            data = json.loads(body)
        except Exception as e:
            lines.append(f"  LD#{i} FAIL {e}")
            continue
        types = []
        def walk(o):
            if isinstance(o, dict):
                t = o.get("@type")
                if t:
                    types.append(t if isinstance(t, str) else str(t))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(data)
        lines.append(f"  LD#{i} types={types}")
        if "Article" in types or (isinstance(data, dict) and data.get("@type") == "Article"):
            art = data if isinstance(data, dict) and data.get("@type") == "Article" else None
            if art is None and isinstance(data, dict) and "@graph" in data:
                for n in data["@graph"]:
                    if isinstance(n, dict) and n.get("@type") == "Article":
                        art = n
            if art:
                lines.append(f"    Article headline={art.get('headline','')[:100]}")
                lines.append(f"    Article url={art.get('url','')}")
                lines.append(f"    Article desc={str(art.get('description',''))[:120]}")
        if "BreadcrumbList" in types:
            # extract itemListElement names only
            def bc_names(o, acc=None):
                acc = acc or []
                if isinstance(o, dict):
                    if o.get("@type") == "ListItem" and "name" in o:
                        acc.append(o["name"])
                    for v in o.values():
                        bc_names(v, acc)
                elif isinstance(o, list):
                    for v in o:
                        bc_names(v, acc)
                return acc
            lines.append(f"    BC items={bc_names(data)}")

OUT.write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT)
