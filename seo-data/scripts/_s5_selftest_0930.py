# -*- coding: utf-8 -*-
"""Самопроверка задачи С-5: каждый блок копирования читается, у витрины один путь, HEAD без JSON-LD."""
import html
import json
import re
from pathlib import Path

T = (Path(__file__).parents[1] / "tilda-briefs/tier2-breadcrumbs-struktura-2026-09-30.html").read_text(encoding="utf-8")
s5 = T[T.find('id="s1"'):T.find('id="s3"')]
print("длинных тире:", T.count("\u2014") + T.count("\u2013"))
for h3 in re.split(r"<h3>", s5)[1:]:
    title = h3[:h3.find("</h3>")]
    boxes = [html.unescape(b) for b in re.findall(r"<pre id=\"[^\"]+\">(.*?)</pre>", h3, re.S)]
    t123 = boxes[-1]
    head = boxes[0] if len(boxes) == 2 else ""
    crumbs, types = [], []
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t123, re.S):
        d = json.loads(m)
        types.append(d["@type"])
        if d["@type"] == "BreadcrumbList":
            crumbs = [i["name"] for i in d["itemListElement"]]
    vis = [re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r'<(?:a href="https://alsn\.ru/[^"]+"|span style="opacity:\.75)[^>]*>(.*?)</', t123)]
    ok = crumbs[1:] == vis and types.count("BreadcrumbList") == 1 and "ld+json" not in head
    print("OK " if ok else "ОШИБКА", title, "| HEAD:", head or "пусто", "| LD:", types, "| путь:", " / ".join(crumbs), "| экран:", " / ".join(vis))
