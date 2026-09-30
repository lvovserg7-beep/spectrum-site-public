# -*- coding: utf-8 -*-
import html
import json
from pathlib import Path

p = Path(__file__).with_name("_qa_alts_live.json")
d = json.loads(p.read_text(encoding="utf-8"))
lines = []

false_m = []
real_m = []
for r in d["results"]:
    if r["status"] != "mismatch":
        continue
    live = html.unescape(r.get("live") or "")
    exp = r.get("expected") or ""
    if live == exp:
        false_m.append(r)
        r["status"] = "ok_unescaped"
    else:
        real_m.append(r)

empty = [r for r in d["results"] if r["status"] == "empty"]
ok = sum(1 for r in d["results"] if r["status"] in ("ok", "ok_other", "ok_unescaped"))

lines.append("Проверка живых alt, 16.09.2026")
lines.append(f"Всего карточек: {d['total']}")
lines.append(f"Совпало: {ok}")
lines.append(f"Пустой alt: {len(empty)}")
lines.append(f"Расхождение текста: {len(real_m)}")
lines.append(f"Кавычки HTML (&quot;), по сути ок: {len(false_m)}")
lines.append("")
lines.append("=== ПУСТОЙ ALT ===")
for r in empty:
    sku = r.get("sku") or "без артикула"
    lines.append(f"{sku}\t{r.get('title')}\t{r.get('url')}")
lines.append("")
lines.append("=== ТЕКСТ НЕ ТОТ ===")
for r in real_m:
    sku = r.get("sku") or "без артикула"
    variant = "вариант" if r.get("parent") else "родитель/обычный"
    lines.append(f"SKU {sku} ({variant})")
    lines.append(f"  товар: {r.get('title')}")
    lines.append(f"  ждали: {r.get('expected')}")
    lines.append(f"  сейчас: {html.unescape(r.get('live') or '')}")
    lines.append("")

out = Path(__file__).with_name("_qa_alts_report.txt")
out.write_text("\n".join(lines), encoding="utf-8")
print("ok", ok, "empty", len(empty), "mismatch", len(real_m), "quot", len(false_m))
print("wrote", out)
