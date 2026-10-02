"""Склеивает HEAD и блоки из инструкции tier4-ecom-v3 как на Тильде и снимает скриншоты."""
import html
import re
import subprocess
from pathlib import Path

import build_ecom_v3_brief as br

S = Path(br.p.SCR)
doc = open(br.OUT, encoding="utf-8").read()
pre = {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<pre id="(\w+)"[^>]*>(.*?)</pre>', doc, re.S)}
blocks = pre["e2a"] + pre["e3a"] + pre["e4a"]
for ph, local, _, _ in br.IMGS:
    blocks = blocks.replace(ph, local)
assert "ВСТАВЬТЕ" not in blocks
page = (f'<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'{pre["e1a"]}<style>body{{margin:0;font-family:Arial}}.t123{{}}</style></head><body>'
        f'<div style="background:#111;color:#fff;padding:20px">меню Тильды</div>'
        f'<div class="t123"><nav style="font-size:14px;color:#8a8a8a;padding:12px 20px 8px">⌂ / Интеграция с поставщиками</nav></div>'
        f'<div class="t-rec t123">{blocks}</div><div style="padding:40px;background:#eee">форма Тильды</div></body></html>')
out = S / "_ecom-tilda-selftest.html"
out.write_text(page, encoding="utf-8")
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for w, h, tag in ((1440, 5600, "desk"),):
    png = S / f"_ecom-selftest-{tag}.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000",
                    "--allow-file-access-from-files", f"--window-size={w},{h}", f"--screenshot={png}", out.as_uri()],
                   capture_output=True, timeout=120)
    print(png.name, png.exists())
