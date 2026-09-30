# -*- coding: utf-8 -*-
"""Control slice 29.09.2026: Yandex clusters p0..p4 + control phrases."""
from __future__ import annotations

import json
from pathlib import Path

import _control_slice_2026_09_24 as base

OUT = Path(__file__).resolve().parent / "_control-slice-out-2026-09-29.json"

PERIODS = dict(base.PERIODS)
PERIODS["p4"] = ("21-27.09", 7, "e45f2afe-3304-415a-b54c-45de3405fb15.txt")

CONTROL = base.CONTROL + [
    "интеграция 1с с ozon",
    "интеграция 1с с wildberries",
    "сопровождение 1с",
    "купить лицензию 1с",
]

CLUSTERS = ["mp", "b2b", "impl", "support", "lic", "bitrix", "brand", "tg", "dev", "other"]


def main() -> None:
    loaded = {}
    for key, (label, days, fname) in PERIODS.items():
        rows = base.load_queries(fname)
        loaded[key] = {"label": label, "days": days, "rows": rows, "agg": base.agg(rows, days)}

    compare = []
    for c in CLUSTERS:
        row = {"cluster": c}
        for key in PERIODS:
            a = loaded[key]["agg"].get(c, {})
            row[key] = {
                "showsDay": a.get("showsDay", 0),
                "clicksDay": a.get("clicksDay", 0),
                "ctr": a.get("ctr", 0),
                "pos": a.get("avgPos"),
                "shows": a.get("shows", 0),
                "clicks": a.get("clicks", 0),
            }
        compare.append(row)

    controls = []
    for phrase in CONTROL:
        item = {"q": phrase}
        for key in PERIODS:
            hit = base.find_query(loaded[key]["rows"], phrase)
            item[key] = (
                {"q": hit["q"], "shows": hit["shows"], "clicks": hit["clicks"], "pos": round(hit["pos"], 1)}
                if hit
                else None
            )
        controls.append(item)

    tops = {
        c: [
            {"q": t["q"], "shows": t["shows"], "clicks": t["clicks"], "pos": t["pos"]}
            for t in loaded["p4"]["agg"].get(c, {}).get("top", [])
        ]
        for c in ("mp", "b2b", "impl", "support", "lic", "brand", "bitrix")
    }

    payload = {"periods": {k: v[:2] for k, v in PERIODS.items()}, "compare": compare, "controls": controls, "topsP4": tops}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    for row in compare:
        print(
            f'{row["cluster"]:8}',
            " | ".join(
                f'{k} {row[k]["showsDay"]:>6} {row[k]["clicksDay"]:>5} {row[k]["ctr"]:>5}% pos {row[k]["pos"]}'
                for k in PERIODS
            ),
        )
    print()
    for it in controls:
        print(
            f'{it["q"]:42}',
            " | ".join(
                (f'{k} {it[k]["shows"]}/{it[k]["clicks"]} п{it[k]["pos"]}' if it[k] else f"{k} -")
                for k in PERIODS
            ),
        )
    print()
    for c, lst in tops.items():
        print(c, [(t["q"], t["shows"], t["clicks"], t["pos"]) for t in lst])


if __name__ == "__main__":
    main()
