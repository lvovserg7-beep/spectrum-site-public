import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
d = json.loads((Path(__file__).with_name("_sup_cards_live_0930.json")).read_text(encoding="utf-8"))
only = sys.argv[1].split(",") if len(sys.argv) > 1 else list(d)
for s in only:
    m = d[s]
    print("=" * 20, s)
    for b in m["blocks"]:
        if b["type"] == "585":
            t = re.sub(r"\s+", " ", b["text"])
            print(t[:2600])
