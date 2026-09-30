import csv
from pathlib import Path

p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

lines = []
for r in rows:
    cat = r.get("Category") or ""
    if "поддержк" in cat.lower() or "поддержк" in (r.get("Title") or "").lower():
        lines.append(repr(r.get("Title")))
        lines.append("  SEO " + repr(r.get("SEO title")))
        lines.append("  DES " + repr(r.get("SEO descr")))
        lines.append("  PRICE " + repr(r.get("Price")))

Path(
    r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_seo-csv-support.txt"
).write_text("\n".join(lines), encoding="utf-8")
print(len(lines))
