import csv
from pathlib import Path
p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005-seo.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))
lines = []
for r in rows:
    t = r["SEO title"]
    if r.get("SKU") in {"ФрешКасса_СТ_12", "ФрешБС_Нул_12", "4601546117588", "2900002156850"}:
        lines.append(f"{r.get('SKU')}\n  T {t} ({len(t)})\n  D {r['SEO descr']}\n  K {r['SEO keywords']}")
Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_spot.txt").write_text("\n".join(lines), encoding="utf-8")
