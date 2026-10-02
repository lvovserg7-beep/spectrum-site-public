# -*- coding: utf-8 -*-
import html
import re
from pathlib import Path

h = Path(__file__).with_name("_dev_v3_live_check_0930.html").read_text(encoding="utf-8")
m = re.search(r'id="rec4363614001".*?(?=<div id="rec")', h, re.S)
c = m.group(0) if m else ""
who = re.search(r'class="who">(.*?)</div>', c, re.S)
alt = re.search(r'alt="([^"]+)"', c)
who_txt = html.unescape(re.sub(r"<[^>]+>", "", who.group(1))) if who else "NO"
print("WHO", who_txt)
print("ALT", alt.group(1) if alt else "NO")
print("мазницына", h.count("Мазницына"), "мазницина", h.count("Мазницина"))
print("sofia in B1", "Софья" in c)
print("sofia in B2", "Софья" in (re.search(r'id="rec4363615101".*?(?=<div id="rec")', h, re.S) or type("x", (), {"group": lambda *a: ""})()).group(0))
