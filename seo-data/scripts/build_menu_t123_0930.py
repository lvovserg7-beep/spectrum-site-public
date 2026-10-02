# -*- coding: utf-8 -*-
"""Боевой код шапки alsn.ru для T123 на странице Header (правило .cursor/rules/tilda-menu-v3.mdc).

В меню попадают только страницы, которые сейчас открываются на alsn.ru (проверка _menu_live_check_0930.py
пишет _menu_live_0930.json). Страницы, которых ещё нет, выпадают сами; после их публикации перезапустить
проверку и этот сборщик.

Выход:
  seo-data/tilda-briefs/_menu-t123-2026-09-30.txt      - код для вставки в T123
  seo-data/competitors/screens/preview-menu-t123-live.html - та же шапка над примером страницы
"""
import json
import re
from pathlib import Path

import build_menu_preview_0930 as bm

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
LIVE = HERE / "_menu_live_0930.json"
OUT_CODE = ROOT / "seo-data/tilda-briefs/_menu-t123-2026-09-30.txt"
OUT_PREVIEW = ROOT / "seo-data/competitors/screens/preview-menu-t123-live.html"

CONSULT = "#popup:konsultacia"
SEARCH = "#opensearch"
PHONE, PHONE_HREF = "+7 (495) 260-04-03", "tel:+74952600403"
EMAIL = "mail@alsn.ru"
LOGO = "https://static.tildacdn.com/tild6634-3863-4731-a232-653239393635/_5.png"
# Пока новой страницы нет, пункт ведёт на живую страницу с теми же товарами.
FALLBACK = {
    "/licenzii": "/products",
    "/licenzii-1c-buhgalteriya": "/buhv8",
    "/licenzii-1c-ut": "/upt8",
    "/licenzii-1c-ka": "/kompleksnaya_avtomatizaciya",
    "/licenzii-1c-zup": "/zup8",
    "/licenzii-1c-unf": "/upravlenie_nashei_firmoi",
}


def live_set():
    data = json.loads(LIVE.read_text(encoding="utf-8"))
    return {u for u, v in data.items() if not u.startswith("_") and v.get("status") == 200}


def ok(href, live):
    return not href.startswith("/") or href in live


def resolve(href, live):
    if ok(href, live):
        return href
    alt = FALLBACK.get(href, "")
    return alt if alt and ok(alt, live) else ""


def filter_menu(menu, live):
    out = []
    for name, allink, promo, cols in menu:
        allink = allink if allink and ok(allink[1], live) else None
        if promo:
            k, text, btn, href = promo
            href = CONSULT if href == bm.CONSULT_HREF else href
            href = resolve(href, live)
            promo = (k, text, btn, href) if href else None
        new_cols = []
        for t, href, d, kids in cols:
            if not ok(href, live):
                continue
            kids = [(k, resolve(h, live), n) for k, h, n in kids]
            kids = [x for x in kids if x[1]]
            if len(kids) == 1 and kids[0][1] == href:
                kids = []
            new_cols.append((t, href, d, kids))
        if new_cols:
            out.append((name, allink, promo, new_cols))
    return out


def header(menu):
    lis = []
    for i, sec in enumerate(menu):
        lis.append(f'<li><button type="button" aria-expanded="false" aria-controls="alsnP{i}">{bm.e(sec[0])}</button>'
                   f'{bm.panel_a(sec, "alsnP" + str(i))}</li>')
    return f"""<header class="mh" id="alsnMh">
<div class="in bar">
 <a class="logo" href="/" aria-label="Аллсан Интеграция, на главную"><img src="{LOGO}" alt="Аллсан Интеграция" width="120" height="54"></a>
 <nav aria-label="Основное меню"><ul class="top">{''.join(lis)}</ul></nav>
 <div class="tools">
  <div class="ph"><a href="{PHONE_HREF}">{PHONE}</a><small><a href="mailto:{EMAIL}">{EMAIL}</a></small></div>
  <a class="ic" href="{SEARCH}" aria-label="Поиск по сайту">{bm.ICON_SEARCH}</a>
  <a class="btn m" href="{CONSULT}">Получить консультацию</a>
  <button class="ic burger" type="button" aria-label="Открыть меню" aria-expanded="false">{bm.ICON_BURGER}</button>
 </div>
</div>
</header>
<div class="mh-sp" aria-hidden="true"></div>
<div class="mh-shade" id="alsnShade"></div>"""


def css():
    c = bm.CSS_A + bm.CSS_C
    c = c.replace(".mh{position:sticky;top:0;z-index:100;",
                  ".mh{position:fixed;top:0;left:0;right:0;z-index:990;")
    c = c.replace("z-index:90}", "z-index:980}").replace("z-index:120;", "z-index:995;")
    head = """
.mh,.mm,.mh-shade{--bg:#F7F8FA;--acc:#F55823;--ink:#212121;--line:#D7DADD;--soft:#FDE7DE;--mut:#6b7075}
.mh,.mm{font-family:Onest,system-ui,sans-serif;-webkit-font-smoothing:antialiased;text-align:left}
.mh *,.mm *{box-sizing:border-box}
.mh a,.mm a{color:inherit;text-decoration:none;border:0}
.mh ul,.mm ul{margin:0;padding:0}
.mh .in{max-width:1240px;margin:0 auto;padding:0 28px}
.mh .btn,.mm .btn{display:inline-flex;align-items:center;gap:10px;padding:12px 20px;border-radius:12px;font-weight:600;font-size:15px;line-height:1.2;white-space:nowrap;border:0;cursor:pointer;font-family:inherit}
.mh .btn.m,.mm .btn.m{background:var(--acc);color:#fff}
.mh .btn.m:hover,.mm .btn.m:hover{background:#e04c1a;color:#fff}
.mh .ph a{display:block}
.mh .ph small a{color:#9aa0a6}
.mh-sp{height:76px}
"""
    tail = """
@media(max-width:1000px){.mh .in{padding:0 18px}.mh-sp{height:64px}}
"""
    return head + c + tail


def js():
    return (bm.JS.replace("getElementById('mh')", "getElementById('alsnMh')")
            .replace("getElementById('mhShade')", "getElementById('alsnShade')")
            .replace("getElementById('mm')", "getElementById('alsnMm')"))


def mobile(menu):
    old = bm.MENU
    bm.MENU = menu
    try:
        m = bm.mobile()
    finally:
        bm.MENU = old
    return (m.replace('id="mm"', 'id="alsnMm"')
            .replace(bm.PHONE_HREF, PHONE_HREF).replace(f">{bm.PHONE}<", f">{PHONE}<")
            .replace(bm.CONSULT_HREF, CONSULT))


def minify_css(s):
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    s = re.sub(r"\s*\n\s*", "", s)
    return s


def code(menu):
    return (f"<!-- Шапка alsn.ru: чёрная полоса и белая мега-панель. Правило tilda-menu-v3.mdc. Собрано build_menu_t123_0930.py -->\n"
            f"{bm.FONTS}\n<style>{minify_css(css())}</style>\n"
            f"{header(menu)}\n{mobile(menu)}\n<script>{js().strip()}</script>\n")


def report(menu, live):
    dropped = []
    for name, allink, promo, cols in bm.MENU:
        refs = ([allink[1]] if allink else []) + ([promo[3]] if promo else [])
        for t, href, d, kids in cols:
            refs.append(href)
            refs += [h for _, h, _ in kids]
        dropped += [f"{name}: {u}" + (f" (пока ведёт на {FALLBACK[u]})" if u in FALLBACK else "")
                    for u in refs if u.startswith("/") and u not in live]
    return sorted(set(dropped))


def main():
    live = live_set()
    menu = filter_menu(bm.MENU, live)
    snippet = code(menu)
    OUT_CODE.write_text(snippet, encoding="utf-8")
    page = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Шапка alsn.ru для T123 (только живые страницы)</title>
<style>body{{margin:0;font-family:Arial,sans-serif;background:#fff}}.demo{{max-width:1240px;margin:0 auto;padding:40px 28px 1200px;color:#3d4247;font-size:16px;line-height:1.6}}</style>
</head><body>
<div class="t-rec">{snippet}</div>
<div class="demo"><h1 style="font-size:40px;color:#212121">Пример страницы под шапкой</h1>
<p>Это тот же код, что лежит в <code>seo-data/tilda-briefs/_menu-t123-2026-09-30.txt</code>. Поиск и кнопка «Получить консультацию» здесь не открываются: они работают только на сайте Тильды.</p></div>
<script>/* только для превью: #open=N раскрывает раздел, #mobile открывает мобильное меню */
(function(){{var h=location.hash,m=h.match(/open=(\\d)/),li=document.querySelectorAll('#alsnMh .top>li');
if(m&&li[m[1]])li[m[1]].querySelector('button').click();
if(h.indexOf('mobile')>-1){{document.querySelector('#alsnMh .burger').click();var d=document.querySelectorAll('#alsnMm>details');if(d[0]){{d[0].open=true;var dd=d[0].querySelector('details');if(dd)dd.open=true}}}}}})();</script>
</body></html>"""
    OUT_PREVIEW.write_text(page, encoding="utf-8")
    print(OUT_CODE, len(snippet.encode("utf-8")), "байт")
    print(OUT_PREVIEW)
    for name, allink, promo, cols in menu:
        print(f"[{name}] все: {allink[1] if allink else '-'} | промо: {promo[3] if promo else '-'}")
        for t, href, d, kids in cols:
            print(f"   {t} {href}" + (" -> " + ", ".join(h for _, h, _ in kids) if kids else ""))
    print("Не вошли (страниц ещё нет):", ", ".join(report(menu, live)))


if __name__ == "__main__":
    main()
