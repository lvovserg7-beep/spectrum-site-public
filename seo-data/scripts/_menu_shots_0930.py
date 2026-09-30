# -*- coding: utf-8 -*-
"""Скриншоты макетов меню (headless Chrome) для проверки."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "seo-data/competitors/screens"
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def shot(name, w, h, frag):
    url = (SCREENS / f"preview-menu-v3-{name[0]}.html").as_uri() + frag
    out = SCREENS / f"_menu-{name}.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    f"--window-size={w},{h}", f"--screenshot={out}", url], capture_output=True, timeout=120)
    print(out, out.exists())


def mobile(name):
    frame = SCREENS / f"_menu-frame-{name}.html"
    src = (SCREENS / f"preview-menu-v3-{name[0]}.html").as_uri() + "#mobile"
    frame.write_text(f'<html><body style="margin:0;background:#ccc"><iframe src="{src}" '
                     f'style="width:390px;height:844px;border:0;background:#fff"></iframe></body></html>', encoding="utf-8")
    out = SCREENS / f"_menu-{name}.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    "--allow-file-access-from-files", "--window-size=600,844", f"--screenshot={out}", frame.as_uri()],
                   capture_output=True, timeout=120)
    frame.unlink()
    print(out, out.exists())


shot("a-products", 1440, 760, "#open=1")
shot("a-services", 1440, 760, "#open=0")
shot("b-services", 1440, 760, "#open=0&row=0")
mobile("a-mobile")
mobile("b-mobile")
