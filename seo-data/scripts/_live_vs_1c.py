# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path
import xlrd

XLS = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\prices\price_1c.xls")
CSV = Path(r"C:\Users\ALSN_LSA\Desktop\store-163322-202609161005.csv")
OUT = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\prices\_live-showcase-prices.txt")

HUB = [
    ("4601546116697", 9400, "1 место эл."),
    ("2900001833561", 21300, "Сервер МИНИ эл."),
    ("4601546117588", 31800, "5 мест эл."),
    ("2900001833578", 74100, "сервер эл."),
    ("2900001833585", 126800, "сервер x64 эл."),
    ("4601546117595", 60900, "10 мест эл."),
    ("2900001833547", 114300, "20 мест эл."),
    ("2900001833554", 274300, "50 мест эл."),
    ("2900001847209", 527200, "100 мест эл."),
    ("2900002133608", 1563700, "300 мест эл."),
    ("2900002133615", 2600400, "500 мест эл."),
    ("4601546106780", 126800, "сервер x64 коробка"),
    ("4601546106773", 74100, "сервер коробка"),
    ("4601546109019", 21300, "Сервер МИНИ коробка"),
    ("4601546080875", 9400, "1 место коробка"),
    ("4601546080882", 31800, "5 мест коробка"),
    ("4601546080899", 60900, "10 мест коробка"),
    ("4601546080905", 114300, "20 мест коробка"),
    ("4601546080912", 274300, "50 мест коробка"),
    ("4601546080929", 527200, "100 мест коробка"),
    ("4601546080936", 1563700, "300 мест коробка"),
    ("4601546080943", 2600400, "500 мест коробка"),
]

ITS = [
    ("КППроф12", 68400), ("КППроф6", 36307), ("КППроф3", 20104),
    ("КПБаз12", 29004), ("КПБаз6", 15334), ("КППроф1", 9301),
    ("КППроф8_4ЛЦ", 38000),
    ("2900002577563", 26000), ("2900002577600", 52000), ("2900002577648", 104000),
    ("2900002577686", 156000), ("2900002577723", 208000),
    ("КПГУПроф12", 59988), ("КПГУБаз12", 28992), ("2900002256680", 89300),
    ("КПМед12", 66324), ("2900002577761", 13000),
    ("2900002577808", 15860), ("2900002577822", 31720), ("2900002577846", 63440),
    ("2900002577860", 95160), ("2900002577884", 126880),
    ("КППроф2", 14701), ("КППроф4", 25505), ("КППроф5", 30904),
    ("КППроф7", 41707), ("КППроф8", 47109), ("КППроф9", 52510),
    ("КППроф10", 57906), ("КППроф11", 63305),
    ("КПБаз1", 3927), ("КПБаз2", 6208), ("КПБаз3", 8488), ("КПБаз4", 10770),
    ("КПБаз5", 13052), ("КПБаз7", 17613), ("КПБаз8", 19865), ("КПБаз9", 22178),
    ("КПБаз10", 24458), ("КПБаз11", 26740),
    ("КППроф1ЛЦ", 7751), ("КППроф2ЛЦ", 12253), ("КППроф3ЛЦ", 16755),
    ("КППроф4ЛЦ", 21256), ("КППроф5ЛЦ", 25758), ("КППроф6ЛЦ", 30259),
    ("КППроф7ЛЦ", 34761), ("КППроф8ЛЦ", 39264), ("КППроф9ЛЦ", 43766),
    ("КППроф10ЛЦ", 48264), ("КППроф11ЛЦ", 52765), ("КППроф12ЛЦ", 57000),
    ("КППроф24ЛЦ", 102600),
    ("КПБаз1ЛЦ", 3273), ("КПБаз2ЛЦ", 5174), ("КПБаз3ЛЦ", 7077),
    ("КПБаз4ЛЦ", 8976), ("КПБаз5ЛЦ", 10879), ("КПБаз6ЛЦ", 12781),
    ("КПБаз7ЛЦ", 14682), ("КПБаз8ЛЦ", 16581), ("КПБаз9ЛЦ", 18484),
    ("КПБаз10ЛЦ", 20384), ("КПБаз11ЛЦ", 22286), ("КПБаз12ЛЦ", 24168),
]

FRESH_LIVE = [
    ("1С Касса Фреш Расширенный на 12 месяцев", 7200),
    ("1С Розница Фреш на 12 месяцев", 18100),
    ("1С Гаражи Фреш", 27500),
    ("1С МДЛП Фреш на 12 месяцев", 20500),
    ("1С Фреш Управляющий на 12 месяцев", 30800),
    ("1С Фреш Расчет квартплаты и бухгалтерия ЖКХ ПРОФ на 12 месяцев", 32200),
    ("1С Фреш Медицина Больница Интернет-версия на 12 месяцев", 21000),
    ("1С Фреш Медицина Больничная аптека Интернет-версия на 12 месяцев", 21000),
    ("1С Фреш Медицина Диетическое питание Интернет-версия на 12 месяцев", 31800),
    ("1С Фреш Медицина Клиническая лаборатория Интернет-версия на 12 месяцев", 24000),
    ("1С Фреш Медицина Регион Интернет-версия для интеграции с ЕГИСЗ на 12 месяцев", 21000),
    ("1С Садовод Фреш", 27500),
    ("1С CRM ПРОФ Фреш на 12 месяцев", 10000),
    ("1С:Фреш Касса. Стандартный на 12 месяцев", 4800),
    ("1С Бухгалтерия сельскохозяйственного предприятия Фреш ПРОФ на 12 месяцев", 33600),
    ("1С Фреш БизнесСтарт Нулевка на 12 месяцев", 2988),
    ("1С Фреш БизнесСтарт ИП без сотрудников на 12 месяцев", 6000),
    ("1С Фреш БизнесСтарт УСН и патент с сотрудниками на 12 месяцев", 7800),
    ("1С Фреш БизнесСтарт ОСН без бухгалтера на 12 месяцев", 10200),
]


def load_rec():
    wb = xlrd.open_workbook(str(XLS))
    sh = wb.sheet_by_index(0)
    rec = {}
    names = {}
    for r in range(2, sh.nrows):
        v = sh.cell_value(r, 0)
        if v in ("", None):
            continue
        sku = str(int(v)) if isinstance(v, float) and v == int(v) else str(v).strip()
        try:
            pf = float(sh.cell_value(r, 4))
        except (TypeError, ValueError):
            continue
        if pf > 0:
            rec[sku] = pf
            names[sku] = str(sh.cell_value(r, 1)).strip()
    return rec, names


def fmt(n):
    return f"{int(round(n)):,}".replace(",", " ")


def main():
    rec, names = load_rec()
    csv_rows = []
    with CSV.open(encoding="utf-8-sig", newline="") as f:
        csv_rows = list(csv.DictReader(f, delimiter=";"))
    by_sku = {(r.get("SKU") or "").strip(): r for r in csv_rows}

    lines = ["Живые витрины alsn.ru, проверка 16.09.2026. CSV на диске уже обновлён, сайт ещё нет."]
    lines.append("")

    def report(page, rows):
        lines.append(f"=== {page}")
        ok = miss = bad = 0
        bad_rows = []
        miss_rows = []
        for sku, live, *rest in rows:
            label = rest[0] if rest else names.get(sku, sku)
            if sku not in rec:
                miss += 1
                miss_rows.append((sku, live, label))
                continue
            if abs(live - rec[sku]) > 0.51:
                bad += 1
                csv_p = (by_sku.get(sku) or {}).get("Price")
                bad_rows.append((sku, live, rec[sku], csv_p, label))
            else:
                ok += 1
        lines.append(f"совпало {ok}, устарело {bad}, нет в прайсе 1С {miss}")
        for sku, live, recp, csv_p, label in bad_rows:
            lines.append(
                f"DIFF {sku}\tвитрина {fmt(live)}\t1С {fmt(recp)}\tCSV {csv_p}\t{label[:70]}"
            )
        for sku, live, label in miss_rows:
            lines.append(f"NO1C {sku}\tвитрина {fmt(live)}\t{label[:70]}")
        lines.append("")

    report("https://alsn.ru/dopolnitelnie_licenzii", [(a, b, c) for a, b, c in HUB])
    report("https://alsn.ru/its", [(a, b, names.get(a, a)) for a, b in ITS])

    # Fresh: match live name to CSV title then SKU
    lines.append("=== https://alsn.ru/1cfresh")
    ok = miss = bad = 0
    for live_name, live_p in FRESH_LIVE:
        hit = None
        key = live_name.lower()[:40]
        for r in csv_rows:
            t = (r.get("Title") or "").lower()
            if key[:25] in t or t[:25] in live_name.lower():
                hit = r
                break
        if not hit:
            # looser
            tokens = [w for w in re.split(r"\W+", live_name.lower()) if len(w) > 4]
            best = None
            best_n = 0
            for r in csv_rows:
                t = (r.get("Title") or "").lower()
                n = sum(1 for w in tokens if w in t)
                if n > best_n:
                    best_n = n
                    best = r
            hit = best if best_n >= 3 else None
        sku = (hit.get("SKU") if hit else "") or ""
        if sku not in rec:
            miss += 1
            lines.append(f"NO1C {sku or '-'}\tвитрина {fmt(live_p)}\t{live_name[:70]}")
            continue
        if abs(live_p - rec[sku]) > 0.51:
            bad += 1
            lines.append(
                f"DIFF {sku}\tвитрина {fmt(live_p)}\t1С {fmt(rec[sku])}\tCSV {hit.get('Price')}\t{live_name[:70]}"
            )
        else:
            ok += 1
    lines.append(f"фреш: совпало {ok}, устарело {bad}, нет в прайсе {miss}")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
