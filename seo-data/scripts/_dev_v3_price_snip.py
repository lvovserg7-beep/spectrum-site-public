# -*- coding: utf-8 -*-
from pathlib import Path
h = Path(__file__).with_name("_dev_v3_live_check_0930.html").read_text(encoding="utf-8")
keys = [
    "Типичный проект - 1,2-2,0",
    "Сколько займёт и из чего цена?",
    "Сколько стоит внедрение?",
    "стоимость проекта считаем по ТЗ",
]
out = []
for k in keys:
    i = h.find(k)
    out.append(f"=== {k} idx={i} ===")
    out.append(h[max(0, i - 80): i + 280] if i >= 0 else "NO")
    out.append("")
Path(__file__).with_name("_dev_v3_price_snip.txt").write_text("\n".join(out), encoding="utf-8")
print("ok")
