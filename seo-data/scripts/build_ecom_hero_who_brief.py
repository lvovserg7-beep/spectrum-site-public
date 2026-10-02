# -*- coding: utf-8 -*-
"""Инструкция для Тильды: на /ecom подпись с именем сотрудника на телефоне под фото первого экрана.

Меняются только мобильные строки .v3 .hf в HEAD страницы (канон HERO_CSS из mp_hero_frame.py, 01.10.2026).
HEAD отдаётся целиком (tilda-v3-full-paste.mdc). Выход:
  seo-data/tilda-briefs/_head-ecom-2026-09-30.txt (обновляется)
  seo-data/tilda-briefs/tier4-ecom-podpis-foto-2026-10-01.html
"""
import html
import os
import re
import sys
import urllib.request as u

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402

BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
HEAD_TXT = os.path.join(BR, "_head-ecom-2026-09-30.txt")
OUT = os.path.join(BR, "tier4-ecom-podpis-foto-2026-10-01.html")
URL = "https://alsn.ru/ecom"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"

OLD = [
    ".v3 .hf .ph{position:relative;order:-1;aspect-ratio:16/10}",
    ".v3 .hf .ph img{object-position:40% 25%}",
    ".v3 .hf .veil{background:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff 100%)}",
    ".v3 .hf .who{top:12px;bottom:auto;right:12px;font-size:11.5px}",
]
NEW = [
    ".v3 .hf .ph{position:relative;order:-1;aspect-ratio:auto;padding-top:62.5%}",
    ".v3 .hf .ph img{bottom:auto;height:auto;aspect-ratio:16/10;object-position:40% 25%}",
    ".v3 .hf .veil{bottom:auto;aspect-ratio:16/10;background:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff 100%)}",
    ".v3 .hf .who{position:static;margin:8px 20px 18px;padding:0;background:none;border:0;border-radius:0;font-size:13px;line-height:1.4;color:var(--mut)}\n"
    ".v3 .hf .who b{color:var(--ink)}",
]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


head = open(HEAD_TXT, encoding="utf-8").read()
if OLD[-1] in head:
    live = u.urlopen(u.Request(URL + "?chk=1001b", headers={"User-Agent": UA}), timeout=30).read().decode("utf-8")
    assert norm(head) in norm(live), "HEAD на сайте отличается от файла: сначала сверить"
    for o, n in zip(OLD, NEW):
        assert head.count(o) == 1, o
        head = head.replace(o, n)
    open(HEAD_TXT, "w", encoding="utf-8").write(head)
assert all(n in head for n in NEW)


def box(cid, text):
    return (f'<div class="copybox"><pre id="{cid}">{html.escape(text, quote=False)}</pre>'
            f'<button type="button" data-copy="{cid}">Копировать</button></div>')


doc = f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>/ecom: подпись под фото на телефоне - 01.10.2026</title>
<style>{b.BRIEF_CSS}
.where{{background:#F7F8FA;border:1px solid #D7DADD;border-radius:12px;padding:12px 14px;margin:10px 0}}</style>
</head><body><div class="wrap">
<h1>/ecom: подпись с именем под фото на телефоне</h1>
<p class="muted">Страница «Интеграция 1С с поставщиками телеком- и IT-оборудования» (<a href="{URL}">{URL}</a>, в списке Тильды <code>ecom</code>) · 01.10.2026 · каждый шаг после письменного «да» · «Опубликовать» отдельным шагом · макет: <a href="../competitors/screens/preview-ecom-v3.html">preview-ecom-v3.html</a> (сузить окно до телефона)</p>

<div class="callout danger">HEAD сайта (данные компании) не трогать, только HEAD страницы ecom. Блоки T123 не трогать. Telegram-бот, robots.txt, Bing, Twitter / X - не трогаем.</div>

<div class="callout ok"><strong>Уже сделано - не трогать:</strong> раздел «Результаты клиентов» (кейс ООО «СЦ» и видеоотзыв X-COM по отдельности) опубликован, проверено на сайте 01.10.2026.</div>

<section class="task" id="p1">
  <h2><span class="num">П-1</span> HEAD страницы целиком</h2>
  <span class="lbl">Что сделать</span>
  <p>Заменить код в HEAD страницы /ecom. Меняются только стили первого экрана для телефона, остальное совпадает с тем, что на сайте сейчас (сверено 01.10.2026).</p>
  <span class="lbl">Зачем</span>
  <p>На телефоне плашка «Павел Агеев · ведущий аналитик 1С, эксперт по интеграциям» лежит поверх фото вверху и закрывает кадр. После правки она стоит серой строкой под фото, над надписью «B2B-поставщики». На компьютере ничего не меняется: подпись остаётся плашкой в правом нижнем углу фото.</p>
  <span class="lbl">Как в Тильде</span>
  <ol class="steps">
    <li>Список страниц → <strong>ecom</strong> → шестерёнка <strong>Настройки</strong> → <strong>Дополнительно</strong> → «HTML-код для вставки внутрь HEAD».</li>
    <li>Скопировать старое содержимое в блокнот, это откат.</li>
    <li>В поле: Ctrl+A → Delete → вставить код ниже целиком → <strong>Сохранить изменения</strong>.</li>
  </ol>
  {box("h1", head)}
  <p class="muted">Тот же код в файле <code>_head-ecom-2026-09-30.txt</code>.</p>
</section>

<section class="task" id="p2">
  <h2><span class="num">П-2</span> Опубликовать</h2>
  <ol class="steps"><li>После «да» нажать <strong>«Опубликовать»</strong> на странице ecom.</li></ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-ecom-podpis-foto-2026-10-01.html</code>, собран <code>seo-data/scripts/build_ecom_hero_who_brief.py</code>. Открывать локально, на alsn.ru не заливать.</p>
</div>
{b.COPY_JS}
</body></html>
"""
chk = re.sub(r"<pre.*?</pre>", "", doc, flags=re.S)
assert "\u2014" not in chk and "\u2013" not in chk, "тире"
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, len(head))
