# -*- coding: utf-8 -*-
import re
import urllib.request
import json
from pathlib import Path

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_probe_alt_sections.txt"


def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def textish(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


lines = []
for path in ["/caseecomsc", "/xitsadmarketplace", "/clients"]:
    html = fetch("https://alsn.ru" + path)
    lines.append(f"\n==== {path} ====")
    for m in re.finditer(r'<div id="(rec\d+)"[^>]*>', html):
        rid = m.group(1)
        start = m.start()
        head = html[start : start + 500]
        tm = re.search(r'data-record-type="(\d+)"', head)
        typ = tm.group(1) if tm else "?"
        nxt = re.search(r'<div id="rec\d+"', html[start + 20 :])
        end = start + 20 + nxt.start() if nxt else min(len(html), start + 20000)
        chunk = html[start:end]
        titles = []
        for pat in [
            r"<h[1-3][^>]*>(.*?)</h[1-3]>",
            r'class="[^"]*t-section__title[^"]*"[^>]*>([^<]+)',
            r'class="[^"]*t-title[^"]*"[^>]*>([^<]{3,120})',
            r'class="[^"]*t-name[^"]*"[^>]*>([^<]{3,120})',
            r'field="title"[^>]*>([^<]{3,120})',
        ]:
            for mm in re.finditer(pat, chunk, re.I | re.S):
                t = textish(mm.group(1))
                if t and t not in titles:
                    titles.append(t[:100])
        before = html[max(0, start - 3500) : start]
        hs = list(re.finditer(r"<h[1-3][^>]*>(.*?)</h[1-3]>", before, re.I | re.S))
        hb = textish(hs[-1].group(1))[:100] if hs else ""
        # also t-title before
        if not hb:
            ts = list(
                re.finditer(
                    r'class="[^"]*(?:t-section__title|t-title)[^"]*"[^>]*>([^<]{3,100})',
                    before,
                    re.I,
                )
            )
            if ts:
                hb = textish(ts[-1].group(1))[:100]
        imgs = []
        for im in re.finditer(r"<img\b([^>]*)>", chunk, re.I):
            inn = im.group(1)
            src_m = re.search(r'(?:src|data-original)="([^"]+)"', inn)
            alt_m = re.search(r'alt="([^"]*)"', inn)
            if not src_m:
                continue
            src = src_m.group(1)
            fn = src.rsplit("/", 1)[-1].split("?")[0]
            a = alt_m.group(1) if alt_m else ""
            key = fn.lower()
            if any(
                x in key
                for x in [
                    "logo",
                    "tatneft",
                    "lanit",
                    "goodwood",
                    "xcom",
                    "page-0001",
                    "noroot",
                    "photo.jpg",
                    "0001_1",
                ]
            ) or fn.startswith("_"):
                imgs.append(f"{fn}|alt={a[:30]}|20x={'/resize/20x/' in src}")
        if not imgs and typ not in ("594", "795", "670", "668"):
            continue
        lines.append(
            f"  {rid} T{typ} before=[{hb}] titles={titles[:4]} n_img={len(imgs)}"
        )
        for im in imgs[:15]:
            lines.append(f"     - {im}")

data = json.loads((ROOT / "_alts-tail-live-2026-09-23.json").read_text(encoding="utf-8"))
lines.append("\n==== ENRICHED SAMPLE ====")
for it in data["items"][:3]:
    lines.append(
        json.dumps(
            {
                k: it.get(k)
                for k in (
                    "path",
                    "file",
                    "section",
                    "near",
                    "block",
                    "rec",
                    "index_in_block",
                    "orient_lines",
                )
            },
            ensure_ascii=False,
        )
    )
for it in data["items"]:
    if it["path"] == "/clients" and it["file"] in (
        "GoodWood.jpg",
        "noroot.jpg",
        "0001_1.jpg",
        "noroot.png",
    ):
        lines.append(
            json.dumps(
                {
                    k: it.get(k)
                    for k in (
                        "file",
                        "section",
                        "near",
                        "block",
                        "rec",
                        "index_in_block",
                        "orient_lines",
                    )
                },
                ensure_ascii=False,
            )
        )

OUT.write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT)
