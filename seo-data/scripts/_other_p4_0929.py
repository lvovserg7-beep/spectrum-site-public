# -*- coding: utf-8 -*-
import _control_slice_2026_09_24 as base

for fname, label in (
    ("b8f739e9-9dcc-4c62-8b65-722dbbbd53de.txt", "p3"),
    ("e45f2afe-3304-415a-b54c-45de3405fb15.txt", "p4"),
):
    rows = base.load_queries(fname)
    tot = sum(r["clicks"] for r in rows), sum(r["shows"] for r in rows)
    print(label, "rows", len(rows), "clicks/shows in top", tot)
    clicked = sorted([r for r in rows if r["clicks"]], key=lambda r: -r["clicks"])
    for r in clicked:
        print("  ", base.classify(r["q"]), r["q"], r["shows"], r["clicks"], round(r["pos"], 1))
