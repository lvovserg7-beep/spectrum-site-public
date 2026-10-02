import json
from pathlib import Path

D = Path(__file__).resolve().parent
d = json.loads((D / "_sup_cards_live_0930.json").read_text(encoding="utf-8"))
out = []
for s, m in d.items():
    out.append(f"===== {s} | H1: {m['h1']} | LD: {m['ld']}")
    out.append("TITLE " + m["title"])
    out.append("DESC " + m["desc"])
    out.append("SEQ " + " ".join(f"{b['type']}:{b['rec']}" for b in m["blocks"]))
    for b in m["blocks"]:
        if b["type"] in ("180", "1033", "65", "585", "758"):
            t = b["text"].replace("\n", " / ")
            out.append(f"  rec{b['rec']} T{b['type']} | " + (t if b["type"] == "585" else t[:400]))
(D / "_sup_dump.txt").write_text("\n".join(out), encoding="utf-8")
