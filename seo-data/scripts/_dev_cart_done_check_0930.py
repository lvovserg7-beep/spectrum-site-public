# Проверка живого alsn.ru: development1c v3 (Д-0..Д-7) и карточки модуля МП (К-4, К-5, К-7)
import json, random, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
OUT = Path(__file__).with_suffix(".txt")
lines = []


def log(s=""):
    print(s)
    lines.append(str(s))


def get(url):
    for i in range(6):
        u = url + ("&" if "?" in url else "?") + "v=" + str(random.randint(10**6, 10**7))
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "ru"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            log(f"  повтор {i+1}: {e}")
            time.sleep(random.uniform(2, 4))
    raise SystemExit("не скачалось: " + url)


# ---------- development1c ----------
log("=== development1c ===")
html = get("https://alsn.ru/development1c")
(Path(__file__).parent / "_dev_cart_done_check_0930.html").write_text(html, encoding="utf-8")
head, _, body = html.partition("</head>")

ref = (ROOT / "tilda-briefs/_head-development1c-2026-09-30.txt").read_text(encoding="utf-8")
ref_lines = [l.strip() for l in ref.splitlines() if l.strip()]
miss = [l for l in ref_lines if l not in head]
log(f"HEAD: строк эталона {len(ref_lines)}, нет в живом <head>: {len(miss)}")
for l in miss[:15]:
    log("   нет: " + l[:160])
log(f"  FAQPage в head: {'FAQPage' in head}; '.v3 .hf' в head: {'.v3 .hf' in head}; <style> в head: {head.count('<style')}")
for q in re.findall(r'"name":\s*"([^"]+\?)"', ref):
    log(f"  вопрос в head={q in head} на экране={q in body}: {q[:80]}")

new_marks = {
    "Д-3 рамка hf": 'class="hf',
    "Д-3 H1": "Внедрение 1С <br>под <span>ключ</span>",
    "Д-3 лента": "Как идёт внедрение",
    "Д-3 подпись Софьи": "<b>Софья Мазницына</b>",
    "Д-4 паспорт .pass": 'class="pass',
    "Д-4 #route": 'id="route"',
    "Д-4 #cfgs": 'id="cfgs"',
    "Д-4 #price": 'id="price"',
    "Д-4 консультационное": "онсультационн",
    "Д-4 agile": "gile",
    "Д-5 финал": "Разберём, какой контур 1С вам нужен",
}
for k, m in new_marks.items():
    log(f"  {k}: {body.count(m)}")
ph = re.findall(r'<img[^>]+src="([^"]+)"[^>]*alt="Софья Мазницына[^"]*"', body)
log(f"  Д-0 фото Софьи: {ph}")
log(f"  заглушка ВСТАВЬТЕ в HTML: {'ВСТАВЬТЕ' in html}")
log(f"  h1 на странице: {len(re.findall(r'<h1[ >]', body))}")

m = re.search(r'<div id="rec3989707201"[^>]*>', body)
log(f"  Д-2 крошки rec3989707201: {m.group(0) if m else 'НЕТ'}")
recs = re.findall(r'<div id="rec(\d+)" class="r t-rec[^"]*"([^>]*)>', body)
log(f"  всего t-rec: {len(recs)}")
for rid, attrs in recs[:12]:
    tp = re.search(r'data-record-type="(\d+)"', attrs)
    bg = re.search(r'background-color:\s*([^;"]+)', attrs)
    log(f"    rec{rid} T{tp.group(1) if tp else '?'} bg={bg.group(1) if bg else '-'}")

old = [
    "Без головной боли и стресса", "Внедрение 1С под ключ на платформе 1С:Предприятие",
    "Сергея Львова", "Особенности тарифа", "индивидуальная скидка",
    "Над вашим проектом работают три специалиста", "Благодарности за внедрение",
    "Почему выбирают", "Более 15 лет", "Этапы внедрения 1С", "Личный Кабинет",
    "Примеры работ по сопровождению 1С", "Переход с УТ 10.3", "Экономим до 50%",
    "Что если, я оплачу", "Полезные страницы по внедрению 1С", "Отправьте заявку на расчет",
    "Какие конфигурации 1С внедряем", "Внедрение и сопровождение 1С Документооборот 8",
]
log("  Д-6 старые фразы в теле:")
for s in old:
    log(f"    {body.count(s)} · {s}")

# ---------- карточки ----------
log("\n=== карточки модуля ===")
cards = {
    "OZON": "https://alsn.ru/casemarketplace/tproduct/913805053-713209120582-modul-integratsii-1s-s-ozon",
    "WB": "https://alsn.ru/casemarketplace/tproduct/913805053-553126495292-modul-integratsii-1s-s-wildberries",
    "OZON+WB": "https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz",
}
for name, url in cards.items():
    time.sleep(random.uniform(2, 4))
    h = get(url)
    (Path(__file__).parent / f"_cart_{name.replace('+','_')}_0930.html").write_text(h, encoding="utf-8")
    log(f"--- {name} {url}")
    log(f"  +300%: {h.count('+300%')}; 'БЕСПЛАТНО': {h.count('БЕСПЛАТНО')}; 'подскажет, куда и сколько': {h.count('подскажет, куда и сколько')}; 'на своё усмотрение': {h.count('на своё усмотрение')}")
    log(f"  sku itemprop: {re.findall(r'itemprop=.sku.[^>]*>', h)[:3]}")
    log(f"  sku текст: {re.findall(r'js-store-prod-sku[^>]*>([^<]*)<', h)[:3]}")
    log(f"  price_old: {re.findall(r'(?:js-product-price-old|price_old|js-store-prod-price-old)[^>]*>([^<]*)<', h)[:4]}")
    po = re.findall(r'"priceold"\s*:\s*"?([^,"}]*)', h)[:4]
    sj = re.findall(r'"sku"\s*:\s*"([^"]*)"', h)[:4]
    log(f"  priceold в json: {po}")
    log(f"  sku в json: {sj}")
    log(f"  44 000/79 000: {h.count('44 000')}/{h.count('79 000')}; 44000/79000: {h.count('44000')}/{h.count('79000')}")

OUT.write_text("\n".join(lines), encoding="utf-8")
