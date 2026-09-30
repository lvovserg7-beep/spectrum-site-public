import csv
from pathlib import Path

src = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
dst = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005-seo.csv")
with src.open(encoding="utf-8-sig", newline="") as f:
    a = list(csv.DictReader(f, delimiter=";"))
with dst.open(encoding="utf-8-sig", newline="") as f:
    b = list(csv.DictReader(f, delimiter=";"))

assert len(a) == len(b) == 332
seo_cols = {"SEO title", "SEO descr", "SEO keywords"}
diff_other = 0
for x, y in zip(a, b):
    assert x["Tilda UID"] == y["Tilda UID"]
    for k in x:
        if k in seo_cols:
            continue
        if (x.get(k) or "") != (y.get(k) or ""):
            diff_other += 1
            print("OTHER DIFF", k, x.get("SKU"))
print("other-col diffs", diff_other)
print("t1 5", [r["SEO title"] for r in b if r.get("SKU") == "4601546117588"][0])
print("kw empty", sum(1 for r in b if not (r.get("SEO keywords") or "").strip()))
# leftover ugly
ugly = []
for r in b:
    t = r["SEO title"]
    if t.endswith("Ст | Аллсан") or "ЗУП ЗУП" in t or t.endswith("к | Аллсан"):
        ugly.append(t)
print("ugly", ugly[:15], "n", len(ugly))
# count changed titles
ch = sum(1 for x, y in zip(a, b) if x.get("SEO title") != y.get("SEO title"))
print("title changed", ch)
print("descr changed", sum(1 for x, y in zip(a, b) if x.get("SEO descr") != y.get("SEO descr")))
