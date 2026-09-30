# -*- coding: utf-8 -*-
"""Четыре варианта первого экрана «Модуль 1С для маркетплейсов»: фото на весь экран, текст и кнопки на фото.

Берёт готовый макет preview-casemarketplace-v3.html и меняет в нём только крошки и первый экран.
Выход: seo-data/competitors/screens/preview-casemarketplace-hero-{a,b,c,d}.html
       seo-data/competitors/mp-hero-design-options-2026-09-30.html
"""
import io
import os
import re

import build_mp_hub_v3_preview as p

ROOT = p.ROOT
SCR = os.path.join(ROOT, "competitors", "screens")
PHOTO = "../../brand-images/allsun-hero-mp-employee-module.jpg"

p.main()
BASE = io.open(p.OUT, encoding="utf-8").read()

EYEBROW = '<div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>Модуль Аллсан для селлеров</div>'
H1 = "<h1>Модуль 1С <br>для <span>маркетплейсов</span></h1>"
LEAD = ('<p class="lead">Остатки и цены уходят из вашей 1С на обе площадки, заказы приходят обратно. '
        "Утром в 1С уже посчитана маржа за вчера по каждому товару на Ozon и Wildberries.</p>")
FACTS = ('<div class="facts"><span><b>Ozon и Wildberries</b> в одном модуле</span>'
         "<span><b>УТ, УНФ, КА, ERP</b></span><span><b>от 40 700 ₽</b> в год</span></div>")
WHO = '<div class="who"><b>Сергей Никешин</b> · ведущий разработчик модуля</div>'
IMG = (f'<img class="bg" src="{PHOTO}" alt="Сергей Никешин, ведущий разработчик модуля интеграции 1С '
       'с Ozon и Wildberries, за работой с отчётами модуля в 1С" fetchpriority="high">')


def btns(ghost):
    return ('<div class="btns"><a class="btn m" href="#popup:konsultacia">Показать на моём кабинете <span class="ar">→</span></a>'
            f'<a class="btn {ghost}" href="#price">Цена от 40 700 ₽</a></div>')


DAY_ITEMS = re.search(r'<div class="track">(.*?)</div>\s*</div></div>\s*</div>', BASE, re.S).group(1)

COMMON = """
/* первый экран: фото на весь экран */
.fh{position:relative;display:flex;align-items:center;min-height:calc(100vh - 110px);min-height:calc(100svh - 110px);overflow:hidden;background:#1b1b1b}
.fh img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:68% 40%}
.fh .veil{position:absolute;inset:0;pointer-events:none}
.fh .in{position:relative;z-index:2;width:100%}
.fh .txt{max-width:610px;padding:56px 0}
.fh h1{margin-bottom:22px}
.fh .lead{max-width:540px}
.fh .btns{margin-bottom:0}
.fh .who{position:absolute;z-index:3;right:28px;bottom:24px;font-size:12.5px;line-height:1.3;padding:7px 12px;border-radius:10px}
.fh .who b{font-weight:600}
.btn.w{background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.45)}
.btn.w:hover{background:rgba(255,255,255,.2)}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px}
.facts span{font-size:14px;padding:8px 12px;border-radius:10px}
.facts b{font-weight:700}
.crumb-bar .crumb{padding:14px 0}
@media(max-width:1000px){
 .fh{display:block;min-height:0}
 .fh img.bg{position:relative;display:block;height:auto;aspect-ratio:1/.82;object-position:64% 30%}
 .fh .veil{bottom:auto;height:82vw}
 .fh .txt{padding:0 0 34px;margin-top:-56px}
 .fh h1{font-size:44px}
 .fh .lead{font-size:17px;margin-bottom:24px}
 .fh .who{top:14px;right:14px;bottom:auto;font-size:11.5px}
 .fh .btns .btn{width:100%;justify-content:center}
}
"""

VARIANTS = {
    "a": {
        "name": "Тёмная вуаль слева",
        "about": "Фото на весь экран, слева тёмное затемнение, текст белый. Самый «дорогой» и контрастный вид, кнопки хорошо видны.",
        "crumb_bg": "#111111", "crumb_fg": "#cfcfcf",
        "css": """
.fh.a .veil{background:linear-gradient(90deg,rgba(17,17,17,.9) 0%,rgba(17,17,17,.74) 36%,rgba(17,17,17,.2) 62%,rgba(17,17,17,0) 78%)}
.fh.a h1{color:#fff}
.fh.a .lead{color:rgba(255,255,255,.86)}
.fh.a .who{background:rgba(17,17,17,.55);color:#fff;backdrop-filter:blur(6px)}
@media(max-width:1000px){.fh.a{background:#111}.fh.a .veil{background:linear-gradient(180deg,rgba(17,17,17,0) 50%,#111 100%)}}
""",
        "hero": lambda: f'<section class="fh a">{IMG}<div class="veil"></div><div class="in"><div class="txt">{EYEBROW}{H1}{LEAD}{btns("w")}</div></div>{WHO}</section>',
        "day": True,
    },
    "b": {
        "name": "Светлая вуаль и три факта",
        "about": "Фото на весь экран, слева светлая дымка в цвет сайта, текст тёмный. Ближе всего к остальным страницам, добавлены три коротких факта.",
        "crumb_bg": "#ffffff", "crumb_fg": "#8a8a8a",
        "css": """
.fh.b{background:#fff}
.fh.b .veil{background:linear-gradient(90deg,rgba(255,255,255,.97) 0%,rgba(255,255,255,.9) 34%,rgba(255,255,255,.35) 58%,rgba(255,255,255,0) 72%)}
.fh.b .facts span{background:#fff;border:1px solid var(--line);color:#3d4247}
.fh.b .facts b{color:var(--ink)}
.fh.b .who{background:rgba(255,255,255,.9);color:var(--ink);border:1px solid var(--line)}
@media(max-width:1000px){.fh.b .veil{background:linear-gradient(180deg,rgba(255,255,255,0) 50%,#fff 100%)}}
""",
        "hero": lambda: f'<section class="fh b">{IMG}<div class="veil"></div><div class="in"><div class="txt">{EYEBROW}{H1}{LEAD}{FACTS}{btns("g")}</div></div>{WHO}</section>',
        "day": True,
    },
    "c": {
        "name": "Белая карточка на фото",
        "about": "Фото без затемнения, чистое. Текст и кнопки на белой карточке поверх снимка слева. Видно и фото, и склад, и экраны 1С.",
        "crumb_bg": "#ffffff", "crumb_fg": "#8a8a8a",
        "css": """
.fh.c .veil{background:rgba(0,0,0,.06)}
.fh.c .txt{background:#fff;border-radius:26px;padding:40px 40px 38px;max-width:590px;box-shadow:0 20px 50px rgba(0,0,0,.14)}
.fh.c h1{font-size:60px}
.fh.c .lead{font-size:18px;margin-bottom:28px}
.fh.c .who{background:none;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.7);padding:0}
@media(max-width:1000px){.fh.c{background:#fff}.fh.c .txt{padding:26px 22px 24px;margin:-48px 0 18px}.fh.c h1{font-size:40px}.fh.c .in{padding:0 14px}}
""",
        "hero": lambda: f'<section class="fh c">{IMG}<div class="veil"></div><div class="in"><div class="txt">{EYEBROW}{H1}{LEAD}{btns("g")}</div></div>{WHO}</section>',
        "day": True,
    },
    "d": {
        "name": "Фото в рамке, текст на фото",
        "about": "Фото не шире контента страницы, поэтому не мылится. Поля по бокам залиты графитом. Заголовок над мониторами, текст и кнопки в нижнем левом углу. Лента «Как выглядит день с модулем» отдельным светлым блоком ниже, как сейчас на сайте.",
        "crumb_bg": "#161616", "crumb_fg": "#cfcfcf",
        "css": """
.fh.d{display:block;min-height:0;background:#161616;padding:6px 0 34px;overflow:visible}
.fh.d .frame{position:relative;max-width:1184px;margin:0 auto;aspect-ratio:16/9;border-radius:24px;overflow:hidden;background:#0d0d0d;box-shadow:0 0 0 1px rgba(255,255,255,.08)}
.fh.d img.bg{object-position:50% 0}
.fh.d .veil{background:linear-gradient(180deg,rgba(0,0,0,.66) 0%,rgba(0,0,0,.3) 15%,rgba(0,0,0,0) 27%),radial-gradient(ellipse 48% 42% at 0% 100%,rgba(0,0,0,.88) 0%,rgba(0,0,0,.6) 50%,rgba(0,0,0,0) 100%)}
.fh.d .top{position:absolute;left:0;top:0;z-index:2;padding:clamp(16px,2.6vw,32px) clamp(18px,3.4vw,40px)}
.fh.d .top .eyebrow{margin-bottom:8px}
.fh.d .top h1{font-size:clamp(28px,3.8vw,46px);white-space:nowrap;margin:0;color:#fff}
.fh.d .bot{position:absolute;left:0;bottom:0;z-index:2;padding:0 clamp(18px,3.4vw,40px) clamp(18px,3vw,36px)}
.fh.d .bot .lead{color:rgba(255,255,255,.9);font-size:clamp(14px,1.45vw,18px);max-width:clamp(260px,29vw,350px);margin:0 0 clamp(12px,1.6vw,20px)}
.fh.d .bot .btn{padding:clamp(12px,1.3vw,16px) clamp(16px,1.9vw,24px);font-size:clamp(14px,1.3vw,16px)}
.fh.d h1,.fh.d .lead{text-shadow:0 1px 14px rgba(0,0,0,.5)}
.fh.d .who{top:auto;right:clamp(14px,2vw,22px);bottom:clamp(14px,2vw,22px);background:rgba(0,0,0,.5);color:#fff;backdrop-filter:blur(6px)}
@media(max-width:1240px){.fh.d .in.wrap{padding:0 28px}}
@media(max-width:1000px){
 .fh.d{padding:0 0 30px}
 .fh.d .in.wrap{padding:0}
 .fh.d .frame{aspect-ratio:auto;border-radius:0;overflow:visible;background:none;box-shadow:none}
 .fh.d img.bg{aspect-ratio:16/10;object-position:40% 25%}
 .fh.d .veil{height:62.5vw;background:linear-gradient(180deg,rgba(22,22,22,0) 55%,#161616 100%)}
 .fh.d .top,.fh.d .bot{position:static;padding:0 18px}
 .fh.d .top{margin-top:-40px}
 .fh.d .top h1{white-space:normal;font-size:40px;margin-bottom:16px}
 .fh.d .bot .lead{max-width:none;font-size:17px}
 .fh.d .bot .btn{padding:17px 26px;font-size:16px}
 .fh.d .who{top:14px;bottom:auto;right:14px}
}
""",
        "hero": lambda: (f'<section class="fh d"><div class="in wrap"><div class="frame">{IMG}<div class="veil"></div>'
                         f'<div class="top">{EYEBROW}<h1>Модуль 1С для <span>маркетплейсов</span></h1></div>'
                         f'<div class="bot">{LEAD}{btns("w")}</div>{WHO}</div></div></section>'),
        "day": True,
    },
    "e": {
        "name": "По эскизу: белое поле с текстом, фото справа, в рамке",
        "about": "Первый экран в рамке, как паспорт модуля, по ширине сайта. Слева на белом заголовок, текст и кнопки. Справа фото с мониторами и Сергеем, левый край фото плавно уходит в белый. Лента дня отдельным блоком ниже.",
        "crumb_bg": "#ffffff", "crumb_fg": "#8a8a8a",
        "css": """
.fh.e{display:block;min-height:0;background:#fff;overflow:visible;padding:4px 0 0}
.fh.e .frame{position:relative;height:clamp(400px,38vw,470px);border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff}
.fh.e img.bg{left:auto;right:0;width:60%;height:100%;object-fit:cover;object-position:62% 0}
.fh.e .veil{left:auto;right:0;width:60%;background:linear-gradient(90deg,#fff 0%,rgba(255,255,255,.6) 3%,rgba(255,255,255,0) 7%)}
.fh.e .txt{position:relative;z-index:2;height:100%;width:40%;max-width:none;padding:clamp(24px,3vw,40px);display:flex;flex-direction:column}
.fh.e h1{font-size:clamp(30px,3.1vw,42px);margin-bottom:14px}
.fh.e .lead{font-size:clamp(14.5px,1.3vw,17px);margin-bottom:20px;max-width:none}
.fh.e .btns{margin-top:auto;flex-wrap:nowrap;gap:10px}
.fh.e .btns .btn{padding:13px 16px;font-size:14.5px;white-space:nowrap}
.fh.e .who{background:rgba(255,255,255,.92);color:var(--ink);border:1px solid var(--line);right:16px;bottom:16px}
@media(min-width:1001px) and (max-width:1200px){.fh.e .btns{flex-wrap:wrap}.fh.e .txt{width:43%}.fh.e img.bg,.fh.e .veil{width:57%}}
@media(max-width:1000px){
 .fh.e .frame{height:auto}
 .fh.e img.bg{width:100%;height:auto;aspect-ratio:16/10;object-position:40% 25%}
 .fh.e .veil{left:0;width:100%;height:auto;aspect-ratio:16/10;bottom:auto;background:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff 100%)}
 .fh.e .txt{width:auto;height:auto;padding:0 20px 24px;margin-top:-10px}
 .fh.e h1{font-size:38px}
 .fh.e .btns{flex-wrap:wrap}.fh.e .btns .btn{padding:17px 26px;font-size:16px}
 .fh.e .who{top:12px;bottom:auto;right:12px}
}
""",
        "hero": lambda: (f'<section class="fh e"><div class="in"><div class="frame">{IMG}<div class="veil"></div><div class="txt">{EYEBROW}'
                         f'<h1>Модуль 1С <br>для <span>маркетплейсов</span></h1>{LEAD}{btns("g")}</div>{WHO}</div></div></section>'),
        "day": True,
    },
}


def build(key, v):
    html = BASE
    css = COMMON + v["css"]
    html = html.replace("</style>", css + "</style>", 1)
    html = re.sub(r"<title>.*?</title>", f"<title>Модуль 1С для маркетплейсов - первый экран, вариант {key.upper()}: {v['name']}</title>", html)
    crumb = (f'<div class="crumb-bar" style="background:{v["crumb_bg"]}"><div class="in crumb" style="color:{v["crumb_fg"]}">⌂ / Модуль 1С для маркетплейсов</div></div>')
    i = html.index('<div class="in crumb">')
    j = html.index("<!-- DAY TIMELINE -->") if v["day"] else html.index("<!-- BODY -->")
    html = html[:i] + crumb + "\n\n<!-- HERO -->\n" + v["hero"]() + "\n\n" + html[j:]
    assert "\u2014" not in html and "\u2013" not in html
    out = os.path.join(SCR, f"preview-casemarketplace-hero-{key}.html")
    io.open(out, "w", encoding="utf-8").write(html)
    return out


def index():
    cards = "".join(
        f'<a class="c" href="screens/preview-casemarketplace-hero-{k}.html"><div class="k">Вариант {k.upper()}</div>'
        f'<b>{v["name"]}</b><p>{v["about"]}</p><span>Открыть макет →</span></a>'
        for k, v in VARIANTS.items()
    )
    doc = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Первый экран «Модуль 1С для маркетплейсов» - 4 варианта - 30.09.2026</title>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;600;800&display=swap" rel="stylesheet">
<style>
body{{margin:0;font-family:'Onest',Arial,sans-serif;background:#F7F8FA;color:#212121}}
.w{{max-width:1100px;margin:0 auto;padding:48px 28px}}
h1{{font-size:40px;font-weight:800;letter-spacing:-.02em;margin:0 0 10px}}
.s{{color:#6b7075;font-size:16px;line-height:1.55;margin:0 0 30px;max-width:760px}}
.g{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}
.c{{display:block;background:#fff;border:1px solid #D7DADD;border-radius:20px;padding:24px 24px 22px;color:inherit;text-decoration:none}}
.c:hover{{border-color:#F55823}}
.k{{font-family:monospace;color:#F55823;font-size:13px;margin-bottom:8px}}
.c b{{font-size:20px}}.c p{{color:#3d4247;font-size:15px;line-height:1.5}}.c span{{color:#F55823;font-weight:600}}
.n{{margin-top:26px;font-size:14px;color:#6b7075;line-height:1.55}}
@media(max-width:800px){{.g{{grid-template-columns:1fr}}}}
</style></head><body><div class="w">
<h1>Первый экран: фото на весь экран</h1>
<p class="s">Страница «Модуль 1С для маркетплейсов» (https://alsn.ru/casemarketplace). Во всех вариантах фото Сергея занимает первый экран, заголовок, текст и кнопки лежат прямо на фото, подпись про разработчика маленькая. Ниже первого экрана страница такая же, как сейчас на сайте.</p>
<div class="g">{cards}</div>
<p class="n">Проверить телефон: открыть макет и сузить окно браузера или нажать F12 → значок телефона. Все четыре варианта перестраиваются под ширину 390 px.<br>
Фото сейчас 1024×576. На большом мониторе оно будет чуть мягким. Для запуска лучше исходник снимка от 1920 px по ширине.</p>
</div></body></html>"""
    out = os.path.join(ROOT, "competitors", "mp-hero-design-options-2026-09-30.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    return out


if __name__ == "__main__":
    for k, v in VARIANTS.items():
        print("ok", build(k, v))
    print("ok", index())
