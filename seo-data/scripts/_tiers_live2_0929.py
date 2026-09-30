# -*- coding: utf-8 -*-
import json
from pathlib import Path

rows = json.loads(Path(__file__).with_name("_tiers_live_0929.json").read_text(encoding="utf-8"))
for r in rows:
    if r.get("n_lists", 0) > 1 or r.get("last_url_ok") is False or not r.get("bc_ok", True) or r["path"] in (
            "/cases", "/vesii", "/1c-ozon", "/1c-wildberries", "/casemarketplace", "/1c-ozon-old", "/development1c", "/erp-time-price"):
        print(r["path"], "style", r.get("style"), "lists", r.get("n_lists"), "urlok", r.get("last_url_ok"),
              "bc_ok", r.get("bc_ok"), "vis", r.get("visible_blocks"), "t758", r.get("t758"), "noindex", r.get("noindex"))
