# -*- coding: utf-8 -*-
import csv
from pathlib import Path

src = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
dst = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005-seo.csv")
skus = [
    "КПБаз1ЛЦ",
    "КППроф8_4ЛЦ",
    "ФрешБС_УСНиП_ОТЧ_12",
]
want = [
    "Энергетика",
    "Распознавание",
    "Колледж",
]
with src.open(encoding="utf-8-sig", newline="") as f:
    a = { (r.get("SKU") or r.get("Tilda UID")): r for r in csv.DictReader(f, delimiter=";") }
with dst.open(encoding="utf-8-sig", newline="") as f:
    b = list(csv.DictReader(f, delimiter=";"))

out = []
for sku in skus:
    r = a.get(sku)
    n = next(x for x in b if (x.get("SKU") or "") == sku)
    out.append("=== " + sku)
    out.append("Title: " + (r.get("Title") or ""))
    out.append("SEOold T: " + (r.get("SEO title") or ""))
    out.append("SEOnew T: " + n["SEO title"])
    out.append("SEOnew D: " + n["SEO descr"])
    out.append("SEOnew K: " + n["SEO keywords"])

for r in b:
    if any(w in (r.get("SEO title") or "") for w in want):
        old = a.get(r.get("SKU") or "", {})
        out.append("=== " + (r.get("SKU") or ""))
        out.append("Title: " + (old.get("Title") or r.get("Title") or ""))
        out.append("T: " + r["SEO title"])
        out.append("D: " + r["SEO descr"])

Path(__file__).with_name("_qa_store_seo2.txt").write_text("\n".join(out), encoding="utf-8")
print("ok")
