import csv
from pathlib import Path

p = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
with p.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

out = Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_seo-csv-more.txt")
lines = []

lines.append("=== EMPTY SEO ===")
for r in rows:
    if not (r.get("SEO title") or "").strip():
        lines.append(
            f"UID={r.get('Tilda UID')} parent={r.get('Parent UID')} SKU={r.get('SKU')!r} cat={r.get('Category')!r}"
        )
        lines.append(f"  Title={r.get('Title')!r}")
        lines.append(f"  Price={r.get('Price')!r}")

lines.append("\n=== MP / SUPPORT / FRESH sample ===")
for r in rows:
    cat = r.get("Category") or ""
    title = r.get("Title") or ""
    if any(
        x in cat or x.lower() in title.lower()
        for x in (
            "Модуль",
            "маркетплейс",
            "Техническая поддержка",
            "Фреш",
            "Fresh",
        )
    ):
        lines.append(
            f"SKU={r.get('SKU')} | {cat[:50]} | {title[:80]} | SEO={ (r.get('SEO title') or '')[:70]}"
        )

t1 = {
    "4601546117588",
    "4601546117595",
    "2900001833547",
    "2900001833585",
}
lines.append("\n=== T1 SKUs ===")
for r in rows:
    if (r.get("SKU") or "") in t1:
        lines.append(f"{r.get('SKU')} title={r.get('SEO title')!r}")
        lines.append(f"  descr={r.get('SEO descr')!r}")
        lines.append(f"  price={r.get('Price')!r} parent={r.get('Parent UID')!r}")

lines.append("\n=== PARENT UID groups ===")
from collections import defaultdict

g = defaultdict(list)
for r in rows:
    pid = (r.get("Parent UID") or "").strip()
    if pid:
        g[pid].append(r)
for pid, kids in list(g.items())[:20]:
    parent = next((x for x in rows if x.get("Tilda UID") == pid), None)
    lines.append(
        f"parent UID {pid} title={(parent or {}).get('Title', '?')[:70]} kids={len(kids)}"
    )
    for k in kids:
        lines.append(f"    SKU={k.get('SKU')} {k.get('Title')[:70]}")

# prices sample
lines.append("\n=== PRICE samples ===")
for r in rows[:8]:
    lines.append(repr(r.get("Price")))

# descr with подарк
n_gift = sum(1 for r in rows if "подар" in (r.get("SEO descr") or "").lower())
n_mix = sum(
    1
    for r in rows
    if "внедрен" in (r.get("SEO title") or "").lower()
    or "техподдерж" in (r.get("SEO title") or "").lower()
)
lines.append(f"\ndescr with подар: {n_gift}")
lines.append(f"title with внедрение/техподдержка: {n_mix}")

out.write_text("\n".join(lines), encoding="utf-8")
print("ok")
