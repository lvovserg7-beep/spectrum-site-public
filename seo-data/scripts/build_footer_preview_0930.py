# -*- coding: utf-8 -*-
"""Общий подвал alsn.ru в паре с меню вариант C (tilda-menu-v3.mdc): макет HTML.

Ссылки берутся из MENU (build_menu_preview_0930) через тот же фильтр живых страниц, что и шапка
(build_menu_t123_0930: _menu_live_0930.json + FALLBACK). Контакты и соцсети - с текущего подвала T420 rec1209876901.
"""
import html
import subprocess
import time
import urllib.request
from pathlib import Path

import build_menu_preview_0930 as bm
import build_menu_t123_0930 as mt

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "seo-data/competitors/screens"
OUT = SCREENS / "preview-footer-v3.html"
OUT_CODE = ROOT / "seo-data/tilda-briefs/_footer-t123-2026-09-30.txt"
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}

ADDRESS = "Москва, Зеленоград, ул. Юности, д. 8, комната 503"
SOCIAL = [("VK", "https://vk.com/allsun_int"), ("Telegram", "https://t.me/alsnint"),
          ("YouTube", "https://www.youtube.com/channel/UC8cpwuRWOL9W6CTi8WubM1w")]
LEGAL = [("Политика обработки персональных данных", "/privacy"), ("Карта сайта", "/sitemap")]
# Реквизиты - как на странице «Контакты» (https://alsn.ru/contacts), сверено 30.09.2026
REQ = [
    ("Компания", "ООО «Аллсан Интеграция»"),
    ("Генеральный директор", "Львов С. А."),
    ("ОГРН", "1187746742611"),
    ("ИНН", "7735178314"),
    ("КПП", "773501001"),
    ("Юридический адрес", "124536, г. Москва, вн. тер. г. муниципальный округ Савелки, г. Зеленоград, ул. Юности, д. 8, помещ. 1/5"),
    ("Банк", "Московский филиал АО КБ «Модульбанк»"),
    ("БИК", "044525092"),
    ("Корр. счёт", "30101810645250000092"),
    ("Расчётный счёт", "40702810170010086510"),
]
DISCLAIMER = ('Телефон для регионов <a href="tel:88002600403">8 (800) 260-04-03</a>. '
              "Информация на сайте носит справочный характер и не является публичной офертой. Использование материалов сайта запрещено.")

# Блоки общего подвала Тильды rec984550646 / rec1250142141 (клиенты) и rec984444346 (сертификаты)
CLIENTS_WIDE = "https://static.tildacdn.com/tild6137-6133-4463-b034-623136346261/--.jpg"
CLIENTS_TALL = "https://static.tildacdn.com/tild3364-3436-4061-b165-623335386363/alsn-clients-vertica.jpg"
CERTS = [
    ("tild3735-3836-4238-b866-616161303866", "Сертификат соответствия",
     "Сертификат соответствия ГОСТ Р ИСО/МЭК 27001-2021 ООО «Аллсан Интеграция», № РОСС RU.32001.04ИБФ1.ОС44.73354"),
    ("tild3135-3535-4039-b633-363130313362", "Разрешение на знак",
     "Разрешение на применение знака соответствия «ПромТехСтандарт» ООО «Аллсан Интеграция», № РОСС RU.32001.04ИБФ1.ОС44.73354Р"),
]
CERT_FILE = "---ISO_pages-to-jpg-.jpg"


def e(s):
    return html.escape(s, quote=True)


def alive(path):
    for _ in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(f"https://alsn.ru{path}?f=3", headers=UA), timeout=30) as r:
                return r.status == 200
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return False
        except Exception:
            pass
        time.sleep(3)
    return False


def columns(menu):
    """Раздел меню -> колонка подвала: страницы 2-го уровня и их главные дети без дублей."""
    cols = []
    for name, allink, _promo, sec_cols in menu:
        links, seen = [], set()
        if allink:
            links.append((allink[0], allink[1]))
            seen.add(allink[1])
        for title, href, _d, kids in sec_cols:
            if href not in seen:
                links.append((title, href))
                seen.add(href)
            if name in ("Продукты", "Лицензии") or title == "Битрикс24" and name == "Услуги":
                for k, h, _n in kids:
                    if h not in seen and h not in mt.FALLBACK.values():
                        links.append((k, h))
                        seen.add(h)
        cols.append((name, links))
    by = dict(cols)
    company = by.pop("О компании", []) + by.pop("Наш опыт", [])
    order = ["О компании", "Кейсы", "Отзывы", "Команда", "Реальная автоматизация", "СМИ о нас", "Блог", "Вакансии", "Для стажёров", "Контакты"]
    company.sort(key=lambda x: order.index(x[0]) if x[0] in order else 99)
    rename = {"Внедрение 1С под ключ": "Внедрение 1С", "Интеграция 1С с маркетплейсами": "Модуль 1С для маркетплейсов",
              "Интеграция 1С с поставщиками B2B": "Интеграция с поставщиками", "Чат-боты 1С для мессенджеров": "Чат-боты 1С",
              "Ozon": "Интеграция 1С с Ozon", "Wildberries": "Интеграция 1С с Wildberries", "Телеграм-бот 1С": "Telegram-бот 1С",
              "Реальная автоматизация": "Реальная автоматизация, ТОП 10 ЦРА"}
    out = [(k, [(rename.get(t, t), h) for t, h in v]) for k, v in by.items()]
    out.append(("Компания", [(rename.get(t, t), h) for t, h in company]))
    return out


CSS = """
.mf{--bg:#F7F8FA;--acc:#F55823;--ink:#212121;--line:#D7DADD;--mut:#6b7075;font-family:Onest,system-ui,sans-serif;background:#111214;color:#cfd2d6}
.mf,.mf *{box-sizing:border-box}
.mf a{color:inherit;text-decoration:none}
.mf .in{max-width:1240px;margin:0 auto;padding:0 28px}
.mf .btn{display:inline-flex;align-items:center;gap:10px;padding:12px 20px;border-radius:12px;font-weight:600;font-size:15px;white-space:nowrap;border:0;cursor:pointer;font-family:inherit;background:var(--acc);color:#fff}
.mf .btn:hover{background:#e04c1a}
.mf .top{display:grid;grid-template-columns:300px minmax(0,1fr);gap:56px;padding:64px 0 48px}
.mf .brand img{height:54px;width:auto;display:block;margin-bottom:18px}
.mf .brand p{margin:0 0 20px;font-size:14.5px;line-height:1.55;color:#9aa0a6;max-width:280px}
.mf .ph{display:block;font-weight:700;font-size:22px;color:#fff;margin-bottom:4px}
.mf .ml{display:inline-block;font-size:15px;color:#e9eaec;margin-bottom:12px}
.mf .ml:hover,.mf .ph:hover{color:var(--acc)}
.mf address{font-style:normal;font-size:14px;line-height:1.5;color:#9aa0a6;margin-bottom:22px}
.mf .brand .btn{margin-bottom:24px}
.mf .soc{display:flex;flex-wrap:wrap;gap:8px}
.mf .soc a{padding:7px 12px;border:1px solid #3a3d42;border-radius:10px;font-size:13.5px;font-weight:500;color:#e9eaec}
.mf .soc a:hover{border-color:var(--acc);color:var(--acc)}
.mf .cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px}
.mf .col h3{margin:0 0 16px;display:flex;align-items:center;gap:8px;font-size:15px;font-weight:700;color:#fff}
.mf .col h3::before{content:"";width:14px;height:2px;background:var(--acc)}
.mf .col ul{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.mf .col li a{font-size:14.5px;line-height:1.4;color:#cfd2d6}
.mf .col li a:hover{color:var(--acc)}
.mf .col li.all a{color:var(--acc);font-weight:600}
.mf .trust{display:flex;flex-wrap:wrap;gap:10px;padding:22px 0;border-top:1px solid #2a2d31}
.mf .trust span{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;color:#e9eaec}
.mf .trust span::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--acc)}
.mf .trust span+span{margin-left:14px}
.mf .trust a{text-decoration:underline;text-decoration-color:#3a3d42;text-underline-offset:3px}
.mf .trust a:hover{color:var(--acc);text-decoration-color:var(--acc)}
.mf .bot{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 28px;padding:20px 0 28px;border-top:1px solid #2a2d31;font-size:13px;color:#8a8f95}
.mf .bot nav{display:flex;flex-wrap:wrap;gap:8px 24px}
.mf .bot a:hover{color:#fff}
.mf .right{min-width:0}
.mf .rq{border-top:1px solid #2a2d31;padding:14px 0}
.mf .rq summary{list-style:none;display:flex;align-items:center;gap:8px 18px;flex-wrap:wrap;cursor:pointer;font-size:13.5px;color:#9aa0a6}
.mf .rq summary::-webkit-details-marker{display:none}
.mf .rq .sh{font-variant-numeric:tabular-nums}
.mf .rq .tg{display:inline-flex;align-items:center;gap:6px;color:var(--acc);font-weight:600}
.mf .rq .tg::after{content:"";width:6px;height:6px;border-right:1.6px solid currentColor;border-bottom:1.6px solid currentColor;transform:rotate(45deg) translateY(-2px);transition:transform .2s}
.mf .rq[open] .tg::after{transform:rotate(-135deg) translateY(-1px)}
.mf .cp{margin-left:auto;padding:6px 12px;border-radius:9px;border:1px solid #3a3d42;background:transparent;color:#e9eaec;font:500 13px Onest,sans-serif;cursor:pointer}
.mf .cp:hover,.mf .cp.ok{border-color:var(--acc);color:var(--acc)}
.mf .rq dl{margin:14px 0 4px;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px 24px}
.mf .rq dl>div{min-width:0}
.mf .rq dl>div.w{grid-column:span 2}
.mf .rq dt{font-size:12px;color:#8a8f95;margin-bottom:2px}
.mf .rq dd{margin:0;font-size:13px;line-height:1.4;color:#e9eaec;overflow-wrap:anywhere;font-variant-numeric:tabular-nums}
.mf .req{padding:0 0 28px;font-size:12.5px;line-height:1.55;color:#6f757b;max-width:980px}
.mf .req a:hover{color:#fff}
.mf .srch{display:flex;align-items:center;gap:12px;height:52px;padding:0 8px 0 18px;margin:0 0 8px;border:1px solid #3a3d42;border-radius:14px;color:#9aa0a6;font-size:15px;margin-bottom:32px}
.mf .srch svg{width:18px;height:18px;flex:0 0 auto}
.mf .srch span{flex:1 1 auto}
.mf .srch b{padding:9px 16px;border-radius:10px;background:#1d1f22;color:#e9eaec;font-weight:600;font-size:14px}
.mf .srch:hover{border-color:var(--acc)}.mf .srch:hover b{background:var(--acc);color:#fff}
.mf .band{background:#fff;color:var(--ink);border-top:1px solid var(--line)}
.mf .band .grid{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:40px;padding:64px 0}
.mf .eyebrow{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--acc);margin-bottom:14px}
.mf .rails{display:flex;flex-direction:column;gap:4px}.mf .rails i{display:block;height:2px;width:22px;background:var(--acc);border-radius:2px}
.mf .band h2{margin:0 0 24px;font-size:32px;line-height:1.15;font-weight:800;letter-spacing:-.02em;color:var(--ink)}
.mf .logos{border:1px solid var(--line);border-radius:22px;padding:20px 24px;background:#fff}
.mf .logos img{display:block;width:100%;height:auto}
.mf .more{display:inline-flex;gap:8px;margin-top:16px;font-weight:600;font-size:15px;color:var(--acc)}
.mf .more::after{content:"→"}
.mf .certs{background:var(--bg);border:1px solid var(--line);border-radius:22px;padding:24px;display:flex;flex-direction:column;gap:14px}
.mf .certs h3{margin:0;font-size:20px;line-height:1.25;font-weight:800;color:var(--ink)}
.mf .certs p{margin:0;font-size:14px;line-height:1.5;color:#3d4247}
.mf .scans{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.mf .scan{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;padding:8px;position:relative}
.mf .scan img{display:block;width:100%;height:auto;border-radius:6px}
.mf .scan span{display:block;margin-top:8px;font-size:12.5px;font-weight:600;color:var(--ink);text-align:center}
.mf .scan:hover{border-color:var(--acc)}
.mf .certs .small{font-size:12.5px;color:var(--mut)}
.mf-lb{position:fixed;inset:0;z-index:1000;background:rgba(17,18,20,.88);display:none;align-items:center;justify-content:center;padding:24px;cursor:zoom-out}
.mf-lb.on{display:flex}
.mf-lb img{max-width:100%;max-height:100%;border-radius:8px;box-shadow:0 20px 60px rgba(0,0,0,.4)}
.mf-lb button{position:absolute;top:16px;right:16px;width:44px;height:44px;border-radius:12px;border:1px solid #3a3d42;background:#111214;color:#fff;font-size:22px;cursor:pointer}
@media(max-width:1180px){.mf .band .grid{grid-template-columns:minmax(0,1fr) 320px}}
@media(max-width:1180px){.mf .top{grid-template-columns:260px minmax(0,1fr);gap:40px}.mf .cols{gap:24px}}
@media(max-width:1000px){
 .mf .in{padding:0 18px}
 .mf .top{grid-template-columns:minmax(0,1fr);gap:8px;padding:44px 0 24px}
 .mf .brand{padding-bottom:28px;border-bottom:1px solid #2a2d31}
 .mf .brand img{height:44px}
 .mf .brand .btn{display:flex;justify-content:center;width:100%;padding:15px}
 .mf .cols{grid-template-columns:minmax(0,1fr);gap:0}
 .mf .col{border-bottom:1px solid #2a2d31;min-width:0}
 .mf .col details summary{list-style:none;display:flex;justify-content:space-between;align-items:center;padding:16px 0;cursor:pointer}
 .mf .col details summary::-webkit-details-marker{display:none}
 .mf .col details summary::after{content:"+";font-size:24px;line-height:1;color:var(--acc)}
 .mf .col details[open] summary::after{content:"−"}
 .mf .col h3{margin:0;font-size:17px}
 .mf .col ul{padding:0 0 18px 22px}
 .mf .trust{flex-direction:column;gap:10px}.mf .trust span+span{margin-left:0}
 .mf .bot{flex-direction:column}
 .mf .band .grid{grid-template-columns:minmax(0,1fr);gap:28px;padding:44px 0}
 .mf .band h2{font-size:26px}
 .mf .logos{padding:14px}
 .mf .srch b{display:none}
 .mf .rq{padding:14px 0}
 .mf .rq .sh{flex:1 1 100%}
 .mf .rq dl{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 16px}
}
@media(min-width:1001px){.mf .col details>summary{pointer-events:none;list-style:none}.mf .col details>summary::-webkit-details-marker{display:none}}
"""

JS = """
(function(){var q=window.matchMedia('(min-width:1001px)');
function sync(){document.querySelectorAll('#alsnMf .col details').forEach(function(d){d.open=q.matches;});}
sync();(q.addEventListener?q.addEventListener('change',sync):q.addListener(sync));
var lb=document.getElementById('alsnMfLb'),im=lb.querySelector('img');
function close(){lb.classList.remove('on');im.removeAttribute('src');}
document.querySelectorAll('#alsnMf [data-zoom]').forEach(function(a){a.addEventListener('click',function(ev){
ev.preventDefault();im.src=a.href;im.alt=a.querySelector('img').alt;lb.classList.add('on');});});
lb.addEventListener('click',close);
document.querySelectorAll('#alsnMf .cp').forEach(function(b){b.addEventListener('click',function(ev){
ev.preventDefault();ev.stopPropagation();var t=b.getAttribute('data-copy'),l=b.textContent;
function done(){b.textContent='Скопировано';b.classList.add('ok');setTimeout(function(){b.textContent=l;b.classList.remove('ok');},1800);}
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(done);}
else{var x=document.createElement('textarea');x.value=t;document.body.appendChild(x);x.select();document.execCommand('copy');x.remove();done();}});});
document.addEventListener('keydown',function(ev){if(ev.key==='Escape')close();});})();
"""


def band():
    scans = "".join(
        f'<a class="scan" href="https://static.tildacdn.com/{cid}/{CERT_FILE}" data-zoom>'
        f'<img src="https://thb.tildacdn.com/{cid}/-/resize/360x/{CERT_FILE}" alt="{e(alt)}" width="360" height="509" loading="lazy">'
        f'<span>{e(label)}</span></a>' for cid, label, alt in CERTS)
    return f"""<div class="band"><div class="in grid">
 <div class="cl">
  <div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>Наши клиенты</div>
  <h2>С нами работают торговые, производственные и IT-компании</h2>
  <div class="logos"><picture><source media="(max-width:480px)" srcset="{CLIENTS_TALL}">
   <img src="{CLIENTS_WIDE}" alt="Клиенты Аллсан: Татнефть, X-Com, Артис, Merlion, Норникель, ЛАНИТ, GoodWood, ПЭК, Импульс Телеком, Сокол, Атомспецтранс, Армтек, Brigo, Simon, Rapart" width="1680" height="525" loading="lazy"></picture></div>
  <a class="more" href="/clients">Отзывы клиентов</a>
 </div>
 <aside class="certs">
  <div class="eyebrow" style="margin:0"><span class="rails"><i></i><i></i><i></i></span>Сертификаты</div>
  <h3>Сертификат ISO 27001</h3>
  <p>ГОСТ Р ИСО/МЭК 27001-2021 (ISO/IEC 27001:2013), разработка компьютерного программного обеспечения.</p>
  <div class="scans">{scans}</div>
  <span class="small">Действует до 30.03.2028. Нажмите, чтобы открыть скан.</span>
 </aside>
</div></div>"""


def requisites():
    rows = "".join(f'<div class="{"w" if len(v) > 40 else ""}"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in REQ)
    plain = "\n".join(f"{k}: {v}" for k, v in REQ)
    short = " · ".join(f"{k} {v}" if k in ("ИНН", "КПП", "ОГРН") else v for k, v in REQ if k in ("Компания", "ИНН", "КПП", "ОГРН"))
    return (f'<details class="rq"><summary><span class="sh">{e(short)}</span>'
            f'<span class="tg">Все реквизиты</span>'
            f'<button type="button" class="cp" data-copy="{e(plain)}">Скопировать</button></summary>'
            f'<dl>{rows}</dl></details>')


SEARCH_BAR = ('<a class="srch" href="{hook}" aria-label="Поиск по сайту">'
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
              '<span>Поиск по сайту</span><b>Найти</b></a>')


def footer(cols, legal):
    col_html = []
    for name, links in cols:
        all_cls = ' class="all"'
        lis = "".join(
            f'<li{all_cls if t.startswith("Все ") else ""}><a href="{e(h)}">{e(t)}</a></li>' for t, h in links)
        col_html.append(f'<div class="col"><details open><summary><h3>{e(name)}</h3></summary><ul>{lis}</ul></details></div>')
    soc = "".join(f'<a href="{e(h)}" target="_blank" rel="noopener">{e(n)}</a>' for n, h in SOCIAL)
    leg = "".join(f'<a href="{e(h)}">{e(t)}</a>' for t, h in legal)
    return f"""<footer class="mf" id="alsnMf">
{band()}
<div class="in">
 <div class="top">
  <div class="brand">
   <a href="/" aria-label="Аллсан Интеграция, на главную"><img src="{mt.LOGO}" alt="Аллсан Интеграция" width="120" height="54"></a>
   <p>Внедряем, дорабатываем и сопровождаем 1С. Делаем свои модули для Ozon, Wildberries и поставщиков телеком и IT.</p>
   <a class="ph" href="{mt.PHONE_HREF}">{mt.PHONE}</a>
   <a class="ml" href="mailto:{mt.EMAIL}">{mt.EMAIL}</a>
   <address>{e(ADDRESS)}</address>
   <a class="btn" href="{mt.CONSULT}">Получить консультацию</a>
   <div class="soc">{soc}</div>
  </div>
  <div class="right">{SEARCH_BAR.format(hook=mt.SEARCH)}
  <nav class="cols" aria-label="Разделы сайта">{''.join(col_html)}</nav></div>
 </div>
 {requisites()}
 <div class="trust"><span>Работаем с 2015 года</span><span><a href="{bm.CRA_HREF}">{bm.CRA}</a></span><span>1С:Франчайзи</span></div>
 <div class="bot"><span>© 2015-2026 ООО «Аллсан Интеграция»</span><nav aria-label="Документы">{leg}</nav></div>
 <p class="req">{DISCLAIMER}</p>
</div>
<div class="mf-lb" id="alsnMfLb" role="dialog" aria-label="Скан сертификата"><button type="button" aria-label="Закрыть">×</button><img alt=""></div>
</footer>"""


def main():
    live = mt.live_set()
    menu = mt.filter_menu(bm.MENU, live)
    cols = columns(menu)
    legal = [(t, h) for t, h in LEGAL if alive(h)]
    body = footer(cols, legal)
    page = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Подвал alsn.ru - вариант v3</title>{bm.FONTS}
<style>body{{margin:0;font-family:Onest,system-ui,sans-serif}}
.demo{{background:#F7F8FA;padding:72px 0;border-top:1px solid #D7DADD}}.demo .in{{max-width:1240px;margin:0 auto;padding:0 28px}}
.demo h2{{margin:0 0 10px;font-size:42px;font-weight:800;letter-spacing:-.02em;color:#212121}}.demo p{{margin:0;color:#6b7075;font-size:18px}}
@media(max-width:1000px){{.demo h2{{font-size:32px}}.demo .in{{padding:0 18px}}}}
{CSS}</style></head><body>
<section class="demo"><div class="in"><h2>Финальный призыв страницы</h2><p>Так выглядит конец любой страницы v3 перед подвалом.</p></div></section>
{body}
<script>{JS}</script></body></html>"""
    OUT.write_text(page.replace("\u2014", "-").replace("\u2013", "-"), encoding="utf-8")
    print(OUT)
    code = (f"<!-- alsn.ru: общий подвал v3 (tilda-footer-v3). Всё в одном T123 на странице Footer. -->\n{bm.FONTS}\n"
            f"<style>{mt.minify_css(CSS)}</style>\n{body}\n<script>{JS.strip()}</script>\n")
    OUT_CODE.write_text(code.replace("\u2014", "-").replace("\u2013", "-"), encoding="utf-8")
    print(OUT_CODE, len(code.encode("utf-8")), "байт")
    for name, links in cols:
        print(f"[{name}]", ", ".join(f"{t} {h}" for t, h in links))
    print("Документы:", legal)

    shot = SCREENS / "_footer-desktop.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    "--window-size=1440,1900", f"--screenshot={shot}", OUT.as_uri()], capture_output=True, timeout=120)
    frame = SCREENS / "_footer-frame.html"
    frame.write_text(f'<html><body style="margin:0;background:#ccc"><iframe src="{OUT.as_uri()}" '
                     f'style="width:390px;height:2700px;border:0;background:#fff"></iframe></body></html>', encoding="utf-8")
    mob = SCREENS / "_footer-mobile.png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    "--allow-file-access-from-files", "--window-size=600,2700", f"--screenshot={mob}", frame.as_uri()],
                   capture_output=True, timeout=120)
    frame.unlink()
    print(shot, shot.exists(), mob, mob.exists())


if __name__ == "__main__":
    main()
