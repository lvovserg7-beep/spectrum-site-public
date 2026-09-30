# -*- coding: utf-8 -*-
"""Live check of caseecomsc + xitsadmarketplace vs expected SEO."""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
OUT = Path(__file__).resolve().parent / "_case-pages-live-2026-09-23.json"

STRIP = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html",
            "Accept-Language": "ru-RU,ru;q=0.9",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def textish(s: str) -> str:
    return WS.sub(" ", STRIP.sub(" ", s or "")).strip()


def one(html: str, *pats: str) -> str:
    for p in pats:
        m = re.search(p, html, re.I | re.S)
        if m:
            return textish(m.group(1))
    return ""


def count_ld(html: str, typ: str) -> int:
    n = 0
    for m in re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    ):
        body = m.group(1)
        if typ in body:
            n += 1
    return n


def empty_meaningful_alts(html: str) -> list[dict]:
    icon = re.compile(
        r"(?i)(?:\.svg$|Tilda_Icons|kisspng|emoji|Vector_|Layer_|favicon|"
        r"29557530|_5\.png|_9\.png)"
    )
    out = []
    for m in re.finditer(r"<img\b([^>]*)>", html, re.I | re.S):
        inn = m.group(1)
        src_m = re.search(r'(?:src|data-original|data-src)="([^"]+)"', inn)
        alt_m = re.search(r'alt="([^"]*)"', inn)
        if not src_m:
            continue
        src = src_m.group(1)
        fn = src.rsplit("/", 1)[-1].split("?")[0]
        if not fn or icon.search(fn) or icon.search(src):
            continue
        alt = (alt_m.group(1) if alt_m else "").strip()
        if alt and alt.lower() not in {"image", "img", "фото", "картинка"}:
            continue
        # keep logos / letters / noroot / photo / image.png
        low = fn.lower()
        keep = (
            "logo" in low
            or "tatneft" in low
            or "lanit" in low
            or "goodwood" in low
            or "xcom" in low
            or "noroot" in low
            or low == "photo.jpg"
            or low == "image.png"
            or "page-0001" in low
            or "0001" in low
            or low.startswith("_")
            or "thumb_" in low
            or low in ("c8561e493ab77c8933fc.png", "5e82004a227a092f3923.png")
        )
        if not keep:
            continue
        out.append({"file": fn, "alt": alt, "src": src.split("?")[0][:180]})
    # dedupe by file+rec-ish src host path
    seen = set()
    uniq = []
    for it in out:
        k = (it["file"], it["src"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(it)
    return uniq


def crumbs_kind(html: str) -> str:
    if 'aria-label="Хлебные крошки"' not in html and "Хлебные крошки" not in html:
        # also check for home icon crumbs
        if re.search(r'aria-label=["\']Главная["\']', html) and re.search(
            r">\s*/\s*<", html
        ):
            pass
        else:
            return "NONE"
    # arrow style?
    if "Главная →" in html or "Главная &rarr;" in html or "Главная →" in html:
        return "ARROW"
    if re.search(r"Главная\s*→", html):
        return "ARROW"
    if 'aria-label="Хлебные крошки"' in html or re.search(
        r'aria-label=["\']Хлебные крошки["\']', html
    ):
        # look for slash separators near crumbs
        m = re.search(
            r'aria-label=["\']Хлебные крошки["\'][^>]*>(.*?)</nav>',
            html,
            re.I | re.S,
        )
        chunk = m.group(1) if m else html
        if "→" in chunk or "&rarr;" in chunk.lower():
            return "ARROW"
        return "CANON"
    return "OTHER"


def check_page(path: str, expect: dict) -> dict:
    url = "https://alsn.ru" + path
    html = fetch(url + "?v=check2309")
    title = one(html, r"<title[^>]*>(.*?)</title>")
    desc = one(
        html,
        r'name=["\']description["\']\s+content=["\']([^"\']*)["\']',
        r'content=["\']([^"\']*)["\']\s+name=["\']description["\']',
    )
    h1 = one(html, r"<h1\b[^>]*>(.*?)</h1>")
    og_t = one(
        html,
        r'property=["\']og:title["\']\s+content=["\']([^"\']*)["\']',
        r'content=["\']([^"\']*)["\']\s+property=["\']og:title["\']',
    )
    og_d = one(
        html,
        r'property=["\']og:description["\']\s+content=["\']([^"\']*)["\']',
        r'content=["\']([^"\']*)["\']\s+property=["\']og:description["\']',
    )
    og_img = one(
        html,
        r'property=["\']og:image["\']\s+content=["\']([^"\']*)["\']',
        r'content=["\']([^"\']*)["\']\s+property=["\']og:image["\']',
    )
    canon = one(
        html,
        r'rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']',
        r'href=["\']([^"\']*)["\']\s+rel=["\']canonical["\']',
    )

    # contamination checks for xitsad
    bad_sc = []
    for phrase in expect.get("must_not_contain", []):
        if phrase.lower() in html.lower():
            bad_sc.append(phrase)
    good = []
    for phrase in expect.get("must_contain", []):
        good.append({"phrase": phrase, "ok": phrase.lower() in html.lower()})

    alts = empty_meaningful_alts(html)
    return {
        "path": path,
        "url": url,
        "title": title,
        "title_ok": expect.get("title_substr", "").lower() in title.lower()
        if expect.get("title_substr")
        else None,
        "description": desc[:220],
        "desc_ok": expect.get("desc_substr", "").lower() in desc.lower()
        if expect.get("desc_substr")
        else None,
        "h1": h1,
        "h1_ok": expect.get("h1_substr", "").lower() in h1.lower()
        if expect.get("h1_substr")
        else None,
        "og_title": og_t[:120],
        "og_desc": og_d[:160],
        "og_image": og_img[:160],
        "og_image_bad_resize504": "/resize/504x/" in (og_img or ""),
        "canonical": canon,
        "crumbs": crumbs_kind(html),
        "ld_breadcrumb": count_ld(html, "BreadcrumbList"),
        "ld_webpage": count_ld(html, "WebPage"),
        "ld_article": count_ld(html, "Article"),
        "must_contain": good,
        "must_not_contain_hits": bad_sc,
        "empty_alts": alts,
        "empty_alts_n": len(alts),
        # lead snippet
        "lead_snip": textish(
            re.search(r"<h1\b[^>]*>.*?</h1>(.{0,500})", html, re.I | re.S).group(1)
            if re.search(r"<h1\b[^>]*>.*?</h1>", html, re.I | re.S)
            else ""
        )[:240],
    }


EXPECT = {
    "/caseecomsc": {
        "title_substr": "поставщик",
        "desc_substr": "СЦ",
        "h1_substr": "СЦ",
        "must_contain": ["ООО «СЦ»", "поставщик"],
        "must_not_contain": ["ХИТСАД", "маркетплейс"],
    },
    "/xitsadmarketplace": {
        "title_substr": "ХИТСАД",
        "desc_substr": "ХИТСАД",
        "h1_substr": "ХИТСАД",
        "must_contain": ["ХИТСАД", "маркетплейс"],
        "must_not_contain": [
            "ООО «СЦ»",
            "телеком- и IT-оборудования для ООО «СЦ»",
            "B2B-поставщиками",
        ],
    },
}


def main() -> None:
    rows = []
    for path, exp in EXPECT.items():
        print("check", path)
        row = check_page(path, exp)
        rows.append(row)
        print(
            " ",
            "title_ok=",
            row["title_ok"],
            "h1_ok=",
            row["h1_ok"],
            "crumbs=",
            row["crumbs"],
            "empty_alts=",
            row["empty_alts_n"],
            "contam=",
            row["must_not_contain_hits"],
        )
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
