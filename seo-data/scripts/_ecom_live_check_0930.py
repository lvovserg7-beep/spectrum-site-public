"""Проверка живой alsn.ru/ecom после переноса дизайна v3 (tier4-ecom-v3-2026-09-30.html)."""
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
h = urllib.request.urlopen(urllib.request.Request("https://alsn.ru/ecom?c=chk1346", headers={"User-Agent": UA})).read().decode("utf-8")
Path(__file__).with_name("_ecom_live_chk.html").write_text(h, encoding="utf-8")
head, body = h[:h.index("</head>")], h[h.index("<body"):]


def ok(cond, msg):
    print("OK " if cond else "!! ", msg)


print("title:", re.findall(r"<title>(.*?)</title>", head))
print("desc:", re.findall(r'<meta name="description" content="([^"]*)"', head))
print("og:title:", re.findall(r'<meta property="og:title" content="([^"]*)"', head))
print("og:desc:", re.findall(r'<meta property="og:description" content="([^"]*)"', head))
types = []
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head, re.S):
    try:
        d = json.loads(m.group(1))
        types.append(d.get("@type"))
        if d.get("@type") == "FAQPage":
            faq = d
        if d.get("@type") == "WebPage":
            print("WebPage dateModified:", d.get("dateModified"))
    except Exception as e:
        print("!! битый JSON-LD", e)
print("JSON-LD:", types)
ok(head.count("<style>") >= 1 and ".v3 .hf{" in head, "стили v3 в HEAD")
ok(".v3 .cmp.sup" in head and ".v3 .pane .shotz" in head, "стили таблицы и вкладок в HEAD")
ok("FAQPage" in types, "FAQPage в HEAD")
ok("\u2014" not in "".join(re.findall(r"<title>(.*?)</title>", head)), "в title нет длинного тире")

recs = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', body)]
print("== блоков на странице:", len(recs))
for i, (pos, rid, typ) in enumerate(recs):
    end = recs[i + 1][0] if i + 1 < len(recs) else len(body)
    t = re.sub(r"<(script|style).*?</\1>", " ", body[pos:end], flags=re.S)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
    print(f"{i+1:2d} rec{rid} T{typ} | {t[:100]}")

h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.S)
print("H1:", [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip() for x in h1])
ok(len(h1) == 1, "один H1")
ok(body.count('class="v3"') >= 3, f'блоков .v3: {body.count(chr(99)+"lass=" + chr(34) + "v3" + chr(34))}')
ok("Павел Агеев" in body and "ведущий аналитик 1С, эксперт по интеграциям" in body, "подпись Павла")
ok("4356795101" not in body, "галерея с картинками выключена")
for k in ("allsun-hero-ecom-sup", "case-xcom-video-cove", "ecom-1c-podbor-nalic", "ecom-1c-rezerv-u-pos", "ecom-1c-sopostavleni",
          "ecom-1c-ostatki-po-p", "ecom-1c-monitor-zagr", "ecom-1c-monitoring-a", "ecom-1c-otchet-rezer"):
    ok(k in body, "картинка " + k)
ok("ВСТАВЬТЕ" not in body and "../../" not in body, "нет заглушек и локальных путей")
old = ["Однократная оплата без ежегодного продления", "Проверьте эффективность и незадействованный", "Заказать аудит и расчет проекта",
       "Компании, занятые в интернет-торговле", "Что дает интеграция 1С с поставщиками по API", "Отзывы о работе Аллан",
       "Игорь Роганков рассказал", "Посмотреть клиентов"]
for s in old:
    ok(s not in body, "старый блок убран: " + s)
for s in ("Отправьте заявку на расчет", "У нас есть решение для", "Наши клиенты"):
    ok(s in body, "остался: " + s)

try:
    import build_ecom_v3_brief as br  # noqa
except SystemExit:
    pass
