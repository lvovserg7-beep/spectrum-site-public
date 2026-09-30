# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

URLS = [
    "/",
    "/development1c",
    "/kompleksnaya_avtomatizaciya",
    "/erp-time-price",
    "/casemarketplace",
    "/ecom",
    "/support1c",
    "/its",
    "/1cfresh",
    "/dopolnitelnie_licenzii",
    "/about_us",
    "/contacts",
    "/vacancy",
    "/cra",
    "/clients",
    "/publication",
    "/telegram1c",
    "/bitrix24",
    "/etm-ipro",
    "/merlion",
    "/ocs",
    "/marvel",
    "/treolan",
    "/3logic",
    "/caseecomsc",
    "/xitsadmarketplace",
    "/cases",
    "/products",
    "/1cbitrix",
    "/buhv8",
    "/zup8",
    "/upt8",
    "/upravlenie_nashei_firmoi",
    "/dokumentooborot8",
    "/perehod-s-upp-na-ka-unf-ut",
    "/integrationsite",
    "/integrationeco",
    "/blog",
    "/internship",
    "/persons",
    "/review",
    "/outsorce_vs_inhouse",
    "/store",
    "/amo_crm",
    "/whatsapp",
    "/crmfurniture",
    "/constr",
]


def fetch(path: str) -> str:
    url = "https://alsn.ru" + ("" if path == "/" else path) + "?bc=2309e"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def audit_one(path: str) -> dict:
    html = fetch(path)
    m = re.search(
        r'aria-label=["\']Хлебные крошки["\'][\s\S]{0,1600}</nav>',
        html,
    )
    has_arrow = bool(re.search(r"Главная\s*→", html))
    has_home = bool(
        m
        and (
            'viewBox="0 0 24 24"' in m.group(0)
            or 'aria-label="Главная"' in m.group(0)
        )
    )
    bc = len(re.findall(r"BreadcrumbList", html))
    crumb = ""
    if m:
        crumb = re.sub(r"<[^>]+>", " ", m.group(0))
        crumb = re.sub(r"\s+", " ", crumb).strip()[:160]

    if not m:
        style = "NONE"
    elif has_arrow:
        style = "ARROW"
    elif has_home:
        style = "CANON"
    else:
        style = "OTHER"

    bc_names: list[str] = []
    bc_ok = True
    for block in re.finditer(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    ):
        body = block.group(1).strip()
        if "BreadcrumbList" not in body:
            continue
        try:
            data = json.loads(body)
        except Exception:
            bc_ok = False
            bc_names.append("INVALID_JSON")
            continue
        graphs = data.get("@graph", [data] if isinstance(data, dict) else data)
        if not isinstance(graphs, list):
            graphs = [graphs]
        for g in graphs:
            if isinstance(g, dict) and g.get("@type") == "BreadcrumbList":
                for it in g.get("itemListElement") or []:
                    bc_names.append(it.get("name", ""))

    # visible last crumb name
    last_vis = ""
    if m:
        spans = re.findall(r"<span[^>]*>([^<]*)</span>", m.group(0))
        names = [s.strip() for s in spans if s.strip() and s.strip() != "/"]
        if names:
            last_vis = names[-1]

    last_ld = bc_names[-1] if bc_names and bc_names[-1] != "INVALID_JSON" else ""
    name_match = bool(last_vis and last_ld and last_vis == last_ld)

    return {
        "path": path,
        "style": style,
        "bc_blocks": bc,
        "bc_ok": bc_ok,
        "bc_names": bc_names,
        "crumb": crumb,
        "last_vis": last_vis,
        "last_ld": last_ld,
        "name_match": name_match,
    }


def main() -> None:
    rows = []
    for path in URLS:
        try:
            row = audit_one(path)
            rows.append(row)
            print(
                f"{row['style']}|bc={row['bc_blocks']}|match={row['name_match']}|{path}|{row['crumb'][:90]}"
            )
        except Exception as e:
            rows.append(
                {
                    "path": path,
                    "style": "ERR",
                    "bc_blocks": 0,
                    "bc_ok": False,
                    "bc_names": [],
                    "crumb": str(e),
                    "last_vis": "",
                    "last_ld": "",
                    "name_match": False,
                }
            )
            print(f"ERR|0|{path}|{e}")

    out = Path(__file__).with_name("_bc-live-2026-09-23.json")
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SUMMARY", dict(Counter(r["style"] for r in rows)))
    print("OUT", out)


if __name__ == "__main__":
    main()
