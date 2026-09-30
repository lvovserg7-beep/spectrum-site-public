# -*- coding: utf-8 -*-
import json
import re
import urllib.request
from pathlib import Path

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}

TAIL = [
    "/its",
    "/1cfresh",
    "/dopolnitelnie_licenzii",
    "/cra",
    "/publication",
    "/integrationeco",
    "/blog",
    "/persons",
    "/outsorce_vs_inhouse",
    "/whatsapp",
    "/crmfurniture",
    "/constr",
    "/cases",
    "/store",
]


def fetch(path: str) -> str:
    url = "https://alsn.ru" + path + "?bc=detail23"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def main() -> None:
    rows = []
    for path in TAIL:
        try:
            html = fetch(path)
            h1m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
            h1 = strip_tags(h1m.group(1) if h1m else "")
            titlem = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
            title = strip_tags(titlem.group(1) if titlem else "")
            m = re.search(
                r'aria-label=["\']Хлебные крошки["\'][\s\S]{0,1800}</nav>',
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
            if not m:
                style = "NONE"
            elif has_arrow:
                style = "ARROW"
            elif has_home:
                style = "CANON"
            else:
                style = "OTHER"

            last_vis = ""
            crumb = ""
            if m:
                crumb = strip_tags(m.group(0))[:200]
                spans = [
                    s.strip()
                    for s in re.findall(r"<span[^>]*>([^<]*)</span>", m.group(0))
                    if s.strip() and s.strip() != "/"
                ]
                last_vis = spans[-1] if spans else crumb

            bc_names: list[str] = []
            bc_ids: list[str] = []
            bc_invalid = False
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
                    bc_invalid = True
                    bc_names.append("INVALID")
                    continue
                graphs = data.get("@graph", [data] if isinstance(data, dict) else data)
                if not isinstance(graphs, list):
                    graphs = [graphs]
                for g in graphs:
                    if isinstance(g, dict) and g.get("@type") == "BreadcrumbList":
                        bc_ids.append(str(g.get("@id", "")))
                        for it in g.get("itemListElement") or []:
                            bc_names.append(it.get("name", ""))

            rows.append(
                {
                    "path": path,
                    "style": style,
                    "h1": h1,
                    "title": title,
                    "last_vis": last_vis,
                    "crumb": crumb,
                    "bc_names": bc_names,
                    "bc_ids": bc_ids,
                    "bc_invalid": bc_invalid,
                    "bc_count": len(bc_ids),
                }
            )
            print(
                f"{path} {style} | h1={h1[:60]} | vis={last_vis[:60]} | ld={bc_names} ids={bc_ids}"
            )
        except Exception as e:
            rows.append({"path": path, "style": "ERR", "error": str(e)})
            print(path, "ERR", e)

    out = Path(__file__).with_name("_bc-tail-detail-2026-09-23.json")
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved", out)


if __name__ == "__main__":
    main()
