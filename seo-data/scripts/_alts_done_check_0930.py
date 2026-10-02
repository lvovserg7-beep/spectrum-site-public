# -*- coding: utf-8 -*-
"""Сверка двух инструкций по alt с живым alsn.ru (30.09.2026).

Читает пункты из tier2-alts-sitewide-2026-09-21.html (волны 2 и 3)
и tier2-alts-tail-2026-09-28.html (кейс СЦ, кейс ХИТСАД, Клиенты),
скачивает страницы и для каждого пункта ставит статус:
  DONE  - у всех <img> с этим файлом на странице (в нужном rec) alt заполнен
  OPEN  - есть <img> с этим файлом и пустым alt
  GONE  - файла на странице больше нет
  BG    - файл есть только как фон (не <img>)
Результат: _alts_done_check_0930.json
"""
from __future__ import annotations

import html as H
import json
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
BRIEFS = ROOT.parent / "tilda-briefs"
SITEWIDE = BRIEFS / "tier2-alts-sitewide-2026-09-21.html"
TAIL = BRIEFS / "tier2-alts-tail-2026-09-28.html"
OUT = ROOT / "_alts_done_check_0930.json"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
IMG_RE = re.compile(r"<img\b([^>]*)>", re.I | re.S)
ATTR_RE = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.S)
REC_RE = re.compile(r'id="(rec\d+)"')
GENERIC = {"", "image", "img", "фото", "картинка", "picture"}


def fetch(url: str, tries: int = 5) -> str:
    for i in range(tries):
        u = f"{url}?v={random.randint(100000, 999999)}"
        req = urllib.request.Request(
            u,
            headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "ru-RU,ru;q=0.9",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return ""
            time.sleep(4 + i * 4)
        except Exception:
            time.sleep(4 + i * 4)
    raise RuntimeError(f"fetch failed: {url}")


def attrs(inner: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in ATTR_RE.finditer(inner):
        out[m.group(1).lower()] = m.group(2) if m.group(2) is not None else m.group(3)
    return out


def base(s: str) -> str:
    return urlparse(s).path.rsplit("/", 1)[-1]


def page_imgs(html: str) -> list[dict]:
    recs = [(m.start(), m.group(1)) for m in REC_RE.finditer(html)]
    out = []
    for m in IMG_RE.finditer(html):
        a = attrs(m.group(1))
        srcs = {base(a.get(k, "")) for k in ("src", "data-original", "data-src", "data-lazy-src") if a.get(k)}
        srcs.discard("")
        if not srcs:
            continue
        rec = ""
        for pos, rid in recs:
            if pos < m.start():
                rec = rid
            else:
                break
        out.append({"files": srcs, "alt": H.unescape(a.get("alt", "")).strip(), "rec": rec})
    return out


def status_for(html: str, imgs: list[dict], fn: str, rec: str | None = None) -> tuple[str, list[str]]:
    if not html:
        return "GONE", []
    hits = [i for i in imgs if fn in i["files"]]
    if rec:
        in_rec = [i for i in hits if i["rec"] == rec]
        if in_rec:
            hits = in_rec
    if not hits:
        if re.search(r"/" + re.escape(fn) + r"[\"')?]", html):
            return "BG", []
        return "GONE", []
    alts = [i["alt"] for i in hits]
    if all(a.lower() not in GENERIC for a in alts):
        return "DONE", alts
    return "OPEN", alts


def parse_sitewide(raw: str) -> list[dict]:
    items = []
    for m in re.finditer(
        r'<h3>(\d+)\. Файл <code>([^<]+)</code></h3>\s*<p class="muted">.*?<a href="([^"]+)"',
        raw, re.S,
    ):
        items.append({"brief": "sitewide", "wave": 2, "n": int(m.group(1)),
                      "file": H.unescape(m.group(2)), "url": m.group(3)})
    for m in re.finditer(
        r'<p><strong>(\d+)\.</strong>\s*страница «[^»]+» \((https://alsn\.ru[^)]*)\).*?файл в кабинете: ([^<\s]+)</p>',
        raw, re.S,
    ):
        items.append({"brief": "sitewide", "wave": 3, "n": int(m.group(1)),
                      "file": H.unescape(m.group(3)), "url": m.group(2)})
    return items


def parse_tail(raw: str) -> list[dict]:
    items = []
    for m in re.finditer(r'<article class="img">(.*?)</article>', raw, re.S):
        a = m.group(1)
        fn = re.search(r"Файл <code>([^<]+)</code>", a).group(1)
        url = re.search(r"\((https://alsn\.ru[^)]*)\)", a).group(1)
        rec = re.search(r"id (rec\d+)", a)
        pid = re.search(r'<pre id="(alt-\d+)">', a).group(1)
        items.append({"brief": "tail", "id": pid, "file": H.unescape(fn), "url": url,
                      "rec": rec.group(1) if rec else None})
    return items


def main() -> None:
    items = parse_sitewide(SITEWIDE.read_text(encoding="utf-8"))
    items += parse_tail(TAIL.read_text(encoding="utf-8"))
    urls = sorted({i["url"].rstrip("/") for i in items})
    extra = ["https://alsn.ru/clients", "https://alsn.ru/about_us",
             "https://alsn.ru/caseecomsc", "https://alsn.ru/xitsadmarketplace"]
    for u in extra:
        if u not in urls:
            urls.append(u)
    print(f"пунктов: {len(items)}, страниц: {len(urls)}")
    pages: dict[str, str] = {}
    for u in urls:
        try:
            pages[u] = fetch(u)
            print(f"  {u}: {len(pages[u])} байт")
        except Exception as e:
            pages[u] = None  # type: ignore
            print(f"  {u}: ОШИБКА {e}")
        time.sleep(random.uniform(2, 4))
    parsed = {u: page_imgs(h) for u, h in pages.items() if h}

    for it in items:
        u = it["url"].rstrip("/")
        h = pages.get(u)
        if h is None:
            it["status"], it["alts"] = "ERR", []
            continue
        st, alts = status_for(h, parsed.get(u, []), it["file"], it.get("rec"))
        it["status"], it["alts"] = st, alts
        if it.get("wave") == 2:
            per = {}
            for pu, ph in pages.items():
                if not ph:
                    continue
                s2, a2 = status_for(ph, parsed[pu], it["file"])
                if s2 in ("DONE", "OPEN"):
                    per[urlparse(pu).path] = s2
            it["other_pages"] = per

    for it in items:
        key = f"w{it['wave']}-{it['n']}" if it["brief"] == "sitewide" else it["id"]
        rec = it.get("rec") or ""
        print(f"{it['brief']:8} {key:8} {it['status']:5} {urlparse(it['url']).path:45} {it['file']:28} {rec:15} {it['alts']}")
        if it.get("other_pages"):
            print("            другие страницы:", it["other_pages"])

    summ: dict[str, dict[str, int]] = {}
    for it in items:
        summ.setdefault(it["brief"], {}).setdefault(it["status"], 0)
        summ[it["brief"]][it["status"]] += 1
    print("ИТОГ", summ)
    OUT.write_text(json.dumps({"date": "2026-09-30", "summary": summ, "items": items},
                              ensure_ascii=False, indent=1, default=list), encoding="utf-8")
    print("JSON", OUT)


if __name__ == "__main__":
    main()
