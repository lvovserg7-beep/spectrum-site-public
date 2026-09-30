# -*- coding: utf-8 -*-
"""Блоки T123 для страницы «Интеграция 1С с Ozon» (alsn.ru/1c-ozon).

Собирает из одного источника:
  - инструкцию для Тильды: seo-data/tilda-briefs/tier4-1c-ozon-design-2026-09-28.html
  - локальное превью:      seo-data/competitors/screens/preview-1c-ozon.html
"""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BRIEF = os.path.join(ROOT, "seo-data", "tilda-briefs", "tier4-1c-ozon-design-2026-09-28.html")
PREVIEW = os.path.join(ROOT, "seo-data", "competitors", "screens", "preview-1c-ozon.html")

BUY_OZON = "https://alsn.ru/casemarketplace/tproduct/913805053-713209120582-modul-integratsii-1s-s-ozon"
BUY_BOTH = "https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz"
IMG_CLUSTER = "https://static.tildacdn.com/tild3563-6433-4535-a231-653461616463/noroot.png"
IMG_UNIT = "https://static.tildacdn.com/tild6161-6139-4730-b039-636631623135/___OZON_WB.jpg"
IMG_DRR = "https://static.tildacdn.com/tild6233-3339-4062-b232-666133343034/noroot.png"

CSS = """<style>
.as{--bg:#F7F8FA;--acc:#F55823;--ink:#212121;--line:#D7DADD;--soft:#FDE7DE;--mut:#5f6368;font-family:'Roboto',Arial,sans-serif;color:var(--ink);background:var(--bg);padding:64px 20px;box-sizing:border-box}
.as *{box-sizing:border-box}
.as.w{background:#fff}
.as.d{background:var(--ink);color:#fff}
.as-in{max-width:1160px;margin:0 auto}
.as-k{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}
.as h1{font-family:inherit;font-size:48px;line-height:1.1;font-weight:700;margin:0 0 18px;color:var(--ink)}
.as h2,.as .as-h2{font-family:inherit;font-size:34px;line-height:1.2;font-weight:700;margin:0 0 28px;color:inherit}
.as h3{font-family:inherit;font-size:24px;line-height:1.25;font-weight:700;margin:0 0 10px;color:var(--ink)}
.as-lead{font-size:19px;line-height:1.5;color:#3c4043;margin:0 0 22px;max-width:580px}
.as-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px}
.as-chips span{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;font-size:14px}
.as-price{display:inline-block;background:#fff;border:1px solid var(--line);border-radius:10px;padding:10px 16px;font-size:16px;margin:0 0 24px}
.as-price b{color:var(--acc);font-size:20px}
.as-btns{display:flex;flex-wrap:wrap;gap:12px}
.as-btn{display:inline-block;padding:15px 26px;border-radius:10px;font-size:16px;font-weight:700;line-height:1.2;text-decoration:none!important;transition:background .2s}
.as-btn.m{background:var(--acc);color:#fff!important}
.as-btn.m:hover{background:#dd4a18}
.as-btn.g{border:1.5px solid var(--ink);color:var(--ink)!important;background:transparent}
.as-hero{display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
.as-step{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.as-step small{display:block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}
.as-step b{display:block;font-size:19px;margin-bottom:4px}
.as-step span{font-size:14px;color:var(--mut)}
.as-step.r{background:var(--ink);border-color:var(--ink);color:#fff}
.as-step.r span{color:#cfcfcf}
.as-arr{text-align:center;color:var(--acc);font-size:20px;line-height:30px}
.as-note{font-size:15px;color:var(--mut);margin:20px 0 0}
.as-note a{color:var(--ink)!important;text-decoration:underline}
.as-grid{display:grid;gap:16px}
.as-g3{grid-template-columns:repeat(3,1fr)}
.as-g2{grid-template-columns:repeat(2,1fr)}
.as-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px}
.as.w .as-card{background:var(--bg)}
.as-card.a{border:2px solid var(--acc);background:#fff}
.as-ico{width:38px;height:38px;border-radius:10px;background:var(--soft);display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.as-ico i{display:block;width:16px;height:2px;background:var(--acc);box-shadow:0 -5px 0 var(--acc),0 5px 0 var(--acc)}
.as-card b{display:block;font-size:18px;margin-bottom:6px}
.as-card p{font-size:15px;line-height:1.45;color:var(--mut);margin:0}
.as-row{display:grid;grid-template-columns:.9fr 1.1fr;gap:44px;align-items:center;margin-bottom:44px}
.as-row p{font-size:16px;line-height:1.55;color:#3c4043;margin:0}
.as-shot{background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;box-shadow:0 8px 24px rgba(33,33,33,.06)}
.as-shot img{display:block;width:100%;height:auto;border-radius:8px}
.as-shot.top img{aspect-ratio:1121/500;object-fit:cover;object-position:top}
.as-strip{display:flex;justify-content:space-between;align-items:center;gap:20px;background:#fff;border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:14px;padding:20px 24px;font-size:16px;line-height:1.5}
.as-strip a{color:var(--acc)!important;font-weight:700;text-decoration:none!important;white-space:nowrap}
.as-case{display:grid;grid-template-columns:.8fr 1.2fr;gap:44px;align-items:center}
.as-big{font-size:56px;font-weight:700;line-height:1;margin-bottom:10px}
.as-mini{font-size:15px;color:var(--mut);margin:0}
.as-quote{border-left:4px solid var(--acc);background:var(--bg);border-radius:0 14px 14px 0;padding:22px 26px}
.as-quote p{font-size:19px;line-height:1.5;margin:0 0 12px}
.as-quote small{font-size:14px;color:var(--mut)}
.as-quote a{display:inline-block;margin-top:12px;color:var(--acc)!important;font-weight:700;text-decoration:none!important}
.as-pr{font-size:34px;font-weight:700;margin:12px 0 2px}
.as-link{display:inline-block;margin-top:16px;color:var(--acc)!important;font-weight:700;text-decoration:none!important}
.as-cta{display:flex;justify-content:space-between;align-items:center;gap:32px}
.as-cta .as-btn{flex-shrink:0;white-space:nowrap}
.as.d .as-h2{margin:0 0 8px;color:#fff}
.as.d .as-lead{color:#cfcfcf;margin:0}
@media (max-width:960px){.as-hero,.as-row,.as-case{grid-template-columns:1fr;gap:28px}.as-g3{grid-template-columns:1fr 1fr}.as h1{font-size:38px}.as-cta{flex-direction:column;align-items:flex-start}}
@media (max-width:640px){.as{padding:44px 16px}.as-g3,.as-g2{grid-template-columns:1fr}.as h1{font-size:31px}.as h2,.as .as-h2{font-size:26px;margin-bottom:20px}.as-lead{font-size:17px}.as-btn,.as-cta .as-btn{width:100%;text-align:center;white-space:normal}.as-strip{flex-direction:column;align-items:flex-start}.as-big{font-size:44px}.as-row{margin-bottom:32px}}
</style>"""

ICO = '<div class="as-ico"><i></i></div>'

BLOCKS = [
    {
        "id": "o2",
        "num": "O-2",
        "title": "Первый экран: заголовок, цена, две кнопки и схема",
        "what": "Добавить новый первый экран сразу под хлебными крошками. В нём тот же заголовок H1 «Интеграция 1С с Ozon», короткое объяснение, цена, кнопки «Записаться на демонстрацию» и «Купить модуль», справа схема «кабинет Ozon → модуль Аллсан → результат».",
        "why": "Сейчас наверху только заголовок и абзац, без цены и без кнопки. Человек из поиска не понимает, сколько стоит и что нажать. У конкурентов цены на первом экране тоже нет, поэтому здесь можно выделиться.",
        "where": "Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). Первый блок под меню - хлебные крошки (дом / Модуль 1С для маркетплейсов / Интеграция 1С с Ozon). Новый блок ставим <strong>сразу под крошками</strong>, над текущим блоком с заголовком «Интеграция 1С с Ozon».",
        "code": f"""<section class="as">
<div class="as-in as-hero">
<div>
<div class="as-k">Модуль для селлеров Ozon</div>
<h1>Интеграция 1С с Ozon</h1>
<p class="as-lead">Модуль Аллсан выгружает остатки и цены из вашей 1С в кабинет Ozon и забирает заказы обратно в 1С. Маржа по каждому товару считается в 1С каждый день.</p>
<div class="as-chips"><span>FBS</span><span>rFBS</span><span>DBS</span><span>любое число кабинетов</span></div>
<div class="as-price">от <b>40 700 ₽</b> в год · 1С:УТ, УНФ, КА, ERP</div>
<div class="as-btns"><a class="as-btn m" href="#popup:konsultacia">Записаться на демонстрацию</a><a class="as-btn g" href="{BUY_OZON}">Купить модуль</a></div>
<p class="as-note">Работаете ещё и с Wildberries? Смотрите <a href="https://alsn.ru/casemarketplace">модуль интеграции 1С с маркетплейсами</a>.</p>
</div>
<div>
<div class="as-step"><small>Кабинет Ozon Seller</small><b>Заказы, отчёты, реклама</b><span>все кабинеты и юрлица</span></div>
<div class="as-arr">↓</div>
<div class="as-step"><small>Модуль Аллсан</small><b>Обмен и расчёты в 1С</b><span>УТ · УНФ · КА · ERP</span></div>
<div class="as-arr">↓</div>
<div class="as-step r"><small>Результат</small><b>Товар в наличии на нужных складах</b><span>и видно, где реклама съедает маржу</span></div>
</div>
</div>
</section>""",
    },
    {
        "id": "o3",
        "num": "O-3",
        "title": "Что синхронизируется: шесть карточек вместо абзаца",
        "what": "Добавить блок с заголовком H2 «Что синхронизируется с Ozon» и шестью карточками. Тексты те же, что сейчас в абзаце, только разложены по карточкам.",
        "why": "Сейчас это один сплошной абзац. Карточки читаются за секунды: человек сразу видит, закрывает ли модуль его задачу.",
        "where": "Ставим сразу под новым первым экраном (задача O-2).",
        "code": f"""<section class="as w">
<div class="as-in">
<h2>Что синхронизируется с Ozon</h2>
<div class="as-grid as-g3">
<div class="as-card">{ICO}<b>Остатки и цены</b><p>Из 1С в кабинет Ozon, автоматически или вручную.</p></div>
<div class="as-card">{ICO}<b>Заказы FBS</b><p>Создаются в 1С сами, без ручного ввода.</p></div>
<div class="as-card">{ICO}<b>Отправления</b><p>Подготовка отправлений, этикетки и акты из 1С.</p></div>
<div class="as-card">{ICO}<b>Финансовые отчёты</b><p>Отчёты Ozon приходят в 1С, маржа считается автоматически.</p></div>
<div class="as-card">{ICO}<b>Реклама</b><p>Доля рекламных расходов по каждому товару каждый день.</p></div>
<div class="as-card">{ICO}<b>Последняя миля</b><p>Перевыставление услуг последней мили Ozon с НДС.</p></div>
</div>
</div>
</section>""",
    },
    {
        "id": "o4",
        "num": "O-4",
        "title": "Что особенно важно на Ozon: три скриншота из 1С",
        "what": "Добавить блок с заголовком H2 «Что особенно важно на Ozon»: кластеры, маржа, реклама. У каждого пункта короткий текст и настоящий скриншот из 1С. Внизу плашка про последнюю милю со ссылкой на отдельную страницу.",
        "why": "Это то, чего нет в обычном обмене 1С с Ozon и нет у конкурентов на странице Ozon. Скриншоты показывают, что модуль реальный, а не обещание. Картинки уже лежат на сайте, загружать ничего не нужно.",
        "where": "Ставим сразу под блоком «Что синхронизируется с Ozon» (задача O-3).",
        "code": f"""<section class="as">
<div class="as-in">
<h2>Что особенно важно на Ozon</h2>
<div class="as-row">
<div><div class="as-k">Кластеры</div><h3>Сколько и на какой склад отгрузить</h3><p>Модуль берёт остатки FBO с Ozon, продажи и сроки доставки по кластерам и подсказывает, сколько товара везти в каждый регион. Товар реже пропадает из наличия и выше стоит в выдаче.</p></div>
<div class="as-shot"><img src="{IMG_CLUSTER}" alt="Расчёт потребностей по кластерам Ozon в 1С" loading="lazy" width="1153" height="463"></div>
</div>
<div class="as-row">
<div><div class="as-k">Маржа</div><h3>Сколько вы заработали на каждом товаре</h3><p>Себестоимость, доставка Ozon, налог и эквайринг сведены в один отчёт. Прибыль видна по категориям и по каждому товару.</p></div>
<div class="as-shot top"><img src="{IMG_UNIT}" alt="Отчёт по себестоимости и прибыли Ozon в 1С" loading="lazy" width="1121" height="1055"></div>
</div>
<div class="as-row">
<div><div class="as-k">Реклама</div><h3>Какая реклама съедает маржу</h3><p>Модуль каждый день считает долю рекламных расходов по товарам, поиск и трафарет отдельно. Видно, где рекламу пора остановить.</p></div>
<div class="as-shot"><img src="{IMG_DRR}" alt="Расчёт доли рекламных расходов Ozon в 1С" loading="lazy" width="823" height="412"></div>
</div>
<div class="as-strip"><span><b>Последняя миля.</b> Услуги последней мили Ozon перевыставляются с НДС за три клика в 1С.</span><a href="https://alsn.ru/perevystavlenie-uslug-posledney-mili-ozon-v-1s">Как это работает →</a></div>
</div>
</section>""",
    },
    {
        "id": "o5",
        "num": "O-5",
        "title": "Результат клиента: кейс EcoTide",
        "what": "Добавить блок с цифрой «20 млн ₽» и цитатой руководителя магазина EcoTide со ссылкой на видеоотзыв.",
        "why": "На странице Ozon сейчас нет ни одного отзыва. EcoTide - как раз магазин на Ozon, и этот видеоотзыв уже опубликован на странице модуля. Цифра из отзыва клиента убеждает сильнее любого описания функций.",
        "where": "Ставим сразу под блоком «Что особенно важно на Ozon» (задача O-4).",
        "code": """<section class="as w">
<div class="as-in">
<h2>Результат клиента</h2>
<div class="as-case">
<div><div class="as-big">20 млн ₽</div><p class="as-mini">выручки на Ozon за 6 месяцев с нуля, магазин EcoTide</p></div>
<div class="as-quote"><p>«Мы начали наш бизнес на OZON совершенно с 0 и всего за полгода сделали выручку в 20 000 000 рублей. Благодаря правильной организации контроля и учёта в программе 1С наш товар поднялся в ТОПе на 2 место по всей РФ».</p><small>Елизавета, руководитель магазина EcoTide</small><br><a href="https://alsn.ru/casemarketplace#rec1108347471">Смотреть видеоотзыв →</a></div>
</div>
</div>
</section>""",
    },
    {
        "id": "o6",
        "num": "O-6",
        "title": "Кому подходит: три ситуации",
        "what": "Добавить блок с заголовком H2 «Кому подходит»: одна строка и три карточки с узнаваемыми ситуациями.",
        "why": "Человек быстрее узнаёт себя в конкретной ситуации, чем в общем описании. Текст тот же по смыслу, что сейчас на странице.",
        "where": "Ставим сразу под блоком «Результат клиента» (задача O-5).",
        "code": """<section class="as">
<div class="as-in">
<h2>Кому подходит</h2>
<p class="as-lead">Селлерам и компаниям, у которых учёт уже в 1С, а продажи идут или планируются на Ozon.</p>
<div class="as-grid as-g3">
<div class="as-card"><b>Остатки ведут вручную</b><p>и уже начались ошибки, отмены и штрафы.</p></div>
<div class="as-card"><b>Несколько кабинетов</b><p>или несколько юрлиц на Ozon в одной 1С.</p></div>
<div class="as-card"><b>Не видно прибыли</b><p>по товарам после комиссий, логистики и рекламы.</p></div>
</div>
</div>
</section>""",
    },
    {
        "id": "o7",
        "num": "O-7",
        "title": "Сколько стоит: две карточки с кнопками покупки",
        "what": "Добавить блок с заголовком H2 «Сколько стоит»: две карточки «Только Ozon» и «Ozon и Wildberries», в каждой цена и ссылка на покупку в каталоге. Ниже сноска про внедрение и скидку.",
        "why": "Сейчас цена спрятана в абзаце, а кнопка одна и только на Ozon. Две карточки рядом показывают, что обе площадки выходят выгоднее, и сразу ведут в корзину.",
        "where": "Ставим сразу под блоком «Кому подходит» (задача O-6).",
        "code": f"""<section class="as w" id="price">
<div class="as-in">
<h2>Сколько стоит</h2>
<div class="as-grid as-g2">
<div class="as-card"><b>Только Ozon</b><div class="as-pr">40 700 ₽</div><p>в год с НДС</p><a class="as-link" href="{BUY_OZON}">Купить модуль 1С для Ozon →</a></div>
<div class="as-card a"><b>Ozon и Wildberries</b><div class="as-pr">69 990 ₽</div><p>в год с НДС, один модуль на обе площадки</p><a class="as-link" href="{BUY_BOTH}">Купить модуль на обе площадки →</a></div>
</div>
<p class="as-note">Стоимость внедрения уточняем на звонке: она зависит от доработок вашей 1С. После окончания годовой подписки модуль продолжает работать, подписка даёт обновления*. При заказе внедрения, техподдержки или лицензий 1С от 100 тыс. ₽ - скидка 50% на первый год.</p>
<p class="as-note">* Принимаем любые предложения по новым функциям модуля. Часть из них можем реализовать бесплатно, на своё усмотрение.</p>
</div>
</section>""",
    },
    {
        "id": "o8",
        "num": "O-8",
        "title": "Заявка внизу страницы: тёмная плашка с кнопкой",
        "what": "Добавить последний экран перед блоком «Наши клиенты»: тёмная плашка с призывом и кнопкой «Записаться на демонстрацию». Кнопка открывает ту же форму заявки, что и кнопки на странице модуля.",
        "why": "Кто дочитал до конца, должен сразу видеть, что делать дальше. Форма та же, заявки приходят туда же, куда и сейчас.",
        "where": "Ставим сразу под блоком «Сколько стоит» (задача O-7) и <strong>над</strong> заголовком «Наши клиенты».",
        "code": """<section class="as d">
<div class="as-in as-cta">
<div><div class="as-h2">Покажем, как это работает с вашим кабинетом Ozon</div><p class="as-lead">Созвонимся по видеосвязи, покажем модуль и ответим, подойдёт ли он к вашей 1С.</p></div>
<a class="as-btn m" href="#popup:konsultacia">Записаться на демонстрацию</a>
</div>
</section>""",
    },
]


def esc(s):
    return html.escape(s, quote=False)


def copybox(cid, text):
    return f'<div class="copybox"><pre id="{cid}">{esc(text)}</pre><button type="button" data-copy="{cid}">Копировать</button></div>'


T123_STEPS = """<ol class="steps">
<li>Навести мышь на нижний край блока, <strong>над которым</strong> ставим новый (см. «Где ставить»), → кнопка «+» (или «Добавить блок»).</li>
<li>Категория «Другое» → блок <strong>T123 «HTML-код»</strong> (в поиске библиотеки можно набрать <code>T123</code>).</li>
<li>В блоке → «Контент» → стереть пример и вставить код ниже целиком → «Сохранить и закрыть».</li>
<li>«Настройки» блока → «Отступ сверху» и «Отступ снизу» поставить 0 (у кода свои отступы) → «Сохранить и закрыть».</li>
</ol>"""


def task_html(b):
    return f"""
<section class="task" id="{b['id']}">
<h2><span class="num">{b['num']}</span> {b['title']}</h2>
<span class="lbl">Что сделать</span><p>{b['what']}</p>
<span class="lbl">Зачем</span><p>{b['why']}</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где ставить.</strong> {b['where']}</div>
{T123_STEPS}
<div class="pair-label">Код для T123</div>
{copybox(b['id'] + 'c', b['code'])}
</section>"""


BRIEF_CSS = """
:root{--bg:#f4f3ef;--card:#fff;--text:#1a1a1a;--muted:#5c5c5c;--border:#e2e2de;--ok:#1a7f4b;--ok-bg:#e8f6ee;--warn:#9a6700;--warn-bg:#fff6e0;--danger:#b42318;--danger-bg:#fdecea;--code:#0f172a}
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--text);background:var(--bg)}
.wrap{max-width:960px;margin:0 auto;padding:24px 18px 72px}
h1{font-size:26px;margin:0 0 6px;letter-spacing:-.02em}
h2{font-size:20px;margin:0 0 10px}
p{margin:0 0 8px}
a{color:#0b5cad}
.muted{color:var(--muted);font-size:14px}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 16px}
.pill{display:inline-block;padding:3px 10px;border-radius:999px;font-size:12px;font-weight:650;border:1px solid var(--border);background:#fff}
.pill.ok{color:var(--ok);background:var(--ok-bg);border-color:#c6e6d3}
.pill.warn{color:var(--warn);background:var(--warn-bg);border-color:#f0dfa0}
.callout{border-radius:10px;padding:12px 14px;margin:12px 0 18px;border:1px solid var(--border);background:var(--card);font-size:14px}
.callout.danger{background:var(--danger-bg);border-color:#f5c2c0}
.callout.warn{background:var(--warn-bg);border-color:#f0dfa0}
.callout.ok{background:var(--ok-bg);border-color:#c6e6d3}
.toc{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:12px 16px;margin:0 0 20px}
.toc ol{margin:6px 0 0;padding-left:22px}
.toc a{text-decoration:none}
.task{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px 18px;margin:0 0 18px}
.task .num{display:inline-block;background:#111;color:#fff;border-radius:999px;font-size:12px;font-weight:700;padding:2px 10px;margin-right:6px}
.lbl{display:block;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:14px 0 4px}
ol.steps{margin:4px 0 0;padding-left:22px}
ol.steps>li{margin:6px 0}
.where{background:#fafaf8;border:1px dashed var(--border);border-radius:8px;padding:10px 12px;margin:8px 0 10px;font-size:14px}
.copybox{position:relative;margin:6px 0 10px}
.copybox pre{margin:0;background:var(--code);color:#e5e7eb;border-radius:10px;padding:12px 12px 40px;overflow-x:auto;white-space:pre-wrap;word-break:break-word;font:12.5px/1.4 ui-monospace,Consolas,monospace;max-height:340px}
.copybox button{position:absolute;right:8px;bottom:8px;background:#fff;border:1px solid #ccc;border-radius:8px;padding:4px 10px;font-size:12px;font-weight:650;cursor:pointer}
.copybox button.ok{background:var(--ok-bg)}
.pair-label{font-size:12px;font-weight:700;color:var(--muted);margin:8px 0 2px}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin:6px 0 0;background:#fff}
th,td{border:1px solid var(--border);padding:7px 9px;text-align:left;vertical-align:top}
th{background:#fafaf8;font-weight:650}
code{font-size:13px}
.order{font-size:14px;margin:6px 0 0;padding-left:22px}
"""

COPY_JS = """<script>
document.querySelectorAll(".copybox button[data-copy]").forEach(function(btn){
  btn.addEventListener("click", async function(){
    var pre=document.getElementById(btn.getAttribute("data-copy"));
    if(!pre) return;
    await navigator.clipboard.writeText(pre.textContent);
    var t=btn.textContent; btn.textContent="Скопировано"; btn.classList.add("ok");
    setTimeout(function(){btn.textContent=t; btn.classList.remove("ok");},1200);
  });
});
</script>"""

OLD_BLOCKS = """<table>
<tr><th>Что на экране сейчас</th><th>Тип блока</th><th>Что сделать</th></tr>
<tr><td>Заголовок «Интеграция 1С с Ozon» и абзац «Модуль Аллсан выгружает остатки и цены из вашей 1С…» со ссылкой на «Модуль интеграции 1С с маркетплейсами»</td><td>заголовок + текст</td><td>Выключить. Заголовок H1 и ссылка теперь в новом первом экране (O-2).</td></tr>
<tr><td>Заголовок «Что синхронизируется с Ozon» и абзац «Остатки и цены из 1С в кабинет Ozon…»</td><td>текстовый блок</td><td>Выключить. Заменён карточками (O-3).</td></tr>
<tr><td>Заголовок «Кому подходит» и абзац «Селлерам и компаниям, у которых учёт уже в 1С…»</td><td>текстовый блок</td><td>Выключить. Заменён карточками (O-6).</td></tr>
<tr><td>Заголовок «Сколько стоит» и абзац «Подписка на модуль только для Ozon - от 40 700 ₽…»</td><td>текстовый блок</td><td>Выключить. Заменён карточками цены (O-7).</td></tr>
<tr><td>Кнопка «Купить модуль 1С для Ozon»</td><td>кнопка</td><td>Выключить. Ссылки на покупку теперь в карточках цены (O-7).</td></tr>
</table>"""


def build_brief():
    toc = "".join(f'<li><a href="#{b["id"]}">{b["num"]}. {b["title"]}</a></li>' for b in BLOCKS)
    tasks = "".join(task_html(b) for b in BLOCKS)
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Новый вид страницы «Интеграция 1С с Ozon» - 28.09.2026</title>
<style>{BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Новый вид страницы «Интеграция 1С с Ozon»</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-ozon">https://alsn.ru/1c-ozon</a> (в списке Тильды <code>1c-ozon</code>) · проверка живого сайта 28.09.2026 · только Тильда · каждый шаг после письменного «да» · «Опубликовать» один раз в самом конце (O-10)</p>
<div class="pills"><span class="pill ok">концепция согласована 28.09</span><span class="pill warn">10 шагов, картинки уже на сайте</span></div>

<div class="callout danger">HEAD сайта не трогать (там данные компании). В HEAD этой страницы уже есть служебный код (WebPage, хлебные крошки) - его <strong>не стирать</strong>, новый код ставить в конец. Telegram-бот не снимать. robots.txt, Bing, Twitter - не делаем. Меню, подвал, «Наши клиенты» и «Сертификаты» не трогаем.</div>

<div class="callout warn"><strong>Как устроено.</strong> Новые экраны - это блоки T123 «HTML-код» с готовым кодом. Оформление (цвета, шрифты, карточки) лежит один раз в HEAD страницы (O-1), поэтому в редакторе Тильды блоки T123 выглядят как код. Настоящий вид - в «Предпросмотре» и после публикации. Старые блоки не удаляем, а <strong>выключаем</strong> (O-9): их можно вернуть одной кнопкой.</div>

<div class="callout ok"><strong>Не трогать:</strong> title, описание страницы, картинку для пересылки, служебный код в HEAD, хлебные крошки (только цвет фона в O-9). H1 остаётся тем же: «Интеграция 1С с Ozon».</div>

<div class="toc"><strong>Порядок шагов</strong><ol>
<li><a href="#o0">O-0. Резервная копия страницы</a></li>
<li><a href="#o1">O-1. Оформление в HEAD страницы</a></li>
{toc}
<li><a href="#o9">O-9. Выключить старые блоки и выровнять фон крошек</a></li>
<li><a href="#o10">O-10. Предпросмотр и публикация</a></li>
</ol></div>

<section class="task" id="o0">
<h2><span class="num">O-0</span> Резервная копия страницы</h2>
<span class="lbl">Что сделать</span><p>Сделать копию страницы и не публиковать её.</p>
<span class="lbl">Зачем</span><p>Если что-то пойдёт не так, старый вариант останется под рукой целиком.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Список страниц проекта alsn.ru → строка «Интеграция 1С с Ozon» (<code>1c-ozon</code>) → «Ещё» (три точки) → «Дублировать» (или «Копировать страницу»).</li>
<li>Копию <strong>не публиковать</strong> и адрес ей не менять. Работаем дальше в оригинале <code>1c-ozon</code>.</li>
</ol>
</section>

<section class="task" id="o1">
<h2><span class="num">O-1</span> Оформление в HEAD страницы</h2>
<span class="lbl">Что сделать</span><p>Добавить один блок стилей в HEAD страницы Ozon. Он отвечает за вид всех новых экранов: фон #F7F8FA, оранжевые кнопки, карточки, мобильную версию.</p>
<span class="lbl">Зачем</span><p>Так оформление задаётся один раз, а не копируется в каждый блок. Потом тот же код пойдёт на страницу Wildberries, и обе страницы будут выглядеть одинаково.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Страница <code>1c-ozon</code> → «Настройки» (шестерёнка) → «Дополнительно» → «HTML-код для вставки внутрь HEAD».</li>
<li>В поле уже есть служебный код (начинается с <code>&lt;script type="application/ld+json"&gt;</code>). Ничего не стирать. Поставить курсор <strong>в самый конец</strong>, после последнего <code>&lt;/script&gt;</code>, нажать Enter.</li>
<li>Вставить код ниже целиком → «Сохранить изменения».</li>
</ol>
<div class="pair-label">Код в конец HEAD страницы</div>
{copybox('o1c', CSS)}
</section>
{tasks}

<section class="task" id="o9">
<h2><span class="num">O-9</span> Выключить старые блоки и выровнять фон крошек</h2>
<span class="lbl">Что сделать</span><p>Выключить пять старых блоков, которые заменили новые экраны. Фон хлебных крошек сделать таким же светлым, как у нового первого экрана.</p>
<span class="lbl">Зачем</span><p>Иначе на странице будет два заголовка H1 и двойной текст. Выключенный блок не виден гостям и поисковикам, но остаётся в редакторе, его можно включить обратно.</p>
<span class="lbl">Как в Тильде</span>
<div class="where"><strong>Где искать.</strong> Страница «Интеграция 1С с Ozon» (https://alsn.ru/1c-ozon). После шагов O-2…O-8 старые блоки окажутся ниже новой заявки (тёмная плашка «Покажем, как это работает…») и выше заголовка «Наши клиенты». Узнать их можно по первым словам:</div>
{OLD_BLOCKS}
<ol class="steps">
<li>На каждом из пяти блоков: навести мышь → слева меню блока «Ещё» / три точки → «Выключить блок» (в некоторых версиях «Скрыть блок» или значок глаза). Блок станет полупрозрачным.</li>
<li>Если пункта «Выключить» нет - не удалять, написать мне, подберём другой способ.</li>
<li>Хлебные крошки (первый блок под меню, T123) → «Настройки» → «Цвет фона» → <code>#F7F8FA</code> → «Сохранить и закрыть». Код крошек не трогать.</li>
</ol>
<div class="pair-label">Цвет фона крошек</div>
{copybox('o9c', '#F7F8FA')}
<p class="muted">Итоговый порядок сверху вниз: меню → крошки → первый экран (O-2) → «Что синхронизируется» (O-3) → «Что особенно важно на Ozon» (O-4) → «Результат клиента» (O-5) → «Кому подходит» (O-6) → «Сколько стоит» (O-7) → тёмная плашка с заявкой (O-8) → выключенные старые блоки → «Наши клиенты» → «Сертификаты» → подвал.</p>
</section>

<section class="task" id="o10">
<h2><span class="num">O-10</span> Предпросмотр и публикация</h2>
<span class="lbl">Что сделать</span><p>Посмотреть страницу в предпросмотре на компьютере и телефоне, потом опубликовать.</p>
<span class="lbl">Зачем</span><p>Публикация одна, после того как всё собрано: гости не увидят страницу наполовину.</p>
<span class="lbl">Как в Тильде</span>
<ol class="steps">
<li>Кнопка «Предпросмотр» сверху. Нажать «Записаться на демонстрацию» - должна открыться форма заявки. Нажать «Купить модуль» - должна открыться карточка модуля для Ozon.</li>
<li>В предпросмотре переключить вид на телефон: карточки встают в одну колонку, кнопки на всю ширину.</li>
<li>«Опубликовать».</li>
</ol>
</section>

<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-ozon-design-2026-09-28.html</code> · код собирает <code>seo-data/scripts/build_mp_ozon_blocks.py</code> · превью: <code>seo-data/competitors/screens/preview-1c-ozon.html</code></p>
</div>
{COPY_JS}
</body>
</html>"""
    open(BRIEF, "w", encoding="utf-8").write(doc)


def build_preview():
    head = """<div style="background:#000;color:#fff;font:14px Roboto,Arial,sans-serif;padding:18px 24px;display:flex;justify-content:space-between"><b style="color:#F55823">АЛЛСАН</b><span>Разработка · Техподдержка · Продукты 1С · Кейсы · О нас</span><span>+7 (495) 260-04-03</span></div>
<div style="background:#F7F8FA;color:#8a8a8a;font:14px Roboto,Arial,sans-serif;padding:14px 20px"><div style="max-width:1160px;margin:0 auto">⌂ / Модуль 1С для маркетплейсов / Интеграция 1С с Ozon</div></div>"""
    tail = """<div style="background:#fff;padding:40px 20px;text-align:center;font:700 28px Roboto,Arial,sans-serif;color:#212121">Наши клиенты</div>"""
    body = "\n".join(b["code"] for b in BLOCKS)
    doc = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<title>Превью 1c-ozon</title>{CSS}<style>body{{margin:0}}</style></head><body>{head}{body}{tail}</body></html>"""
    open(PREVIEW, "w", encoding="utf-8").write(doc)


if __name__ == "__main__":
    build_brief()
    build_preview()
    print("ok", BRIEF, PREVIEW)
