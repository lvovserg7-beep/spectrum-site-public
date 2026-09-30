import csv
from collections import Counter
from pathlib import Path

p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    rows = list(reader)
    fields = reader.fieldnames

out = Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_seo-csv-preview.txt")
lines = []
lines.append("FIELDS:\n" + "\n".join(fields or []))
lines.append(f"\nROWS: {len(rows)}")
seo_t = [r.get("SEO title", "") or "" for r in rows]
seo_d = [r.get("SEO descr", "") or "" for r in rows]
seo_k = [r.get("SEO keywords", "") or "" for r in rows]
lines.append(f"empty SEO title: {sum(1 for x in seo_t if not x.strip())}")
lines.append(f"empty SEO descr: {sum(1 for x in seo_d if not x.strip())}")
lines.append(f"empty SEO keywords: {sum(1 for x in seo_k if not x.strip())}")
lines.append(f"filled FB title: {sum(1 for r in rows if (r.get('FB title') or '').strip())}")
parents = sum(1 for r in rows if not (r.get("Parent UID") or "").strip())
children = sum(1 for r in rows if (r.get("Parent UID") or "").strip())
lines.append(f"parents/standalone: {parents} variants: {children}")
cats = Counter((r.get("Category") or "").strip() or "(no cat)" for r in rows)
lines.append("\nTOP CATS:")
for c, n in cats.most_common(25):
    lines.append(f"  {n:4d}  {c}")

# samples of filled SEO
filled = [r for r in rows if (r.get("SEO title") or "").strip()]
lines.append(f"\nFILLED SEO TITLE samples ({len(filled)}):")
for r in filled[:40]:
    lines.append(
        f"- SKU={r.get('SKU')} parent={r.get('Parent UID')} | {r.get('SEO title')!r}"
    )
    d = (r.get("SEO descr") or "")[:160]
    if d:
        lines.append(f"  descr: {d}")

# brand issues
bad_brand = []
for r in rows:
    blob = " ".join(
        [
            r.get("SEO title") or "",
            r.get("SEO descr") or "",
            r.get("SEO keywords") or "",
            r.get("Title") or "",
        ]
    )
    if "Алсан" in blob and "Аллсан" not in blob.replace("Аллсан", ""):
        # has Алсан as standalone typo in SEO?
        pass
    if "Алсан" in (r.get("SEO title") or "") or "Алсан" in (r.get("SEO descr") or ""):
        bad_brand.append(r.get("SKU") or r.get("Title"))

lines.append(f"\nSEO with Алсан (typo): {len(bad_brand)}")
lines.append(repr(bad_brand[:20]))

# title lengths of filled
lens = [len(x) for x in seo_t if x.strip()]
if lens:
    lines.append(f"\nSEO title len min/med/max: {min(lens)} / {sorted(lens)[len(lens)//2]} / {max(lens)}")

out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out, "rows", len(rows))
