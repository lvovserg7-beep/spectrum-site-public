# -*- coding: utf-8 -*-
"""Карта <head> витрин: все куски nominify и вся разметка (JSON-LD, meta, link, script) с указанием, в каком куске она лежит."""
import re
from pathlib import Path

DIR = Path(__file__).parent / "_sc_pages_0930"

for f in sorted(DIR.glob("*.html")):
    page = f.read_text(encoding="utf-8")
    head = page[:page.find("</head>")]
    blocks = [(m.start(), head.find("<!-- nominify end -->", m.start())) for m in re.finditer(r"<!-- nominify begin -->", head)]
    print(f"\n=== {f.stem}: кусков nominify {len(blocks)}, длина head {len(head)}")
    for i, (b, e) in enumerate(blocks):
        part = head[b:e]
        kinds = re.findall(r'"@type":\s*"(\w+)"', part)
        tags = re.findall(r"<(meta|link|script|style|noscript)\b", part)
        print(f"  кусок {i + 1}: {b}-{e}, типы LD {kinds}, теги {sorted(set(tags))}")
    outside = head
    for b, e in reversed(blocks):
        outside = outside[:b] + outside[e:]
    print("  LD вне кусков:", re.findall(r'"@type":\s*"(\w+)"', outside))
    print("  meta name вне кусков:", sorted(set(re.findall(r'<meta name="([^"]+)"', outside))))
    print("  meta property вне кусков:", sorted(set(re.findall(r'<meta property="([^"]+)"', outside))))
    print("  itemprop/ld в body:", len(re.findall(r"application/ld\+json", page[len(head):])))
