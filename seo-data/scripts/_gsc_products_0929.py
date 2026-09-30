# -*- coding: utf-8 -*-
"""GSC page-level totals by product (same regex as API filters on 29.09)."""
from __future__ import annotations

import json
import re
from pathlib import Path

TOOLS = Path(r"C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\agent-tools")

FILES = {
    "25.08-12.09": (19, "a5703157-a05c-4cff-acb1-722045894819.txt"),
    "13-20.09": (8, "d1c69588-8c93-4832-9a52-fbbd312602c9.txt"),
}

PRODUCTS = {
    "mp": r"alsn\.ru/(casemarketplace|1c-ozon|1c-wildberries|xitsadmarketplace|perevystavlenie|event-marketplaces)",
    "b2b": r"alsn\.ru/(ecom|caseecomsc|merlion|ocs|marvel|treolan|3logic|etm-ipro|resurs-media|russkiy-svet|digis|auvix|vtt|dssl|elko|integraciya-1c-dlya-prodavcov)",
    "impl": r"alsn\.ru/(development1c|erp-time-price|kompleksnaya_avtomatizaciya$|perehod-|moy-sklad-perenos|vesii)",
    "support": r"alsn\.ru/support1c",
    "lic": r"alsn\.ru/(its|1cfresh|products|dopolnitelnie_licenzii|buhv8|zup8|upt8|upravlenie_nashei_firmoi|dokumentooborot8|1_obschepit_fastfood|kompleksnaya_avtomatizaciya/tproduct)",
    "bitrix": r"alsn\.ru/(bitrix24|1cbitrix)",
    "tg": r"alsn\.ru/(tb|telegram|case_telegram_bot|keys_po_telegram|keys_po_integratsii_s_messendzherom)",
}

out = {}
for label, (days, fname) in FILES.items():
    raw = json.loads((TOOLS / fname).read_text(encoding="utf-8"))
    rows = raw.get("data") or raw.get("rows") or []
    tot = {"clicks": sum(r["clicks"] for r in rows), "shows": sum(r["impressions"] for r in rows)}
    res = {"_all_pages": tot}
    for p, rx in PRODUCTS.items():
        sel = [r for r in rows if re.search(rx, r["page"])]
        res[p] = {
            "clicks": sum(r["clicks"] for r in sel),
            "shows": sum(r["impressions"] for r in sel),
            "top": sorted(
                [(r["page"].replace("https://alsn.ru", ""), r["clicks"], r["impressions"], r["position"]) for r in sel],
                key=lambda x: -x[2],
            )[:4],
        }
    out[label] = {"days": days, "meta": raw.get("metadata", {}), "res": res}

Path(__file__).with_name("_gsc-products-2026-09-29.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
for label, v in out.items():
    print(label, v["meta"].get("start_date"), v["meta"].get("end_date"), v["res"]["_all_pages"])
    for p in PRODUCTS:
        r = v["res"][p]
        print(" ", p, r["clicks"], r["shows"], r["top"])
