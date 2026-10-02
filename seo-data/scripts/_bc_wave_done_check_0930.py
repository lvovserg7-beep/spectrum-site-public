# -*- coding: utf-8 -*-
"""Сверка живого alsn.ru с tier2-breadcrumbs-wave-2026-09-28.html (В-3...В-8)
и tier2-breadcrumbs-sitewide-2026-09-18.html (T2 case_telegram_bot), 30.09.2026."""
import html as H
import json
import random
import re
import time
import urllib.error
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}


def get(url):
    s = 0
    for _ in range(6):
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


def fresh(path):
    return get(f"https://alsn.ru{path}?v={random.randint(1, 10**7)}")


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
            out.append([("?сломанный JSON", "")])
            continue
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        for g in nodes:
            if isinstance(g, dict) and g.get("@type") == "BreadcrumbList":
                out.append([(it.get("name"), norm(it.get("item"))) for it in g.get("itemListElement") or []])
    return out


def navs(body):
    out = []
    for m in re.finditer(r'<nav[^>]*aria-label="Хлебные крошки"[^>]*>.*?</nav>', body, re.S):
        raw = m.group(0)
        rtag = re.findall(r'<div id="rec\d+"[^>]*>', body[:m.start()])
        bg = re.search(r"background-color:\s*(#[0-9a-fA-F]{3,6})", rtag[-1] if rtag else "")
        items = []
        for tag, attrs, inner in re.findall(r'<(a|span)\b([^>]*)>(.*?)</\1>', raw, re.S):
            t = txt(inner)
            if not t or t == "/":
                continue
            h = re.search(r'href="([^"]+)"', attrs)
            items.append((t, norm(h.group(1)) if tag == "a" and h else None))
        out.append({"bg": bg.group(1).lower() if bg else "", "items": items,
                    "home": "aria-label=\"Главная\"" in raw, "arrow": "→" in raw})
    return out


def t758(body):
    return [{"rec": m.group(1), "text": txt(m.group(2))[:150]}
            for m in re.finditer(r'<div id="rec(\d+)"[^>]*data-record-type="758"[^>]*>(.*?)(?=<div id="rec\d+")', body, re.S)]


ECOM = ("Интеграция с поставщиками", "/ecom")
DEV = ("Внедрение 1С", "/development1c")
SUP = ("Техподдержка 1С", "/support1c")

# (задача, путь, родители, имя; None = только проверить, что старого блока нет и крошки одни)
PAGES = [
    ("В-3", "/cracasesoftvideo", [("ЦРА", "/cra")], "Кейс «Софтвидео»"),
    ("В-4", "/persons/interw_lvov", [("Команда", "/persons")], "Интервью Сергея Львова"),
]
for p in ["/outsorce_vs_inhouse", "/review", "/merlion", "/ocs", "/marvel", "/treolan", "/3logic",
          "/constr", "/etm-ipro", "/perehod-s-upp-na-ka-unf-ut"]:
    PAGES.append(("В-6", p, None, None))
for p, n in [("/vtt", "ВТТ"), ("/dssl", "DSSL"), ("/elko", "Элко Рус"), ("/digis", "DIGIS"),
             ("/auvix", "AUVIX"), ("/resurs-media", "Ресурс-Медиа"), ("/russkiy-svet", "Русский Свет")]:
    PAGES.append(("В-7", p, [ECOM], n))
for p, par, n in [("/perehod-s-ut-na-unf", DEV, "Переход с УТ на УНФ"),
                  ("/perehod-s-dokumentooborota-2-1-na-3-0", DEV, "Переход на Документооборот 3.0"),
                  ("/perehod-s-ut-10-3", DEV, "Переход с УТ 10.3 на 11.5"),
                  ("/moy-sklad-perenos-v-1s", DEV, "Переход с МойСклад на 1С"),
                  ("/sinhronizaciya-bp-i-bp", SUP, "Синхронизация БП и БП"),
                  ("/sinhronizaciya-mezhdu-zup-i-zup", SUP, "Синхронизация ЗУП и ЗУП"),
                  ("/sinhronizaciya-mezhdu-ut-i-ut", SUP, "Синхронизация УТ и УТ")]:
    PAGES.append(("В-8", p, [par], n))
PAGES.append(("T2", "/case_telegram_bot", [("Кейсы", "/cases")], "Кейсы Telegram-ботов"))


def check(task, path, parents, name):
    st, page = fresh(path)
    if st != 200:
        return {"task": task, "path": path, "status": st, "probs": [f"страница отвечает {st}"]}
    i = page.find("</head>")
    head, body = page[:i], page[i:]
    probs = []
    nv = navs(body)
    old = t758(body)
    lh, lb = lds(head), lds(body)
    if not nv:
        probs.append("нет видимых крошек T123")
    elif len(nv) > 1:
        probs.append(f"видимых крошек T123 {len(nv)} шт.")
    if nv and (not nv[0]["home"] or nv[0]["arrow"]):
        probs.append("крошки не в виде дом + /")
    if old:
        probs.append("старый блок T758: " + " | ".join(f"rec{o['rec']} «{o['text']}»" for o in old))
    if "Главная →" in txt(body[:200000]):
        probs.append("на экране есть «Главная →»")
    if len(lh) + len(lb) != 1:
        probs.append(f"служебных путей {len(lh) + len(lb)} (HEAD {len(lh)}, холст {len(lb)})")
    vis = [x for x in (nv[0]["items"] if nv else []) if x[0] != "Главная"]
    if parents is not None:
        want_vis = [(n, u) for n, u in parents] + [(name, None)]
        want_ld = [("Главная", "/")] + list(parents) + [(name, path)]
        if nv and vis != want_vis:
            probs.append("на экране: " + " / ".join(t + (f"→{h}" if h else "") for t, h in vis))
        for l in lh + lb:
            if l != want_ld:
                probs.append("служебный путь: " + " / ".join(f"{n}({u})" for n, u in l))
    else:
        ldn = [[n for n, _ in l][1:] for l in lh + lb]
        visn = [t for t, _ in vis]
        if nv and ldn and ldn[0] != visn:
            probs.append(f"имена не совпадают: экран {visn}, код {ldn[0]}")
    return {"task": task, "path": path, "status": st, "vis": vis, "bg": nv[0]["bg"] if nv else "",
            "ld_head": lh, "ld_body": lb, "t758": old, "probs": probs}


def showcase_check():
    """В-5: универсальный скрипт в HEAD витрины и на карточке."""
    st, page = fresh("/1_obschepit_fastfood")
    head, body = page[:page.find("</head>")], page[page.find("</head>"):]
    r = {"task": "В-5", "path": "/1_obschepit_fastfood", "status": st, "probs": []}
    r["script_in_head"] = "alsn-bc-jsonld" in head
    r["ld_head"], r["ld_body"] = lds(head), lds(body)
    cards = sorted(set(re.findall(r'href="(https://alsn\.ru/1_obschepit_fastfood/tproduct/[^"]+)"', body)))
    r["card"] = cards[0] if cards else ""
    if not r["script_in_head"]:
        r["probs"].append("нет универсального скрипта карточек в HEAD витрины")
    if cards:
        time.sleep(3)
        cst, cp = get(cards[0] + f"?v={random.randint(1, 10**7)}")
        ch = cp[:cp.find("</head>")]
        r["card_status"] = cst
        r["card_script"] = "alsn-bc-jsonld" in ch
        r["card_ld_static"] = lds(ch)
        if not r["card_script"]:
            r["probs"].append("на карточке нет скрипта")
        if any(l and l[-1][0] == "Фастфуд и Общепит" for l in r["card_ld_static"]):
            r["probs"].append("на карточку протекает путь витрины")
    else:
        r["probs"].append("ссылок на карточки не найдено")
    return r


res = []
for t, p, par, n in PAGES:
    r = check(t, p, par, n)
    res.append(r)
    print(f"{t} {p:<45} {'OK' if not r['probs'] else '; '.join(r['probs'])}", flush=True)
    time.sleep(2 + random.random() * 2)
r = showcase_check()
res.append(r)
print(f"В-5 /1_obschepit_fastfood {'OK' if not r['probs'] else '; '.join(r['probs'])} | карточка {r.get('card')}", flush=True)

json.dump(res, open("_bc_wave_done_check_0930.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
