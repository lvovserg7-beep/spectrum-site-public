# -*- coding: utf-8 -*-
"""Скриншоты макетов страниц поставщиков (headless Chrome) для проверки."""
import subprocess
import sys
from pathlib import Path

SCREENS = Path(__file__).resolve().parents[1] / "competitors" / "screens"
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARGS = [CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000", "--allow-file-access-from-files"]


def shot(page, tag, w, h):
    out = SCREENS / f"_ecom-{tag}.png"
    subprocess.run(ARGS + [f"--window-size={w},{h}", f"--screenshot={out}", (SCREENS / page).as_uri()], capture_output=True, timeout=120)
    print(out.name, out.exists())


def mobile(page, tag, h=3000, anchor=""):
    frame = SCREENS / f"_ecom-frame-{tag}.html"
    frame.write_text(f'<html><body style="margin:0;background:#ccc"><iframe src="{(SCREENS / page).as_uri()}{anchor}" '
                     f'style="width:390px;height:{h}px;border:0;background:#fff"></iframe></body></html>', encoding="utf-8")
    out = SCREENS / f"_ecom-{tag}.png"
    subprocess.run(ARGS + [f"--window-size=420,{h}", f"--screenshot={out}", frame.as_uri()], capture_output=True, timeout=120)
    frame.unlink()
    print(out.name, out.exists())


w = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
shot("preview-ecom-v3.html", "hub-desk", w, 6200)
shot("preview-ecom-card-merlion-v3.html", "card-desk", w, 4600)
mobile("preview-ecom-v3.html", "hub-mob")
mobile("preview-ecom-card-merlion-v3.html", "card-mob")
mobile("preview-ecom-v3.html", "hub-mob-reports", 2400, "#reports")
