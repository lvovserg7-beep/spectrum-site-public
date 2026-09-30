import csv
from pathlib import Path
p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))
lines = []
for r in rows:
    blob = (r.get("Title") or "") + (r.get("SKU") or "")
    if "8+4" in blob or "КП8" in (r.get("SKU") or "") or "подар" in (r.get("Title") or "").lower():
        lines.append(repr(r.get("SKU")))
        lines.append(repr(r.get("Title")))
        lines.append("---")
Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_find_kp.txt").write_text(
    "\n".join(lines), encoding="utf-8"
)
