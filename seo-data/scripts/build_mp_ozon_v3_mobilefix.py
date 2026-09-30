# -*- coding: utf-8 -*-
"""Правка для телефона на странице «Интеграция 1С с Ozon» после проверки 28.09.2026."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_mp_ozon_v3_brief as v  # noqa: E402

OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-1c-ozon-v3-mobile-2026-09-28.html")

FIX_RAW = """.photo img{aspect-ratio:16/9;object-position:50% 50%}
.tabs+.pane .shot img{aspect-ratio:1121/515;object-fit:cover;object-position:top}
.body .in>*,.hero .in>*,.pane>*,.case>*,.letter>*,.qpanel>*{min-width:0}
@media(max-width:1000px){
 .hero .in,.body .in,.qpanel,.case,.prices,.fit,.pane.on,.letter,.route,.final .in{grid-template-columns:minmax(0,1fr)}
 .tabs{width:auto}.tabs button{padding:10px 12px;font-size:14px}
 .case .big{font-size:56px}
 .in{padding:0 18px}
 .hero .in{gap:24px}.hero .in>div:first-child{padding-bottom:0!important}.photo{margin-bottom:0}
}"""
FIX = "<style>\n" + v.prefix_css(FIX_RAW) + "\n</style>"

LIVE_COVER = "https://optim.tildacdn.com/tild3363-3664-4966-b837-393439303735/-/resize/800x/-/format/webp/case-ecotide-video-c.jpg.webp"
B2_LIVE = v.B2.replace(v.PH_COVER, LIVE_COVER)
assert v.PH_COVER not in B2_LIVE and 'data-tab="2"' in B2_LIVE

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Интеграция 1С с Ozon - правка для телефона - 28.09.2026</title>
<style>{b.BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Интеграция 1С с Ozon - фото, телефон и ссылки на отчёты</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-ozon">https://alsn.ru/1c-ozon</a> (в списке Тильды <code>1c-ozon</code>) · проверка живого сайта 28.09.2026, 14:05 · шаг после письменного «да»</p>
<div class="pills"><span class="pill ok">новый дизайн опубликован</span><span class="pill warn">осталось 2 правки, «Опубликовать» один раз в конце</span></div>

<div class="callout ok"><strong>Уже готово - не трогать:</strong> три новых блока стоят по порядку, старые блоки выключены, один заголовок H1, фото Сергея и обложка видео загружены, стили и частые вопросы в HEAD страницы, крошки на белом фоне. Работают кнопки заявки, ссылки «Купить», вкладки с отчётами, видеоотзыв и письмо СТГ ГВАРД. Карточка с ценой едет рядом при прокрутке.</div>

<section class="task" id="m1">
<h2><span class="num">М-1</span> Фото Сергея целиком, только отчёт Ozon во вкладке маржи, страница по ширине телефона</h2>
<span class="lbl">Что сделать</span><p>Дописать в конец HEAD страницы короткую правку стилей. Она чинит три вещи сразу.</p>
<span class="lbl">Зачем</span><p><strong>Фото на первом экране.</strong> Сейчас снимок обрезан, и левый монитор с отчётом «Расчёт себестоимости» уходит за край. После правки видно весь кадр: три монитора с отчётами и Сергея.</p>
<p><strong>Вкладка «Маржа по товарам».</strong> Сейчас в ней два отчёта подряд: Ozon и под ним WB. Страница про Ozon, поэтому остаётся только верхний отчёт «Расчёт себестоимости» с надписью OZON.</p>
<p><strong>Телефон.</strong> Сейчас страница шире экрана: правый край текста, цены и кнопок обрезан, страницу можно сдвинуть пальцем вбок. Виновата полоса вкладок «Маржа по товарам / Кластеры Ozon / Реклама»: она растягивает всю колонку. После правки всё помещается в ширину экрана.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Ничего не стирать. Курсор в самый конец, после последней строки → Enter → вставить код ниже → «Сохранить изменения».</li>
</ol>
{b.copybox('m1c', FIX)}
</section>

<section class="task" id="m2">
<h2><span class="num">М-2</span> Ссылки на отчёты и видеоотзыв в новом окне</h2>
<span class="lbl">Что сделать</span><p>Заменить код основного блока на новый. В нём две правки.</p>
<span class="lbl">Зачем</span><p><strong>Ссылки на отчёты.</strong> Подписи «Отчёт по марже», «Расчёт по кластерам», «Расчёт ДРР» в тёмной панели «На какие вопросы отвечает модуль» сейчас оранжевые, но не нажимаются. После замены клик прокручивает страницу к разделу 03 «Отчёты, которых нет в типовом обмене» и сразу открывает нужную вкладку. Человек видит настоящий экран отчёта в 1С.</p>
<p><strong>Видеоотзыв EcoTide.</strong> Сейчас ролик запускается прямо на странице. По правилу проекта обложка с кнопкой play остаётся, а сам ролик открывается в новом окне VK Видео по обычной ссылке.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Второй новый блок T123, сразу под лентой «Как выглядит день с модулем». Начинается с карточки «Паспорт модуля 40 700 ₽», внутри разделы 01-07 до «Частые вопросы».</div>
<ol class="steps">
<li>Этот блок → «Контент» → выделить весь код (Ctrl+A) → удалить.</li>
<li>Вставить код ниже целиком → «Сохранить и закрыть». Настройки блока (отступы 0) не менять. Адреса фото и обложки видео в коде уже стоят.</li>
<li>После шагов М-1 и М-2: «Опубликовать».</li>
</ol>
{b.copybox('m2c', B2_LIVE)}
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-ozon-v3-mobile-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_ozon_v3_mobilefix.py</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT)
