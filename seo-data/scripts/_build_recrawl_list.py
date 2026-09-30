# -*- coding: utf-8 -*-
"""Список URL на переобход после CSV title/descr/price. Не отправляет в Вебмастер."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
expected = json.loads((root / "_qa_alts_expected.json").read_text(encoding="utf-8"))
price_txt = (root.parent / "prices" / "_price-updates.txt").read_text(encoding="utf-8")

SKIP_SKU = {
    "4601546117588",  # 5 мест, переобход 15.09.2026
    "4601546117595",  # 10 мест
    "2900001833547",  # 20 мест
    "2900001833585",  # сервер x86-64
}

price_skus = []
for line in price_txt.splitlines():
    if not line.strip() or line.startswith("updated"):
        continue
    sku = line.split("\t", 1)[0].strip()
    if sku:
        price_skus.append(sku)
price_set = set(price_skus)

HUBS = [
    ("https://alsn.ru/dopolnitelnie_licenzii", "витрина доп. лицензий"),
    ("https://alsn.ru/its", "витрина 1С:КП / ИТС"),
    ("https://alsn.ru/1cfresh", "витрина 1С:Фреш"),
    ("https://alsn.ru/buhv8", "раздел Бухгалтерия"),
    ("https://alsn.ru/upt8", "раздел Управление торговлей"),
    ("https://alsn.ru/zup8", "раздел ЗУП"),
    ("https://alsn.ru/kompleksnaya_avtomatizaciya", "раздел КА"),
    ("https://alsn.ru/upravlenie_nashei_firmoi", "раздел УНФ"),
    ("https://alsn.ru/dokumentooborot8", "раздел Документооборот"),
    ("https://alsn.ru/products", "раздел Продукты"),
    ("https://alsn.ru/casemarketplace", "витрина модулей МП"),
    ("https://alsn.ru/support1c", "витрина техподдержки"),
]

# коммерческий приоритет карточек (Яндекс клики / GSC показы / цены)
PRIORITY_SKU = [
    "КППроф12",
    "КППроф12ЛЦ",
    "КПБаз12",
    "КПБаз12ЛЦ",
    "КППроф6",
    "КППроф3",
    "КПБаз6",
    "КПБаз8",
    "КПГУПроф12",
    "КПГУБаз12",
    "КПМед12",
    "2900002256680",  # КП УПП 12, GSC 289 показов; запрос «1с артикул 2900002256680»
    "КППроф8_4ЛЦ",
    "4601546092540",  # БП ПРОФ коробка
    "4601546116680",  # БП ПРОФ эл
    "4601546091970",  # БП КОРП коробка
    "2900001850445",  # БП КОРП эл
    "4601546117588",
    "4601546117595",
    "2900001833547",
    "2900001833585",
    "4601546122216",  # 1 место эл. если есть
]

by_sku = {}
by_uid = {}
for row in expected:
    url = (row.get("url") or "").split("?", 1)[0].rstrip("/")
    if "/tproduct/" not in url:
        continue
    sku = (row.get("sku") or "").strip()
    uid = str(row.get("uid") or "")
    item = {"sku": sku, "uid": uid, "title": row.get("title") or "", "url": url}
    if sku and sku not in by_sku:
        by_sku[sku] = item
    if uid and uid not in by_uid:
        by_uid[uid] = item

unique = {}
for row in expected:
    url = (row.get("url") or "").split("?", 1)[0].rstrip("/")
    if "/tproduct/" not in url:
        continue
    sku = (row.get("sku") or "").strip()
    if sku in SKIP_SKU:
        continue
    unique.setdefault(url, {"sku": sku, "title": row.get("title") or ""})

price_urls = []
seen_p = set()
for sku in price_skus:
    item = by_sku.get(sku)
    if not item:
        continue
    if item["sku"] in SKIP_SKU:
        continue
    if item["url"] in seen_p:
        continue
    seen_p.add(item["url"])
    price_urls.append(item)

prio_urls = []
seen_pr = set()
for sku in PRIORITY_SKU:
    item = by_sku.get(sku)
    if not item or item["sku"] in SKIP_SKU:
        continue
    if item["url"] in seen_pr:
        continue
    seen_pr.add(item["url"])
    prio_urls.append(item)

# КПБаз12ЛЦ и КППроф12 ищутся ещё по title, если sku в json другой
def find_title(*needles):
    out = []
    for url, meta in unique.items():
        blob = f"{meta['sku']} {meta['title']}".lower()
        if all(n.lower() in blob for n in needles):
            out.append({"sku": meta["sku"], "title": meta["title"], "url": url})
    return out

extra_names = [
    ("КПБаз12ЛЦ", find_title("базов", "12", "льгот")),
    ("1 место", find_title("клиентская", "1 ")),
]

lines_paste = []
for url, _ in HUBS:
    lines_paste.append(url)
for url in sorted(unique):
    lines_paste.append(url)

# дедуп paste preserving order
paste_seen = set()
paste = []
for u in lines_paste:
    if u not in paste_seen:
        paste_seen.add(u)
        paste.append(u)

out_dir = root.parent / "tilda-briefs"
out_txt = out_dir / "recrawl-catalog-2026-09-16.txt"
out_prio = out_dir / "recrawl-catalog-priority-2026-09-16.txt"

prio_block = []
prio_block.append("# Переобход после CSV title / description / price")
prio_block.append("# Дата списка: 16.09.2026")
prio_block.append("# Яндекс.Вебмастер alsn.ru: квота 960, остаток 960")
prio_block.append("# Не слать: ?editionuid=  и 4 карточки T1 (уже DONE 15.09)")
prio_block.append("# Bing / Twitter не трогать")
prio_block.append("")
prio_block.append(f"# Итого в буфер: {len(paste)} URL (12 витрин/разделов + {len(unique)} карточек)")
prio_block.append("")
prio_block.append("## 1. Витрины и разделы (обязательно)")
for url, name in HUBS:
    prio_block.append(f"{url}")
prio_block.append("")
prio_block.append(f"## 2. Сменилась цена в CSV ({len(price_urls)} шт.)")
for item in price_urls:
    prio_block.append(item["url"])
prio_block.append("")
prio_block.append("## 3. Коммерческий приоритет (КП / БП), если ещё нет в п.2")
for item in prio_urls:
    if item["url"] in seen_p:
        continue
    prio_block.append(item["url"])
prio_block.append("")
prio_block.append("## Не слать (уже переобход 15.09.2026 15:31, title KEEP)")
prio_block.append("https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-368525678472-1s-predpriyatie-8-prof-klientskaya-litse")
prio_block.append("https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-359060596292-1s-predpriyatie-8-prof-klientskaya-litse")
prio_block.append("https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-729293580752-1s-predpriyatie-8-prof-klientskaya-litse")
prio_block.append("https://alsn.ru/dopolnitelnie_licenzii/tproduct/1231123726-905369310501-1s-predpriyatie-83-prof-litsenziya-na-se")

out_txt.write_text("\n".join(paste) + "\n", encoding="utf-8")
out_prio.write_text("\n".join(prio_block) + "\n", encoding="utf-8")

print(f"unique_tproduct {len(unique)}")
print(f"hubs {len(HUBS)}")
print(f"paste {len(paste)}")
print(f"price {len(price_urls)}")
print(f"prio extra {sum(1 for i in prio_urls if i['url'] not in seen_p)}")
print("missing price sku:")
for sku in price_skus:
    if sku not in by_sku:
        print(f"  {sku}")
print("wrote", out_txt)
print("wrote", out_prio)
