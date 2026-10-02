# -*- coding: utf-8 -*-
"""Инструкция v3: три типа внедрения + фамилия Мазницына - вставка HEAD, B1 и B2 целиком."""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_vnedrenie_v3_preview as p  # noqa: E402

p.main()
BR = os.path.join(b.ROOT, "seo-data", "tilda-briefs")
OUT = os.path.join(BR, "tier4-development1c-types-2026-09-30.html")
HEAD_TXT = os.path.join(BR, "_head-development1c-2026-09-30.txt")
URL = "https://alsn.ru/development1c"

src = open(os.path.join(p.SCR, "preview-development1c-v3.html"), encoding="utf-8").read()


def cut(start, end, keep_end=False):
    i = src.index(start)
    j = src.index(end, i)
    return src[i + len(start):j + (len(end) if keep_end else 0)].strip()


hero = cut("<!-- HERO -->", "<!-- BODY -->").replace(p.PHOTO, p.PHOTO_CDN)
B1 = f'<div class="v3">\n{hero}\n</div>'
body = cut("<!-- BODY -->", "<!-- FINAL -->")
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()
for a, c in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
             ("'[data-zoom]'", "'.v3 [data-zoom]'"), ("'a[data-tab]'", "'.v3 a[data-tab]'")):
    script = script.replace(a, c)

B2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'
HEAD = open(HEAD_TXT, encoding="utf-8").read().strip()

assert "Мазницына" in B1
assert "Мазницина" not in B1
assert p.PHOTO_CDN in B1
assert "../../" not in B1
assert "Мазницына" not in B2
assert "Три типа внедрения" in B2
assert "Консультационное" in B2
assert "MPV" not in B2
assert "депортамент" not in B2
assert "консультационный, agile и проектный" in HEAD
assert ".v3 .prices.three .pc .p{" in HEAD
for s in (HEAD, B1, B2):
    assert "\u2014" not in s and "\u2013" not in s


def box(cid, text):
    return (
        f'<div class="copybox"><pre id="{cid}">{html.escape(text, quote=False)}</pre>'
        f'<button type="button" data-copy="{cid}">Копировать</button></div>'
    )


doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Три типа внедрения на странице «Внедрение 1С» - 30.09.2026</title>
<style>{b.BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Три типа внедрения на странице «Внедрение 1С»</h1>
<p class="muted">Страница: «Внедрение 1С» (<a href="{URL}">{URL}</a>, в списке Тильды <code>development1c</code>) · страница уже в формате v3: копируете блок целиком, вставляете поверх, ничего не ищете внутри · каждый шаг после письменного «да» · «Опубликовать» один раз в конце (Т-4)</p>
<div class="pills"><span class="pill ok">макет готов</span><span class="pill warn">4 шага, вставка целиком</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-development1c-v3.html">макет страницы</a> (открыть в браузере). Блок 07 - три типа внедрения. На первом экране подпись: Софья Мазницына.</div>

<div class="callout danger">HEAD <strong>сайта</strong> (Настройки сайта → Вставка кода) не трогать. Крошки и последний экран с телефоном (B3) не трогать. В шагах Т-1, Т-2 и Т-3 старое содержимое поля стереть целиком и вставить новое. robots.txt, Bing, Twitter не трогаем.</div>

<div class="toc"><strong>Шаги</strong><ol>
<li><a href="#t1">Т-1. HEAD страницы целиком</a></li>
<li><a href="#t2">Т-2. Первый экран целиком (фамилия Мазницына)</a></li>
<li><a href="#t3">Т-3. Основной блок (паспорт и разделы) целиком</a></li>
<li><a href="#t4">Т-4. Опубликовать</a></li>
</ol></div>

<section class="task" id="t1">
<h2><span class="num">Т-1</span> HEAD страницы целиком</h2>
<span class="lbl">Что сделать</span><p>Стереть всё в HEAD этой страницы и вставить один готовый код. В нём оформление карточек и новый ответ на вопрос «Сколько стоит внедрение?».</p>
<span class="lbl">Зачем</span><p>Без новой строки стилей крупные слова на карточках поедут. Ответ в служебном коде должен совпадать с текстом на экране из следующего шага.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Список страниц → <code>development1c</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Скопировать старое содержимое в блокнот (Ctrl+A, Ctrl+C). Это откат.</li>
<li>В поле: Ctrl+A → Delete → вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
{box('t1a', HEAD)}
</section>

<section class="task" id="t2">
<h2><span class="num">Т-2</span> Первый экран целиком (фамилия Мазницына)</h2>
<span class="lbl">Что сделать</span><p>Открыть T123 первого экрана в рамке. Стереть весь код и вставить код ниже. В подписи на фото: Софья Мазницына. Адрес картинки тот же, что уже на сайте.</p>
<span class="lbl">Зачем</span><p>В фамилии буква «ы»: Мазницына, не Мазницина.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Внедрение 1С» (https://alsn.ru/development1c). Холст сразу под крошками: рамка с заголовком «Внедрение 1С под ключ» и фото справа (на живом сайте rec4363614001). Не путать с блоком паспорта ниже.</div>
<ol class="steps">
<li>Клик по этому T123 → «Контент».</li>
<li>Ctrl+A → Delete → вставить код ниже целиком → «Сохранить и закрыть».</li>
</ol>
{box('t2a', B1)}
</section>

<section class="task" id="t3">
<h2><span class="num">Т-3</span> Основной блок (паспорт и разделы) целиком</h2>
<span class="lbl">Что сделать</span><p>Открыть T123 с паспортом слева и разделами 01-08 справа. Стереть весь код в поле и вставить код ниже. Серый экран внизу с телефоном не открывать.</p>
<span class="lbl">Зачем</span><p>В этом блоке сразу паспорт, вопрос про цену, три типа внедрения и частые вопросы.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где.</strong> Страница «Внедрение 1С» (https://alsn.ru/development1c). Следующий T123 после первого экрана: паспорт «после звонка» слева и разделы с номерами 01-08 справа (на живом сайте rec4363615101). Не путать с T123 первого экрана и с T123 «Разберём, какой контур 1С вам нужен».</div>
<ol class="steps">
<li>Клик по этому T123 → «Контент».</li>
<li>Ctrl+A → Delete → вставить код ниже целиком → «Сохранить и закрыть».</li>
</ol>
{box('t3a', B2)}
</section>

<section class="task" id="t4">
<h2><span class="num">Т-4</span> Опубликовать</h2>
<span class="lbl">Что сделать</span><p>Опубликовать страницу «Внедрение 1С».</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Вверху редактора <code>development1c</code> → «Опубликовать». Отдельный шаг, после «да».</li>
<li>Написать в чат «опубликовано»: проверю фамилию Мазницына на первом экране, три карточки типов и ответ в частых вопросах.</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-development1c-types-2026-09-30.html</code> · HEAD: <code>seo-data/tilda-briefs/_head-development1c-2026-09-30.txt</code> · макет: <code>seo-data/competitors/screens/preview-development1c-v3.html</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

assert "Найти" not in doc
assert "Заменить на" not in doc
assert "\u2014" not in doc and "\u2013" not in doc
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, "HEAD", len(HEAD), "B1", len(B1), "B2", len(B2))


if __name__ == "__main__":
    pass
