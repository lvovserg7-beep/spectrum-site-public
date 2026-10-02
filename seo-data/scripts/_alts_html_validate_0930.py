# -*- coding: utf-8 -*-
"""Проверка разметки двух инструкций по alt после чистки."""
import re
from html.parser import HTMLParser
from pathlib import Path

VOID = {"meta", "br", "img", "input", "link", "hr"}
DIR = Path(__file__).resolve().parent.parent / "tilda-briefs"


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.st, self.err = [], []

    def handle_starttag(self, t, a):
        if t not in VOID:
            self.st.append(t)

    def handle_endtag(self, t):
        if t in VOID:
            return
        if self.st and self.st[-1] == t:
            self.st.pop()
        else:
            self.err.append((t, self.getpos(), self.st[-3:]))


for f in ["tier2-alts-sitewide-2026-09-21.html", "tier2-alts-tail-2026-09-28.html"]:
    s = (DIR / f).read_text(encoding="utf-8")
    p = P()
    p.feed(s)
    ids = re.findall(r'<pre id="([^"]+)"', s)
    btn = re.findall(r'data-copy="([^"]+)"', s)
    print(f, "errors", p.err[:5], "unclosed", p.st, "pre", len(ids), "btn", len(btn),
          "dupe", len(ids) - len(set(ids)), "missing", set(btn) - set(ids),
          "dash", s.count("\u2014") + s.count("\u2013"))
