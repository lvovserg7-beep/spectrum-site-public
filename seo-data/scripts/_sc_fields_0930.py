# -*- coding: utf-8 -*-
"""Из сохранённых страниц витрин достать поле HEAD страницы и поле T123 крошек как они лежат в Тильде."""
import json
import re
from pathlib import Path

DIR = Path(__file__).parent / "_sc_pages_0930"
NB, NE = "<!-- nominify begin -->", "<!-- nominify end -->"


def fields(page):
    head = page[:page.find("</head>")]
    pages_hc = 'data-tilda-page-headcode="yes"' in page
    b = head.rfind(NB)
    e = head.rfind(NE)
    page_head = head[b + len(NB):e] if pages_hc and b != -1 and e > b else None
    m = re.search(r'<div id="rec(\d+)"[^>]*data-record-type="131"[^>]*>(?:(?!<div id="rec).)*?aria-label="Хлебные крошки"', page, re.S)
    rec, t123 = None, None
    if m:
        rec = m.group(1)
        s = page.find(NB, m.start()) + len(NB)
        t123 = page[s:page.find(NE, s)]
    return {"page_head": page_head, "rec": rec, "t123": t123}


if __name__ == "__main__":
    out = {}
    for f in sorted(DIR.glob("*.html")):
        r = fields(f.read_text(encoding="utf-8"))
        out[f.stem] = r
        ph = r["page_head"] or ""
        print(f.stem, "rec", r["rec"], "| head", len(ph), "LD:", ph.count("ld+json"), "script:", ph.count("<script"),
              "| t123", len(r["t123"] or ""), "LD:", (r["t123"] or "").count("ld+json"))
    json.dump(out, open(DIR / "_fields.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
