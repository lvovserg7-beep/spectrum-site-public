# -*- coding: utf-8 -*-
"""Проверка живого alsn.ru: что из tier4-postavshiki-v3 и tier4-ecom-rezultaty уже сделано (30.09.2026).

Только чтение сайта. Вывод - по странице: HEAD, первый экран, основная часть, последний экран,
старые блоки выключены, заголовок вкладки. Для /ecom - стили Р-1 и раздельные кейс / видео Р-2.
"""
import html
import json
import os
import random
import re
import sys
import time
import urllib.request as u

HERE = os.path.dirname(os.path.abspath(__file__))
BR = os.path.join(HERE, "..", "tilda-briefs")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
SLUGS = ["merlion", "ocs", "treolan", "marvel", "digis", "elko", "3logic", "etm-ipro",
         "resurs-media", "auvix", "vtt", "dssl", "russkiy-svet"]
LIVE = json.load(open(os.path.join(HERE, "_sup_cards_live_0930.json"), encoding="utf-8"))


def get(url):
    for k in range(6):
        try:
            req = u.Request(f"{url}?v={random.randint(10**6, 10**7)}", headers={
                "User-Agent": UA, "Accept": "text/html,application/xhtml+xml", "Accept-Language": "ru-RU,ru;q=0.9",
                "Cache-Control": "no-cache"})
            return u.urlopen(req, timeout=40).read().decode("utf-8")
        except Exception as e:  # noqa: BLE001
            print("  повтор", url, e, file=sys.stderr)
            time.sleep(3 + 2 * k)
    raise RuntimeError(url)


def old_recs(slug):
    bl = LIVE[slug]["blocks"]
    i = next(k for k, x in enumerate(bl) if x["type"] == "180")
    j = next(k for k, x in enumerate(bl) if x["type"] == "795")
    return [x["rec"] for x in bl[i:j]]


def check_sup(slug):
    page = get(f"https://alsn.ru/{slug}")
    head, bodyh = page.split("</head>", 1)
    ready = open(os.path.join(BR, f"_head-{slug}-2026-09-30.txt"), encoding="utf-8").read()
    lds = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', ready, re.S)]
    faq = next(x for x in lds if x["@type"] == "FAQPage")
    name = next(x for x in lds if x["@type"] == "WebPage")["name"]
    q1 = faq["mainEntity"][0]["name"]
    title = re.search(r"<title>(.*?)</title>", head, re.S)
    title = html.unescape(title.group(1)).strip() if title else ""
    recs = old_recs(slug)
    alive = [r for r in recs if f'id="rec{r}"' in bodyh]
    res = {
        "1 HEAD": ".v3 .hf" in head and '"FAQPage"' in head and q1 in html.unescape(head),
        "2 первый экран": 'class="hf"' in bodyh or 'class="hf ' in bodyh,
        "3 основная часть": 'class="pass"' in bodyh,
        "4 последний экран": 'class="final"' in bodyh,
        "5 старое выключено": not alive,
        "6 заголовок": title == f"{name} - модуль обмена | Аллсан",
    }
    return res, {"title": title, "старых_осталось": f"{len(alive)}/{len(recs)}"}


def check_ecom():
    page = get("https://alsn.ru/ecom")
    head, bodyh = page.split("</head>", 1)
    return {
        "Р-1 стили": ".v3 .letter.vid{" in head,
        "Р-2 блок видео отдельно": 'class="letter vid"' in bodyh and "Видеоотзыв X-COM о работе с Аллсан" in bodyh,
        "Р-2 ссылка кейса в карточке": 'class="go" href="https://alsn.ru/caseecomsc"' in bodyh,
    }


if __name__ == "__main__":
    out = {}
    for s in SLUGS:
        r, info = check_sup(s)
        out[s] = {"checks": r, **info}
        print(s, " ".join(f"[{'+' if v else '-'}] {k}" for k, v in r.items()), info)
        time.sleep(random.uniform(2, 4))
    e = check_ecom()
    out["ecom"] = e
    print("ecom", " ".join(f"[{'+' if v else '-'}] {k}" for k, v in e.items()))
    json.dump(out, open(os.path.join(HERE, "_sup_ecom_done_check_0930.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
