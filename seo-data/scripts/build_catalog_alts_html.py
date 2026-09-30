# -*- coding: utf-8 -*-
"""Build Tilda HTML instruction with product photo alts."""
from __future__ import annotations

import csv
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_store_seo import (  # noqa: E402
    SPACE_RE,
    core_name,
    delivery,
    delivery_short,
    kind,
)

CSV = Path(r"c:\Users\ALSN_LSA\Desktop\store-163322-202609161005-seo.csv")
LIVE = Path(__file__).with_name("_qa_alts_live.json")
OUT = Path(
    r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\tilda-briefs"
    r"\tier2-catalog-alts-2026-09-16.html"
)

KEEP_ALT = {
    "4601546117588": "Клиентская лицензия 1С ПРОФ на 5 рабочих мест",
    "4601546117595": "Клиентская лицензия 1С ПРОФ на 10 рабочих мест",
    "2900001833547": "Клиентская лицензия 1С ПРОФ на 20 рабочих мест",
    "2900001833585": "Лицензия 1С ПРОФ на сервер x86-64",
}
ALT_MAX = 125
STRIP_EXTRA = re.compile(
    r"\s*(?:Интернет-версия|через Интернет)\s*",
    re.I,
)


def restore_colon(s: str) -> str:
    if s.startswith("1С ") and not s.startswith("1С:"):
        return "1С:" + s[3:]
    return s


def variant_core(row: dict, title: str) -> str:
    core = core_name(title)
    parent = (row.get("Parent UID") or "").strip()
    seats = re.search(r"(?:^|[\s-])(\d+)\s*$", core)
    if parent and seats:
        n = int(seats.group(1))
        word = "место" if n == 1 else "мест"
        core = re.sub(r"[\s-]+\d+\s*$", "", core).strip()
        core = f"{core} на {n} {word}"
    core = STRIP_EXTRA.sub(" ", core)
    core = SPACE_RE.sub(" ", core).strip(" -.,")
    return restore_colon(core)


def fit(text: str) -> str:
    t = SPACE_RE.sub(" ", text).strip(" -.,")
    while len(t) > ALT_MAX and " " in t:
        t = t.rsplit(" ", 1)[0].rstrip(" ,.;-(")
    return t


def make_alt(row: dict) -> str:
    sku = (row.get("SKU") or "").strip()
    if sku in KEEP_ALT:
        return KEEP_ALT[sku]
    title = row.get("Title") or ""
    k = kind(row)
    if k == "support":
        alt = title.replace("Техподдержка по 1С", "Техподдержка 1С")
        alt = alt.replace(" / ", ", ")
        return fit(alt)
    if k == "mp":
        tlow = title.lower()
        if (
            "ozon" in tlow
            and "wildberries" not in tlow
            and "wb" not in tlow
            and "озон+wb" not in tlow
        ):
            return "Модуль интеграции 1С с Ozon"
        if "wildberries" in tlow and "ozon" not in tlow:
            return "Модуль интеграции 1С с Wildberries"
        return "Модуль интеграции 1С с Ozon и Wildberries"
    core = variant_core(row, title)
    if k == "fresh" and "фреш" not in core.lower() and "fresh" not in core.lower():
        core = "1С:Фреш " + core
    ds = delivery_short(delivery(row))
    alt = core
    if ds and ds not in alt.lower() and "поставк" not in alt.lower() and "коробк" not in alt.lower():
        alt = f"{alt}, {ds}"
    return fit(alt)


def photo_name(url: str) -> str:
    u = (url or "").strip().split("?")[0]
    if "/" not in u:
        return ""
    return u.rsplit("/", 1)[-1]


def cat_name(row: dict, by_uid: dict[str, dict]) -> str:
    cat = (row.get("Category") or "").split(";")[0].strip()
    if cat:
        return cat
    parent = (row.get("Parent UID") or "").strip()
    if parent and parent in by_uid:
        return cat_name(by_uid[parent], by_uid)
    return "Без раздела"


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


REDO_EMPTY_UID = {
    "889199487282",  # СНТ
    "920860758832",  # Договоры 8
    "601537363831",  # ЗУП КОРП эл
    "658261749802",  # 100 мест эл
    "293950783102",  # 300 мест эл
    "159637201592",  # 50 мест эл
    "556990081002",  # 500 мест эл
    "136066752982",  # цифровое животноводство
    "599820132332",  # СППР
    "729903995532",  # тепловодоканал
    "257692803132",  # теплосеть
    "909487433562",  # Фреш ИП
    "865515246452",  # КППроф8_4ЛЦ
    "579717645782",  # коробка 10
    "583281700322",  # коробка 100
    "758650958432",  # коробка 20
    "792021947492",  # коробка 300
    "206773331182",  # коробка 5
    "295893253862",  # коробка 50
    "308293969592",  # коробка 500
    "845146210291",  # Фастфуд коробка, родитель
    "413216341712",  # модуль Озон+WB, родитель
    "215664845112",  # техподдержка 3 часа, родитель
}
REDO_REWRITE_UID = {
    "837358323511": "1С:Общепит Клиентские лицензии на рабочие места на 20 мест, эл. поставка",
    "226213368711": "1С:Общепит. Клиентские лицензии на рабочие места на 5 мест",
}


def select_redo(items: list[dict]) -> list[dict]:
    """Empty alts plus two общепит parents with seat-count text on the shared photo."""
    redo = []
    for it in items:
        uid = it["uid"]
        if uid in REDO_REWRITE_UID:
            it = dict(it)
            it["why"] = "rewrite"
            it["live_alt"] = REDO_REWRITE_UID[uid]
            redo.append(it)
        elif uid in REDO_EMPTY_UID:
            it = dict(it)
            it["why"] = "empty"
            it["live_alt"] = ""
            redo.append(it)
    return redo


def main() -> None:
    with CSV.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    by_uid = {(r.get("Tilda UID") or "").strip(): r for r in rows}

    items = []
    for r in rows:
        sku = (r.get("SKU") or "").strip()
        alt = make_alt(r)
        if "—" in alt or "–" in alt or "Алсан" in alt:
            raise SystemExit(f"bad alt: {sku} {alt}")
        if alt.lower().startswith(("картинка", "изображение", "фото ")):
            raise SystemExit(f"bad start: {sku} {alt}")
        items.append(
            {
                "uid": (r.get("Tilda UID") or "").strip(),
                "sku": sku,
                "title": (r.get("Title") or "").strip(),
                "alt": alt,
                "cat": cat_name(r, by_uid),
                "parent": (r.get("Parent UID") or "").strip(),
                "url": (r.get("Url") or "").strip(),
                "photo": photo_name(r.get("Photo") or ""),
                "keep": sku in KEEP_ALT,
            }
        )

    items = select_redo(items)
    if not items:
        raise SystemExit("redo list empty")

    groups: dict[str, list] = defaultdict(list)
    for it in items:
        groups[it["cat"]].append(it)

    cat_order = sorted(groups, key=lambda c: (c == "Без раздела", c.lower()))

    toc = []
    body = []
    n = 0
    for i, cat in enumerate(cat_order, 1):
        cid = f"cat-{i}"
        toc.append(f'<li><a href="#{cid}">{esc(cat)}</a> ({len(groups[cat])})</li>')
        body.append(f'<section class="task" id="{cid}">')
        body.append(f"<h2>{esc(cat)}</h2>")
        for it in groups[cat]:
            n += 1
            sku = it["sku"]
            q = " ".join(
                [sku, it["title"], it["alt"], it["photo"], it["uid"]]
            ).lower()
            note = ""
            if it.get("why") == "rewrite":
                note = (
                    f'<p class="muted">Сейчас на сайте: <code>{esc(it.get("live_alt") or "")}</code>. '
                    "Заменить. Варианты 1/5/10/20 не открывать: одно фото на родителя.</p>"
                )
            elif it.get("why") == "empty":
                note = '<p class="muted">Сейчас Alt пустой. Вставить текст ниже.</p>'
            if not sku:
                find = (
                    "В поиске товаров вставьте название (артикула нет - это родитель вариантов)."
                )
                sku_block = (
                    f'<p class="muted">Артикула нет. Искать по названию.</p>'
                    f'<div class="copybox"><pre id="t-{n}">{esc(it["title"])}</pre>'
                    f'<button type="button" data-copy="t-{n}">Копировать название</button></div>'
                )
            else:
                find = "Товары → поиск → вставить артикул → открыть найденную карточку."
                sku_block = (
                    f'<p><strong>Арт.</strong> <code>{esc(sku)}</code></p>'
                    f'<div class="copybox"><pre id="s-{n}">{esc(sku)}</pre>'
                    f'<button type="button" data-copy="s-{n}">Копировать артикул</button></div>'
                )
            link = ""
            if it["url"]:
                link = (
                    f'<p class="muted"><a href="{esc(it["url"])}" target="_blank" rel="noopener">'
                    f"Открыть на сайте</a>"
                    f'{(" · файл фото: " + esc(it["photo"])) if it["photo"] else ""}</p>'
                )
            body.append(
                f'<article class="prod" data-q="{esc(q)}" data-n="{n}">'
                f'<label class="done"><input type="checkbox" data-key="{esc(it["uid"] or sku or str(n))}"> сделано</label>'
                f"<h3><span class=\"num\">{n}</span> {esc(it['title'])}</h3>"
                f"{note}"
                f'<span class="lbl">Как найти</span><p>{find}</p>'
                f"{sku_block}"
                f'<span class="lbl">Вставить в Alt</span>'
                f'<div class="copybox"><pre id="a-{n}">{esc(it["alt"])}</pre>'
                f'<button type="button" data-copy="a-{n}">Копировать Alt</button></div>'
                f"{link}"
                f"</article>"
            )
        body.append("</section>")

    page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Каталог Тильды - Alt у фото товаров - 16.09.2026</title>
  <style>
    :root {{
      --bg: #f4f3ef; --card: #fff; --text: #1a1a1a; --muted: #5c5c5c;
      --border: #e2e2de; --ok: #1a7f4b; --ok-bg: #e8f6ee; --warn: #9a6700;
      --warn-bg: #fff6e0; --danger: #b42318; --danger-bg: #fdecea;
      --info: #0b6e99; --info-bg: #e8f4fa; --code: #0f172a;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      color: var(--text); background: var(--bg);
    }}
    .wrap {{ max-width: 920px; margin: 0 auto; padding: 24px 18px 72px; }}
    h1 {{ font-size: 26px; margin: 0 0 6px; letter-spacing: -0.02em; }}
    h2 {{ font-size: 20px; margin: 0 0 10px; }}
    h3 {{ font-size: 16px; margin: 0 0 8px; }}
    p {{ margin: 0 0 8px; }}
    a {{ color: #0b5cad; }}
    .muted {{ color: var(--muted); font-size: 14px; }}
    .pills {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 16px; }}
    .pill {{
      display: inline-block; padding: 3px 10px; border-radius: 999px;
      font-size: 12px; font-weight: 650; border: 1px solid var(--border); background: #fff;
    }}
    .pill.ok {{ color: var(--ok); background: var(--ok-bg); border-color: #c6e6d3; }}
    .pill.warn {{ color: var(--warn); background: var(--warn-bg); border-color: #f0dfa0; }}
    .pill.danger {{ color: var(--danger); background: var(--danger-bg); border-color: #f5c2c0; }}
    .pill.info {{ color: var(--info); background: var(--info-bg); border-color: #bddceb; }}
    .callout {{
      border-radius: 10px; padding: 12px 14px; margin: 12px 0 18px;
      border: 1px solid var(--border); background: var(--card); font-size: 14px;
    }}
    .callout.danger {{ background: var(--danger-bg); border-color: #f5c2c0; }}
    .callout.warn {{ background: var(--warn-bg); border-color: #f0dfa0; }}
    .callout.info {{ background: var(--info-bg); border-color: #bddceb; }}
    .toc {{
      background: var(--card); border: 1px solid var(--border);
      border-radius: 10px; padding: 12px 16px; margin: 0 0 20px;
    }}
    .toc ol {{ margin: 6px 0 0; padding-left: 22px; }}
    .toc li {{ margin: 3px 0; }}
    .toc a {{ text-decoration: none; }}
    .task {{
      background: var(--card); border: 1px solid var(--border);
      border-radius: 12px; padding: 16px 18px 18px; margin: 0 0 18px;
    }}
    .prod {{
      border-top: 1px solid var(--border); padding: 14px 0 4px; margin-top: 8px;
      position: relative;
    }}
    .prod:first-of-type {{ border-top: 0; margin-top: 0; }}
    .prod.is-done {{ opacity: 0.55; }}
    .num {{
      display: inline-block; background: #111; color: #fff; border-radius: 999px;
      font-size: 12px; font-weight: 700; padding: 2px 10px; margin-right: 6px;
    }}
    .lbl {{
      display: block; font-size: 11px; font-weight: 700; letter-spacing: 0.04em;
      text-transform: uppercase; color: var(--muted); margin: 14px 0 4px;
    }}
    ol.steps {{ margin: 4px 0 0; padding-left: 22px; }}
    ol.steps > li {{ margin: 6px 0; }}
    .path {{
      font-family: ui-monospace, Consolas, monospace; font-size: 12.5px;
      background: #111; color: #f5f5f4; border-radius: 8px;
      padding: 8px 10px; margin: 6px 0 8px; overflow-x: auto;
    }}
    .copybox {{ position: relative; margin: 6px 0 10px; }}
    .copybox pre {{
      margin: 0; background: var(--code); color: #e5e7eb; border-radius: 10px;
      padding: 12px 12px 40px; overflow-x: auto; white-space: pre-wrap;
      word-break: break-word; font: 13px/1.4 ui-monospace, Consolas, monospace;
    }}
    .copybox button, button.inline-copy {{
      position: absolute; right: 8px; bottom: 8px; background: #fff;
      border: 1px solid #ccc; border-radius: 8px; padding: 4px 10px;
      font-size: 12px; font-weight: 650; cursor: pointer;
    }}
    button.inline-copy {{ position: static; margin-left: 6px; }}
    .copybox button:hover, button.inline-copy:hover {{ background: #f3f4f6; }}
    .copybox.ok button, button.inline-copy.ok {{ background: var(--ok-bg); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; margin: 6px 0 0; background: #fff; }}
    th, td {{ border: 1px solid var(--border); padding: 7px 9px; text-align: left; vertical-align: top; }}
    th {{ background: #fafaf8; font-weight: 650; }}
    .sticky {{
      position: sticky; top: 0; z-index: 5; background: var(--bg);
      padding: 10px 0 12px; margin: 0 0 8px;
    }}
    .sticky input {{
      width: 100%; padding: 10px 12px; border: 1px solid var(--border);
      border-radius: 10px; font-size: 15px;
    }}
    .done {{
      position: absolute; right: 0; top: 14px; font-size: 13px; color: var(--muted);
    }}
    .hidden {{ display: none !important; }}
    @media print {{
      body {{ background: #fff; }}
      .copybox button, .sticky, .done {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Alt у фото товаров - остаток</h1>
    <p class="muted">Живая Тильда alsn.ru · 16.09.2026 · только то, что ещё пустое или с чужим текстом. {len(items)} карточек. Остальные 295 не трогать. Файл открывать локально, на сайт не заливать.</p>
    <div class="pills">
      <span class="pill danger">остаток после проверки</span>
      <span class="pill info">каталог товаров</span>
      <span class="pill ok">CSV alt не умеет - только руками</span>
      <span class="pill warn">Twitter / X - SKIP</span>
      <span class="pill danger">Bing - SKIP</span>
      <span class="pill">robots.txt не трогать</span>
    </div>

    <div class="callout danger">
      Это инструкция для ручной вставки в кабинете Тильды. Title, цену и SEO-поля карточки не менять. Telegram-бот не снимать. Общий HEAD сайта (Organization / WebSite / имя «Аллсан Интеграция») не затирать.
    </div>

    <section class="task" id="how">
      <h2><span class="num">1</span> Куда вставлять</h2>
      <span class="lbl">Что сделать</span>
      <p>Добить Alt только у карточек из списка ниже. Готовые 295 не открывать.</p>
      <span class="lbl">Зачем</span>
      <p>Если картинка не загрузилась или человек пользуется программой чтения с экрана - виден текст. Поиск по картинкам тоже читает эту подпись. Через Excel/CSV Тильда alt не принимает.</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Кабинет Тильды → проект alsn.ru → <strong>Каталог</strong> / <strong>Товары</strong> (магазин, не страница витрины).</li>
        <li>В поиск вставьте <strong>артикул</strong> (кнопка «Копировать артикул»). Не ищите только по длинному названию.</li>
        <li>Откройте найденную карточку. Если это родитель с вариантами мест - править фото родителя, не карточку 1/5/10/20.</li>
        <li>Блок с фото (обычно слева от названия). Клик по превью картинки.</li>
        <li>Поле <strong>Alt</strong> / «SEO: alt-текст для изображения» / «Альтернативный текст» / «Описание изображения».</li>
        <li>Вставьте текст кнопкой «Копировать Alt» → <strong>Сохранить</strong> карточку.</li>
        <li>Мелкие иконки и SVG не заполнять. Логотип в шапке сайта не трогать.</li>
        <li>Когда пачка готова - если Тильда просит опубликовать витрину, это отдельный шаг в конце.</li>
      </ol>
      <div class="path">Товары → поиск по артикулу → карточка → фото → Alt → Сохранить</div>
      <p class="muted">Подробный приём для обычных блоков страницы (не каталог) - файл <code>tilda-how-to-alt-2026-09-11.html</code> в этой папке.</p>
    </section>

    <div class="callout warn">
      <strong>Не трогать:</strong> название товара, цена, SEO title / descr / keywords, текст карточки, JSON-LD, robots.txt, Twitter, Bing, Telegram-бот, HEAD сайта.
    </div>

    <div class="sticky">
      <input id="q" type="search" placeholder="Фильтр: артикул, название, alt..." />
      <p class="muted" id="stat">В списке {len(items)}. Отметьте «сделано», чтобы не потерять место.</p>
    </div>

    <div class="toc">
      <strong>Разделы</strong>
      <ol>
        {"".join(toc)}
      </ol>
    </div>

    {"".join(body)}

    <section class="task" id="pub">
      <h2><span class="num">2</span> Опубликовать витрины</h2>
      <span class="lbl">Что сделать</span>
      <p>Когда Alt на карточках сохранены - опубликовать витрины, если Тильда не вывела фото сразу.</p>
      <span class="lbl">Зачем</span>
      <p>Иначе подпись останется только в черновике товара.</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Страницы витрин: <a href="https://alsn.ru/dopolnitelnie_licenzii">/dopolnitelnie_licenzii</a>, <a href="https://alsn.ru/its">/its</a>, <a href="https://alsn.ru/1cfresh">/1cfresh</a> и остальные разделы каталога.</li>
        <li>Если просит публикацию страницы - «Опубликовать».</li>
      </ol>
    </section>

    <section class="task" id="skip">
      <h2>Что не делать</h2>
      <table>
        <tr><th>Пункт</th><th>Почему</th></tr>
        <tr><td>Писать alt в CSV и снова заливать каталог</td><td>Тильда это поле через выгрузку не принимает</td></tr>
        <tr><td>Вставлять alt в поле «Текст» карточки</td><td>Гость увидит подпись на экране</td></tr>
        <tr><td>Настройки Twitter / X</td><td>В Twitter не продвигаемся</td></tr>
        <tr><td>Bing</td><td>Bing не ведём</td></tr>
        <tr><td>Файл robots.txt</td><td>На Тильде его нельзя редактировать</td></tr>
        <tr><td>Снятие Telegram-бота</td><td>На живом сайте бота не снимаем</td></tr>
        <tr><td>HEAD всего сайта</td><td>Там данные компании на все страницы</td></tr>
        <tr><td>Карточки, которых нет в этом файле</td><td>Уже совпали при проверке 16.09.2026</td></tr>
        <tr><td>Отдельный Alt на 1 / 5 / 10 / 20 мест</td><td>Тильда держит одно фото на родителя</td></tr>
      </table>
    </section>

    <p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-catalog-alts-2026-09-16.html</code>. На alsn.ru не заливать.</p>
  </div>
  <script>
    function flash(btn) {{
      btn.classList.add("ok");
      const t = btn.textContent;
      btn.textContent = "Скопировано";
      setTimeout(() => {{ btn.textContent = t; btn.classList.remove("ok"); }}, 1200);
    }}
    document.querySelectorAll(".copybox button[data-copy]").forEach((btn) => {{
      btn.addEventListener("click", async () => {{
        const pre = document.getElementById(btn.getAttribute("data-copy"));
        if (!pre) return;
        await navigator.clipboard.writeText(pre.textContent);
        flash(btn);
      }});
    }});
    const KEY = "alsn-catalog-alts-redo-2026-09-16";
    const saved = JSON.parse(localStorage.getItem(KEY) || "{{}}");
    function refreshStat() {{
      const cards = [...document.querySelectorAll(".prod")].filter((el) => !el.classList.contains("hidden"));
      const done = cards.filter((el) => el.querySelector("input") && el.querySelector("input").checked).length;
      document.getElementById("stat").textContent =
        "Показано " + cards.length + " из {len(items)}. Сделано в фильтре: " + done + ".";
    }}
    document.querySelectorAll(".prod input[type=checkbox]").forEach((box) => {{
      const k = box.getAttribute("data-key");
      if (saved[k]) {{
        box.checked = true;
        box.closest(".prod").classList.add("is-done");
      }}
      box.addEventListener("change", () => {{
        saved[k] = box.checked;
        localStorage.setItem(KEY, JSON.stringify(saved));
        box.closest(".prod").classList.toggle("is-done", box.checked);
        refreshStat();
      }});
    }});
    document.getElementById("q").addEventListener("input", (e) => {{
      const q = (e.target.value || "").trim().toLowerCase();
      document.querySelectorAll(".prod").forEach((el) => {{
        const hay = (el.getAttribute("data-q") || "");
        el.classList.toggle("hidden", q && !hay.includes(q));
      }});
      document.querySelectorAll("section.task").forEach((sec) => {{
        if (!sec.id || !sec.id.startsWith("cat-")) return;
        const vis = [...sec.querySelectorAll(".prod")].some((el) => !el.classList.contains("hidden"));
        sec.classList.toggle("hidden", q && !vis);
      }});
      refreshStat();
    }});
    refreshStat();
  </script>
</body>
</html>
"""
    if "—" in page or "–" in page:
        raise SystemExit("em dash in HTML")
    OUT.write_text(page, encoding="utf-8")
    print("wrote", OUT)
    print("items", len(items), "cats", len(groups))
    print("empty", sum(1 for i in items if i.get("why") == "empty"))
    print("rewrite", sum(1 for i in items if i.get("why") == "rewrite"))
    print("no_sku", sum(1 for i in items if not i["sku"]))


if __name__ == "__main__":
    main()
