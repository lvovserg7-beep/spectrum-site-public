# -*- coding: utf-8 -*-
"""Инструкция для Тильды: вариант 3 «Паспорт модуля» на странице «Интеграция 1С с Ozon»."""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402

SRC = os.path.join(b.ROOT, "seo-data", "competitors", "screens", "preview-1c-ozon-v3.html")
OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-1c-ozon-v3-2026-09-28.html")

PH_PHOTO = "ВСТАВЬТЕ_ССЫЛКУ_НА_ФОТО"
PH_COVER = "ВСТАВЬТЕ_ССЫЛКУ_НА_ОБЛОЖКУ"
PH_SEO = "ВСТАВЬТЕ_ССЫЛКУ_НА_ЭКРАН_SEO"
PH_REEXP = "ВСТАВЬТЕ_ССЫЛКУ_НА_ЭКРАН_УСЛУГ"
IMG_LETTER = "https://static.tildacdn.com/tild3461-3830-4564-a330-396237393635/----.jpg"

src = open(SRC, encoding="utf-8").read()


def prefix_selectors(sel):
    out = []
    for s in sel.split(","):
        s = s.strip()
        if not s:
            continue
        if s.startswith(".lb"):
            out.append(s)
        elif s in (":root", "body"):
            out.append(".v3")
        elif s == "*":
            out.append(".v3 *")
        else:
            out.append(".v3 " + s)
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


css_raw = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
CSS_V3 = prefix_css(css_raw)

HEAD_CODE = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">\n'
    "<style>\n" + CSS_V3 + "\n</style>"
)

FAQ = [
    ("С какими конфигурациями 1С работает модуль?", "С 1С:Управление торговлей, 1С:УНФ, 1С:Комплексная автоматизация и 1С:ERP."),
    ("Что будет, когда закончится подписка?", "Модуль продолжит работать. Подписка нужна для обновлений под изменения API Ozon и техподдержки. Продление стоит столько же, сколько покупка."),
    ("Можно подключить несколько кабинетов Ozon?", "Да, число кабинетов не ограничено."),
    ("Сколько стоит внедрение?", "Зависит от того, насколько доработана ваша 1С. Посмотрим базу на звонке и назовём цену до начала работ."),
]
FAQ_LD = '<script type="application/ld+json">\n' + json.dumps({
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
}, ensure_ascii=False, indent=2) + "\n</script>"


def cut(start, end):
    i = src.index(start)
    j = src.index(end, i)
    return src[i:j].strip()


hero = cut("<!-- HERO -->", "<!-- BODY -->")
body = cut("<!-- BODY -->", '<section class="final">')
final = cut('<section class="final">', "<script>")
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1).strip()

hero = hero.replace("../../brand-images/allsun-hero-mp-employee-module.jpg", PH_PHOTO)
body = body.replace("../../brand-images/case-ecotide-video-cover.jpg", PH_COVER)
body = body.replace("../../brand-images/reviews/review-stgguard-2025-07-02.jpg", IMG_LETTER)
body = body.replace("../../brand-images/ozon-screens/ozon-1c-seo-generator.png", PH_SEO)
body = body.replace("../../brand-images/ozon-screens/ozon-1c-perevystavlenie-uslug.png", PH_REEXP)
body = body.replace('<a class="btn g" href="#">Купить модуль для Ozon</a>', f'<a class="btn g" href="{b.BUY_OZON}">Купить модуль для Ozon</a>')
body = body.replace('<a class="btn m" href="#">Купить на обе площадки</a>', f'<a class="btn m" href="{b.BUY_BOTH}">Купить на обе площадки</a>')
assert 'href="#"' not in body, "остались пустые ссылки"
assert "../../" not in hero + body + final, "остались локальные пути"

for a, c in (("'.tabs button'", "'.v3 .tabs button'"), ("'.pane'", "'.v3 .pane'"),
             ("'.video[data-embed]'", "'.v3 .video[data-embed]'"), ("'[data-zoom]'", "'.v3 [data-zoom]'"),
             ("'a[data-tab]'", "'.v3 a[data-tab]'")):
    script = script.replace(a, c)

B1 = f'<div class="v3">\n{hero}\n</div>'
B2 = f'<div class="v3">\n{body}\n</div>\n<script>\n(function(){{\n{script}\n}})();\n</script>'
B3 = f'<div class="v3">\n{final}\n</div>'


def box(cid, text, tpl=False):
    cls = ' class="tpl"' if tpl else ""
    return f'<div class="copybox"><pre id="{cid}"{cls}>{html.escape(text, quote=False)}</pre><button type="button" data-copy="{cid}">Копировать</button></div>'


OLD = """<table>
<tr><th>Что на экране сейчас (сверху вниз)</th><th>Тип блока</th></tr>
<tr><td>Оранжевая надпись «Модуль для селлеров Ozon», заголовок «Интеграция 1С с Ozon», цена 40 700 ₽ и маршрут из трёх шагов</td><td>T123 HTML-код</td></tr>
<tr><td>«Что синхронизируется с Ozon», шесть карточек</td><td>T123 HTML-код</td></tr>
<tr><td>«Что особенно важно на Ozon», три ряда со скриншотами</td><td>T123 HTML-код</td></tr>
<tr><td>«Результат клиента», EcoTide и 20 млн ₽</td><td>T123 HTML-код</td></tr>
<tr><td>«Кому подходит», три карточки</td><td>T123 HTML-код</td></tr>
<tr><td>«Сколько стоит», карточки «Только Ozon» и «Ozon и Wildberries»</td><td>T123 HTML-код</td></tr>
<tr><td>Тёмная плашка «Покажем, как это работает с вашим кабинетом Ozon»</td><td>T123 HTML-код</td></tr>
</table>"""

EXTRA_CSS = """
.urlrow{display:grid;grid-template-columns:170px 1fr;gap:10px;align-items:center;margin:8px 0}
.urlrow input{width:100%;padding:9px 11px;border:1px solid #cfcfca;border-radius:8px;font:14px ui-monospace,Consolas,monospace}
.urlrow input.ok{border-color:#1a7f4b;background:#e8f6ee}
.urlstate{font-size:13px;margin-top:6px}
"""

TPL_JS = """<script>
(function(){
var P=%s, C=%s;
var pres=[].slice.call(document.querySelectorAll('pre.tpl'));
pres.forEach(function(p){p._tpl=p.textContent;});
function upd(){
  var ph=document.getElementById('u-photo').value.trim(), cv=document.getElementById('u-cover').value.trim();
  document.getElementById('u-photo').classList.toggle('ok',/^https:\\/\\/static\\.tildacdn\\.com\\//.test(ph));
  document.getElementById('u-cover').classList.toggle('ok',/^https:\\/\\/static\\.tildacdn\\.com\\//.test(cv));
  pres.forEach(function(p){p.textContent=p._tpl.split(P).join(ph||P).split(C).join(cv||C);});
  var s=document.getElementById('u-state');
  s.textContent=(ph&&cv)?'Ссылки подставлены в код шагов В-3 и В-4.':'Пока в коде стоят заглушки. Вставьте обе ссылки.';
}
['u-photo','u-cover'].forEach(function(id){document.getElementById(id).addEventListener('input',upd);});
upd();
})();
</script>""" % (json.dumps(PH_PHOTO, ensure_ascii=False), json.dumps(PH_COVER, ensure_ascii=False))

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый дизайн страницы «Интеграция 1С с Ozon» (вариант 3) - 28.09.2026</title>
<style>{b.BRIEF_CSS}{EXTRA_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый дизайн страницы «Интеграция 1С с Ozon»</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-ozon">https://alsn.ru/1c-ozon</a> (в списке Тильды <code>1c-ozon</code>) · вариант 3 «Паспорт модуля» · 28.09.2026 · каждый шаг после письменного «да» · «Опубликовать» один раз в конце (В-7)</p>
<div class="pills"><span class="pill ok">макет согласован</span><span class="pill warn">8 шагов, старое выключаем, не удаляем</span></div>

<div class="callout">Как выглядит результат: <a href="../competitors/screens/preview-1c-ozon-v3.html">макет страницы</a> (открыть в браузере). Меню сайта, хлебные крошки, «Наши клиенты» и подвал остаются как есть.</div>

<div class="callout danger">HEAD сайта не трогать (данные компании). В HEAD страницы уже есть служебный код и оформление прошлой версии: <strong>ничего не стирать</strong>, новое дописывать в конец. Старые блоки выключать, а не удалять: так можно откатиться за минуту. robots.txt, Bing, Twitter не трогаем.</div>

<div class="toc"><strong>Шаги</strong><ol>
<li><a href="#v0">В-0. Загрузить фото Сергея и обложку видеоотзыва</a></li>
<li><a href="#v1">В-1. Оформление нового дизайна в HEAD страницы</a></li>
<li><a href="#v2">В-2. Белый фон у хлебных крошек</a></li>
<li><a href="#v3">В-3. Первый экран с фото</a></li>
<li><a href="#v4">В-4. Основная часть: паспорт модуля и разделы 01-07</a></li>
<li><a href="#v5">В-5. Заявка внизу страницы</a></li>
<li><a href="#v6">В-6. Выключить семь блоков прошлой версии</a></li>
<li><a href="#v7">В-7. Опубликовать</a></li>
</ol></div>

<section class="task" id="v0">
<h2><span class="num">В-0</span> Загрузить фото Сергея и обложку видеоотзыва</h2>
<span class="lbl">Что сделать</span><p>Загрузить в Тильду две картинки и получить их адреса. Остальные картинки (скриншоты 1С, письмо СТГ ГВАРД) уже на сайте.</p>
<span class="lbl">Зачем</span><p>Код страницы берёт картинки по адресу. Пока фото и обложки нет в Тильде, на их месте будет пустота.</p>
<span class="lbl">Файлы на компьютере</span>
<table>
<tr><th>Что</th><th>Файл в папке проекта</th></tr>
<tr><td>Фото Сергея Никешина у мониторов</td><td><code>seo-data/brand-images/allsun-hero-mp-employee-module.jpg</code></td></tr>
<tr><td>Обложка видеоотзыва EcoTide («20 млн за 6 мес»)</td><td><code>seo-data/brand-images/case-ecotide-video-cover.jpg</code></td></tr>
</table>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Открыть страницу <code>1c-ozon</code> на редактирование. Прокрутить в самый низ холста, над подвалом → «+» → «Изображение» → блок <strong>T107</strong> («Картинка на всю ширину» или просто «Картинка»).</li>
<li>В новом блоке → «Контент» → «Загрузить файл» → выбрать фото Сергея → «Сохранить и закрыть».</li>
<li>Добавить ещё один блок T107 так же и загрузить в него обложку видеоотзыва.</li>
<li>Вверху редактора нажать «Предпросмотр». На открывшейся странице внизу правой кнопкой по фото → «Открыть изображение в новой вкладке». Скопировать адрес из строки браузера. Он должен начинаться с <code>https://static.tildacdn.com/</code>. Если адрес начинается с <code>thb.tildacdn.com</code> или в нём есть <code>/-/resize/</code>, пришлите его в чат, поправлю.</li>
<li>Вставить адрес в поле ниже. То же для обложки.</li>
<li>Оба блока T107 → «Ещё» / три точки → «Выключить блок». <strong>Не удалять</strong>, иначе Тильда может убрать файл.</li>
</ol>
<div class="urlrow"><label for="u-photo">Адрес фото Сергея</label><input id="u-photo" placeholder="https://static.tildacdn.com/tild..../....jpg"></div>
<div class="urlrow"><label for="u-cover">Адрес обложки видео</label><input id="u-cover" placeholder="https://static.tildacdn.com/tild..../....jpg"></div>
<div class="urlstate" id="u-state"></div>
</section>

<section class="task" id="v1">
<h2><span class="num">В-1</span> Оформление нового дизайна в HEAD страницы</h2>
<span class="lbl">Что сделать</span><p>Дописать в конец HEAD страницы шрифт Onest, стили нового дизайна и служебный блок частых вопросов.</p>
<span class="lbl">Зачем</span><p>Без стилей новые блоки будут голым текстом. Служебный блок вопросов подсказывает Яндексу и Google, что на странице есть ответы про конфигурации, подписку и цену. Все стили начинаются с <code>.v3</code> и не задевают остальной сайт и старые блоки.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Ничего не стирать. Курсор в самый конец, после последней строки → Enter → вставить первый код → Enter → вставить второй код → «Сохранить изменения».</li>
</ol>
<div class="pair-label">Код 1: шрифт и стили</div>
{box('v1a', HEAD_CODE)}
<div class="pair-label">Код 2: частые вопросы (служебный)</div>
{box('v1b', FAQ_LD)}
</section>

<section class="task" id="v2">
<h2><span class="num">В-2</span> Белый фон у хлебных крошек</h2>
<span class="lbl">Что сделать</span><p>Поменять фон блока крошек с серого на белый.</p>
<span class="lbl">Зачем</span><p>Новый первый экран белый. Серая полоса крошек над ним будет выглядеть как лишняя плашка.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Самый верх холста, сразу под меню. Блок T123 со строкой «дом / Модуль 1С для маркетплейсов / Интеграция 1С с Ozon».</div>
<ol class="steps">
<li>Блок крошек → «Настройки» → «Цвет фона» → вставить цвет ниже → «Сохранить и закрыть». Код крошек не трогать.</li>
</ol>
{box('v2a', '#FFFFFF')}
</section>

<section class="task" id="v3">
<h2><span class="num">В-3</span> Первый экран с фото</h2>
<span class="lbl">Что сделать</span><p>Поставить под крошками новый первый экран: заголовок «Интеграция 1С с Ozon», две кнопки, фото Сергея с подписью и светлая лента «Как выглядит день с модулем».</p>
<span class="lbl">Зачем</span><p>Первое, что видит человек: о чём страница, что модуль делает и живой разработчик модуля за работой. Кнопка сразу открывает форму заявки.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Навести мышь между блоком крошек и старым первым экраном (оранжевая надпись «Модуль для селлеров Ozon») → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
<div class="callout warn">Сначала сделайте шаг В-0: в коде должен стоять адрес фото, а не слово «ВСТАВЬТЕ_ССЫЛКУ_НА_ФОТО».</div>
{box('v3a', B1, tpl=True)}
</section>

<section class="task" id="v4">
<h2><span class="num">В-4</span> Основная часть: паспорт модуля и разделы 01-07</h2>
<span class="lbl">Что сделать</span><p>Одним блоком поставить всё остальное: карточку модуля сбоку и разделы «На какие вопросы отвечает модуль», «Как идут данные», вкладки с отчётами, отзывы клиентов (видео EcoTide и письмо СТГ ГВАРД), «Кому подходит», «Сколько стоит», частые вопросы.</p>
<span class="lbl">Зачем</span><p>Карточка с ценой и кнопками едет рядом, пока человек листает страницу, поэтому все разделы должны быть в одном блоке с ней. Кнопки «Купить» ведут в карточки каталога, видеоотзыв открывается в новом окне VK Видео, письмо открывается целиком по клику.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага В-3 → «+» → «Другое» → <strong>T123 «HTML-код»</strong>.</li>
<li>«Контент» → вставить код ниже → «Сохранить и закрыть». Код длинный, это нормально.</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
<div class="callout warn">В коде должен стоять адрес обложки из шага В-0, а не «ВСТАВЬТЕ_ССЫЛКУ_НА_ОБЛОЖКУ».</div>
{box('v4a', B2, tpl=True)}
</section>

<section class="task" id="v5">
<h2><span class="num">В-5</span> Заявка внизу страницы</h2>
<span class="lbl">Что сделать</span><p>Поставить последний экран: «Покажем модуль на вашем кабинете Ozon», телефон и кнопка «Записаться на демонстрацию».</p>
<span class="lbl">Зачем</span><p>Кто дочитал до конца, получает понятный следующий шаг, не прокручивая наверх.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Под блоком из шага В-4 → «+» → «Другое» → <strong>T123 «HTML-код»</strong> → «Контент» → вставить код → «Сохранить и закрыть».</li>
<li>«Настройки» блока → отступы 0 → «Сохранить и закрыть».</li>
</ol>
{box('v5a', B3)}
</section>

<section class="task" id="v6">
<h2><span class="num">В-6</span> Выключить семь блоков прошлой версии</h2>
<span class="lbl">Что сделать</span><p>Выключить старые экраны, которые теперь повторяют новые.</p>
<span class="lbl">Зачем</span><p>Иначе на странице будет два заголовка «Интеграция 1С с Ozon» и всё содержимое дважды. Выключенный блок не виден на сайте, но остаётся в редакторе на случай отката.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Семь блоков T123 подряд сразу под новым блоком из шага В-5. Блоки, выключенные раньше (старые тексты «Что синхронизируется…», кнопка «Купить модуль 1С для Ozon»), так и оставить выключенными.</div>
<ol class="steps">
<li>У каждого блока из таблицы → «Ещё» / три точки → «Выключить блок». Блок станет полупрозрачным.</li>
<li>Меню, крошки, «Наши клиенты», подвал и два выключенных T107 из шага В-0 не трогать.</li>
</ol>
{OLD}
</section>

<section class="task" id="v7">
<h2><span class="num">В-7</span> Опубликовать</h2>
<span class="lbl">Что сделать</span><p>Опубликовать страницу.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Вверху редактора → «Опубликовать».</li>
<li>Написать в чат «опубликовано»: проверю живую страницу (один заголовок, кнопки, видео, письмо, телефон).</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-ozon-v3-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_ozon_v3_brief.py</code> из макета <code>seo-data/competitors/screens/preview-1c-ozon-v3.html</code></p>
</div>
{b.COPY_JS}
{TPL_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, len(HEAD_CODE), len(B1), len(B2), len(B3))
