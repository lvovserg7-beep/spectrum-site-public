# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from pathlib import Path

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
OUT = Path(__file__).resolve().parent / "_case-pages-detail-2026-09-23.txt"


def fetch(u: str) -> str:
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def textish(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


lines: list[str] = []
for path in ["/caseecomsc", "/xitsadmarketplace"]:
    html = fetch("https://alsn.ru" + path)
    lines.append(f"\n==== {path} ====")

    dm = re.search(
        r'name=["\']description["\']\s+content=["\']([^"\']*)["\']', html, re.I
    )
    desc = dm.group(1) if dm else ""
    lines.append(f"DESC: {desc}")
    lines.append(
        "  chars: "
        + f"×={'×' in desc} −={'−' in desc} —={'—' in desc} –={'–' in desc}"
    )

    lines.append(f"  Все кейсы: {'Все кейсы' in html}")
    has_arrow = bool(re.search("Главная\\s*→", html))
    lines.append(f"  Главная→: {has_arrow}")
    lines.append(f"  УФН: {'УФН' in html}  УНФ: {'УНФ' in html}")

    srcs = re.findall(
        r'href="(https://alsn\.ru[^"]*)"[^>]*>[^<]{0,40}Источник', html, re.I
    )
    lines.append(f"  Источник hrefs: {srcs}")

    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.I | re.S):
        t = textish(m.group(1))
        if "результат" in t.lower() or "достиг" in t.lower():
            lines.append(f"  H2: [{t}]")

    for m in re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    ):
        body = m.group(1).strip()
        try:
            json.loads(body)
            ok = "PARSE_OK"
        except Exception as e:
            ok = f"PARSE_FAIL {e}"
        if "BreadcrumbList" in body:
            typ = "BreadcrumbList"
        elif "Article" in body:
            typ = "Article"
        elif "WebPage" in body:
            typ = "WebPage"
        elif "Organization" in body:
            typ = "Organization"
        else:
            typ = "other"
        lines.append(f"  LD {typ}: {ok}")
        if typ == "BreadcrumbList":
            names = re.findall(r'"name"\s*:\s*"([^"]+)"', body)
            lines.append(f"    names={names}")
        if typ == "Article":
            for key in ("headline", "description", "url"):
                mm = re.search(rf'"{key}"\s*:\s*"([^"]*)"', body)
                if mm:
                    lines.append(f"    {key}={mm.group(1)[:120]}")

    # visible crumb last name
    cm = re.search(
        r'aria-label=["\']Хлебные крошки["\'][^>]*>(.*?)</nav>', html, re.I | re.S
    )
    if cm:
        lines.append(f"  crumbs text: [{textish(cm.group(1))[:200]}]")

    lines.append("  logo-like empty/filled:")
    for m in re.finditer(r"<img\b([^>]*)>", html, re.I):
        inn = m.group(1)
        src_m = re.search(r'(?:src|data-original)="([^"]+)"', inn)
        alt_m = re.search(r'alt="([^"]*)"', inn)
        if not src_m:
            continue
        fn = src_m.group(1).rsplit("/", 1)[-1].split("?")[0]
        low = fn.lower()
        if not any(
            x in low
            for x in (
                "logo",
                "tatneft",
                "lanit",
                "thumb_",
                "5e82004a",
                "c8561e49",
                "goodwood",
                "xcom",
                "logo11",
            )
        ) and low not in ("_.png",):
            continue
        alt = alt_m.group(1) if alt_m else ""
        mark = "EMPTY" if not alt.strip() else "OK"
        lines.append(f"    {mark} {fn} | [{alt}]")

OUT.write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT)
