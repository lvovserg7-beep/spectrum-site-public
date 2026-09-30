# -*- coding: utf-8 -*-
"""Control slice 24.09.2026: cluster compare + control queries."""
from __future__ import annotations

import json
import re
from pathlib import Path

TOOLS = Path(r"C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-tools")
OUT = Path(__file__).resolve().parent / "_control-slice-out-2026-09-24.json"

PERIODS = {
    "p0": ("01-25.08", 25, "851f1463-ec60-43fb-9210-d59498fc6dd5.txt"),  # start
    "p1": ("26.08-04.09", 10, "abfb7b27-1553-4a72-9071-f59755ee1214.txt"),  # window1
    "p2": ("05-12.09", 8, "d88d263e-6771-400f-8607-ecba1529ad54.txt"),  # prev slice
    "p3": ("13-20.09", 8, "b8f739e9-9dcc-4c62-8b65-722dbbbd53de.txt"),  # current
}

BRAND = re.compile(r"аллсан|allsun|allsan|алсан|алсн|\balsn\b", re.I)

CONTROL = [
    "модуль маркетплейсов 1с",
    "модуль 1с для маркетплейсов",
    "модули маркетплейсов для 1с",
    "1с ут интеграция с маркетплейсами",
    "модуль интеграции 1с с маркетплейсами",
    "мерлион b2b",
    "ocs b2b",
    "втт b2b",
    "интеграция с поставщиком",
    "1с обмен с поставщиками",
    "внедрение 1с комплексная автоматизация",
    "1с внедрение ка",
    "стоимость внедрения 1с erp",
    "техподдержка 1с",
    "битрикс 24 стоимость внедрения",
    "аллсан",
    "алсан интеграция",
]


def classify(q: str) -> str:
    s = q.lower()
    if BRAND.search(s):
        return "brand"
    if (
        (re.search(r"маркетплейс|ozon|озон|wildberries|вайлдберр|\bwb\b|модуль", s)
         and re.search(r"1с|1c|маркет", s))
        or re.search(r"ozon|озон|wildberries|вайлдберр", s)
    ):
        return "mp"
    if re.search(
        r"мерлион|merlion|ocs|втт|vtt|treolan|треолан|ресурс медиа|auvix|аувикс|"
        r"этм|netlab|cisco|телеком|b2b|б2б|3logic|дссл|dssl|elko|марвел|осиэс|"
        r"русский свет|ipro|поставщик",
        s,
    ):
        return "b2b"
    if re.search(r"техподдержк|сопровожден|обслуживан|аутсорс|программист 1с на час", s):
        return "support"
    if re.search(r"доработк|кастом|печатн.*форм", s):
        return "dev"
    if re.search(
        r"внедрен|erp|комплексн.*автомат|1с внедрение|\bка\b.*внедр|"
        r"стоимость внедрения|erp на производ",
        s,
    ):
        return "impl"
    if re.search(r"битрикс|bitrix", s):
        return "bitrix"
    if re.search(r"лиценз|итс|\bкп\b|fresh|фреш|коробк|купить 1с|цена.*1с", s):
        return "lic"
    if re.search(r"телеграм|telegram|бот", s):
        return "tg"
    return "other"


def load_queries(fname: str) -> list[dict]:
    raw = json.loads((TOOLS / fname).read_text(encoding="utf-8"))
    # shape: {queries: [...]} or {report, queries}
    qs = raw.get("queries") or raw.get("data") or []
    out = []
    for r in qs:
        q = r.get("query_text") or r.get("query") or ""
        out.append(
            {
                "q": q,
                "shows": r.get("TOTAL_SHOWS") or r.get("shows") or 0,
                "clicks": r.get("TOTAL_CLICKS") or r.get("clicks") or 0,
                "pos": r.get("AVG_SHOW_POSITION") or r.get("position") or 0,
            }
        )
    return out


def agg(rows: list[dict], days: int) -> dict:
    out: dict[str, dict] = {}
    for r in rows:
        c = classify(r["q"])
        o = out.setdefault(
            c, {"shows": 0, "clicks": 0, "posSum": 0, "n": 0, "top": []}
        )
        o["shows"] += r["shows"]
        o["clicks"] += r["clicks"]
        o["posSum"] += r["pos"] * r["shows"]
        o["n"] += 1
        o["top"].append(r)
    for c, o in out.items():
        o["ctr"] = round(100 * o["clicks"] / o["shows"], 2) if o["shows"] else 0
        o["avgPos"] = round(o["posSum"] / o["shows"], 1) if o["shows"] else None
        o["showsDay"] = round(o["shows"] / days, 1)
        o["clicksDay"] = round(o["clicks"] / days, 2)
        o["top"] = sorted(o["top"], key=lambda x: -x["shows"])[:6]
        for t in o["top"]:
            t["ctr"] = (
                round(100 * t["clicks"] / t["shows"], 2) if t["shows"] else 0
            )
            t["pos"] = round(t["pos"], 1)
    return out


def find_query(rows: list[dict], phrase: str) -> dict | None:
    pl = phrase.lower()
    exact = next((r for r in rows if r["q"].lower() == pl), None)
    if exact:
        return exact
    return next((r for r in rows if pl in r["q"].lower()), None)


def main() -> None:
    loaded = {}
    for key, (label, days, fname) in PERIODS.items():
        rows = load_queries(fname)
        loaded[key] = {
            "label": label,
            "days": days,
            "n": len(rows),
            "agg": agg(rows, days),
            "rows": rows,
        }

    clusters = ["mp", "b2b", "impl", "support", "lic", "bitrix", "brand", "tg", "dev", "other"]
    compare = []
    for c in clusters:
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
            hit = find_query(loaded[key]["rows"], phrase)
            if hit:
                item[key] = {
                    "shows": hit["shows"],
                    "clicks": hit["clicks"],
                    "pos": round(hit["pos"], 1),
                    "ctr": round(100 * hit["clicks"] / hit["shows"], 2)
                    if hit["shows"]
                    else 0,
                }
            else:
                item[key] = None
        controls.append(item)

    # site totals from trend (hardcode from API we already have)
    trend_shows = [
        468, 419, 864, 812, 825, 881, 613, 245, 284, 635, 574, 624, 614, 537, 251,
        210, 606, 537, 695, 689, 714, 322, 269, 661, 712, 839, 992, 880, 438, 348,
        973, 739, 921, 764, 755, 292, 288, 793, 883, 981, 879, 688, 260, 269,
        848, 850, 875, 944, 743, 337, 359,
    ]
    trend_clicks = [
        6, 4, 7, 11, 16, 11, 5, 2, 8, 11, 9, 9, 9, 6, 6, 7, 12, 14, 10, 11, 16, 3, 0,
        9, 13, 7, 13, 7, 3, 4, 15, 5, 11, 11, 8, 4, 5, 14, 13, 6, 17, 9, 4, 2,
        13, 13, 16, 12, 10, 2, 3,
    ]
    # indices: 0=Aug1 ... 50=Sep20
    def period_avg(arr, start, end):
        chunk = arr[start : end + 1]
        return round(sum(chunk) / len(chunk), 1)

    site = {
        "p0": {"showsDay": period_avg(trend_shows, 0, 24), "clicksDay": period_avg(trend_clicks, 0, 24)},
        "p1": {"showsDay": period_avg(trend_shows, 25, 34), "clicksDay": period_avg(trend_clicks, 25, 34)},
        "p2": {"showsDay": period_avg(trend_shows, 35, 42), "clicksDay": period_avg(trend_clicks, 35, 42)},
        "p3": {"showsDay": period_avg(trend_shows, 43, 50), "clicksDay": period_avg(trend_clicks, 43, 50)},
    }

    payload = {
        "date": "2026-09-24",
        "periods": {k: {"label": v[0], "days": v[1]} for k, v in PERIODS.items()},
        "site": site,
        "compare": compare,
        "controls": controls,
        "tops": {
            k: {
                c: loaded[k]["agg"].get(c, {}).get("top", [])
                for c in ("mp", "b2b", "impl", "support", "lic", "brand")
            }
            for k in PERIODS
        },
        "sqi": 240,
        "diag": "TOO_MANY_DOMAINS_ON_SEARCH",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)
    for row in compare:
        if row["cluster"] in ("mp", "b2b", "impl", "support", "lic", "brand", "bitrix"):
            print(
                row["cluster"],
                "p0", row["p0"]["showsDay"], row["p0"]["clicksDay"], row["p0"]["ctr"],
                "| p2", row["p2"]["showsDay"], row["p2"]["clicksDay"], row["p2"]["ctr"],
                "| p3", row["p3"]["showsDay"], row["p3"]["clicksDay"], row["p3"]["ctr"],
            )


if __name__ == "__main__":
    main()
