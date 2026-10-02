# -*- coding: utf-8 -*-
"""Сверка живого alsn.ru с tier2-breadcrumbs-struktura-2026-09-30.html."""
import html as H
import json
import random
import re
import time
import urllib.request

import build_bc_struktura_0930 as B

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def get(url):
    s = 0
    for _ in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            s = e.code
            if s == 404:
                break
        except Exception:
            s = 0
        time.sleep(3 + random.random() * 3)
    return s, ""


def txt(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def norm(u):
    return (u or "").replace("https://alsn.ru", "").rstrip("/") or "/"


def lds(part):
    out = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', part, re.S | re.I):
        if "BreadcrumbList" not in m.group(1):
            continue
        try:
            data = json.loads(m.group(1))
        except Exception:
            out.append({"bad": True, "items": []})
            continue
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for g in nodes:
            if isinstance(g, dict) and g.get("@type") == "BreadcrumbList":
                out.append({"items": [(it.get("name"), norm(it.get("item"))) for it in g.get("itemListElement") or []]})
    return out


def navs(body):
    out = []
    for m in re.finditer(r'<nav[^>]*aria-label="Хлебные крошки"[^>]*>.*?</nav>', body, re.S):
        raw = m.group(0)
        rec = re.findall(r'<div id="rec(\d+)"[^>]*>', body[:m.start()])
        rtag = re.findall(r'<div id="rec\d+"[^>]*>', body[:m.start()])
        bg = re.search(r"background-color:\s*(#[0-9a-fA-F]{3,6})", rtag[-1] if rtag else "")
        col = re.search(r"color:\s*(#[0-9a-fA-F]{3,6})", raw)
        items = []
        for tag, attrs, inner in re.findall(r'<(a|span)\b([^>]*)>(.*?)</\1>', raw, re.S):
            t = txt(inner)
            if not t or t == "/":
                continue
            h = re.search(r'href="([^"]+)"', attrs)
            items.append((t, norm(h.group(1)) if tag == "a" and h else None))
        out.append({"rec": rec[-1] if rec else "", "bg": bg.group(1).lower() if bg else "",
                    "color": col.group(1).lower() if col else "", "items": items})
    return out


def check(path, parents, name, mode, bg_want=None):
    st, page = get(f"https://alsn.ru{path}?v={random.randint(1, 10**6)}")
    probs = []
    if st != 200:
        return {"path": path, "status": st, "probs": [f"страница отвечает {st}"]}
    i = page.find("</head>")
    head, body = page[:i], page[i:]
    want_vis = [(n, "/" + s) for n, s in parents] + [(name, None)]
    want_ld = [("Главная", "/")] + [(n, "/" + s) for n, s in parents] + [(name, path)]

    nv = navs(body)
    if not nv:
        probs.append("нет видимых крошек")
    elif len(nv) > 1:
        probs.append(f"видимых крошек {len(nv)} шт.")
    vis = nv[0]["items"] if nv else []
    tail = [x for x in vis if x[0] != "Главная"]
    if nv and tail != want_vis:
        probs.append("на экране: " + " / ".join(f"{t}{'→' + h if h else ''}" for t, h in tail))
    if nv and bg_want and nv[0]["bg"] != bg_want.lower():
        probs.append(f"фон T123 {nv[0]['bg'] or 'пустой'}, нужен {bg_want}")

    lh, lb = lds(head), lds(body)
    allld = lh + lb
    if len(allld) != 1:
        probs.append(f"служебных путей {len(allld)} (HEAD {len(lh)}, холст {len(lb)})")
    if mode == "showcase" and lh:
        probs.append("служебный путь витрины ещё в HEAD (протечёт на карточки)")
    if mode == "showcase" and not lb:
        probs.append("служебного пути нет в T123 на холсте")
    for l in allld:
        if l["items"] != want_ld:
            probs.append("служебный путь: " + " / ".join(f"{n}" for n, _ in l["items"]))
    card = re.search(r'href="(https://alsn\.ru/[^"]*/tproduct/[^"]+)"', body)
    return {"path": path, "status": st, "vis": vis, "ld": [l["items"] for l in allld],
            "card": card.group(1) if card else "", "probs": probs}


def card_check(url, showcase_name):
    st, page = get(url)
    head = page[:page.find("</head>")]
    bad = [l for l in lds(head) if l["items"] and l["items"][-1][0] == showcase_name]
    return st, len(bad)


res = []
for g in B.GROUPS:
    for p in g[4]:
        path, parents, name, mode = p[:4]
        bg = p[5] if len(p) > 5 else None
        r = check(path, parents, name, mode, bg)
        r["group"] = g[0]
        if mode == "showcase" and r.get("card"):
            st, leak = card_check(r["card"], name)
            if leak:
                r["probs"].append(f"на карточке товара виден путь витрины ({r['card']})")
        res.append(r)
        print(f"{g[0]} {path:<55} {'OK' if not r['probs'] else '; '.join(r['probs'])}")
        time.sleep(1)

json.dump(res, open("_bc_struct_verify_0930.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
