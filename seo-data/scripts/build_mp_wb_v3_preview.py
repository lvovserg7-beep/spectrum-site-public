"""Макет страницы «Интеграция 1С с Wildberries» на стилях эталона 1c-ozon (v3).

Стили берутся из preview-1c-ozon-v3.html как есть, меняется только тело.
Выход: seo-data/competitors/screens/preview-1c-wildberries-v3.html
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "competitors", "screens", "preview-1c-ozon-v3.html")
OUT = os.path.join(ROOT, "competitors", "screens", "preview-1c-wildberries-v3.html")

BUY_WB = "https://alsn.ru/casemarketplace/tproduct/913805053-553126495292-modul-integratsii-1s-s-wildberries"
BUY_BOTH = "https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz"
VID_BARCODE = "https://vkvideo.ru/video-181185386_456239062"
VID_REVIEWS = "https://vkvideo.ru/video-181185386_456239072"

IMG = "../../brand-images/"
SCR = IMG + "wb-screens/"

EXTRA_CSS = """
.pane a.shot{display:block;cursor:zoom-in}
.pane .shot img.wbm{aspect-ratio:1121/485;object-fit:cover}
"""

BODY = f"""
<div class="head"><div class="in"><b style="color:#F55823">АЛЛСАН</b><span>Разработка · Техподдержка · Продукты 1С · Кейсы · О нас</span><span>+7 (495) 260-04-03</span></div></div>
<div class="in crumb">⌂ / Модуль 1С для маркетплейсов / Интеграция 1С с Wildberries</div>

<!-- HERO -->
<section class="hero">
 <div class="in">
  <div style="padding-bottom:44px">
   <div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>Модуль Аллсан для селлеров</div>
   <h1>Интеграция 1С <br>с&nbsp;<span>Wildberries</span></h1>
   <p class="lead">Остатки и цены уходят из вашей 1С в кабинет Wildberries, заказы приходят обратно. Утром уже посчитана маржа за вчера с логистикой, хранением и штрафами WB.</p>
   <div class="btns">
    <a class="btn m" href="#popup:konsultacia">Показать на моём кабинете <span class="ar">→</span></a>
    <a class="btn g" href="#price">Цена от 40 700 ₽</a>
   </div>
  </div>
  <div class="photo">
   <img src="{IMG}allsun-hero-mp-employee-module.jpg" alt="Сергей Никешин, ведущий разработчик модуля интеграции 1С с Wildberries, Аллсан Интеграция">
   <div class="tag"><b>Сергей Никешин</b><span>ведущий разработчик модуля, Аллсан Интеграция</span></div>
  </div>
 </div>
</section>

<!-- DAY TIMELINE -->
<div class="day">
 <div class="in"><div class="box">
  <div class="lbl">Как выглядит день с модулем</div>
  <div class="track">
   <div class="it"><span class="t mono">по расписанию</span><b>Остатки на вашем складе</b>и цены уходят из 1С в Wildberries сами</div>
   <div class="it"><span class="t mono">сразу</span><b>Новый заказ FBS</b>появляется в 1С сам, этикетки печатаются из 1С</div>
   <div class="it"><span class="t mono">утром</span><b>Маржа за вчера</b>с логистикой, хранением и штрафами WB<a class="more" href="#reports" data-tab="0">Отчёт по марже →</a></div>
   <div class="it"><span class="t mono">каждый день</span><b>Ответы на отзывы</b>ИИ готовит ответы, вы проверяете и отправляете<a class="more" href="#reports" data-tab="1">Автоответы →</a></div>
   <div class="it"><span class="t mono">перед закупкой</span><b>Прогноз закупок</b>сколько товара заказать у поставщика<a class="more" href="#reports" data-tab="2">Прогноз закупок →</a></div>
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
   <div class="per">в год, только Wildberries</div>
   <dl>
    <dt>Конфигурации</dt><dd>УТ, УНФ, КА, ERP</dd>
    <dt>Схемы</dt><dd>FBO, FBS, DBS</dd>
    <dt>Кабинеты</dt><dd>любое число</dd>
    <dt>Код</dt><dd>открытый</dd>
    <dt>После подписки</dt><dd>продолжает работать</dd>
   </dl>
   <a class="btn m" href="#popup:konsultacia">Записаться на демонстрацию</a>
   <a class="btn g" href="#price">Купить модуль</a>
   <div class="small">Wildberries и Ozon вместе - 69 990 ₽ в год.</div>
   <div class="trust"><span>с 2015 года</span><span>ТОП 10 ЦРА</span><span>1С:Франчайзи</span></div>
  </aside>

  <div>
   <!-- 01 questions -->
   <div class="sec">
    <div class="num"><span class="n">01</span><span class="ln"></span></div>
    <h2>На какие вопросы отвечает модуль</h2>
    <p class="sub">Вопросы, которые селлер Wildberries задаёт каждую неделю. Ответы собираются в 1С без выгрузок в Excel.</p>
    <div class="qpanel">
     <div class="q big">
      <b>Сколько я заработал вчера на каждом товаре?</b>
      Модуль сводит отчёт Wildberries и себестоимость из 1С в один расчёт рентабельности.
      <div class="mini">
       <div><span>Выручка и выкуп</span><span>из отчёта WB</span></div>
       <div><span>Логистика и хранение</span><span>из WB</span></div>
       <div><span>Штрафы и удержания</span><span>из WB</span></div>
       <div><span>Себестоимость</span><span>из 1С</span></div>
       <div><span>Маржа</span><span>за вчера</span></div>
      </div>
      <a class="go" href="#reports" data-tab="0">Отчёт по марже →</a>
     </div>
     <div class="q"><b>Кто ответит на сотню отзывов?</b>ИИ читает отзыв, понимает тон и пишет ответ. Менеджер проверяет тексты и отправляет их одной кнопкой.<a class="go" href="#reports" data-tab="1">Автоответы →</a></div>
     <div class="q"><b>Когда пополнять свой склад?</b>Модуль берёт суточный расход по товарам и считает, сколько заказать у поставщика на выбранный срок.<a class="go" href="#reports" data-tab="2">Прогноз закупок →</a></div>
    </div>
   </div>

   <!-- 02 route -->
   <div class="sec">
    <div class="num"><span class="n">02</span><span class="ln"></span></div>
    <h2>Как идут данные</h2>
    <p class="sub">Модуль стоит внутри вашей 1С и работает с Wildberries через официальный API. Руками ничего переносить не нужно.</p>
    <div class="route">
     <div class="node"><div class="k">Ваша 1С</div><b>Учёт</b><ul><li>номенклатура и цены</li><li>остатки складов</li><li>себестоимость</li></ul></div>
     <div class="pipe"><div>остатки и цены</div><div class="back">заказы</div></div>
     <div class="node mid"><div class="k">Модуль Аллсан</div><b>Обмен и расчёты</b><ul><li>заказы в 1С</li><li>этикетки и штрихкоды поставок</li><li>маржа, отзывы, закупки</li></ul></div>
     <div class="pipe"><div>выгрузка</div><div class="back">отчёты WB</div></div>
     <div class="node"><div class="k">Кабинет Wildberries</div><b>Продажи</b><ul><li>карточки и остатки</li><li>заказы FBO, FBS, DBS</li><li>финансовые отчёты</li></ul></div>
    </div>
   </div>

   <!-- 03 tabs -->
   <div class="sec" id="reports">
    <div class="num"><span class="n">03</span><span class="ln"></span></div>
    <h2>Отчёты, которых нет в типовом обмене</h2>
    <p class="sub">Настоящие экраны модуля в 1С.</p>
    <div class="tabs">
     <button class="on" data-t="0">Маржа по товарам</button>
     <button data-t="1">Отзывы с ИИ</button>
     <button data-t="2">Прогноз закупок</button>
    </div>
    <div class="pane on">
     <a class="shot" href="{SCR}wb-1c-marzha.jpg" data-zoom><img class="wbm" src="{SCR}wb-1c-marzha.jpg" alt="Расчёт рентабельности Wildberries в 1С по товарам"></a>
     <div class="txt"><b>Сколько вы заработали на каждом товаре</b><p>Выручка, выкуп, возвраты, логистика, хранение, платная приёмка, штрафы и себестоимость в одной таблице. Прибыль и маржа видны по категориям и по каждому товару.</p><div class="res">Видно, какие товары работают в минус</div></div>
    </div>
    <div class="pane">
     <a class="shot" href="{SCR}wb-1c-otzyvy-ii.jpg" data-zoom><img src="{SCR}wb-1c-otzyvy-ii.jpg" alt="Работа с отзывами Wildberries в 1С: ответы, подготовленные ИИ" loading="lazy"></a>
     <div class="txt"><b>Ответы на отзывы готовит ИИ</b><p>Модуль загружает отзывы из кабинета, ИИ пишет ответ с учётом оценки и текста. Можно добавить в ответ рекомендацию другого вашего товара. Менеджер проверяет и отправляет все ответы одной кнопкой.</p><div class="res">Для WB нужно только подключение к YandexGPT</div></div>
    </div>
    <div class="pane">
     <a class="shot" href="{SCR}wb-1c-prognoz-zakupok.png" data-zoom><img src="{SCR}wb-1c-prognoz-zakupok.png" alt="Прогноз закупок в 1С для поставок на Wildberries" loading="lazy"></a>
     <div class="txt"><b>Сколько заказать у поставщика</b><p>Задайте суточный расход и срок планирования. Модуль учтёт остаток и то, что уже заказано, и покажет, сколько нужно докупить.</p><div class="res">Товар и упаковка не заканчиваются перед поставкой</div></div>
    </div>
    <div class="extra-h">Ещё в модуле для Wildberries</div>
    <div class="extra">
     <div class="ex">
      <a class="exshot" href="{IMG}ozon-screens/ozon-1c-seo-generator.png" data-zoom aria-label="Открыть экран генератора SEO-описаний"><img src="{IMG}ozon-screens/ozon-1c-seo-generator.png" alt="Генератор SEO-описаний товаров в 1С: ключевые слова, преимущества, минус-слова" loading="lazy"><span class="zoom">Открыть экран</span></a>
      <b>SEO-описания карточек с помощью ИИ</b>
      <p>Выберите товар и задайте ключевые слова, преимущества и минус-слова. Ключи модуль может предложить сам. Остаётся выбрать стиль и длину текста, и ИИ напишет описание прямо в 1С.</p>
     </div>
     <div class="ex">
      <a class="exshot" href="{SCR}wb-1c-shtrihkody.jpg" data-zoom aria-label="Открыть экран штрихкодов"><img src="{SCR}wb-1c-shtrihkody.jpg" alt="Штрихкоды товаров с крупным названием, созданные в 1С" loading="lazy"><span class="zoom">Открыть экран</span></a>
      <b>Штрихкоды с крупным названием товара</b>
      <p>Модуль печатает штрихкоды для поставок с понятным названием и количеством. На складе реже путают товар при комплектации.</p>
     </div>
     <div class="ex">
      <b>Возвраты и отчёт комиссионера</b>
      <p>Возвраты и финансовый отчёт Wildberries загружаются в 1С. По ним модуль и считает маржу, сверять суммы вручную не нужно.</p>
     </div>
     <div class="ex">
      <b>Готовим для Wildberries</b>
      <p>Расчёт по кластерам, доля рекламных расходов, прибыль по менеджерам, маркировка «Честный знак» и реестр продаж юрлицам. Для Ozon эти функции уже работают.</p>
      <span class="need">В разработке</span>
     </div>
    </div>
   </div>

   <!-- 04 video -->
   <div class="sec">
    <div class="num"><span class="n">04</span><span class="ln"></span></div>
    <h2>Модуль в работе</h2>
    <p class="sub">Короткие видео с экрана 1С. Открываются в новом окне.</p>
    <div class="vids">
     <div class="ex">
      <a class="video" href="{VID_BARCODE}" target="_blank" rel="noopener" aria-label="Смотреть видео о печати штрихкодов Wildberries в новом окне">
       <img src="{IMG}case-wb-barcodes-video-cover.jpg" alt="Видео: печать штрихкодов для поставок на Wildberries через 1С" loading="lazy">
       <span class="play"><svg viewBox="0 0 24 24" width="30" height="30"><path d="M8 5v14l11-7z" fill="#fff"/></svg></span>
       <span class="vcap">Смотреть видео</span>
      </a>
      <b>Штрихкоды для поставок на Wildberries</b>
      <p>Как напечатать штрихкоды для маркировки поставки прямо из 1С.</p>
     </div>
     <div class="ex">
      <a class="video" href="{VID_REVIEWS}" target="_blank" rel="noopener" aria-label="Смотреть видео об автоответах на отзывы Wildberries в новом окне">
       <img src="{IMG}case-wb-reviews-video-cover.jpg" alt="Видео: автоответы на отзывы Wildberries из 1С" loading="lazy">
       <span class="play"><svg viewBox="0 0 24 24" width="30" height="30"><path d="M8 5v14l11-7z" fill="#fff"/></svg></span>
       <span class="vcap">Смотреть видео</span>
      </a>
      <b>Автоответы на отзывы Wildberries</b>
      <p>Как ИИ готовит ответы и как отправить их в кабинет одной кнопкой.</p>
     </div>
    </div>
   </div>

   <!-- 05 fit -->
   <div class="sec">
    <div class="num"><span class="n">05</span><span class="ln"></span></div>
    <h2>Кому подходит</h2>
    <div class="fit">
     <div><b>Учёт уже в 1С</b><p>УТ, УНФ, КА или ERP. Модуль встраивается в вашу базу, переходить на другую программу не нужно.</p></div>
     <div><b>Заказов стало много</b><p>Сборочные задания и остатки вручную вести уже тяжело, появляются ошибки и штрафы.</p></div>
     <div><b>Нужна реальная прибыль</b><p>Хочется видеть маржу по каждому товару с учётом логистики и хранения, а не только сумму к перечислению.</p></div>
    </div>
   </div>

   <!-- 06 price -->
   <div class="sec" id="price">
    <div class="num"><span class="n">06</span><span class="ln"></span></div>
    <h2>Сколько стоит</h2>
    <p class="sub">Цены с НДС 5% за год. Стоимость внедрения уточняем на звонке: она зависит от доработок вашей 1С.</p>
    <div class="prices">
     <div class="pc"><div class="nm">Только Wildberries</div><div class="p">40 700 ₽</div><div class="s">в год</div>
      <ul><li>Остатки, цены, заказы и этикетки</li><li>Маржа, отзывы с ИИ, прогноз закупок</li><li>Техподдержка и обновления под API</li></ul>
      <a class="btn g" href="{BUY_WB}">Купить модуль для Wildberries</a></div>
     <div class="pc a"><span class="badge">Выгоднее на 11 410 ₽</span><div class="nm">Wildberries и Ozon</div><div class="p">69 990 ₽</div><div class="s">в год, один модуль на обе площадки</div>
      <ul><li>Всё, что в тарифе для Wildberries</li><li>Обмен с Ozon: FBO, FBS, rFBS, DBS</li><li>Маржа по товарам на обеих площадках</li></ul>
      <a class="btn m" href="{BUY_BOTH}">Купить на обе площадки</a></div>
    </div>
    <p class="note">После окончания годовой подписки модуль продолжает работать. Подписка даёт обновления*, продление стоит столько же, сколько покупка. При заказе внедрения, техподдержки или лицензий 1С от 100 тыс. ₽ скидка 50% на первый год.<br>* Принимаем любые предложения по новым функциям модуля. Часть из них можем реализовать бесплатно, на своё усмотрение.</p>
   </div>

   <!-- 07 faq -->
   <div class="sec faq" style="margin-bottom:40px">
    <div class="num"><span class="n">07</span><span class="ln"></span></div>
    <h2>Частые вопросы</h2>
    <details open><summary>С какими конфигурациями 1С работает модуль?</summary><p>С 1С:Управление торговлей, 1С:УНФ, 1С:Комплексная автоматизация и 1С:ERP.</p></details>
    <details><summary>Что нужно для автоответов на отзывы Wildberries?</summary><p>Подключение к YandexGPT, дадим инструкцию. Отдельная платная подписка в кабинете Wildberries не нужна.</p></details>
    <details><summary>Что будет, когда закончится подписка?</summary><p>Модуль продолжит работать. Подписка нужна для обновлений под изменения API Wildberries и техподдержки. Продление стоит столько же, сколько покупка.</p></details>
    <details><summary>Можно подключить несколько кабинетов Wildberries?</summary><p>Да, число кабинетов не ограничено.</p></details>
    <details><summary>Сколько стоит внедрение?</summary><p>Зависит от того, насколько доработана ваша 1С. Посмотрим базу на звонке и назовём цену до начала работ.</p></details>
   </div>
  </div>
 </div>
</section>

<section class="final">
 <div class="in">
  <div><h2>Покажем модуль на вашем кабинете Wildberries</h2><p>Созвонимся, посмотрим вашу 1С и скажем, что даст модуль.</p><div class="ph">+7 (495) 260-04-03</div></div>
  <a class="btn m" href="#popup:konsultacia">Записаться на демонстрацию <span class="ar">→</span></a>
 </div>
</section>
"""


def main():
    src = io.open(SRC, encoding="utf-8").read()
    head = src[: src.index("</style>")] + EXTRA_CSS + "</style>\n</head>\n<body>\n"
    head = re.sub(r"<title>.*?</title>", "<title>Интеграция 1С с Wildberries - макет v3</title>", head)
    script = src[src.index("<script>"): src.index("</script>") + len("</script>")]
    html = head + BODY + "\n" + script + "\n</body>\n</html>\n"
    assert "\u2014" not in html and "\u2013" not in html
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("ok", OUT)


if __name__ == "__main__":
    main()
