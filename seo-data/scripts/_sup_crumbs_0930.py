import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
d = json.loads((Path(__file__).with_name("_sup_cards_live_0930.json")).read_text(encoding="utf-8"))
import time
for s in (sys.argv[1].split(",") if len(sys.argv) > 1 else d):
    time.sleep(4)
    h = urllib.request.urlopen(urllib.request.Request(f"https://alsn.ru/{s}?c=cr0930", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}), timeout=30).read().decode("utf-8")
    names = re.findall(r'"@type":\s*"ListItem".*?"name":\s*"([^"]+)"', h, re.S)
    crumbs = []
    for m in re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(131|123|758)"[^>]*>(.*?)</div>\s*(?=<div id="rec|<!--)', h, re.S):
        body = m.group(3)
        if "Главная" in body or "breadcrumb" in body.lower() or "⌂" in body or "<svg" in body:
            bg = re.search(r'background-color:\s*([^;"]+)', m.group(0)[:600])
            txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
            cols = sorted(set(re.findall(r"color:\s*(#[0-9a-fA-F]{3,6})", body)))
            crumbs.append((m.group(2), m.group(1), bg.group(1) if bg else "-", cols, txt[:90]))
    print(s, "| LD:", names)
    for c in crumbs:
        print("   ", c)
