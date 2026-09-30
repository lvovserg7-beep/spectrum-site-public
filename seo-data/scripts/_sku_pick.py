# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path

src = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
rows = list(csv.DictReader(src.open(encoding="utf-8-sig", newline=""), delimiter=";"))

want = [
    ("5 мест", r"клиентск.*5"),
    ("10 мест", r"клиентск.*10"),
    ("20 мест", r"клиентск.*20"),
    ("сервер", r"лицензия на сервер"),
    ("бух проф", r"бухгалтерия 8 проф"),
    ("бух корп", r"бухгалтерия 8 корп"),
    ("ут", r"управление торговлей"),
    ("erp", r"erp"),
    ("зуп", r"зарплата и управление персоналом 8"),
    ("ка", r"комплексная автоматизация"),
    ("унф", r"управление нашей фирмой"),
]

out = []
for label, pat in want:
    rx = re.compile(pat, re.I)
    hits = []
    for r in rows:
        title = r.get("Title") or ""
        sku = (r.get("SKU") or "").strip()
        if not sku or not sku[0].isdigit():
            continue
        if rx.search(title):
            hits.append((sku, title[:90], r.get("Price") or ""))
    out.append(f"=== {label} ({len(hits)})")
    for h in hits[:8]:
        out.append(f"{h[0]}\t{h[2]}\t{h[1]}")

Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_sku_pick.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("ok", len(out))
