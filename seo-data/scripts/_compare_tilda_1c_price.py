# -*- coding: utf-8 -*-
"""Compare Tilda catalog prices vs 1C recommended price by SKU. Read-only."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import xlrd

XLS = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\prices\price_1c.xls")
TILDA = Path(r"C:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
OUT = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\prices\_compare-tilda-vs-1c.txt")


def money(raw: str) -> float | None:
    raw = (raw or "").strip().replace(" ", "").replace("\xa0", "").replace(",", ".")
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def fmt(n: float) -> str:
    if n == int(n):
        return f"{int(n):,}".replace(",", " ")
    return f"{n:,.2f}".replace(",", " ")


def main() -> None:
    wb = xlrd.open_workbook(str(XLS))
    sh = wb.sheet_by_index(0)
    header_date = sh.cell_value(0, 8)
    headers = [str(sh.cell_value(1, c)).strip() for c in range(sh.ncols)]
    # col 0 code, col 4 recommended, col 3 currency
    price_by_sku: dict[str, list[tuple[str, float, str]]] = defaultdict(list)
    for r in range(2, sh.nrows):
        sku = str(sh.cell_value(r, 0)).strip()
        if not sku or not any(ch.isdigit() for ch in sku):
            continue
        # xlrd may give float for numeric codes
        if sku.endswith(".0") and sku.replace(".0", "").isdigit():
            sku = sku[:-2]
        if isinstance(sh.cell_value(r, 0), float):
            sku = str(int(sh.cell_value(r, 0)))
        name = str(sh.cell_value(r, 1)).strip()
        currency = str(sh.cell_value(r, 3)).strip()
        rec = sh.cell_value(r, 4)
        if rec in ("", None):
            continue
        try:
            rec_f = float(rec)
        except (TypeError, ValueError):
            continue
        if rec_f <= 0:
            continue
        price_by_sku[sku].append((name, rec_f, currency or "RUB?"))

    with TILDA.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))

    mismatch = []
    not_in_price = []
    no_sku = 0
    ok = 0
    currency_skip = []
    dup_price = []

    for r in rows:
        sku = (r.get("SKU") or "").strip()
        title = (r.get("Title") or "").strip()
        tilda_p = money(r.get("Price") or "")
        if not sku:
            no_sku += 1
            continue
        hits = price_by_sku.get(sku)
        if not hits:
            not_in_price.append((sku, tilda_p, title))
            continue
        currencies = {c for _, _, c in hits}
        recs = {p for _, p, _ in hits}
        if len(recs) > 1:
            dup_price.append((sku, recs, currencies, title))
        rec = next(iter(recs)) if len(recs) == 1 else sorted(recs)[-1]
        cur = next(iter(currencies))
        if cur.upper() not in ("", "RUB", "РУБ", "РУБ.", "RUR"):
            if tilda_p is None or abs(tilda_p - rec) > 0.51:
                currency_skip.append((sku, tilda_p, rec, cur, title))
                continue
        if tilda_p is None:
            mismatch.append((sku, None, rec, cur, title, hits[0][0]))
            continue
        if abs(tilda_p - rec) > 0.51:
            mismatch.append((sku, tilda_p, rec, cur, title, hits[0][0]))
        else:
            ok += 1

    lines = []
    lines.append(f"Прайс 1С: {XLS.name}")
    lines.append(f"Дата в шапке прайса: {header_date}")
    lines.append(f"Колонки: {headers}")
    lines.append(f"Уникальных артикулов в прайсе с рекомендованной ценой: {len(price_by_sku)}")
    lines.append(f"Строк Тильды: {len(rows)}")
    lines.append(f"Совпало по цене: {ok}")
    lines.append(f"Расхождение цены: {len(mismatch)}")
    lines.append(f"Артикул Тильды нет в прайсе 1С: {len(not_in_price)}")
    lines.append(f"Без артикула (варианты и т.п.): {no_sku}")
    lines.append(f"Не RUB / несравнимо напрямую: {len(currency_skip)}")
    lines.append(f"Один артикул, разные цены в прайсе: {len(dup_price)}")
    lines.append("")
    lines.append("=== ЦЕНА ТИЛЬДЫ != рекомендованная цена 1С ===")
    mismatch.sort(key=lambda x: abs((x[1] or 0) - x[2]), reverse=True)
    for sku, tp, rec, cur, title, pname in mismatch:
        delta = (tp - rec) if tp is not None else None
        dlt = f"{delta:+,.0f}".replace(",", " ") if delta is not None else "нет цены"
        tp_s = fmt(tp) if tp is not None else "-"
        lines.append(
            f"{sku}\tТильда {tp_s}\t1С {fmt(rec)} {cur}\tдельта {dlt}\t{title[:90]}"
        )
    lines.append("")
    lines.append("=== Артикул Тильды не найден в прайсе 1С ===")
    for sku, tp, title in not_in_price:
        tp_s = fmt(tp) if tp is not None else "-"
        lines.append(f"{sku}\tТильда {tp_s}\t{title[:90]}")
    lines.append("")
    lines.append("=== Валюта не RUB ===")
    for sku, tp, rec, cur, title in currency_skip:
        tp_s = fmt(tp) if tp is not None else "-"
        lines.append(f"{sku}\tТильда {tp_s}\t1С {fmt(rec)} {cur}\t{title[:90]}")
    lines.append("")
    lines.append("=== Дубли артикула с разными ценами в прайсе ===")
    for sku, recs, curs, title in dup_price:
        lines.append(f"{sku}\tцены {sorted(recs)}\t{curs}\t{title[:80]}")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT)
    print("ok", ok, "mismatch", len(mismatch), "missing", len(not_in_price))


if __name__ == "__main__":
    main()
