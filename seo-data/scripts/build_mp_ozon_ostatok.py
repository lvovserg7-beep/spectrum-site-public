# -*- coding: utf-8 -*-
"""Остаток по странице «Интеграция 1С с Ozon» после проверки 28.09.2026."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402

OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-1c-ozon-ostatok-2026-09-28.html")

CRUMBS = """<nav aria-label="Хлебные крошки" style="font-size:14px;line-height:1.4;color:#8a8a8a;padding:8px 20px 0;">
  <a href="https://alsn.ru/" style="color:#8a8a8a;text-decoration:none;" aria-label="Главная">
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
  </a>
  <span style="margin:0 6px;">/</span>
  <a href="https://alsn.ru/casemarketplace" style="color:#8a8a8a;text-decoration:none;">Модуль 1С для маркетплейсов</a>
  <span style="margin:0 6px;">/</span>
  <span style="color:#555;">Интеграция 1С с Ozon</span>
</nav>"""

CTA_FIX = """<style>
.as-cta .as-btn{flex-shrink:0;white-space:nowrap}
@media (max-width:640px){.as-cta .as-btn{width:100%;white-space:normal}}
</style>"""

O7 = next(x for x in b.BLOCKS if x["id"] == "o7")["code"]

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Интеграция 1С с Ozon - остаток после проверки - 28.09.2026</title>
<style>{b.BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Интеграция 1С с Ozon - остаток после проверки</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-ozon">https://alsn.ru/1c-ozon</a> (в списке Тильды <code>1c-ozon</code>) · проверка живого сайта 28.09.2026, 10:06 · каждый шаг после письменного «да» · «Опубликовать» один раз в конце</p>
<div class="pills"><span class="pill ok">новый вид опубликован</span><span class="pill warn">осталось 3 правки</span></div>

<div class="callout danger">HEAD сайта не трогать. Служебный код в HEAD страницы не стирать, только дописывать в конец. Старые выключенные блоки не включать и не удалять.</div>

<div class="callout ok"><strong>Уже готово - не трогать:</strong> семь новых экранов стоят по порядку, оформление в HEAD страницы, один H1 «Интеграция 1С с Ozon», пять старых блоков выключены, кнопки ведут на форму заявки и в карточки каталога, скриншоты с подписями, title, описание, картинка для пересылки, служебный код с одной датой.</div>

<div class="toc"><strong>Остаток</strong><ol>
<li><a href="#a1">А-1. Вернуть хлебные крошки</a></li>
<li><a href="#a2">А-2. Сноска про новые функции в «Сколько стоит»</a></li>
<li><a href="#a3">А-3. Кнопка в тёмной плашке - в одну строку</a></li>
</ol></div>

<section class="task" id="a1">
<h2><span class="num">А-1</span> Вернуть хлебные крошки</h2>
<span class="lbl">Что сделать</span><p>Над первым экраном снова показать строку «дом / Модуль 1С для маркетплейсов / Интеграция 1С с Ozon». Сейчас её на странице нет.</p>
<span class="lbl">Зачем</span><p>По крошкам человек за один клик уходит на общую страницу модуля. Без них страница Ozon выглядит оторванной от раздела. Служебная разметка пути в HEAD осталась, а видимой строки нет, и поисковик видит расхождение.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Самый верх холста, между меню и новым первым экраном (оранжевая надпись «Модуль для селлеров Ozon» и заголовок «Интеграция 1С с Ozon»). Скорее всего блок крошек T123 выключили вместе со старыми блоками: он полупрозрачный. Может стоять и ниже, среди пяти выключенных старых блоков.</div>
<ol class="steps">
<li><strong>Если выключенный блок крошек нашёлся:</strong> меню блока «Ещё» / три точки → «Включить блок». Если он стоит не наверху - перетащить стрелками «вверх» так, чтобы он был сразу под меню и над первым экраном.</li>
<li><strong>Если блока нет совсем:</strong> навести мышь между меню и первым экраном → «+» → «Другое» → T123 «HTML-код» → «Контент» → вставить код ниже → «Сохранить и закрыть».</li>
<li>У блока крошек → «Настройки» → «Цвет фона» <code>#F7F8FA</code>, «Отступ сверху» и «Отступ снизу» 0 → «Сохранить и закрыть».</li>
</ol>
<div class="pair-label">Код крошек (только если блок пришлось ставить заново)</div>
{b.copybox('a1c', CRUMBS)}
<div class="pair-label">Цвет фона</div>
{b.copybox('a1bg', '#F7F8FA')}
</section>

<section class="task" id="a2">
<h2><span class="num">А-2</span> Сноска про новые функции в «Сколько стоит»</h2>
<span class="lbl">Что сделать</span><p>Заменить код блока «Сколько стоит» на новый. В нём звёздочка у слов «подписка даёт обновления*» и сноска: «Принимаем любые предложения по новым функциям модуля. Часть из них можем реализовать бесплатно, на своё усмотрение».</p>
<span class="lbl">Зачем</span><p>Решение от 28.09: не обещать бесплатные функции без условий, а говорить, что предложения принимаем и часть делаем бесплатно на своё усмотрение. Блок вставили до этого решения.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Блок T123 с заголовком «Сколько стоит» и двумя карточками «Только Ozon» (40 700 ₽) и «Ozon и Wildberries» (69 990 ₽). Стоит сразу над тёмной плашкой «Покажем, как это работает с вашим кабинетом Ozon».</div>
<ol class="steps">
<li>Этот блок → «Контент» → выделить весь код (Ctrl+A) → удалить.</li>
<li>Вставить код ниже целиком → «Сохранить и закрыть». Настройки блока (отступы 0) не менять.</li>
</ol>
<div class="pair-label">Новый код блока «Сколько стоит»</div>
{b.copybox('a2c', O7)}
</section>

<section class="task" id="a3">
<h2><span class="num">А-3</span> Кнопка в тёмной плашке - в одну строку</h2>
<span class="lbl">Что сделать</span><p>Дописать в HEAD страницы короткую правку стиля. Кнопка «Записаться на демонстрацию» в тёмной плашке внизу перестанет переноситься на две строки.</p>
<span class="lbl">Зачем</span><p>Сейчас на компьютере кнопка сжата и текст разбит на «Записаться на / демонстрацию». Выглядит как ошибка вёрстки рядом с главным призывом.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>Ничего не стирать. Курсор в самый конец, после последней строки <code>&lt;/style&gt;</code> (это конец оформления из прошлой инструкции) → Enter → вставить код ниже → «Сохранить изменения».</li>
<li>После трёх правок: «Опубликовать».</li>
</ol>
<div class="pair-label">Код в конец HEAD страницы</div>
{b.copybox('a3c', CTA_FIX)}
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-ozon-ostatok-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_ozon_ostatok.py</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT)
