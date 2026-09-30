import csv
from pathlib import Path

p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

keys = [k for k in rows[0] if k.startswith("Characteristics")]
lines = ["CHARS: " + repr(keys)]
for r in rows[:12]:
    lines.append("---")
    lines.append(r.get("Title", "")[:90])
    for k in keys:
        v = (r.get(k) or "").strip()
        if v:
            lines.append(f"  {k}={v}")
    lines.append(f"  cat={r.get('Category')}")

# unique char values
from collections import Counter
for k in keys:
    c = Counter((r.get(k) or "").strip() for r in rows)
    lines.append(f"\n{k}: {c.most_common(12)}")

Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_seo-csv-chars.txt").write_text(
    "\n".join(lines), encoding="utf-8"
)
print("ok")
