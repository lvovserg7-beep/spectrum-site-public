"""Макет страницы «Модуль 1С для маркетплейсов» (casemarketplace) на стилях эталона 1c-ozon (v3).

Стили берутся из preview-1c-ozon-v3.html как есть, меняется только тело.
Витрина Тильды (rec913805053) остаётся на сайте отдельным блоком, в макете на её месте серая заглушка.
Выход: seo-data/competitors/screens/preview-casemarketplace-v3.html
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "competitors", "screens", "preview-1c-ozon-v3.html")
OUT = os.path.join(ROOT, "competitors", "screens", "preview-casemarketplace-v3.html")

SHOP = "#rec913805053"
IMG_PHOTO = "https://optim.tildacdn.com/tild3632-3333-4139-b730-663861323430/-/format/webp/allsun-hero-mp-emplo.jpg.webp"
IMG_UNIT = "https://static.tildacdn.com/tild6161-6139-4730-b039-636631623135/___OZON_WB.jpg"
IMG_CLUSTER = "https://static.tildacdn.com/tild3563-6433-4535-a231-653461616463/noroot.png"
IMG_DRR = "https://static.tildacdn.com/tild6233-3339-4062-b232-666133343034/noroot.png"
IMG_REVIEWS = "https://static.tildacdn.com/tild3131-6336-4633-b430-376264643262/__.jpg"
IMG_FORECAST = "https://static.tildacdn.com/tild3133-6532-4734-b437-653163333835/noroot.png"
IMG_LETTER = "https://static.tildacdn.com/tild3461-3830-4564-a330-396237393635/----.jpg"
IMG_ECO = "https://optim.tildacdn.com/tild3363-3664-4966-b837-393439303735/-/resize/800x/-/format/webp/case-ecotide-video-c.jpg.webp"
IMG_V_MARGIN = "https://static.tildacdn.com/tild6532-3031-4031-b665-336436353033/______Ozon____1___-0.png"
IMG_V_BARCODE = "https://static.tildacdn.com/tild3536-6565-4562-b435-383364353737/______Wildberries__1.jpg"
IMG_V_REVIEWS = "https://static.tildacdn.com/tild3530-3961-4365-b936-323035313561/__-____Wildberries__.jpg"
VID_ECO = "https://vkvideo.ru/video-181185386_456239037"
VID_MARGIN = "https://vkvideo.ru/video-181185386_456239063"
VID_BARCODE = "https://vkvideo.ru/video-181185386_456239062"
VID_REVIEWS = "https://vkvideo.ru/video-181185386_456239072"
PLAY = '<span class="play"><svg viewBox="0 0 24 24" width="30" height="30"><path d="M8 5v14l11-7z" fill="#fff"/></svg></span>'

Y = '<span class="y">✓</span>'
S = '<span class="s">скоро</span>'
N = '<span class="n">нет</span>'

MAIN_ROWS = [
    ("g", "Отчёты и помощники"),
    ("Ежедневный отчёт по марже: реальная прибыль за каждый день", Y, Y),
    ("Расчёт потребностей по кластерам: куда и сколько отгрузить", Y, S),
    ("Прогноз закупок: когда пополнять свой склад", Y, Y),
    ("Ежедневный расчёт доли рекламных расходов", Y, S),
    ("Автоответы на отзывы с помощью ИИ", Y, Y),
    ("SEO-описания товаров с помощью ИИ", Y, Y),
    ("Расчёт прибыли по менеджерам", Y, S),
    ("Штрихкоды с крупным названием товара", Y, Y),
    ('Перевыставление услуг последней мили Ozon с НДС (<a href="https://alsn.ru/perevystavlenie-uslug-posledney-mili-ozon-v-1s">подробнее</a>)', Y, N),
    ("Реестр продаж юрлицам", Y, S),
    ("g", "Обмен с кабинетом"),
    ("Любое число кабинетов на площадке", Y, Y),
    ("Остатки из 1С в кабинет, автоматически и вручную", Y, Y),
    ("Цены из 1С в кабинет, автоматически и вручную", Y, Y),
    ("Заказы в 1С без ручного ввода", Y, Y),
    ("Схемы продаж", "FBO, FBS, rFBS, DBS", "FBO, FBS, DBS"),
]
MORE_ROWS = [
    ("g", "Товары"),
    ("Добавление и редактирование товара", Y, Y),
    ("Исключение товара из продажи", Y, Y),
    ("Сопоставление уже созданных в кабинете товаров с 1С", Y, Y),
    ("Список товаров с отбором по разным признакам", Y, Y),
    ("Перенос товара в архив", Y, Y),
    ("g", "Остатки"),
    ("Ограничение выгружаемых остатков", Y, Y),
    ("Учёт товаров в резерве", Y, Y),
    ("Учёт плановых поставок в остатках", Y, Y),
    ("Распределение остатков между складами", Y, Y),
    ("g", "Заказы, отправления, возвраты"),
    ("Подготовка отправлений: этикетки, акты, накладные", Y, Y),
    ("Статусы и подробности заказов FBO", Y, Y),
    ("Возвраты: информация и документ возврата в 1С", Y, Y),
    ("Передача маркировки «Честный знак»", Y, S),
    ("Обработка спорных заказов", Y, N),
    ("Разбивка заказа на отправления", Y, N),
    ("g", "Акции и финансы"),
    ("Товары, цены и количество для участия в акциях", Y, N),
    ("Запросы покупателей на скидку: согласование и шаблоны ответов", Y, N),
    ("Загрузка отчёта комиссионера", Y, Y),
]


def table(rows):
    tr = []
    for r in rows:
        if r[0] == "g":
            tr.append(f'<tr class="g"><td colspan="3">{r[1]}</td></tr>')
        else:
            tr.append(f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>")
    return ('<div class="cmpw"><table class="cmp"><thead><tr><th>Функция</th><th>Ozon</th><th>WB</th></tr></thead><tbody>'
            + "".join(tr) + "</tbody></table></div>")


FAQ = [
    ("С какими конфигурациями 1С работает модуль?",
     "С 1С:Управление торговлей, 1С:Управление нашей фирмой (1.6 и 3.0), 1С:Комплексная автоматизация и 1С:ERP. Подключение идёт через официальный API Ozon и Wildberries."),
    ("Сколько стоит модуль?",
     "40 700 ₽ в год за одну площадку, Ozon или Wildberries, и 69 990 ₽ в год за обе. Цены с НДС 5%. Стоимость внедрения назовём после звонка: она зависит от доработок вашей 1С."),
    ("Какие схемы продаж поддерживает модуль?",
     "Для Ozon: FBO, FBS, rFBS и DBS. Для Wildberries: FBO, FBS и DBS. Заказы приходят в 1С сами, этикетки и документы на отправления печатаются из 1С."),
    ("Что будет, когда закончится подписка?",
     "Модуль продолжит работать. Подписка нужна для обновлений под изменения API площадок и новых функций. Продление стоит столько же, сколько покупка."),
    ("Чем модуль отличается от типового обмена 1С с маркетплейсом?",
     "Кроме обмена остатками и заказами в модуле есть ежедневная маржа по товарам, расчёт по кластерам, прогноз закупок, доля рекламных расходов, ответы на отзывы и SEO-описания с помощью ИИ."),
    ("Какая техподдержка входит в модуль?",
     "Стандартная поддержка входит в подписку: обновления под изменения API, заявки по почте персональному менеджеру, ответ в течение суток. Есть экспресс-поддержка на 1, 3, 6 или 12 месяцев: заявки в Telegram, реакция в течение часа, специалист сам подключается к вашей базе."),
    ("Можно заказать новую функцию?",
     "Да. Принимаем любые предложения по новым функциям модуля. Часть из них можем реализовать бесплатно, на своё усмотрение."),
    ("У нас ещё нет 1С. Что делать?",
     "Возьмите тариф «под ключ»: программа 1С, лицензии, техподдержка и модуль в одном заказе. В тарифе СТАРТ модуль Ozon и Wildberries со скидкой 50%, в тарифе ПРОФИ он в подарок."),
]

TEAM = [
    ("tild3433-6363-4436-b733-666266646164/Group_103.png", "Сергей Львов", "основатель, управляющий партнёр, аналитик 1С"),
    ("tild6535-3462-4235-a238-626561623233/Group_104.png", "Павел Агеев", "программист 1С, руководитель проектов, техподдержка"),
    ("tild3735-6532-4732-a263-613661383062/Group_105.png", "Никита Соколов", "программист 1С"),
    ("tild3362-3838-4938-a161-623235383761/Group_100.png", "Энрико Айвазян", "программист 1С, руководитель проектов"),
    ("tild3138-6561-4865-b439-383366386535/Group_101.png", "Ирина Щеглова", "руководитель проектов, аналитик"),
    ("tild3537-6632-4736-b639-616236646639/Group_102.png", "Евгений Анастасьев", "руководитель проектов, программист 1С"),
    ("tild6131-3734-4132-a164-373364303931/Group_99.png", "Роман Заболотный", "руководитель проектов"),
]
team_html = "\n".join(
    f'     <div class="pp"><img src="https://static.tildacdn.com/{p}" alt="{n}, {r}, Аллсан Интеграция" loading="lazy"><div><b>{n}</b>{r}</div></div>'
    for p, n, r in TEAM
)

faq_html = "\n".join(
    f'    <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
    for i, (q, a) in enumerate(FAQ)
)

BODY = f"""
<div class="head"><div class="in"><b style="color:#F55823">АЛЛСАН</b><span>Разработка · Техподдержка · Продукты 1С · Кейсы · О нас</span><span>+7 (495) 260-04-03</span></div></div>
<div class="in crumb">⌂ / Модуль 1С для маркетплейсов</div>

<!-- HERO -->
<section class="hero">
 <div class="in">
  <div style="padding-bottom:44px">
   <div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>Модуль Аллсан для селлеров</div>
   <h1>Модуль 1С <br>для <span>маркетплейсов</span></h1>
   <p class="lead">Остатки и цены уходят из вашей 1С на обе площадки, заказы приходят обратно. Утром в 1С уже посчитана маржа за вчера по каждому товару на Ozon и Wildberries.</p>
   <div class="btns">
    <a class="btn m" href="#popup:konsultacia">Показать на моём кабинете <span class="ar">→</span></a>
    <a class="btn g" href="#price">Цена от 40 700 ₽</a>
   </div>
  </div>
  <div class="photo">
   <img src="{IMG_PHOTO}" alt="Сергей Никешин, ведущий разработчик модуля интеграции 1С с Ozon и Wildberries, Аллсан Интеграция">
   <div class="tag"><b>Сергей Никешин</b><span>ведущий разработчик модуля, Аллсан Интеграция</span></div>
  </div>
 </div>
</section>

<!-- DAY TIMELINE -->
<div class="day">
 <div class="in"><div class="box">
  <div class="lbl">Как выглядит день с модулем</div>
  <div class="track">
   <div class="it"><span class="t mono">по расписанию</span><b>Остатки на вашем складе</b>и цены уходят из 1С на Ozon и Wildberries сами</div>
   <div class="it"><span class="t mono">сразу</span><b>Новый заказ</b>появляется в 1С без ручного ввода</div>
   <div class="it"><span class="t mono">утром</span><b>Маржа за вчера</b>по каждому товару на обеих площадках<a class="more" href="#reports" data-tab="0">Отчёт по марже →</a></div>
   <div class="it"><span class="t mono">каждый день</span><b>Ответы на отзывы</b>ИИ готовит ответы, вы проверяете и отправляете<a class="more" href="#reports" data-tab="3">Автоответы →</a></div>
   <div class="it"><span class="t mono">перед поставкой</span><b>Потребность по кластерам</b>сколько товара везти на каждый склад Ozon<a class="more" href="#reports" data-tab="1">Расчёт по кластерам →</a></div>
  </div>
 </div></div>
</div>

<!-- BODY -->
<section class="body">
 <div class="in">

  <!-- passport -->
  <aside class="pass">
   <div class="ttl">Паспорт модуля</div>
   <div class="price">40 700 ₽</div>
   <div class="per">в год за одну площадку</div>
   <dl>
    <dt>Площадки</dt><dd>Ozon, Wildberries</dd>
    <dt>Схемы Ozon</dt><dd>FBO, FBS, rFBS, DBS</dd>
    <dt>Схемы WB</dt><dd>FBO, FBS, DBS</dd>
    <dt>Конфигурации</dt><dd>УТ, УНФ, КА, ERP</dd>
    <dt>Кабинеты</dt><dd>любое число</dd>
    <dt>Код</dt><dd>открытый</dd>
    <dt>После подписки</dt><dd>продолжает работать</dd>
   </dl>
   <a class="btn m" href="#popup:konsultacia">Записаться на демонстрацию</a>
   <a class="btn g" href="#price">Купить модуль</a>
   <div class="small">Ozon и Wildberries вместе - 69 990 ₽ в год.</div>
   <div class="trust"><span>с 2015 года</span><span>ТОП 10 ЦРА</span><span>1С:Франчайзи</span></div>
  </aside>

  <div>
   <!-- 01 questions -->
   <div class="sec">
    <div class="num"><span class="n">01</span><span class="ln"></span></div>
    <h2>На какие вопросы отвечает модуль</h2>
    <p class="sub">Вопросы, которые селлер задаёт каждую неделю. Ответы собираются в 1С без выгрузок в Excel.</p>
    <div class="qpanel">
     <div class="q big">
      <b>Сколько я заработал вчера на каждом товаре?</b>
      Модуль сводит отчёты Ozon и Wildberries с себестоимостью из 1С в один расчёт.
      <div class="mini">
       <div><span>Выручка</span><span>из отчёта площадки</span></div>
       <div><span>Логистика и комиссия</span><span>из площадки</span></div>
       <div><span>Реклама и штрафы</span><span>по товару</span></div>
       <div><span>Себестоимость</span><span>из 1С</span></div>
       <div><span>Маржа</span><span>за вчера</span></div>
      </div>
      <a class="go" href="#reports" data-tab="0">Отчёт по марже →</a>
     </div>
     <div class="q"><b>Куда и сколько везти на склады?</b>Модуль считает продажи и остатки по кластерам и подсказывает объём поставки в каждый регион.<a class="go" href="#reports" data-tab="1">Расчёт по кластерам →</a></div>
     <div class="q"><b>Кто ответит на сотню отзывов?</b>ИИ читает отзыв и пишет ответ. Менеджер проверяет тексты и отправляет их одной кнопкой.<a class="go" href="#reports" data-tab="3">Автоответы →</a></div>
    </div>
   </div>

   <!-- 02 route -->
   <div class="sec">
    <div class="num"><span class="n">02</span><span class="ln"></span></div>
    <h2>Как идут данные</h2>
    <p class="sub">Модуль стоит внутри вашей 1С и работает с площадками через официальный API. Руками ничего переносить не нужно.</p>
    <div class="route">
     <div class="node"><div class="k">Ваша 1С</div><b>Учёт</b><ul><li>номенклатура и цены</li><li>остатки складов</li><li>себестоимость</li></ul></div>
     <div class="pipe"><div>остатки и цены</div><div class="back">заказы</div></div>
     <div class="node mid"><div class="k">Модуль Аллсан</div><b>Обмен и расчёты</b><ul><li>заказы в 1С</li><li>отправления и этикетки</li><li>маржа, кластеры, отзывы</li></ul></div>
     <div class="pipe"><div>выгрузка</div><div class="back">отчёты</div></div>
     <div class="node"><div class="k">Кабинеты площадок</div><b>Ozon и Wildberries</b><ul><li>карточки и остатки</li><li>заказы по всем схемам</li><li>финансовые отчёты</li></ul></div>
    </div>
   </div>

   <!-- 03 tabs + table -->
   <div class="sec" id="reports">
    <div class="num"><span class="n">03</span><span class="ln"></span></div>
    <h2>Что умеет модуль</h2>
    <p class="sub">Настоящие экраны модуля в 1С и полный список функций для каждой площадки.</p>
    <div class="tabs">
     <button class="on" data-t="0">Маржа по товарам</button>
     <button data-t="1">Кластеры Ozon</button>
     <button data-t="2">Реклама Ozon</button>
     <button data-t="3">Отзывы с ИИ</button>
     <button data-t="4">Прогноз закупок</button>
    </div>
    <div class="pane on">
     <a class="shot" href="{IMG_UNIT}" data-zoom><img class="full" src="{IMG_UNIT}" alt="Отчёты по марже Ozon и Wildberries в 1С"></a>
     <div class="txt"><b>Сколько вы заработали на каждом товаре</b><p>Себестоимость, логистика, комиссия, хранение, штрафы и налог в одном отчёте. Прибыль видна по категориям и по каждому товару, отдельно для Ozon и Wildberries.</p><div class="res">Видно, какие товары работают в минус</div></div>
    </div>
    <div class="pane">
     <a class="shot" href="{IMG_CLUSTER}" data-zoom><img src="{IMG_CLUSTER}" alt="Расчёт потребностей по кластерам Ozon в 1С" loading="lazy"></a>
     <div class="txt"><b>Сколько и на какой склад отгрузить</b><p>Модуль берёт остатки FBO, продажи и сроки доставки по кластерам и считает, сколько товара везти в каждый регион.</p><div class="res">Для Ozon, для Wildberries готовим</div></div>
    </div>
    <div class="pane">
     <a class="shot" href="{IMG_DRR}" data-zoom><img src="{IMG_DRR}" alt="Расчёт доли рекламных расходов Ozon в 1С" loading="lazy"></a>
     <div class="txt"><b>Какая реклама съедает маржу</b><p>Каждый день модуль считает долю рекламных расходов по товарам, поиск и трафарет отдельно.</p><div class="res">Для Ozon, для Wildberries готовим</div></div>
    </div>
    <div class="pane">
     <a class="shot" href="{IMG_REVIEWS}" data-zoom><img src="{IMG_REVIEWS}" alt="Работа с отзывами в 1С: ответы, подготовленные ИИ" loading="lazy"></a>
     <div class="txt"><b>Ответы на отзывы готовит ИИ</b><p>Модуль загружает отзывы, ИИ пишет ответ с учётом оценки и текста и может посоветовать другой ваш товар. Менеджер проверяет и отправляет ответы одной кнопкой.</p><div class="res">Нужен YandexGPT, для Ozon ещё подписка Premium Plus</div></div>
    </div>
    <div class="pane">
     <a class="shot" href="{IMG_FORECAST}" data-zoom><img src="{IMG_FORECAST}" alt="Прогноз закупок в 1С для поставок на Ozon и Wildberries" loading="lazy"></a>
     <div class="txt"><b>Сколько заказать у поставщика</b><p>Задайте суточный расход и срок планирования. Модуль учтёт остаток и то, что уже заказано, и покажет, сколько нужно докупить.</p><div class="res">Товар и упаковка не заканчиваются перед поставкой</div></div>
    </div>

    <div class="extra-h">Функции по площадкам</div>
    {table(MAIN_ROWS)}
    <details class="cmpmore"><summary>Показать все функции обмена</summary>
    {table(MORE_ROWS)}
    </details>
    <p class="cmpnote">«Скоро» - функция в разработке для этой площадки.</p>

    <div class="extra-h">Отдельно про каждую площадку</div>
    <div class="extra">
     <div class="ex"><b>Интеграция 1С с Ozon</b><p>Схемы FBO, FBS, rFBS и DBS, кластеры, доля рекламы, перевыставление услуг последней мили.</p><a class="btn g" style="margin-top:14px" href="https://alsn.ru/1c-ozon">Смотреть решение</a></div>
     <div class="ex"><b>Интеграция 1С с Wildberries</b><p>Схемы FBO, FBS и DBS, маржа с логистикой и хранением, ответы на отзывы, штрихкоды поставок.</p><a class="btn g" style="margin-top:14px" href="https://alsn.ru/1c-wildberries">Смотреть решение</a></div>
    </div>
   </div>

   <!-- 04 case -->
   <div class="sec">
    <div class="num"><span class="n">04</span><span class="ln"></span></div>
    <h2>Отзывы клиентов</h2>
    <p class="sub">Видеоотзыв и благодарственное письмо от селлеров, которые работают с модулем.</p>
    <div class="case">
     <div class="l">
      <div class="big">20<span> млн ₽</span></div>
      <div class="cap">выручка магазина EcoTide на Ozon за полгода с нуля</div>
      <blockquote>«Мы начали наш бизнес на OZON совершенно с 0 и всего за полгода сделали выручку в&nbsp;20&nbsp;000&nbsp;000&nbsp;рублей»</blockquote>
      <div class="who"><b>Елизавета</b>руководитель магазина EcoTide</div>
     </div>
     <div class="r">
      <a class="video" href="{VID_ECO}" target="_blank" rel="noopener" aria-label="Смотреть видеоотзыв EcoTide в новом окне">
       <img src="{IMG_ECO}" alt="Видеоотзыв Елизаветы, руководителя магазина EcoTide" loading="lazy">
       {PLAY}
       <span class="vcap">Смотреть видеоотзыв</span>
      </a>
      <div class="vnote">Елизавета о запуске на Ozon и учёте в 1С</div>
     </div>
    </div>

    <div class="letter">
     <a class="scan" href="{IMG_LETTER}" data-zoom aria-label="Открыть благодарственное письмо СТГ ГВАРД">
      <img src="{IMG_LETTER}" alt="Благодарственное письмо ООО «СТГ ГВАРД» компании Аллсан Интеграция" loading="lazy">
      <span class="zoom">Открыть письмо</span>
     </a>
     <div class="ltxt">
      <div class="lk">Благодарственное письмо · исх. № 547 от 02.07.2025</div>
      <blockquote>«Благодаря модулю от «Аллсан Интеграции» в нашей 1С появилась функция удобного автоматического расчета прибыли продаж по каждому менеджеру, работающему с маркетплейсом. Расчет производится буквально в&nbsp;2&nbsp;клика. <mark>Мы фиксируем ежемесячный рост продаж</mark> от применения этих новых инструментов.»</blockquote>
      <div class="tags"><span>1С:Управление торговлей</span><span>Ozon</span><span>прибыль по менеджерам</span><span>кластеры</span></div>
      <div class="who"><b>Матюхин П.А.</b>генеральный директор ООО «СТГ ГВАРД»</div>
     </div>
    </div>

    <div class="extra-h">Видеоинструкции</div>
    <div class="vids c3">
     <div class="ex">
      <a class="video" href="{VID_MARGIN}" target="_blank" rel="noopener" aria-label="Смотреть видео об ежедневном отчёте по марже Ozon в новом окне">
       <img src="{IMG_V_MARGIN}" alt="Видео: ежедневный отчёт по марже Ozon в 1С" loading="lazy">{PLAY}<span class="vcap">Смотреть видео</span>
      </a>
      <b>Маржа Ozon каждый день</b>
      <p>Как получать отчёт по марже ежедневно, а не раз в месяц.</p>
     </div>
     <div class="ex">
      <a class="video" href="{VID_REVIEWS}" target="_blank" rel="noopener" aria-label="Смотреть видео об автоответах на отзывы Wildberries в новом окне">
       <img src="{IMG_V_REVIEWS}" alt="Видео: автоответы на отзывы Wildberries из 1С" loading="lazy">{PLAY}<span class="vcap">Смотреть видео</span>
      </a>
      <b>Автоответы на отзывы</b>
      <p>Как ИИ готовит ответы и как отправить их одной кнопкой.</p>
     </div>
     <div class="ex">
      <a class="video" href="{VID_BARCODE}" target="_blank" rel="noopener" aria-label="Смотреть видео о печати штрихкодов Wildberries в новом окне">
       <img src="{IMG_V_BARCODE}" alt="Видео: печать штрихкодов для поставок на Wildberries через 1С" loading="lazy">{PLAY}<span class="vcap">Смотреть видео</span>
      </a>
      <b>Штрихкоды для поставок</b>
      <p>Как напечатать штрихкоды для маркировки поставки прямо из 1С.</p>
     </div>
    </div>
   </div>

   <!-- 05 fit -->
   <div class="sec">
    <div class="num"><span class="n">05</span><span class="ln"></span></div>
    <h2>Кому подходит</h2>
    <div class="fit">
     <div><b>Учёт уже в 1С</b><p>УТ, УНФ, КА или ERP. Модуль встраивается в вашу базу, переходить на другую программу не нужно.</p></div>
     <div><b>Продаёте на двух площадках</b><p>Остатки, заказы и отчёты Ozon и Wildberries вручную сводить уже тяжело, появляются ошибки и штрафы.</p></div>
     <div><b>Нужна реальная прибыль</b><p>Хочется видеть маржу по каждому товару на каждой площадке, а не только выручку в кабинетах.</p></div>
    </div>
    <p class="cmpnote">Нужен обмен с поставщиками телеком и IT-оборудования, а не с маркетплейсами? Это другой продукт: <a href="https://alsn.ru/ecom" style="color:var(--acc)">интеграция 1С с B2B-поставщиками</a>.</p>
   </div>

   <!-- 06 team -->
   <div class="sec">
    <div class="num"><span class="n">06</span><span class="ln"></span></div>
    <h2>Кто внедряет модуль</h2>
    <p class="sub">Аналитики, программисты 1С и руководители проектов Аллсан. Эти же люди отвечают на заявки в техподдержку.</p>
    <div class="team">
{team_html}
    </div>
   </div>

   <!-- 07 price -->
   <div class="sec" id="price">
    <div class="num"><span class="n">07</span><span class="ln"></span></div>
    <h2>Сколько стоит</h2>
    <p class="sub">Цены с НДС 5% за год. Стоимость внедрения уточняем на звонке: она зависит от доработок вашей 1С.</p>
    <div class="prices three">
     <div class="pc"><div class="nm">Только Ozon</div><div class="p">40 700 ₽</div><div class="s">в год</div>
      <ul><li>Схемы FBO, FBS, rFBS, DBS</li><li>Маржа, кластеры, реклама</li><li>Техподдержка и обновления</li></ul>
      <a class="btn g" href="{SHOP}">Купить для Ozon</a></div>
     <div class="pc"><div class="nm">Только Wildberries</div><div class="p">40 700 ₽</div><div class="s">в год</div>
      <ul><li>Схемы FBO, FBS, DBS</li><li>Маржа, отзывы, прогноз закупок</li><li>Техподдержка и обновления</li></ul>
      <a class="btn g" href="{SHOP}">Купить для WB</a></div>
     <div class="pc a"><span class="badge">Выгоднее на 11 410 ₽</span><div class="nm">Ozon и Wildberries</div><div class="p">69 990 ₽</div><div class="s">в год, один модуль на обе площадки</div>
      <ul><li>Всё из двух тарифов</li><li>Маржа по обеим площадкам</li><li>Любое число кабинетов</li></ul>
      <a class="btn m" href="{SHOP}">Купить на обе площадки</a></div>
    </div>
    <p class="note">После окончания годовой подписки модуль продолжает работать. Подписка даёт обновления*, продление стоит столько же, сколько покупка. При заказе внедрения, техподдержки или лицензий 1С от 100 тыс. ₽ скидка 50% на первый год на один модуль, от 200 тыс. ₽ на каждый модуль.<br>* Принимаем любые предложения по новым функциям модуля. Часть из них можем реализовать бесплатно, на своё усмотрение.</p>

    <div class="extra-h">Техподдержка модуля</div>
    <div class="extra">
     <div class="ex"><b>Стандартная</b><p>Обновления под новые функции и изменения API площадок. Заявки по почте персональному менеджеру, ответ в течение суток.</p><span class="need">Входит в подписку</span></div>
     <div class="ex"><b>Экспресс</b><p>Заявки в Telegram, реакция в течение часа. Специалист сам подключается к вашей базе и при необходимости связывается с поддержкой площадки или хостинга.</p><span class="need">На 1, 3, 6 или 12 месяцев</span><br><a class="btn g" style="margin-top:14px" href="#popup:konsultacia">Узнать цену</a></div>
    </div>

    <div class="extra-h">Ещё нет 1С? Тарифы «под ключ»</div>
    <div class="extra">
     <div class="ex"><b>СТАРТ</b><p>Для ИП, малого и среднего бизнеса: 1С:УНФ или 1С:УТ ПРОФ, 1С:КП ПРОФ на 12 месяцев по схеме 8+4, сервер МИНИ на 5 подключений, 5 клиентских лицензий, 15 часов техподдержки.</p><span class="need">Модуль Ozon и WB со скидкой 50%</span><br><a class="btn g" style="margin-top:14px" href="#popup:konsultacia">Узнать цену</a></div>
     <div class="ex"><b>ПРОФИ</b><p>Для тех, кто дорос до 1С:Комплексная автоматизация: КА 8, 1С:КП ПРОФ на 12 месяцев по схеме 8+4, серверная лицензия ПРОФ, 10 клиентских лицензий, 100 часов техподдержки.</p><span class="need">Модуль Ozon и WB в подарок</span><br><a class="btn g" style="margin-top:14px" href="#popup:konsultacia">Узнать цену</a></div>
    </div>
   </div>

   <!-- 08 faq -->
   <div class="sec faq" style="margin-bottom:40px">
    <div class="num"><span class="n">08</span><span class="ln"></span></div>
    <h2>Частые вопросы</h2>
{faq_html}
   </div>
  </div>
 </div>
</section>

<!-- SHOWCASE -->
<div class="in" style="margin:0 auto 60px"><div style="border:2px dashed #D7DADD;border-radius:22px;padding:40px;text-align:center;color:#6b7075;font-size:15px">Здесь остаётся витрина Тильды «Цены на модули интеграции 1С с маркетплейсами» с тремя карточками и корзиной (блок rec913805053).<br>Кнопки «Купить» в разделе 07 прокручивают сюда.</div></div>
<!-- /SHOWCASE -->

<section class="final">
 <div class="in">
  <div><h2>Покажем модуль на вашем кабинете</h2><p>Созвонимся, посмотрим вашу 1С и скажем, что даст модуль на Ozon и Wildberries.</p><div class="ph">+7 (495) 260-04-03</div></div>
  <a class="btn m" href="#popup:konsultacia">Записаться на демонстрацию <span class="ar">→</span></a>
 </div>
</section>
"""

EXTRA_CSS = """
.pane a.shot{display:block;cursor:zoom-in}
.tabs+.pane .shot img.full{aspect-ratio:auto;object-fit:contain}
"""


def main():
    src = io.open(SRC, encoding="utf-8").read()
    head = src[: src.index("</style>")] + EXTRA_CSS + "</style>\n</head>\n<body>\n"
    head = re.sub(r"<title>.*?</title>", "<title>Модуль 1С для маркетплейсов - макет v3</title>", head)
    script = src[src.index("<script>"): src.index("</script>") + len("</script>")]
    html = head + BODY + "\n" + script + "\n</body>\n</html>\n"
    assert "\u2014" not in html and "\u2013" not in html
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("ok", OUT)


if __name__ == "__main__":
    main()
