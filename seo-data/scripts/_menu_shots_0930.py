# -*- coding: utf-8 -*-
"""Скриншоты макетов меню (headless Chrome) для проверки."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "seo-data/competitors/screens"
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def page(name):
    return SCREENS / ("preview-menu-t123-live.html" if name.startswith("live") else f"preview-menu-v3-{name[0]}.html")


def shot(name, w, h, frag):
    url = page(name).as_uri() + frag
    out = SCREENS / f"_menu-{name}.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    f"--window-size={w},{h}", f"--screenshot={out}", url], capture_output=True, timeout=120)
    print(out, out.exists())


def mobile(name):
    frame = SCREENS / f"_menu-frame-{name}.html"
    src = page(name).as_uri() + "#mobile"
    frame.write_text(f'<html><body style="margin:0;background:#ccc"><iframe src="{src}" '
                     f'style="width:390px;height:844px;border:0;background:#fff"></iframe></body></html>', encoding="utf-8")
    out = SCREENS / f"_menu-{name}.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    "--allow-file-access-from-files", "--window-size=600,844", f"--screenshot={out}", frame.as_uri()],
                   capture_output=True, timeout=120)
    frame.unlink()
    print(out, out.exists())


shot("live-services", 1440, 700, "#open=0")
shot("live-products", 1440, 700, "#open=1")
shot("live-licenses", 1440, 700, "#open=2")
shot("live-about", 1440, 500, "#open=4")
mobile("live-mobile")
