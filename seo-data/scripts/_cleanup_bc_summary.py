# -*- coding: utf-8 -*-
import json
from pathlib import Path

D = Path(__file__).parent
rows = json.loads((D / "_tiers_live_0929.json").read_text(encoding="utf-8"))
out = []
for r in rows:
    out.append("%s | %s | vis=%s | lists=%s | urlok=%s | last=%s/%s | t758=%s | ealt=%s | ni=%s | %s" % (
        r["path"], r.get("style"), r.get("visible_blocks"), r.get("n_lists"), r.get("last_url_ok"),
        r.get("last_vis"), r.get("last_ld"), r.get("t758"), len(r.get("empty_alt") or []), r.get("noindex"),
        r.get("kind")))
(D / "_cleanup_bc_summary.txt").write_text("\n".join(out), encoding="utf-8")
print(len(out))
