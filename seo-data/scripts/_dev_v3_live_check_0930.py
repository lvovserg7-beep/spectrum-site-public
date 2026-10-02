# -*- coding: utf-8 -*-
"""Проверка живой alsn.ru/development1c после переноса v3."""
import html
import json
import re
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
url = "https://alsn.ru/development1c?c=chk0930c"
req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://alsn.ru/"})
h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
outp = Path(__file__).with_name("_dev_v3_live_check_0930.txt")
htmlp = Path(__file__).with_name("_dev_v3_live_check_0930.html")
htmlp.write_text(h, encoding="utf-8")

head = h[: h.index("</head>")]
body = h[h.index("<body"):]
vis = re.sub(r"<(script|style).*?</\1>", " ", body, flags=re.S)
vis = html.unescape(re.sub(r"<[^>]+>", " ", vis))
vis = re.sub(r"\s+", " ", vis)

checks = []


def ok(name, cond, detail=""):
    checks.append(("OK" if cond else "FAIL", name, detail))


def strip(s):
    return re.sub(r"<[^>]+>", "", s)


h1s = [re.sub(r"\s+", " ", strip(x)).strip() for x in re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)]
title = re.search(r"<title>(.*?)</title>", head, re.S).group(1).strip()
desc = (re.search(r'<meta name="description" content="([^"]*)"', head) or type("x", (), {"group": lambda *a: ""})()).group(1)

ok("title дефис, без длинного тире", "\u2014" not in title and "\u2013" not in title and " - " in title, title)
ok("desc без длинного тире", "\u2014" not in desc and "\u2013" not in desc, desc[:120])
ok("H1 новый (под ключ, без УТ КА ERP в заголовке)", any("Внедрение 1С" in x and "под ключ" in x.lower() and "УТ" not in x for x in h1s) or any(x == "Внедрение 1С под ключ" for x in h1s), str(h1s))
ok("рамка первого экрана .hf", 'class="hf' in h or "class='hf" in h or "hf wide" in h)
ok("фото Софьи на первом экране", "Софья Мазницына" in h)
ok("фамилия без «и»: не Мазницина", "Мазницина" not in h)
ok("Софья не в блоке команды (нет второй карточки)", h.count("Софья Мазницына") <= 2, str(h.count("Софья Мазницына")))
ok("паспорт услуги", "Паспорт услуги" in vis)
ok("цена после звонка", "после звонка" in vis)
ok("лента Как идёт внедрение", "Как идёт внедрение" in vis)
ok("раздел конфигурации", "Какие конфигурации внедряем" in vis or "Какие конфигурации 1С внедряем" in vis)
ok("ссылка КА", "kompleksnaya_avtomatizaciya" in h)
ok("ссылка ERP", "erp-time-price" in h)
ok("ТОП 10 ЦРА ссылка на /cra", 'href="/cra"' in h or 'href="https://alsn.ru/cra"' in h)
ok("старая обложка Под ключ выключена", '"Под ключ". Без головной боли' not in vis and "Без головной боли и стресса" not in vis)
ok("старые тарифы выключены", "Разовое обращение" not in vis)
ok("старый FAQ-заголовок выключен или заменён", vis.count("Частые вопросы по внедрению 1С") == 0)
ok("один H1", len([x for x in h1s if "Внедрение" in x or "ключ" in x.lower()]) <= 1, str(h1s))
ok("нет заглушки фото", "ВСТАВЬТЕ_ССЫЛКУ" not in h)
ok("стили v3 в HEAD", ".v3 .hf{" in head or ".v3 .hf {" in head)
ok("шрифт Onest", "Onest" in head)
ok("нет депортамент", "депортамент" not in h)
ok("три типа внедрения", "Три типа внедрения" in vis)
ok("карточка консультационное", "Консультационное" in vis)
ok("карточка agile", "Agile" in vis)
ok("карточка проектное", "Проектное" in vis)
ok("MVP, не MPV", "MVP" in vis and "MPV" not in h)

lds = []
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
    try:
        lds.append(json.loads(m.group(1)))
    except Exception as e:
        checks.append(("FAIL", "JSON-LD parse", str(e)))

types = [d.get("@type") for d in lds]
ok("Service в HEAD", "Service" in types, str(types))
ok("WebPage в HEAD", "WebPage" in types)
ok("BreadcrumbList в HEAD", "BreadcrumbList" in types)
ok("FAQPage в HEAD", "FAQPage" in types)
ok("HowTo в HEAD", "HowTo" in types)

faq = next((d for d in lds if d.get("@type") == "FAQPage"), None)
nfaq = len((faq or {}).get("mainEntity") or [])
ok("FAQPage 8 вопросов", nfaq == 8, str(nfaq))
howto = next((d for d in lds if d.get("@type") == "HowTo"), None)
nht = len((howto or {}).get("step") or [])
ok("HowTo 5 шагов как на ленте", nht == 5, str(nht))

vis_faq = re.findall(r"<summary>(.*?)</summary>", h, re.S)
ok("видимый FAQ details", len(vis_faq) >= 8, str(len(vis_faq)))

ok("кнопка консультации popup", "#popup:konsultacia" in h)
ok("телефон 260-04-03 в финале", "260-04-03" in vis)

recs = list(re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body))
ok("есть T123 на холсте", any(m.group(2) == "131" for m in recs), str(len(recs)))

lines = [f"{st:4}  {name}" + (f"  | {detail}" if detail else "") for st, name, detail in checks]
fail = sum(1 for st, _, _ in checks if st == "FAIL")
okn = sum(1 for st, _, _ in checks if st == "OK")
report = (
    f"URL {url}\nH1 {h1s}\nTITLE {title}\nLD {types}\n"
    f"OK {okn}  FAIL {fail}  ALL {len(checks)}\n\n" + "\n".join(lines)
)
outp.write_text(report, encoding="utf-8")
print("FAIL" if fail else "OK", fail, "/", len(checks))
