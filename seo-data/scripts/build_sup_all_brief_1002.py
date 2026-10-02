# -*- coding: utf-8 -*-
"""Страницы поставщиков 02.10.2026: исправить 13 действующих, создать 31 новую, обновить /ecom.

Канон текстов: ежегодная оплата (продление по цене покупки), остатки с настроенных складов,
сайт через виртуальные склады, подключение 2 недели (ecom-suppliers-manual.mdc, TD-002/003/004).
Выход:
  seo-data/tilda-briefs/tier4-postavshiki-fix-2026-10-02.html  - 13 действующих страниц
  seo-data/tilda-briefs/tier4-postavshiki-new-2026-10-02.html  - 31 новая страница и /ecom
  seo-data/tilda-briefs/_head-{slug}-2026-10-02.txt, _head-ecom-2026-10-02.txt
  seo-data/tilda-briefs/recrawl-postavshiki-2026-10-02.txt
Запуск: python build_sup_all_brief_1002.py [--refresh]  (--refresh - заново снять живые страницы)
"""
import difflib
import html
import json
import os
import re
import sys
import time
import urllib.request as u

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_ecom_v3_preview as p  # noqa: E402
import build_sup_cards_v3 as c  # noqa: E402
import build_tier3_ecom_brief as t3  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
OUT_FIX = os.path.join(BR, "tier4-postavshiki-fix-2026-10-02.html")
OUT_NEW = os.path.join(BR, "tier4-postavshiki-new-2026-10-02.html")
RECRAWL = os.path.join(BR, "recrawl-postavshiki-2026-10-02.txt")
CACHE = os.path.join(HERE, "_sup_live_1002.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
DATE = "02.10.2026"
BANNED = ("однократ", "один раз, без продления", "без ежегодного", "не нужно</dd>", "снимается с сайта", "снимает его с вашего сайта",
          "вкл/выкл", "склады дистрибьюторов видны", "\u2014", "\u2013")


# ---------------------------------------------------------------- живые страницы
def fetch(url):
    return u.urlopen(u.Request(url, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8")


def recs(src):
    out = []
    ms = list(re.finditer(r'<div id="rec(\d+)" class="r t-rec[^"]*"[^>]*data-record-type="(\d+)"', src))
    for k, m in enumerate(ms):
        end = ms[k + 1].start() if k + 1 < len(ms) else len(src)
        out.append((m.group(1), m.group(2), src[m.start():end]))
    return out


def live_info(slug):
    src = fetch(f"https://alsn.ru/{slug}?chk=1002")
    rr = recs(src)

    def find(marker):
        x = [r for r, t, seg in rr if t == "131" and marker in seg]
        return x[0] if x else ""
    return {
        "title": html.unescape(re.search(r"<title>(.*?)</title>", src, re.S).group(1).strip()),
        "desc": html.unescape(re.search(r'<meta name="description" content="([^"]*)"', src).group(1)),
        "b1": find('class="hf'), "b2": find('class="pass"'), "b3": find('class="final"'),
        "crumbs": find('aria-label="Хлебные крошки"'),
        "t758": any(t == "758" for _, t, _ in rr),
        "old_pay": "однократ" in src.lower(),
        "html": src if slug == "ecom" else "",
    }


def load_live(refresh):
    if os.path.exists(CACHE) and not refresh:
        return json.load(open(CACHE, encoding="utf-8"))
    data = {}
    for slug in ["ecom"] + [s["slug"] for s in c.SUP]:
        data[slug] = live_info(slug)
        print("live", slug, data[slug]["b1"], data[slug]["b2"], data[slug]["b3"], flush=True)
        time.sleep(4)
    json.dump(data, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    return data


# ---------------------------------------------------------------- /ecom
def ecom_blocks(live):
    p.main()
    src = open(os.path.join(p.SCR, "preview-ecom-v3.html"), encoding="utf-8").read()
    up = {
        "allsun-hero-ecom-suppliers.jpg": c.PHOTO_CDN,
        "case-xcom-video-cover.jpg": "https://static.tildacdn.com/tild3163-6538-4435-a432-653937326465/case-xcom-video-cove.jpg",
        "ecom-1c-podbor-nalichie-postavshchik.png": "https://static.tildacdn.com/tild3463-3163-4738-a663-336539303730/ecom-1c-podbor-nalic.png",
        "ecom-1c-rezerv-u-postavshchika.png": "https://static.tildacdn.com/tild3235-3065-4930-a232-633338376531/ecom-1c-rezerv-u-pos.png",
        "ecom-1c-sopostavlenie-nomenklatury.png": "https://static.tildacdn.com/tild6664-6265-4662-b234-373138653364/ecom-1c-sopostavleni.png",
        "ecom-1c-ostatki-po-praysam.png": "https://static.tildacdn.com/tild3035-3531-4462-b931-376532646266/ecom-1c-ostatki-po-p.png",
        "ecom-1c-monitor-zagruzki.png": "https://static.tildacdn.com/tild6434-3561-4231-a461-313439633661/ecom-1c-monitor-zagr.png",
        "ecom-1c-monitoring-avtorezerva.png": "https://static.tildacdn.com/tild6266-6662-4661-b434-313534313062/ecom-1c-monitoring-a.png",
        "ecom-1c-otchet-rezervirovanie.png": "https://static.tildacdn.com/tild3933-3534-4239-a639-653231353966/ecom-1c-otchet-rezer.png",
    }

    def local2cdn(x):
        for path, name in set(re.findall(r'(?:src|href)="([^"]*?/([^"/]+\.(?:png|jpg)))"', x)):
            if name in up:
                x = x.replace(path, up[name])
        assert "../" not in x, "локальные пути"
        return x
    hero = local2cdn(c.cut(src, "<!-- HERO -->", "<!-- BODY -->"))
    body = local2cdn(c.cut(src, "<!-- BODY -->", '<section class="final">'))
    script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
    for a, z in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
                 ("'[data-zoom]'", "'.v3 [data-zoom]'"), ("'a[data-tab]'", "'.v3 a[data-tab]'")):
        script = script.replace(a, z)
    b1 = f'<div class="v3">\n{hero}\n</div>'
    b2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'

    head = open(os.path.join(BR, "_head-ecom-2026-09-30.txt"), encoding="utf-8").read()
    scripts = re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    faq_old = [x for x in scripts if '"FAQPage"' in x]
    assert len(faq_old) == 1
    head = head.replace(faq_old[0], t3.FAQ_SCRIPT)
    assert head.count("<style>") == 1 and ".v3 .letter.vid{" in head and ".v3 .hf .who{position:static" in head

    # живой HEAD /ecom = прошлый файл: старый ответ про оплату и стили кейса на месте
    lh = live["ecom"]["html"]
    assert "Оплата однократная, без ежегодного продления" in lh and ".v3 .letter.vid{" in lh
    # экран и служебный код FAQ - буква в букву
    scr = [(c.strip_tags(q), c.strip_tags(a)) for q, a in re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", body)]
    scr = [x for x in scr if x[0] in dict(t3.FAQ)]
    assert scr == [(q, a) for q, a in t3.FAQ], "FAQ на экране и в HEAD различаются"
    # отчёт о разнице видимого текста с сайтом - для глаз
    def words(x):
        x = re.sub(r"<(script|style).*?</\1>", " ", x, flags=re.S)
        return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).split()
    rr = {r: seg for r, t, seg in recs(lh)}
    rep = []
    for nm, new, rec in (("B1", b1, live["ecom"]["b1"]), ("B2", b2, live["ecom"]["b2"])):
        d = [x for x in difflib.unified_diff(words(rr[rec]), words(new), lineterm="", n=0) if x[:1] in "+-" and x[:3] not in ("+++", "---")]
        rep.append(f"== {nm} rec{rec}: {len(d)} слов отличается\n" + " ".join(d))
    open(os.path.join(HERE, "_ecom_diff_1002.txt"), "w", encoding="utf-8").write("\n\n".join(rep))
    open(os.path.join(BR, "_head-ecom-2026-10-02.txt"), "w", encoding="utf-8").write(head)
    for x in (head, b1, b2):
        low = x.lower()
        assert not any(w in low for w in BANNED), [w for w in BANNED if w in low]
    return head, b1, b2


# ---------------------------------------------------------------- общие куски
def box(cid, text):
    return (f'<div class="copybox"><pre id="{cid}">{html.escape(text, quote=False)}</pre>'
            f'<button type="button" data-copy="{cid}">Копировать</button></div>')


def swap(cid, old, new):
    return f'<span class="lbl">Найти (всё поле)</span>\n{box(cid + "f", old)}\n<span class="lbl">Заменить на</span>\n{box(cid + "r", new)}'


CRUMB = ('<nav aria-label="Хлебные крошки" style="display:flex;align-items:center;flex-wrap:nowrap;font-size:14px;line-height:1.2;'
         'color:#8a8a8a;padding:12px 20px 8px;"> <a href="https://alsn.ru/" aria-label="Главная" title="Главная" '
         'style="display:inline-flex;color:inherit;text-decoration:none;"> <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" '
         'viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.2 3 10.8V21h6.2v-6.5h5.6V21H21V10.8L12 3.2z"/></svg> </a> '
         '<span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span> <a href="https://alsn.ru/ecom" '
         'style="color:inherit;text-decoration:none;white-space:nowrap;">Интеграция с поставщиками</a> '
         '<span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span> <span style="opacity:.75;white-space:nowrap;">{}</span> </nav>')

EXTRA = """
details.page{background:#fff;border:1px solid var(--border,#e2e2de);border-radius:12px;margin:0 0 14px}
details.page>summary{cursor:pointer;list-style:none;padding:14px 18px;font-weight:700;font-size:17px}
details.page>summary::-webkit-details-marker{display:none}
details.page>summary::after{content:"+";float:right;font-weight:400;font-size:22px;line-height:1}
details.page[open]>summary::after{content:"−"}
details.page>summary .num{display:inline-block;background:#111;color:#fff;border-radius:999px;font-size:12px;font-weight:700;padding:2px 10px;margin-right:6px;vertical-align:middle}
details.page>summary .muted{font-weight:400;font-size:14px}
.pbody{padding:0 18px 6px}
.pbody .task h3{margin:0 0 8px}
"""


def doc(title, intro, body_):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<style>{b.BRIEF_CSS}{EXTRA}</style>
</head>
<body>
<div class="wrap">
<h1>{title}</h1>
{intro}
{body_}
</div>
{b.COPY_JS}
</body>
</html>"""


def t123_steps(where):
    return (f'<div class="where"><strong>Где.</strong> {where}</div>\n<ol class="steps">\n'
            '<li>Клик по блоку → «Контент» → Ctrl+A → Delete → вставить код ниже целиком → «Сохранить и закрыть».</li>\n'
            '<li>Отступы блока не менять. Новый блок не добавлять.</li>\n</ol>')


def head_steps(slug, now):
    return ('<ol class="steps">\n'
            f'<li>Список страниц → <code>{slug}</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>\n'
            f'<li>{now}</li>\n'
            '<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>\n</ol>')


# ---------------------------------------------------------------- 13 действующих
def fix_page(n, s, css, lv):
    head, b1, b2, b3, nfaq = c.page_code(s, css)
    open(os.path.join(BR, f"_head-{s['slug']}-2026-10-02.txt"), "w", encoding="utf-8").write(head)
    for x in (head, b1, b2):
        low = x.lower()
        assert not any(w in low for w in BANNED), (s["slug"], [w for w in BANNED if w in low])
    slug, url, name = s["slug"], f"https://alsn.ru/{s['slug']}", c.h1_text(s)
    assert lv["b1"] and lv["b2"], f"на {slug} нет нового дизайна"
    pid = f"f{n}"
    desc_task = ""
    k = 4
    if lv["desc"] != c.desc_new(s):
        desc_task = f"""
<section class="task" id="{pid}-4">
<h3><span class="num">{n}.4</span> Описание для поиска</h3>
<p>Сейчас в описании, которое видно в выдаче, стоит «Оплата однократная». Меняем на срок подключения. Заголовок вкладки не трогаем.</p>
<ol class="steps">
<li>Список страниц → <code>{slug}</code> → «Настройки» → «Главное» (или «SEO») → поле «Описание» → заменить → «Сохранить изменения».</li>
<li>Вкладка «Соцсети» (или «Facebook &amp; SEO»): если там то же старое описание, заменить так же. Картинку превью не трогать.</li>
</ol>
{swap(pid + "d", lv["desc"], c.desc_new(s))}
</section>"""
        k = 5
    return f"""
<details class="page" id="{pid}"{" open" if n == 1 else ""}>
<summary><span class="num">{n:02d}</span> {name} <span class="muted">· alsn.ru/{slug} · {k} шагов</span></summary>
<div class="pbody">
<p class="muted">Страница «{name}» (<a href="{url}">{url}</a>, в списке Тильды <code>{slug}</code>) · макет: <a href="../competitors/screens/preview-sup-{slug}-v3.html">preview-sup-{slug}-v3.html</a> · данные: {c.data_short(s)}</p>

<section class="task" id="{pid}-1">
<h3><span class="num">{n}.1</span> HEAD страницы целиком</h3>
<p>Новые ответы в частых вопросах для поиска и стили: на телефоне подпись «Павел Агеев» встаёт под фото.</p>
{head_steps(slug, "Скопировать старое содержимое в блокнот и сохранить файл, это откат.")}
{box(pid + "h", head)}
<p class="muted">Внутри {nfaq} частых вопросов ровно как на экране. Тот же код - в файле <code>_head-{slug}-2026-10-02.txt</code>.</p>
</section>

<section class="task" id="{pid}-2">
<h3><span class="num">{n}.2</span> Первый экран (B1) целиком</h3>
<p>Абзац под заголовком: остатки с настроенных складов {s['gen']}.</p>
{t123_steps(f'Страница «{name}» ({url}). Блок T123 первого экрана в рамке: заголовок «{name}», справа фото Павла Агеева. В коде <code>rec{lv["b1"]}</code>.')}
{box(pid + "a", b1)}
</section>

<section class="task" id="{pid}-3">
<h3><span class="num">{n}.3</span> Основная часть (B2) целиком</h3>
<p>Паспорт: «в год», «Оплата ежегодно», срок «2 недели»{", сайт через виртуальные склады" if (s["flags"][3] and s["flags"][0]) else ""}. Частый вопрос о продлении: оплата ежегодная, без продления модуль не обновляется. Цены «в год».</p>
{t123_steps(f'Блок T123 сразу под первым экраном: слева паспорт с ценой «103 950 ₽», справа разделы 01-06. В коде <code>rec{lv["b2"]}</code>.')}
{box(pid + "b", b2)}
</section>
{desc_task}
<section class="task" id="{pid}-{k}">
<h3><span class="num">{n}.{k}</span> Опубликовать</h3>
<ol class="steps">
<li>Вверху редактора страницы <code>{slug}</code> → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано {slug}»: проверю живую страницу.</li>
</ol>
</section>
</div>
</details>"""


# ---------------------------------------------------------------- 31 новая
def new_page(n, s, css):
    head, b1, b2, b3, nfaq = c.page_code(s, css)
    open(os.path.join(BR, f"_head-{s['slug']}-2026-10-02.txt"), "w", encoding="utf-8").write(head)
    for x in (head, b1, b2, b3):
        low = x.lower()
        assert not any(w in low for w in BANNED), (s["slug"], [w for w in BANNED if w in low])
    slug, url, name = s["slug"], f"https://alsn.ru/{s['slug']}", c.h1_text(s)
    pid = f"n{n}"
    crumb = CRUMB.format(s["crumb"])
    return f"""
<details class="page" id="{pid}"{" open" if n == 1 else ""}>
<summary><span class="num">{n:02d}</span> {name} <span class="muted">· alsn.ru/{slug} · данные: {c.data_short(s)}</span></summary>
<div class="pbody">
<p class="muted">Новая страница «{name}» (будет <a href="{url}">{url}</a>) · макет: <a href="../competitors/screens/preview-sup-{slug}-v3.html">preview-sup-{slug}-v3.html</a></p>

<section class="task" id="{pid}-1">
<h3><span class="num">{n}.1</span> Копия страницы Мерлиона и её настройки</h3>
<ol class="steps">
<li>Список страниц → страница «Интеграция 1С с Merlion B2B по API» (<code>merlion</code>) → «Ещё» / три точки → «Дублировать» (или «Копировать страницу»). Копия появится в списке с тем же названием.</li>
<li>У копии → «Настройки» → «Главное»: «Заголовок» и «Описание» вставить из блоков ниже, «Адрес страницы» - <code>{slug}</code>. Галочка «Запретить индексацию» должна быть снята.</li>
<li>Вкладка «Соцсети» (или «Facebook &amp; SEO»): заголовок и описание - те же, что ниже. Картинку превью не трогать → «Сохранить изменения».</li>
</ol>
<span class="lbl">Заголовок</span>
{box(pid + "t", c.title_new(s))}
<span class="lbl">Описание</span>
{box(pid + "d", c.desc_new(s))}
<span class="lbl">Адрес страницы</span>
{box(pid + "u", slug)}
</section>

<section class="task" id="{pid}-2">
<h3><span class="num">{n}.2</span> HEAD страницы целиком</h3>
{head_steps(slug, "В копии там код Мерлиона, сохранять его не нужно.")}
{box(pid + "h", head)}
<p class="muted">Внутри: стили, услуга, страница, крошки «Главная / Интеграция с поставщиками / {s['crumb']}» и {nfaq} частых вопросов ровно как на экране. Тот же код - в <code>_head-{slug}-2026-10-02.txt</code>.</p>
</section>

<section class="task" id="{pid}-3">
<h3><span class="num">{n}.3</span> Крошки: выключить старые, заменить новые</h3>
<ol class="steps">
<li>Холст копии. Под меню старый блок крошек T758 «Интеграция 1C по API с B2B поставщиками и дистрибьютерами → Merlion» → «Ещё» / три точки → «Выключить блок».</li>
<li>Под ним блок T123 «дом / Интеграция с поставщиками / Мерлион» → «Контент» → Ctrl+A → Delete → вставить код ниже → «Сохранить и закрыть».</li>
</ol>
{box(pid + "c", crumb)}
</section>

<section class="task" id="{pid}-4">
<h3><span class="num">{n}.4</span> Первый экран (B1)</h3>
{t123_steps("Блок T123 первого экрана в рамке: в копии там заголовок «Интеграция 1С с Merlion B2B по API» и фото Павла Агеева.")}
{box(pid + "a", b1)}
</section>

<section class="task" id="{pid}-5">
<h3><span class="num">{n}.5</span> Основная часть (B2)</h3>
{t123_steps("Блок T123 под первым экраном: слева паспорт «103 950 ₽», справа «Что приходит из Мерлион в 1С» и разделы до «Другие поставщики».")}
{box(pid + "b", b2)}
</section>

<section class="task" id="{pid}-6">
<h3><span class="num">{n}.6</span> Последний экран (B3)</h3>
{t123_steps("Серый блок T123 «Подключим Мерлион к вашей 1С» с телефоном и кнопкой.")}
{box(pid + "f", b3)}
</section>

<section class="task" id="{pid}-7">
<h3><span class="num">{n}.7</span> Опубликовать</h3>
<ol class="steps">
<li>Вверху редактора копии → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано {slug}»: проверю страницу по адресу {url}.</li>
</ol>
</section>
</div>
</details>"""


def ecom_part(head, b1, b2, live):
    lv = live["ecom"]
    url = "https://alsn.ru/ecom"
    nm = "Интеграция 1С с поставщиками телеком- и IT-оборудования"
    return f"""
<details class="page" id="ecom" open>
<summary><span class="num">E</span> {nm} <span class="muted">· alsn.ru/ecom · 4 шага · делать после новых страниц</span></summary>
<div class="pbody">
<p class="muted">Страница «{nm}» (<a href="{url}">{url}</a>, в списке Тильды <code>ecom</code>) · макет: <a href="../competitors/screens/preview-ecom-v3.html">preview-ecom-v3.html</a></p>
<div class="callout warn">Делать, когда новые страницы опубликованы: в таблице поставщиков названия становятся ссылками на них. Если сделать раньше, ссылки поведут на пустую страницу.</div>

<section class="task" id="e-1">
<h3><span class="num">E.1</span> HEAD страницы целиком</h3>
<p>Частые вопросы для поиска: оплата ежегодная, сайт через виртуальные склады, новый вопрос «Сколько времени занимает подключение?». Остальной код как сейчас.</p>
{head_steps("ecom", "Скопировать старое содержимое в блокнот и сохранить файл, это откат.")}
{box("eh", head)}
<p class="muted">Тот же код - в <code>_head-ecom-2026-10-02.txt</code>.</p>
</section>

<section class="task" id="e-2">
<h3><span class="num">E.2</span> Первый экран и лента дня (B1) целиком</h3>
<p>В ленте «Как выглядит день с интеграцией»: остатки с настроенных складов; прайс на сайте через виртуальные склады.</p>
{t123_steps(f'Блок T123 первого экрана в рамке с фото Павла Агеева и серой лентой «Как выглядит день с интеграцией» под ним. В коде <code>rec{lv["b1"]}</code>.')}
{box("ea", b1)}
</section>

<section class="task" id="e-3">
<h3><span class="num">E.3</span> Основная часть (B2) целиком</h3>
<p>Паспорт: «в год», «Подключение 2 недели», «Оплата ежегодно». Таблица: {len(c.NEW_SUP)} новых ссылок на страницы поставщиков. Строки «Асбис», «TFN» и «ТФН» из таблицы убрать: этих поставщиков на сайте больше нет. Сноска «Сайт*», «Как не продать то, чего нет?», схема данных, цены «в год» и сноска о продлении, частые вопросы как в HEAD.</p>
{t123_steps(f'Блок T123 под лентой: слева паспорт «103 950 ₽», справа разделы 01-08. В коде <code>rec{lv["b2"]}</code>.')}
{box("eb", b2)}
</section>

<section class="task" id="e-4">
<h3><span class="num">E.4</span> Опубликовать</h3>
<ol class="steps">
<li>Вверху редактора страницы <code>ecom</code> → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано ecom»: проверю таблицу, ссылки и вопросы.</li>
</ol>
</section>
</div>
</details>"""


RULES = """<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать, меняем только HEAD страницы. Старые блоки выключаем, а не удаляем. robots.txt, Bing, Twitter не трогаем. Telegram-бот на сайте остаётся.</div>"""

CANON = """<section class="task">
<h2>Что пишем и чего не пишем</h2>
<ul class="tight">
<li>Оплата ежегодная. Год продления стоит столько же, сколько покупка: 103 950 ₽ за пакет из 5 поставщиков, 15 645 ₽ за каждого следующего. Без продления модуль перестаёт обновляться, при смене API поставщика может перестать работать (02.10.2026).</li>
<li>Остатки - только с настроенных складов поставщика. Сайт - через виртуальные склады, если 1С уже связана с сайтом. «Снимаем товар с сайта» не пишем.</li>
<li>Срок подключения одного поставщика - 2 недели. SLA и «каждые 15 минут» не пишем.</li>
<li>Набор разделов на каждой странице - по отметкам из таблицы /ecom. Где нет резерва, резерв не обещаем; где только резерв, не обещаем остатки и цены.</li>
</ul>
</section>"""


def main():
    live = load_live("--refresh" in sys.argv)
    c.build_previews()
    css = c.build_css()

    # 1) 13 действующих
    pages = "\n".join(fix_page(i, s, css, live[s["slug"]]) for i, s in enumerate(c.SUP, 1))
    nsteps = sum(5 if live[s["slug"]]["desc"] != c.desc_new(s) else 4 for s in c.SUP)
    toc = "\n".join(f'<li><a href="#f{i}">{c.h1_text(s)}</a> · <code>{s["slug"]}</code></li>' for i, s in enumerate(c.SUP, 1))
    intro = f"""<p class="muted">13 страниц «Интеграция 1С с … по API» на новом дизайне · {DATE} · {nsteps} шагов · каждый шаг после письменного «да» · «Опубликовать» отдельным шагом в конце каждой страницы</p>
<div class="callout"><strong>Что меняется.</strong> На страницах ещё стоят устаревшие тексты: «Оплата однократная», «Продление не нужно», «снимаем товар с сайта», нет срока «2 недели». Меняем HEAD страницы, первый экран и основную часть целиком, плюс описание для поиска. Последний экран, крошки и заголовок вкладки не трогаем. Макеты: <a href="../competitors/sup-cards-design-options-2026-09-30.html">все страницы поставщиков</a>.</div>
{RULES}
<div class="callout warn"><strong>Уже сделано - не трогать:</strong> новый дизайн на всех 13 страницах (30.09.2026); первый экран в рамке и последний экран. Прошлая инструкция <code>tier4-postavshiki-v3-2026-09-30.html</code> (срок «2 недели») заменена этой: срок уже входит в новые блоки. Удаление старых крошек T758 - в <code>tier2-breadcrumbs-wave-2026-09-28.html</code>; служебный код крошек в HEAD уже есть в коде шага 1.</div>
<div class="toc"><strong>Страницы</strong><ol>
{toc}
</ol></div>"""
    fix_doc = doc("Страницы поставщиков: исправить тексты на 13 страницах", intro, pages + "\n" + CANON)
    open(OUT_FIX, "w", encoding="utf-8").write(fix_doc)

    # 2) 31 новая + /ecom
    eh, e1, e2 = ecom_blocks(live)
    newp = "\n".join(new_page(i, s, css) for i, s in enumerate(c.NEW_SUP, 1))
    toc = "\n".join(f'<li><a href="#n{i}">{c.h1_text(s)}</a> · <code>{s["slug"]}</code> · {c.data_short(s)}</li>'
                    for i, s in enumerate(c.NEW_SUP, 1))
    intro = f"""<p class="muted">{len(c.NEW_SUP)} новых страниц поставщиков из таблицы на «Интеграция 1С с поставщиками» (<a href="https://alsn.ru/ecom">https://alsn.ru/ecom</a>) и обновление самой /ecom · {DATE} · по 7 шагов на страницу, на /ecom 4 · каждый шаг после письменного «да» · «Опубликовать» отдельным шагом</p>
<div class="callout"><strong>Как устроено.</strong> Каждая новая страница - копия страницы Мерлиона (<a href="https://alsn.ru/merlion">https://alsn.ru/merlion</a>): меню, крошки, первый экран, основная часть, последний экран, формы и подвал уже на месте. В копии меняем настройки, HEAD и код четырёх блоков. Адреса страниц проверены 02.10.2026: все свободны. Макеты: <a href="../competitors/sup-cards-design-options-2026-09-30.html">все страницы поставщиков</a>.</div>
{RULES}
<div class="callout warn"><strong>Порядок.</strong> Сначала страницы 1-{len(c.NEW_SUP)} (каждую можно делать и публиковать отдельно), в самом конце /ecom: там названия в таблице становятся ссылками на новые страницы. Строки «Асбис», «TFN» и «ТФН» из таблицы убираем, страницы для них не создаём (решение 02.10.2026). Непрофильные поставщики (Тайпит-Мебель, Делия и др.) и строки без отметок страниц не получают.</div>
<div class="toc"><strong>Новые страницы</strong><ol>
{toc}
<li><a href="#ecom">Интеграция 1С с поставщиками (/ecom)</a> - последней</li>
</ol></div>"""
    new_doc = doc(f"Страницы поставщиков: {len(c.NEW_SUP)} новых страниц и /ecom", intro, newp + "\n" + ecom_part(eh, e1, e2, live) + "\n" + CANON)
    open(OUT_NEW, "w", encoding="utf-8").write(new_doc)

    urls = [f"https://alsn.ru/{s['slug']}" for s in c.NEW_SUP] + ["https://alsn.ru/ecom"] + [f"https://alsn.ru/{s['slug']}" for s in c.SUP]
    open(RECRAWL, "w", encoding="utf-8").write("\n".join(urls) + "\n")
    print("fix", OUT_FIX, len(fix_doc) // 1024, "KB")
    print("new", OUT_NEW, len(new_doc) // 1024, "KB")
    print("ecom desc:", live["ecom"]["desc"])


if __name__ == "__main__":
    main()
