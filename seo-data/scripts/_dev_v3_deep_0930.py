# -*- coding: utf-8 -*-
"""Углубленная сверка живой /development1c с инструкцией v3."""
import html
import json
import re
from pathlib import Path

h = Path(__file__).with_name("_dev_v3_live_check_0930.html").read_text(encoding="utf-8")
head = h[: h.index("</head>")]
body = h[h.index("<body"):]
rep = []


def out(*a):
    rep.append(" ".join(str(x) for x in a))


def recs():
    items = [
        (m.start(), m.group(1), m.group(2))
        for m in re.finditer(
            r'<div id="rec(\d+)" class="r t-rec([^"]*)"[^>]*data-record-type="(\d+)"',
            body,
        )
    ]
    # fix: I captured class as group 2 by mistake. redo.
    return items


items = []
for m in re.finditer(
    r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body
):
    items.append((m.start(), m.group(1), m.group(2)))

out("== recs visible vs hidden")
old_markers = [
    "Без головной боли",
    "Разовое обращение",
    "Частые вопросы по внедрению 1С",
    "Экономим до 50%",
    "Документооборот 8",
    "Благодарности за внедрение",
    "Личный Кабинет",
    "Под ключ",
]
for i, (pos, rid, typ) in enumerate(items):
    end = items[i + 1][0] if i + 1 < len(items) else len(body)
    chunk = body[pos:end]
    headc = chunk[:1200]
    hidden = (
        "t-rec_hidden" in headc
        or "r_hidden" in headc[:400]
        or 'style="display:none' in headc
        or "display:none !important" in headc
        or "t-rec_pc_hidden" in headc
    )
    txt = re.sub(r"<(script|style).*?</\1>", " ", chunk, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    txt = re.sub(r"\s+", " ", txt).strip()
    hit = [k for k in old_markers if k in txt]
    if "hf" in chunk or "Паспорт услуги" in txt or "Софья Мазницына" in txt or "Разберём" in txt or hit:
        out(
            f"{i+1:2d} rec{rid} T{typ} {'HIDDEN' if hidden else 'SHOW'} "
            f"| {txt[:140]} | hits={hit}"
        )

# FAQ match
brief = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\tilda-briefs\_head-development1c-2026-09-30.txt").read_text(encoding="utf-8")
# extract FAQPage from live
faq_live = None
howto_live = None
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
    try:
        d = json.loads(m.group(1))
    except Exception:
        continue
    if d.get("@type") == "FAQPage":
        faq_live = d
    if d.get("@type") == "HowTo":
        howto_live = d

# visible summaries inside .v3
v3 = re.search(r'<div class="v3">([\s\S]*?)<div class="v3">', h)
# all v3 blocks
v3_blocks = re.findall(r'<div class="v3">([\s\S]*?)(?:</div>\s*<script>|</div>\s*<div class="v3">|$)', h)
# simpler: from first class="v3" 
idx = h.find('class="v3"')
v3html = h[idx: idx + 80000] if idx >= 0 else ""
vis_q = [html.unescape(re.sub(r"<[^>]+>", "", q)).strip() for q in re.findall(r"<summary>(.*?)</summary>", v3html, re.S)]
ld_q = [x["name"] for x in (faq_live or {}).get("mainEntity") or []]
out("== visible FAQ in v3", vis_q)
out("== LD FAQ", ld_q)
out("FAQ count match", len(vis_q), len(ld_q), vis_q == ld_q)
if vis_q != ld_q:
    for a, bq in zip(vis_q, ld_q):
        if a != bq:
            out(" DIFF", a, "||", bq)

# hero img
imgs = re.findall(r'<section class="hf[^"]*"[^>]*>[\s\S]*?<img src="([^"]+)"', h)
out("== hero img", imgs)
for u in imgs:
    bad = "/resize/" in u or "thb.tildacdn" in u or "ВСТАВЬТЕ" in u
    out("  bad_url" if bad else "  ok_url", u[:180])

# who tag
who = re.search(r'class="who">(.*?)</div>', h, re.S)
out("== who", re.sub(r"<[^>]+>", "", who.group(1) if who else "NONE"))

# team names
team = re.findall(r'<div class="pp">[\s\S]*?<b>(.*?)</b>', h)
out("== team", team)

# crumbs
crumb = re.search(r'aria-label="Хлебные крошки"([\s\S]{0,800})', h)
out("== crumb snippet", re.sub(r"\s+", " ", crumb.group(0)[:400] if crumb else "NONE"))

# rec3989707201 style
m = re.search(r'<div id="rec3989707201"[^>]*>', h)
out("== crumb rec tag", m.group(0) if m else "NONE")

# robots dup
out("== robots count", len(re.findall(r'<meta name="robots"', head)))

# dateModified
out("== dateModified", re.findall(r'"dateModified":\s*"([^"]+)"', head))

# leftover visible old
visible_body = []
for i, (pos, rid, typ) in enumerate(items):
    end = items[i + 1][0] if i + 1 < len(items) else len(body)
    chunk = body[pos:end]
    headc = chunk[:1200]
    hidden = "t-rec_hidden" in headc or "r_hidden" in headc[:400] or 'style="display:none' in headc
    if hidden:
        continue
    txt = re.sub(r"<(script|style).*?</\1>", " ", chunk, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt))
    txt = re.sub(r"\s+", " ", txt).strip()
    visible_body.append((rid, typ, txt[:100]))

out("== SHOW recs count", len(visible_body))
for rid, typ, txt in visible_body:
    if any(k in txt for k in old_markers + ["50 %", "50%", "тариф", "Документооборот"]):
        out("  OLD STILL SHOW rec" + rid, "T" + typ, txt)

# T107
out("== T107 recs", [(rid, typ) for _, rid, typ in items if typ == "270" or typ == "107"])
# record-type for T107 is 270 I think? Tilda T107 = 270. Check
for i, (pos, rid, typ) in enumerate(items):
    end = items[i + 1][0] if i + 1 < len(items) else len(body)
    chunk = body[pos:end]
    if "t107" in chunk[:500].lower() or typ in ("270", "3"):
        headc = chunk[:800]
        hidden = "t-rec_hidden" in headc or "r_hidden" in headc[:400]
        txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", chunk[:1500])))
        if "sofia" in chunk.lower() or "maznits" in chunk.lower() or "vnedrenie-sofia" in chunk or "allsun-hero-vnedr" in chunk:
            out(" T107/photo rec" + rid, "T" + typ, "HIDDEN" if hidden else "SHOW", txt[:120])

Path(__file__).with_name("_dev_v3_deep_0930.txt").write_text("\n".join(rep), encoding="utf-8")
print("ok", len(rep))
