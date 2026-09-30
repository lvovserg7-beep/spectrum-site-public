# -*- coding: utf-8 -*-
"""Check leftover 25 catalog alts on live alsn.ru."""
from __future__ import annotations

import html as htmlmod
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = json.loads((ROOT / "_qa_alts_expected.json").read_text(encoding="utf-8"))
OUT = ROOT / "_qa_alts_leftover_live.json"
REPORT = ROOT / "_qa_alts_leftover_report.txt"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
GALLERY_RE = re.compile(r'"gallery"\s*:\s*(\[.*?\])\s*,\s*"sort"', re.S)

REDO_UID = {
    "889199487282",
    "920860758832",
    "601537363831",
    "658261749802",
    "293950783102",
    "159637201592",
    "556990081002",
    "136066752982",
    "599820132332",
    "729903995532",
    "257692803132",
    "909487433562",
    "865515246452",
    "579717645782",
    "583281700322",
    "758650958432",
    "792021947492",
    "206773331182",
    "295893253862",
    "308293969592",
    "845146210291",
    "413216341712",
    "215664845112",
    "837358323511",
    "226213368711",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "ru-RU,ru;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def gallery_alts(page: str) -> list[str]:
    m = GALLERY_RE.search(page)
    if not m:
        return []
    try:
        arr = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []
    out = []
    for item in arr:
        if isinstance(item, dict):
            out.append((item.get("alt") or "").strip())
    return out


def uid_of(it: dict) -> str:
    return str(it.get("uid") or "")


def check(it: dict) -> dict:
    url = it["url"].split("?", 1)[0]
    exp = (it.get("alt") or "").strip()
    rec = {
        "uid": uid_of(it),
        "sku": it.get("sku") or "",
        "title": it.get("title") or "",
        "url": url,
        "expected": exp,
    }
    try:
        page = fetch(url)
        alts = gallery_alts(page)
        live = htmlmod.unescape(alts[0] if alts else "")
        rec["live"] = live
        rec["gallery_n"] = len(alts)
        if not alts:
            rec["status"] = "no_gallery"
        elif not live:
            rec["status"] = "empty"
        elif live == exp:
            rec["status"] = "ok"
        else:
            rec["status"] = "mismatch"
    except Exception as e:
        rec["status"] = "error"
        rec["error"] = str(e)
    return rec


def main() -> None:
    # unique leftover parents only
    items = []
    seen = set()
    for it in EXPECTED:
        uid = uid_of(it)
        if uid not in REDO_UID or uid in seen:
            continue
        if it.get("parent"):
            continue
        seen.add(uid)
        items.append(it)

    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(check, it) for it in items]
        for fut in as_completed(futs):
            results.append(fut.result())
    results.sort(key=lambda x: x.get("title") or "")

    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    payload = {"total": len(results), "counts": counts, "results": results}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "Остаток 25 карточек, живой сайт 17.09.2026",
        f"Проверено: {len(results)}",
        f"Совпало: {counts.get('ok', 0)}",
        f"Пусто: {counts.get('empty', 0)}",
        f"Текст не тот: {counts.get('mismatch', 0)}",
        f"Нет gallery: {counts.get('no_gallery', 0)}",
        f"Ошибка: {counts.get('error', 0)}",
        "",
    ]
    for st in ("empty", "mismatch", "no_gallery", "error"):
        bad = [r for r in results if r["status"] == st]
        if not bad:
            continue
        lines.append(f"=== {st.upper()} ===")
        for r in bad:
            sku = r["sku"] or "без артикула"
            lines.append(f"{sku}\t{r['title']}")
            lines.append(f"  ждали: {r['expected']}")
            lines.append(f"  сейчас: {r.get('live') or ''}")
            lines.append(f"  {r['url']}")
            if r.get("error"):
                lines.append(f"  err: {r['error']}")
            lines.append("")
    lines.append("=== OK ===")
    for r in results:
        if r["status"] == "ok":
            lines.append(f"{r.get('sku') or 'без артикула'}\t{r['live']}")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False), "n", len(results))
    print("wrote", REPORT)


if __name__ == "__main__":
    main()
