# -*- coding: utf-8 -*-
"""Инструкция для Тильды: на /ecom разделить кейс ООО «СЦ» и видеоотзыв X-COM (раздел 05 «Результаты клиентов»).

Код основного блока (B2) собирается как в build_ecom_v3_brief.py из макета preview-ecom-v3.html,
стили раздела - CASE_CSS из build_ecom_v3_preview.py с префиксом .v3. Выход:
  seo-data/tilda-briefs/tier4-ecom-rezultaty-2026-09-30.html
  seo-data/tilda-briefs/_head-ecom-2026-09-30.txt (дописывается CSS)
"""
import html
import os
import re
import sys
import urllib.request as u

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_ecom_v3_preview as p  # noqa: E402

BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
OUT = os.path.join(BR, "tier4-ecom-rezultaty-2026-09-30.html")
HEAD_TXT = os.path.join(BR, "_head-ecom-2026-09-30.txt")
URL = "https://alsn.ru/ecom"
B2_REC = "rec4356938301"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"

p.main()
src = open(os.path.join(p.SCR, "preview-ecom-v3.html"), encoding="utf-8").read()


def prefix_selectors(sel):
    out = []
    for s in (x.strip() for x in sel.split(",")):
        if s:
            out.append(s if s.startswith(".lb") else ".v3 " + s)
    return ",".join(out)


def prefix_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    res, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        if head.startswith("@media"):
            depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(css[k], 0)
                k += 1
            res.append(head + "{" + prefix_css(css[j + 1:k - 1]) + "}")
            i = k
        else:
            k = css.find("}", j)
            res.append(prefix_selectors(head) + "{" + css[j + 1:k].strip() + "}")
            i = k + 1
    return "\n".join(res)


CSS = prefix_css(p.CASE_CSS)
assert ".v3 .letter.vid{" in CSS and ".v3 .go{" in CSS

# ---------------------------------------------------------------- B2 как в build_ecom_v3_brief.py
body = src[src.index("<!-- BODY -->"):src.index('<section class="final">')].strip()
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
for a, c in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
             ("'[data-zoom]'", "'.v3 [data-zoom]'"), ("'a[data-tab]'", "'.v3 a[data-tab]'")):
    script = script.replace(a, c)
UPLOADED = {
    "case-xcom-video-cover.jpg": "https://static.tildacdn.com/tild3163-6538-4435-a432-653937326465/case-xcom-video-cove.jpg",
    "ecom-1c-podbor-nalichie-postavshchik.png": "https://static.tildacdn.com/tild3463-3163-4738-a663-336539303730/ecom-1c-podbor-nalic.png",
    "ecom-1c-rezerv-u-postavshchika.png": "https://static.tildacdn.com/tild3235-3065-4930-a232-633338376531/ecom-1c-rezerv-u-pos.png",
    "ecom-1c-sopostavlenie-nomenklatury.png": "https://static.tildacdn.com/tild6664-6265-4662-b234-373138653364/ecom-1c-sopostavleni.png",
    "ecom-1c-ostatki-po-praysam.png": "https://static.tildacdn.com/tild3035-3531-4462-b931-376532646266/ecom-1c-ostatki-po-p.png",
    "ecom-1c-monitor-zagruzki.png": "https://static.tildacdn.com/tild6434-3561-4231-a461-313439633661/ecom-1c-monitor-zagr.png",
    "ecom-1c-monitoring-avtorezerva.png": "https://static.tildacdn.com/tild6266-6662-4661-b434-313534313062/ecom-1c-monitoring-a.png",
    "ecom-1c-otchet-rezervirovanie.png": "https://static.tildacdn.com/tild3933-3534-4239-a639-653231353966/ecom-1c-otchet-rezer.png",
}
for local in set(re.findall(r'(?:src|href)="([^"]*?/([^"/]+\.(?:png|jpg)))"', body)):
    if local[1] in UPLOADED:
        body = body.replace(local[0], UPLOADED[local[1]])
assert "../" not in body, "остались локальные пути"
B2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'


# ---------------------------------------------------------------- сверка с живой страницей
def norm(s):
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r">\s+<", "><", s)).strip()


live = u.urlopen(u.Request(URL + "?chk=1640", headers={"User-Agent": UA}), timeout=30).read().decode("utf-8")
i = live.index('<div class="sec" id="case">')
j = live.index('<div class="sec">', i)
live_b2 = norm(live[live.rfind('id="' + B2_REC + '"'):])
new_b2 = norm(B2)
a0 = new_b2.index('<div class="sec" id="case">')
a1 = new_b2.index('<div class="sec">', a0)
before, after = new_b2[:a0], new_b2[a1:]
assert before in live_b2, "код до раздела 05 на сайте отличается от сборки"
assert after in live_b2, "код после раздела 05 на сайте отличается от сборки"
print("сверка: вне раздела 05 код совпадает с сайтом")

# ---------------------------------------------------------------- HEAD-файл
head = open(HEAD_TXT, encoding="utf-8").read()
if ".v3 .letter.vid{" not in head:
    assert head.count("</style>") == 1
    head = head.replace("</style>", CSS + "\n</style>")
    open(HEAD_TXT, "w", encoding="utf-8").write(head)


# ---------------------------------------------------------------- инструкция
def box(cid, text):
    return (f'<div class="copybox"><pre id="{cid}">{html.escape(text, quote=False)}</pre>'
            f'<button type="button" data-copy="{cid}">Копировать</button></div>')


doc = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>/ecom: разделить кейс ООО «СЦ» и видеоотзыв X-COM</title>
<style>{b.BRIEF_CSS}
.where{{background:#F7F8FA;border:1px solid #D7DADD;border-radius:12px;padding:12px 14px;margin:10px 0}}</style>
</head><body><div class="wrap">
<h1>/ecom: разделить кейс ООО «СЦ» и видеоотзыв X-COM</h1>
<p class="muted">Страница «Интеграция 1С с поставщиками телеком- и IT-оборудования» (<a href="{URL}">{URL}</a>, в списке Тильды <code>ecom</code>) · 30.09.2026 · каждый шаг после письменного «да» · «Опубликовать» отдельным шагом в конце · макет: <a href="../competitors/screens/preview-ecom-v3.html#case">preview-ecom-v3.html</a></p>

<div class="callout danger">HEAD сайта (данные компании) не трогать. В HEAD страницы только дописать стили, ничего не стирать. Telegram-бот, robots.txt, Bing, Twitter / X - не трогаем.</div>

<section class="task" id="r1">
  <h2><span class="num">Р-1</span> Стили для нового вида раздела</h2>
  <span class="lbl">Что сделать</span>
  <p>Дописать в HEAD страницы /ecom несколько строк стилей: отдельная карточка кейса и отдельный блок видео.</p>
  <span class="lbl">Зачем</span>
  <p>Сейчас в разделе «Результаты клиентов» видео X-COM стоит в одной рамке с кейсом ООО «СЦ», и гость думает, что видео про этот кейс. После правки кейс со своими цифрами идёт отдельной карточкой, а видео ниже под своим заголовком «Видеоотзыв X-COM о работе с Аллсан».</p>
  <span class="lbl">Как в Тильде</span>
  <ol class="steps">
    <li>Список страниц → <strong>ecom</strong> → шестерёнка <strong>Настройки</strong> → <strong>Дополнительно</strong> → поле «HTML-код для вставки внутрь head».</li>
    <li>Ctrl+F в поле → найти строку ниже. Она в поле одна, в самом конце большого блока стилей.</li>
  </ol>
  <p class="cap">Найти</p>
  {box("f1", "</style>")}
  <ol class="steps" start="3">
    <li>Поставить курсор <strong>перед</strong> <code>&lt;/style&gt;</code>, нажать Enter и вставить код. Остальное в поле не трогать.</li>
  </ol>
  <p class="cap">Вставить перед &lt;/style&gt;</p>
  {box("c1", CSS)}
  <ol class="steps" start="4"><li><strong>Сохранить</strong>. Тот же HEAD целиком лежит в <code>_head-ecom-2026-09-30.txt</code>, если удобнее сверить.</li></ol>
</section>

<section class="task" id="r2">
  <h2><span class="num">Р-2</span> Основной блок: кейс и видео по отдельности</h2>
  <span class="lbl">Что сделать</span>
  <p>Заменить код основного блока страницы. Меняется только раздел 05 «Результаты клиентов», остальное внутри блока остаётся буква в букву как сейчас (сверено с сайтом 30.09.2026).</p>
  <span class="lbl">Зачем</span>
  <p>Кейс ООО «СЦ» (×3, цитата Мельника О.И., три цифры и ссылка «Читать кейс ООО «СЦ» полностью →») становится одной карточкой. Видео X-COM переезжает ниже, в отдельный блок с именем и ролью Игоря Роганкова. Ссылка на кейс переезжает внутрь карточки, строка под цифрами исчезает.</p>
  <span class="lbl">Как в Тильде</span>
  <div class="where"><strong>Где.</strong> Страница /ecom, большой блок <strong>T123</strong> (<code>{B2_REC}</code>) сразу под первым экраном и лентой «Как выглядит день с интеграцией». Слева в нём паспорт с ценой «103 950 ₽», справа разделы 01-07: «На какие вопросы отвечает интеграция», «Как идут данные», «Что видно в 1С», «Какие поставщики уже подключены», «Результаты клиентов», «Кому подходит», «Сколько стоит», «Частые вопросы».</div>
  <ol class="steps">
    <li>Редактор страницы ecom → навести на этот блок → <strong>Контент</strong>.</li>
    <li>Клик в поле кода → Ctrl+A → Delete.</li>
    <li>Вставить код ниже целиком.</li>
    <li><strong>Сохранить и закрыть</strong>.</li>
  </ol>
  <p class="cap">Код блока</p>
  {box("c2", B2)}
</section>

<section class="task" id="r3">
  <h2><span class="num">Р-3</span> Опубликовать</h2>
  <ol class="steps"><li>После «да» нажать <strong>«Опубликовать»</strong> на странице ecom.</li></ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-ecom-rezultaty-2026-09-30.html</code>, собран <code>seo-data/scripts/build_ecom_case_split_brief.py</code>. Открывать локально, на alsn.ru не заливать.</p>
</div>
{b.COPY_JS}
</body></html>
"""
# проверено на живом alsn.ru 30.09.2026 (_sup_ecom_done_check_0930.py): стили в HEAD и блок совпадают с кодом Р-1, Р-2
ALL_DONE = True
if ALL_DONE:
    doc, cnt = re.subn(r'<section class="task" id="r1">.*?<section class="task" id="r3">.*?</section>\n',
                       '<div class="callout warn"><strong>Уже сделано - не трогать:</strong><ul class="tight">\n'
                       "<li>30.09.2026 Р-1: стили карточки кейса и блока видео дописаны в HEAD страницы /ecom.</li>\n"
                       "<li>30.09.2026 Р-2: основной блок заменён, кейс ООО «СЦ» и видеоотзыв X-COM идут раздельно.</li>\n"
                       "<li>30.09.2026 Р-3: страница /ecom опубликована.</li>\n</ul></div>\n", doc, flags=re.S)
    assert cnt == 1
    doc = doc.replace("· 30.09.2026 · каждый шаг", "· Все задачи выполнены 30.09.2026, открытых шагов нет · каждый шаг", 1)
chk = re.sub(r"<pre.*?</pre>", "", doc, flags=re.S)
assert "\u2014" not in chk and "\u2013" not in chk, "длинное или среднее тире"
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, "B2", len(B2), "CSS", len(CSS))
