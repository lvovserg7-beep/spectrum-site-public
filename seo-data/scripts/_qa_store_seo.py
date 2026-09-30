# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path

src = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
dst = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005-seo.csv")
out = Path(__file__).with_name("_qa_store_seo.txt")

KEEP = {
    "4601546117588",
    "4601546117595",
    "2900001833547",
    "2900001833585",
}

with src.open(encoding="utf-8-sig", newline="") as f:
    a = list(csv.DictReader(f, delimiter=";"))
with dst.open(encoding="utf-8-sig", newline="") as f:
    b = list(csv.DictReader(f, delimiter=";"))

lines = []
lines.append(f"rows {len(a)} -> {len(b)}")
lines.append(f"title max {max(len(r['SEO title']) for r in b)}")
lines.append(f"descr max {max(len(r['SEO descr']) for r in b)}")
lines.append(f"kw max {max(len(r['SEO keywords']) for r in b)}")

# leftover problems
flags = {
    "Алсан": [],
    "подар": [],
    "телеграм": [],
    "telegram": [],
    "артикул": [],
    "арт.": [],
    "внедрен": [],
    "ЗУП ЗУП": [],
    "Касса. Станд": [],
    "БизнесСт": [],
    "на рабочие места на": [],
}

for r in b:
    blob = f"{r['SEO title']} {r['SEO descr']} {r['SEO keywords']}"
    sku = r.get("SKU") or r.get("Tilda UID")
    for k in flags:
        if k.lower() in blob.lower():
            flags[k].append(f"{sku}\t{r['SEO title']}")

for k, v in flags.items():
    lines.append(f"flag {k}: {len(v)}")
    for x in v[:8]:
        lines.append(f"  {x}")

# titles ending with 1-2 letter stub
stub = []
for r in b:
    t = r["SEO title"]
    m = re.search(r"\s([А-Яа-яA-Za-z]{1,2})\s+\|\s+Аллсан$", t)
    if m:
        stub.append(t)
lines.append(f"short-stub titles {len(stub)}")
for x in stub[:20]:
    lines.append(f"  {x}")

# T1 keep
lines.append("--- T1 ---")
for sku in KEEP:
    old = next(r for r in a if r.get("SKU") == sku)
    new = next(r for r in b if r.get("SKU") == sku)
    same_t = old["SEO title"] == new["SEO title"]
    same_d = old["SEO descr"] == new["SEO descr"]
    lines.append(f"{sku} title_kept={same_t} descr_kept={same_d}")
    lines.append(f"  T {new['SEO title']}")
    lines.append(f"  D {new['SEO descr']}")
    lines.append(f"  K {new['SEO keywords']}")

# samples by category
lines.append("--- samples ---")
seen = set()
for r in b:
    cat = (r.get("Category") or "")[:40]
    if cat in seen:
        continue
    seen.add(cat)
    lines.append(f"[{cat}]")
    lines.append(f"  T {r['SEO title']} ({len(r['SEO title'])})")
    lines.append(f"  D {r['SEO descr']}")

# 300/500
lines.append("--- 300/500 ---")
for r in b:
    if "300" in (r.get("Title") or "") or "500" in (r.get("Title") or ""):
        if "клиентск" in (r.get("Title") or "").lower() or "серверн" in (r.get("Title") or "").lower():
            lines.append(r["SEO title"])

# empty old vs new
empty_old = sum(1 for r in a if not (r.get("SEO title") or "").strip())
lines.append(f"empty old titles {empty_old}")
lines.append(f"empty new titles {sum(1 for r in b if not r['SEO title'])}")

# FB
fb = [c for c in b[0] if "facebook" in c.lower() or c.lower().startswith("fb")]
lines.append(f"fb cols {fb}")
for c in fb:
    filled = sum(1 for r in b if (r.get(c) or "").strip())
    lines.append(f"  {c} filled {filled}")

out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
