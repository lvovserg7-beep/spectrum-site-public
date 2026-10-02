# -*- coding: utf-8 -*-
"""Скриншоты макетов карточек поставщиков v3 + проверка горизонтальной прокрутки на 390 px."""
import subprocess
import sys
from pathlib import Path

SCREENS = Path(__file__).resolve().parents[1] / "competitors" / "screens"
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARGS = [CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000", "--allow-file-access-from-files"]

slugs = sys.argv[1].split(",")
for slug in slugs:
    page = SCREENS / f"preview-sup-{slug}-v3.html"
    for w, h in ((1440, 900), (1100, 800)):
        out = SCREENS / f"_sup-{slug}-{w}.png"
        subprocess.run(ARGS + [f"--window-size={w},{h}", f"--screenshot={out}", page.as_uri()], capture_output=True, timeout=120)
        print(out.name, out.exists())
    frame = SCREENS / f"_sup-frame-{slug}.html"
    frame.write_text(f'<html><body style="margin:0;background:#ccc"><iframe src="{page.as_uri()}" '
                     f'style="width:390px;height:1400px;border:0;background:#fff"></iframe></body></html>', encoding="utf-8")
    out = SCREENS / f"_sup-{slug}-mob.png"
    subprocess.run(ARGS + ["--window-size=420,1400", f"--screenshot={out}", frame.as_uri()], capture_output=True, timeout=120)
    frame.unlink()
    print(out.name, out.exists())
