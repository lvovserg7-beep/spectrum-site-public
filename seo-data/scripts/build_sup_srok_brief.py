# -*- coding: utf-8 -*-
"""Остаток tier4-postavshiki-v3: срок подключения «2 недели» на 13 карточках поставщиков.

Новый дизайн на всех 13 страницах стоит (проверено на alsn.ru 30.09.2026), но блоки вставлены из версии
до ответа заказчика про срок. Сборщик сверяет живой код с новым (разница только в сроке) и пишет
seo-data/tilda-briefs/tier4-postavshiki-v3-2026-09-30.html заново, только с открытыми шагами.
"""
import html
import os
import re
import sys
import time
import urllib.request as u

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sup_cards_v3 as m  # noqa: E402

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
SROK_DT = "<dt>Подключение</dt><dd>2 недели</dd>"


def norm(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r">\s+<", "><", s)).strip()


def without_srok_b2(b2):
    b2 = norm(b2).replace(SROK_DT, "")
    b2, n = re.subn(r"<details><summary>Сколько времени занимает подключение[^<]*</summary><p>[^<]*</p></details>", "", b2)
    assert n == 1
    return b2


def faq_ld(head):
    return re.search(r'<script type="application/ld\+json">\s*\{[^<]*?"@type": "FAQPage".*?</script>', head, re.S).group(0)


def check_live(s, head, b2):
    h = u.urlopen(u.Request(f"https://alsn.ru/{s['slug']}?chk=1850", headers={"User-Agent": UA}), timeout=30).read().decode("utf-8")
    live = norm(h)
    b2_ok = without_srok_b2(b2) in live
    rest = norm(head.replace(faq_ld(head), ""))
    head_rest_ok = all(norm(x) in live for x in re.split(r"\n(?=<)", head.replace(faq_ld(head), "")) if x.strip())
    head_new_ok = norm(faq_ld(head)) in live
    return b2_ok, head_rest_ok, head_new_ok, bool(rest)


def box(cid, text):
    return m.box(cid, text)


def page_html(n, s, head, b2, need_head):
    slug, url, name = s["slug"], f"https://alsn.ru/{s['slug']}", m.h1_text(s)
    q = f"Сколько времени занимает подключение {s['gen']}?"
    k = 1
    parts = []
    if need_head:
        parts.append(f"""
<section class="task" id="p{n}-{k}">
<h3><span class="num">{n}.{k}</span> HEAD страницы: добавить вопрос про срок</h3>
<p>Код HEAD тот же, что стоит сейчас, плюс вопрос «{q}» в служебном списке частых вопросов. Без него поисковик видит на экране вопрос, которого нет в коде.</p>
<ol class="steps">
<li>Список страниц → <code>{slug}</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{box(f"p{n}h", head)}
<p class="muted">Тот же код в файле <code>_head-{slug}-2026-09-30.txt</code>. Вне списка вопросов код совпадает с тем, что на сайте сейчас (сверено 30.09.2026).</p>
</section>""")
        k += 1
    parts.append(f"""
<section class="task" id="p{n}-{k}">
<h3><span class="num">{n}.{k}</span> Основной блок: строка «Подключение» и вопрос про срок</h3>
<p>В паспорте после «Доступ к API» появится строка «Подключение: 2 недели», в частых вопросах перед «Можно подключить других поставщиков?» вопрос «{q}» с ответом «Подключение одного поставщика занимает 2 недели.». Остальной код блока совпадает с тем, что на сайте сейчас (сверено 30.09.2026).</p>
<div class="where"><strong>Где.</strong> Страница «{name}» ({url}). Блок T123 сразу под первым экраном в рамке: слева паспорт с ценой «103 950 ₽», справа разделы «Что приходит из {s['gen']} в 1С», «Модуль или личный кабинет», «Как идут данные», «Как получить доступ к {s['api']}», «Сколько стоит», «Частые вопросы». Новый блок не добавлять, код меняем в этом.</div>
<ol class="steps">
<li>Навести на блок → «Контент» → клик в поле кода → Ctrl+A → Delete → вставить код ниже целиком → «Сохранить и закрыть».</li>
</ol>
{box(f"p{n}b", b2)}
</section>""")
    k += 1
    parts.append(f"""
<section class="task" id="p{n}-{k}">
<h3><span class="num">{n}.{k}</span> Опубликовать</h3>
<ol class="steps"><li>Вверху редактора страницы <code>{slug}</code> → «Опубликовать». Отдельный шаг, после «да».</li></ol>
</section>""")
    return f"""
<details class="page" id="p{n}"{" open" if n == 1 else ""}>
<summary><span class="num">{n:02d}</span> {name} <span class="muted">· alsn.ru/{slug} · {k} шага</span></summary>
<div class="pbody">
<p class="muted"><a href="{url}">{url}</a> · в списке Тильды <code>{slug}</code> · макет: <a href="../competitors/screens/preview-sup-{slug}-v3.html">preview-sup-{slug}-v3.html</a></p>
{"".join(parts)}
</div>
</details>""", k


def main():
    m.build_previews()
    css = m.build_css()
    pages, toc, total = [], [], 0
    for n, s in enumerate(m.SUP, 1):
        head, b1, b2, b3, nfaq = m.page_code(s, css)
        open(os.path.join(m.BR, f"_head-{s['slug']}-2026-09-30.txt"), "w", encoding="utf-8").write(head)
        b2_ok, head_rest_ok, head_new_ok, _ = check_live(s, head, b2)
        assert b2_ok, f"{s['slug']}: основной блок на сайте отличается не только сроком"
        assert head_rest_ok, f"{s['slug']}: HEAD на сайте отличается не только вопросами"
        sec, steps = page_html(n, s, head, b2, need_head=not head_new_ok)
        pages.append(sec)
        total += steps
        toc.append(f'<li><a href="#p{n}">{m.h1_text(s)}</a> · <code>{s["slug"]}</code> · {steps} шага'
                   + ("" if head_new_ok else "") + "</li>")
        print(s["slug"], "HEAD уже с вопросом" if head_new_ok else "HEAD нужен", "| шагов", steps)
        time.sleep(4)
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Карточки поставщиков: срок подключения - 30.09.2026</title>
<style>{m.b.BRIEF_CSS}{m.BRIEF_EXTRA}</style>
</head>
<body>
<div class="wrap">
<h1>Карточки поставщиков: срок подключения «2 недели»</h1>
<p class="muted">13 страниц «Интеграция 1С с … по API» (Мерлион, OCS, Treolan, Марвел, DIGIS, ЭЛКО, 3Logic, ЭТМ iPRO, Ресурс-Медиа, AUVIX, ВТТ, ДССЛ, Русский Свет) · обновлено 30.09.2026 после проверки сайта: новый дизайн стоит везде, открыто {total} шагов · каждый шаг после письменного «да» · «Опубликовать» отдельным шагом в конце каждой страницы</p>

<div class="callout ok"><strong>Уже сделано - не трогать:</strong> 30.09.2026 на всех 13 страницах опубликован новый дизайн: HEAD страницы, первый экран в рамке, основной блок, последний экран, старые блоки выключены, заголовки вкладок и описания заменены (проверено на сайте). Задачи T3-5 и T3-6 из <code>tier3-ecom-postavshiki-2026-09-30.html</code> закрыты вместе с ним. Фото Павла Агеева, меню и ссылки из таблицы /ecom на месте.</div>

<div class="callout warn"><strong>Что осталось и почему.</strong> Блоки вставляли до ответа заказчика про срок подключения. Теперь срок можно писать: «2 недели». На каждой странице заменить код основного блока (строка в паспорте и вопрос), а на 12 страницах ещё и HEAD (тот же вопрос в служебном коде). На Мерлионе HEAD уже с вопросом, там только основной блок.</div>

<div class="callout danger">HEAD <strong>сайта</strong> не трогать, только HEAD каждой страницы. robots.txt, Bing, Twitter не трогаем. Telegram-бот на сайте остаётся.</div>

<div class="callout"><strong>Хлебные крошки.</strong> Старые крошки со стрелкой (T758) и недостающие T123 - в <code>tier2-breadcrumbs-wave-2026-09-28.html</code>. Служебный код крошек уже в HEAD этих страниц, второй раз не вставлять.</div>

<div class="toc"><strong>Страницы</strong><ol>
{"".join(toc)}
</ol></div>

{"".join(pages)}

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-postavshiki-v3-2026-09-30.html</code> · собирает <code>seo-data/scripts/build_sup_srok_brief.py</code> · HEAD по страницам: <code>seo-data/tilda-briefs/_head-{{slug}}-2026-09-30.txt</code></p>
</div>
{m.b.COPY_JS}
</body>
</html>"""
    chk = re.sub(r"<pre.*?</pre>", "", doc, flags=re.S)
    assert "\u2014" not in chk and "\u2013" not in chk, "тире"
    open(m.OUT, "w", encoding="utf-8").write(doc)
    print("ok", m.OUT, len(doc), "шагов", total)


if __name__ == "__main__":
    main()
