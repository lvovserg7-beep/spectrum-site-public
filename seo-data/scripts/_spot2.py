import csv
from pathlib import Path
p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))
lines = []
for r in rows:
    if r.get("SKU") in {"ФрешКасса_СТ_12", "ФрешБС_Нул_12"}:
        lines.append(repr(r.get("SKU")))
        lines.append(repr(r.get("Title")))
        t = "Купить " + (r.get("Title") or "") + " | Аллсан"
        lines.append("len raw " + str(len(t)))
Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_spot2.txt").write_text("\n".join(lines), encoding="utf-8")
