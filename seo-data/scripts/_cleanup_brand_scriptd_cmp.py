import html
import pathlib
import re

base = pathlib.Path(__file__).parent
brief = (base.parent / "tilda-briefs" / "tier1-tier2-licenzii-ostatok-2026-09-15.html").read_text(encoding="utf-8")
m = re.search(r'<pre id="c-d-script">(.*?)</pre>', brief, re.S)
mine = html.unescape(m.group(1)).strip()
live = html.unescape((base / "_cleanup_brand_scriptd.txt").read_text(encoding="utf-8")).strip()
print("same:", mine == live, len(mine), len(live))
print("long dash in brief:", brief.count("\u2014"), "en dash:", brief.count("\u2013"))
