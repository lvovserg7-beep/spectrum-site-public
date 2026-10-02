# -*- coding: utf-8 -*-
"""Сохранить страницы восьми витрин с живого alsn.ru для разбора HEAD и блока крошек."""
import random
import time
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
SC = ["upt8", "buhv8", "zup8", "upravlenie_nashei_firmoi", "products", "its", "1cfresh", "dokumentooborot8"]
OUT = Path(__file__).parent / "_sc_pages_0930"
OUT.mkdir(exist_ok=True)

for s in SC:
    for _ in range(5):
        try:
            req = urllib.request.Request(f"https://alsn.ru/{s}?v={random.randint(1, 10**6)}", headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                (OUT / f"{s}.html").write_text(r.read().decode("utf-8", "replace"), encoding="utf-8")
            print(s, "ok")
            break
        except Exception as e:
            print(s, e)
            time.sleep(4)
    time.sleep(2)
