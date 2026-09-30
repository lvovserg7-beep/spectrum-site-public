# -*- coding: utf-8 -*-
"""Audit empty/missing img alts on alsn.ru (pages + optional tproduct leftovers)."""
from __future__ import annotations

import html as html_lib
import json
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_qa_page_alts_missing.json"
SITEMAP = "https://alsn.ru/sitemap.xml"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

SKIP_PATH_PREFIX = (
    "/policy",
    "/privacy",
    "/soglashenie",
    "/uslovia-vozvrata",
    "/sitemap",
)
SKIP_FILE_RE = re.compile(
    r"(?:favicon|sprite|pixel|1x1|blank|spacer|icon[_-]?\d|"
    r"tildacdn\.com/.*?/libtilda|static\.tildacdn\.com/.*?/(?:tilda-icons|emoji))",
    re.I,
)
GENERIC_ALT = re.compile(
    r"^(?:image|img|photo|картинка|изображение|фото|untitled|без названия|\.jpg|\.png|\.webp)?$",
    re.I,
)
IMG_RE = re.compile(
    r"<img\b([^>]*)>",
    re.I | re.S,
)
ATTR_RE = re.compile(r"""(\w+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", re.I)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
H2_RE = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.I | re.S)
TITLE_RE = re.compile(r"<title\b[^>]*>(.*?)</title>", re.I | re.S)
STRIP_TAGS = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def fetch(url: str, timeout: int = 35) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def textish(s: str) -> str:
    s = STRIP_TAGS.sub(" ", s or "")
    s = html_lib.unescape(s)
    return WS.sub(" ", s).strip()


def attrs(tag_inner: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in ATTR_RE.finditer(tag_inner):
        k = m.group(1).lower()
        v = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[k] = v or ""
    return out


def basename(src: str) -> str:
    path = urlparse(src).path
    return path.rsplit("/", 1)[-1] if path else src


def nearby_heading(html: str, pos: int) -> str:
    window = html[max(0, pos - 2500) : pos]
    hs = list(H2_RE.finditer(window)) + list(
        re.finditer(r"<h[23]\b[^>]*>(.*?)</h[23]>", window, re.I | re.S)
    )
    if not hs:
        return ""
    last = hs[-1]
    return textish(last.group(1))[:120]


def nearby_text(html: str, pos: int) -> str:
    after = html[pos : pos + 800]
    # accordion title / figcaption / nearby text
    for pat in (
        r'class="[^"]*accordion[^"]*"[^>]*>[\s\S]{0,200}?<[^>]+>([^<]{4,80})',
        r'itemprop="name"[^>]*>([^<]{4,80})',
        r"<figcaption[^>]*>(.*?)</figcaption>",
        r'class="[^"]*t-card__title[^"]*"[^>]*>(.*?)</',
        r'class="[^"]*t-name[^"]*"[^>]*>(.*?)</',
    ):
        m = re.search(pat, after, re.I | re.S)
        if m:
            t = textish(m.group(1))
            if t:
                return t[:100]
    # look slightly before for accordion li title
    before = html[max(0, pos - 1200) : pos]
    m = re.search(
        r"(?:t-name|accordion__title|t-card__title|t-title)[^>]*>([^<]{4,100})",
        before,
        re.I,
    )
    if m:
        return textish(m.group(1))[:100]
    return ""


def block_hint(html: str, pos: int) -> str:
    window = html[max(0, pos - 800) : pos + 200]
    m = re.search(r'data-record-type="(\d+)"', window)
    if m:
        return f"T{m.group(1)}"
    m = re.search(r'id="(rec\d+)"', window)
    if m:
        return m.group(1)
    return ""


def should_skip_img(a: dict[str, str]) -> bool:
    src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
    cls = a.get("class") or ""
    if not src and not a.get("data-original"):
        return True
    if SKIP_FILE_RE.search(src):
        return True
    if "t-slds__bgimg" in cls:  # often decorative bg handled separately
        pass
    w = a.get("width") or ""
    h = a.get("height") or ""
    if w in ("1", "0") or h in ("1", "0"):
        return True
    # tiny icons often have role presentation via class
    if re.search(r"\b(?:icon|sprite|emoji|bullet)\b", cls, re.I) and (
        not a.get("alt") or len(a.get("alt", "")) < 2
    ):
        # still report if large? skip small icon classes
        if "t-btn" in cls or "social" in cls.lower():
            return True
    return False


def is_missing_alt(alt: str) -> bool:
    alt = (alt or "").strip()
    if not alt:
        return True
    if GENERIC_ALT.match(alt):
        return True
    if alt.lower() in {".jpg", ".png", ".webp", ".gif", "null", "undefined"}:
        return True
    return False


def parse_imgs(url: str, html: str) -> list[dict]:
    h1 = ""
    m = H1_RE.search(html)
    if m:
        h1 = textish(m.group(1))[:140]
    title = ""
    m = TITLE_RE.search(html)
    if m:
        title = textish(m.group(1))[:140]

    items = []
    seen = set()
    for m in IMG_RE.finditer(html):
        a = attrs(m.group(1))
        if should_skip_img(a):
            continue
        alt = a.get("alt", "")
        if not is_missing_alt(alt):
            continue
        src = a.get("src") or a.get("data-original") or a.get("data-src") or ""
        if src.startswith("//"):
            src = "https:" + src
        elif src.startswith("/"):
            src = urljoin(url, src)
        fn = basename(src)
        key = (fn, a.get("class", "")[:40])
        if key in seen:
            continue
        seen.add(key)
        # skip pure SVG data / empty
        if not fn or fn.startswith("data:"):
            continue
        # skip logo in header if filename looks like logo and tiny context
        low = fn.lower()
        if "logo" in low and "header" in (a.get("class") or "").lower():
            continue

        pos = m.start()
        items.append(
            {
                "url": url,
                "h1": h1,
                "title": title,
                "file": fn,
                "src": src[:200],
                "alt_now": alt,
                "section": nearby_heading(html, pos),
                "near": nearby_text(html, pos),
                "block": block_hint(html, pos),
                "class": (a.get("class") or "")[:80],
            }
        )
    return items


def sitemap_urls() -> list[str]:
    xml = fetch(SITEMAP)
    locs = re.findall(r"<loc>(https://alsn\.ru/[^<]+)</loc>", xml)
    out = []
    for u in locs:
        p = urlparse(u).path.rstrip("/") or "/"
        if "/tproduct/" in u:
            continue
        if any(p.startswith(s) or p == s for s in SKIP_PATH_PREFIX):
            continue
        out.append(u.split("#")[0])
    # unique preserve order
    seen = set()
    uniq = []
    for u in out:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def check_page(url: str) -> dict:
    try:
        html = fetch(url)
        missing = parse_imgs(url, html)
        return {"url": url, "ok": True, "missing": missing, "n": len(missing)}
    except Exception as e:
        return {"url": url, "ok": False, "error": str(e), "missing": [], "n": 0}


def main() -> None:
    urls = sitemap_urls()
    print(f"pages: {len(urls)}")
    results = []
    all_missing = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = {pool.submit(check_page, u): u for u in urls}
        done = 0
        for fut in as_completed(futs):
            rec = fut.result()
            results.append(rec)
            all_missing.extend(rec.get("missing") or [])
            done += 1
            if done % 15 == 0:
                print(f"  {done}/{len(urls)} … missing so far {len(all_missing)}")
            time.sleep(0.05)

    # also re-check catalog leftover SKUs from previous brief if file exists
    leftover_path = ROOT / "_qa_alts_leftover_live.json"
    catalog_leftover = []
    if leftover_path.exists():
        try:
            catalog_leftover = json.loads(leftover_path.read_text(encoding="utf-8"))
        except Exception:
            catalog_leftover = []

    payload = {
        "date": time.strftime("%Y-%m-%d"),
        "pages_scanned": len(urls),
        "pages_with_missing": sum(1 for r in results if r.get("n", 0) > 0),
        "missing_count": len(all_missing),
        "by_page": sorted(
            [
                {
                    "url": r["url"],
                    "n": r["n"],
                    "h1": (r["missing"][0]["h1"] if r["missing"] else ""),
                    "items": r["missing"],
                }
                for r in results
                if r.get("n", 0) > 0
            ],
            key=lambda x: -x["n"],
        ),
        "all_missing": all_missing,
        "errors": [r for r in results if not r.get("ok")],
        "catalog_leftover_note": (
            "See tier2-catalog-alts-2026-09-16.html; re-verify separately"
            if catalog_leftover
            else ""
        ),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"missing imgs: {len(all_missing)} on {payload['pages_with_missing']} pages")
    for p in payload["by_page"][:20]:
        print(f"  {p['n']:3d}  {p['url']}")


if __name__ == "__main__":
    main()
