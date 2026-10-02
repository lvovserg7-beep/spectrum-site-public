# -*- coding: utf-8 -*-
"""Макет общей страницы «Внедрение 1С» (https://alsn.ru/development1c) на стилях v3.

Стили - из preview-1c-ozon-v3.html, первый экран в рамке (HERO_CSS), шапка - меню C.
Фото профиля: Софья Мазницына.
Выход: seo-data/competitors/screens/preview-development1c-v3.html
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_menu_preview_0930 as menu
from mp_hero_frame import HERO_CSS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCR = os.path.join(ROOT, "competitors", "screens")
SRC = os.path.join(SCR, "preview-1c-ozon-v3.html")
OUT = os.path.join(SCR, "preview-development1c-v3.html")

PHOTO = "../../brand-images/allsun-hero-vnedrenie-sofia-maznitsina.jpg"
PHOTO_CDN = (
    "https://optim.tildacdn.com/tild3830-3363-4031-a461-393231623362/"
    "-/format/webp/allsun-hero-vnedreni.jpg.webp"
)
PHOTO_ALT = (
    "Софья Мазницына, координатор департамента разработки и интеграции "
    "информационных систем, Аллсан Интеграция"
)
WHO = (
    '<div class="who"><b>Софья Мазницына</b> · координатор департамента '
    "разработки и интеграции</div>"
)
EYEBROW = '<div class="eyebrow"><span class="rails"><i></i><i></i><i></i></span>{}</div>'
TRUST = (
    '<div class="trust"><span>с 2015 года</span>'
    '<span><a href="/cra">ТОП 10 ЦРА</a></span>'
    "<span>1С:Франчайзи</span></div>"
)
PHONE = "+7 495 260-04-03"

TEAM = [
    ("https://static.tildacdn.com/tild3433-6363-4436-b733-666266646164/Group_103.png",
     "Сергей Львов", "основатель, управляющий партнёр, аналитик 1С", False),
    ("https://static.tildacdn.com/tild6535-3462-4235-a238-626561623233/Group_104.png",
     "Павел Агеев", "программист 1С, руководитель проектов, техподдержка", False),
    ("https://static.tildacdn.com/tild3735-6532-4732-a263-613661383062/Group_105.png",
     "Никита Соколов", "программист 1С", False),
    ("https://static.tildacdn.com/tild3362-3838-4938-a161-623235383761/Group_100.png",
     "Энрико Айвазян", "программист 1С, руководитель проектов", False),
    ("https://static.tildacdn.com/tild3138-6561-4865-b439-383366386535/Group_101.png",
     "Ирина Щеглова", "руководитель проектов, аналитик", False),
    ("https://static.tildacdn.com/tild3537-6632-4736-b639-616236646639/Group_102.png",
     "Евгений Анастасьев", "руководитель проектов, программист 1С", False),
    ("https://static.tildacdn.com/tild6131-3734-4132-a164-373364303931/Group_99.png",
     "Роман Заболотный", "руководитель проектов", False),
]

FAQ = [
    ("Что если я оплачу, а решение меня не устроит?",
     "Перед началом проекта разбираем задачу и пишем ТЗ, обсуждаем варианты и приходим к общему решению. "
     "Работы доводим до конца, ошибки исправляем. Гарантия 90 дней: в этот срок бесплатно устраним ошибки."),
    ("Вдруг после вас в 1С появятся проблемы?",
     "До начала работ делаем резервную копию. Если возникнут ошибки по нашей работе, устраним их сами и бесплатно."),
    ("Мы в разных регионах. Как будем решать сложности?",
     "Проект делится на этапы: оплата и сдача идут по этапам. Можно связаться с нашими заказчиками и получить рекомендации."),
    ("Как вы защищаете данные клиента?",
     "С каждым клиентом подписываем NDA."),
    ("Какие конфигурации 1С внедряете?",
     "1С:Управление торговлей, 1С:Управление нашей фирмой, 1С:Комплексная автоматизация и 1С:ERP. "
     "Подбираем контур под процессы, а не продаём коробку."),
    ("Сколько стоит внедрение?",
     "Есть три типа: консультационный, agile и проектный. Цифру считаем после звонка. "
     "Консультационный - самый доступный: вы внедряете сами, мы отвечаем на вопросы по договору поддержки. "
     "Agile - средний: идём шагами через рабочие куски. Проектный - самый дорогой, зато смета известна заранее. "
     "Типичный проектный контур - 1,2-2,0 млн ₽. Это ориентир, не оферта."),
    ("Чем внедрение отличается от доработки?",
     "Внедрение - запуск учёта с нуля или переход на новую конфигурацию. Доработка - точечные работы в уже "
     "работающей базе. Если база уже стоит, это другой запрос."),
    ("Сколько длится проект?",
     "Срок зависит от контура и готовности команды на вашей стороне. Работа идёт этапами: обращение и анализ, "
     "ТЗ, согласование стоимости, реализация, тестирование у вас, приёмка этапа."),
]

LINKS = [
    ("Внедрение 1С:Комплексная автоматизация", "https://alsn.ru/kompleksnaya_avtomatizaciya"),
    ("Стоимость и этапы внедрения 1С:ERP", "https://alsn.ru/erp-time-price"),
    ("Техподдержка 1С после запуска", "https://alsn.ru/support1c"),
    ("1С:КП - подписка на сопровождение от 1С", "https://alsn.ru/its"),
    ("Кейсы внедрения и автоматизации", "https://alsn.ru/cases"),
]


def num(n):
    return f'<div class="num"><span class="n">{n:02d}</span><span class="ln"></span></div>'


def faq_html():
    return "\n".join(
        f'    <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(FAQ)
    )


def team_html():
    rows = []
    for src, name, role, local in TEAM:
        alt = f"{name}, {role}, Аллсан Интеграция"
        lz = "" if local else ' loading="lazy"'
        rows.append(
            f'     <div class="pp"><img src="{src}" alt="{alt}"{lz}>'
            f"<div><b>{name}</b>{role}</div></div>"
        )
    return "\n".join(rows)


def hero():
    h1 = '<h1>Внедрение 1С <br>под <span>ключ</span></h1>'
    lead = (
        '<p class="lead">Запускаем учёт с нуля или переводим компанию на новую конфигурацию. '
        "Обследование, настройка, обучение и запуск. Это не техподдержка и не продажа коробки.</p>"
    )
    btns = (
        '<div class="btns">'
        '<a class="btn m" href="#popup:konsultacia">Записаться на консультацию <span class="ar">→</span></a>'
        '<a class="btn g" href="#price">Стоимость после звонка</a></div>'
    )
    return (
        f'<section class="hf wide"><div class="in"><div class="frame">'
        f'<div class="txt">{EYEBROW.format("Услуга Аллсан · учёт под процессы")}{h1}{lead}{btns}</div>'
        f'<div class="ph"><img src="{PHOTO}" alt="{PHOTO_ALT}" fetchpriority="high">'
        f'<div class="veil"></div>{WHO}</div></div></div></section>'
    )


def body():
    notes = {
        "Внедрение 1С:Комплексная автоматизация": "Отдельная страница по КА: состав, вопросы и сравнение с ERP.",
        "Стоимость и этапы внедрения 1С:ERP": "Шесть этапов проекта и из чего складывается стоимость.",
        "Техподдержка 1С после запуска": "Когда учёт уже идёт и нужен внешний отдел, а не новый проект.",
        "1С:КП - подписка на сопровождение от 1С": "Официальная подписка 1С, отдельно от внедрения.",
        "Кейсы внедрения и автоматизации": "Письма и примеры работ, без чужих цифр на этой странице.",
    }
    links = "".join(
        f'<div class="ex"><b>{t}</b><p>{notes[t]}</p><a class="btn g" style="margin-top:14px" href="{u}">Открыть страницу</a></div>'
        for t, u in LINKS
    )
    return f"""
<div class="crumb-bar"><div class="in crumb">⌂ / Внедрение 1С</div></div>

<!-- HERO -->
{hero()}

<div class="day">
 <div class="in"><div class="box">
  <div class="lbl">Как идёт внедрение</div>
  <div class="track">
   <div class="it"><span class="t mono">старт</span><b>Обращение</b>разбираем цели и процессы, не продаём коробку</div>
   <div class="it"><span class="t mono">затем</span><b>Техническое задание</b>фиксируем контур, сроки и этапы</div>
   <div class="it"><span class="t mono">по этапам</span><b>Оплата и работы</b>сдаём и принимаем каждый этап отдельно</div>
   <div class="it"><span class="t mono">у вас</span><b>Тестирование</b>проверяете с руководителем проекта Аллсан</div>
   <div class="it"><span class="t mono">финал этапа</span><b>Приёмка</b>акт по этапу, дальше следующий контур или запуск</div>
  </div>
 </div></div>
</div>
<!-- BODY -->

<section class="body">
 <div class="in">
  <aside class="pass">
   <div class="ttl">Паспорт услуги</div>
   <div class="price">после звонка</div>
   <div class="per">стоимость зависит от типа внедрения</div>
   <dl>
    <dt>Что это</dt><dd>запуск учёта под ваши процессы</dd>
    <dt>Конфигурации</dt><dd>УТ, УНФ, КА, ERP</dd>
    <dt>Для кого</dt><dd>торговля и производство</dd>
    <dt>Команда</dt><dd>аналитик, программист, РП</dd>
    <dt>Гарантия</dt><dd>90 дней</dd>
    <dt>География</dt><dd>вся Россия</dd>
   </dl>
   <a class="btn m" href="#popup:konsultacia">Записаться на консультацию</a>
   <a class="btn g" href="#price">Три типа внедрения</a>
   <div class="small">Проектный контур обычно 1,2-2,0 млн ₽. Консультационный и agile дешевле. Ориентир, не цена «от».</div>
   {TRUST}
  </aside>

  <div>
   <div class="sec">
    {num(1)}
    <h2>На какие вопросы отвечает внедрение</h2>
    <p class="sub">Это запуск учёта, а не коробка с диска и не разовая доработка уже живой базы.</p>
    <div class="qpanel">
     <div class="q big">
      <b>Какую 1С выбрать и что будет в проекте?</b>
      Подбираем УТ, УНФ, КА или ERP под ваши процессы. В проект входят обследование, настройка, обучение и запуск.
      <div class="mini">
       <div><span>Обследование</span><span>процессы и контур</span></div>
       <div><span>Настройка</span><span>под вашу торговлю или производство</span></div>
       <div><span>Обучение</span><span>команда начинает работать в 1С</span></div>
       <div><span>Запуск</span><span>учёт идёт в новой базе</span></div>
       <div><span>Гарантия</span><span>90 дней</span></div>
      </div>
      <a class="go" href="#cfgs">Какие конфигурации →</a>
     </div>
     <div class="q"><b>Сколько займёт и из чего цена?</b>Зависит от типа: консультационный, agile или проектный. Разберём на звонке, какой вам подходит.<a class="go" href="#price">Три типа внедрения →</a></div>
     <div class="q"><b>Как не остаться с недоделанной базой?</b>Сдача по этапам, резервная копия до старта, гарантия 90 дней. Ошибки по нашей работе закрываем сами.<a class="go" href="#route">Этапы →</a></div>
    </div>
   </div>

   <div class="sec" id="route">
    {num(2)}
    <h2>Как идут работы</h2>
    <p class="sub">Три узла проекта. Между ними нет «коробки в подарок»: сначала процессы, потом настройка, потом запуск.</p>
    <div class="route">
     <div class="node"><div class="k">Вы</div><b>Задачи бизнеса</b><ul><li>торговля или производство</li><li>сейчас нет единой 1С</li><li>или переход на новый контур</li></ul></div>
     <div class="pipe"><div>обследование</div><div class="back">ТЗ и оценка</div></div>
     <div class="node mid"><div class="k">Команда Аллсан</div><b>Внедрение</b><ul><li>аналитик</li><li>программист 1С</li><li>руководитель проекта</li></ul></div>
     <div class="pipe"><div>настройка</div><div class="back">обучение</div></div>
     <div class="node"><div class="k">Ваша 1С</div><b>Запуск</b><ul><li>учёт в одной базе</li><li>отчёты без ручных сводов</li><li>команда работает в системе</li></ul></div>
    </div>
   </div>

   <div class="sec" id="cfgs">
    {num(3)}
    <h2>Какие конфигурации внедряем</h2>
    <p class="sub">Отдельные страницы - у КА и ERP. УТ и УНФ разбираем на консультации, отдельный лендинг под них не плодим.</p>
    <div class="extra">
     <div class="ex"><b>1С:Управление торговлей и УНФ</b><p>Торговый контур: склады, заказы, цены. Если этого достаточно, не тащим компанию в ERP.</p></div>
     <div class="ex"><b>1С:Комплексная автоматизация</b><p>Когда нужны финансы, склад, упрощённое производство и регламентированный учёт в одном контуре.</p><a class="btn g" style="margin-top:14px" href="https://alsn.ru/kompleksnaya_avtomatizaciya">Смотреть решение</a></div>
     <div class="ex"><b>1С:ERP</b><p>Производство и сложные процессы. Стоимость и шесть этапов проекта - на отдельной странице.</p><a class="btn g" style="margin-top:14px" href="https://alsn.ru/erp-time-price">Смотреть стоимость ERP</a></div>
    </div>
   </div>

   <div class="sec">
    {num(4)}
    <h2>Как принимаем работу</h2>
    <p class="sub">Без чужих цифр и чужих видео. Здесь то, что уже закреплено на странице внедрения.</p>
    <div class="fit">
     <div><b>Оплата по этапам</b><p>Не просим закрыть весь проект заранее. Сдача и оплата идут по согласованным этапам.</p></div>
     <div><b>Резервная копия и гарантия</b><p>До работ снимаем копию базы. Гарантия 90 дней: ошибки по нашей работе чиним бесплатно.</p></div>
     <div><b>NDA</b><p>Данные клиента не «на честном слове». С каждым договором подписываем соглашение о неразглашении.</p></div>
    </div>
    <p class="cmpnote">Примеры работ и письма клиентов - на странице <a href="https://alsn.ru/cases" style="color:var(--acc)">кейсов</a>.</p>
   </div>

   <div class="sec">
    {num(5)}
    <h2>Кому подходит</h2>
    <div class="fit">
     <div><b>Торговля и производство</b><p>Юрлица с выручкой от 500 млн ₽ в год. Нужна одна 1С вместо разрозненного учёта.</p></div>
     <div><b>Переход на новый контур</b><p>УТ, КА или ERP вместо старой базы или нескольких программ. Коробку «как есть» не ставим.</p></div>
     <div><b>Нужны отчёты без ручной сводки</b><p>Собственник, финдиректор, главбух или ИТ-директор хотят видеть прибыль и остатки без Excel.</p></div>
    </div>
    <p class="cmpnote">База уже работает и нужна точечная доработка? Это другой запрос, не этот проект. После запуска учёта сопровождение - на странице <a href="https://alsn.ru/support1c" style="color:var(--acc)">техподдержки 1С</a>.</p>
   </div>

   <div class="sec">
    {num(6)}
    <h2>Кто внедряет 1С</h2>
    <p class="sub">Координатор проекта, аналитики, программисты 1С и руководители проектов Аллсан.</p>
    <div class="team">
{team_html()}
    </div>
   </div>

   <div class="sec" id="price">
    {num(7)}
    <h2>Три типа внедрения</h2>
    <p class="sub">От самого доступного к самому предсказуемому. Какой подойдёт и сколько это будет стоить - скажем после звонка.</p>
    <div class="prices three">
     <div class="pc"><div class="nm">Консультационное</div><div class="p">доступный</div><div class="s">самый недорогой тип</div>
      <ul><li>Вы сами внедряете нужную 1С</li><li>Покупаете у нас техподдержку</li><li>Вопросы задаёте по ходу, мы отвечаем быстро</li></ul>
      <a class="btn g" href="https://alsn.ru/support1c">Смотреть техподдержку</a></div>
     <div class="pc"><div class="nm">Agile</div><div class="p">средний</div><div class="s">шагами, через MVP</div>
      <ul><li>Каждый раз делаем рабочий кусок, который уже можно запускать</li><li>По этому куску внедряем и делаем следующий шаг</li><li>Система растёт итерациями, без одного огромного ТЗ сразу</li></ul>
      <a class="btn g" href="#popup:konsultacia">Записаться на консультацию</a></div>
     <div class="pc a"><span class="badge">предсказуемый</span><div class="nm">Проектное</div><div class="p">по смете</div><div class="s">самый дорогой тип</div>
      <ul><li>Сначала пишем один большой проект</li><li>Потом внедряем строго по нему</li><li>Стоимость известна заранее, сюрпризов меньше</li></ul>
      <a class="btn m" href="#popup:konsultacia">Записаться на консультацию</a></div>
    </div>
    <p class="note">Проектный контур обычно 1,2-2,0 млн ₽. Это средний чек проектного внедрения, не цена консультационного или agile и не цена «от».</p>
    <div class="extra-h">Полезные страницы по внедрению 1С</div>
    <div class="extra">{links}</div>
   </div>

   <div class="sec faq" style="margin-bottom:40px">
    {num(8)}
    <h2>Частые вопросы</h2>
{faq_html()}
   </div>
  </div>
 </div>
</section>
<!-- FINAL -->

<section class="final">
 <div class="in">
  <div><h2>Разберём, какой контур 1С вам нужен</h2><p>Созвонимся, посмотрим процессы и скажем, это УТ, КА или ERP и из чего сложится проект.</p><div class="ph">{PHONE}</div></div>
  <a class="btn m" href="#popup:konsultacia">Записаться на консультацию <span class="ar">→</span></a>
 </div>
</section>
"""


EXTRA_CSS = """
@media(min-width:1141px){.v3 .hf.wide .txt{width:470px}.v3 .hf.wide .ph{aspect-ratio:auto;width:calc(100% - 448px)}.v3 .hf.wide .ph img{object-position:72% 40%}}
@media(min-width:1001px) and (max-width:1140px){.v3 .hf.wide .ph img{object-position:80% 40%}}
@media(max-width:1000px){.v3 .hf .ph img{object-position:70% 30%}}
.prices.three .pc{display:flex;flex-direction:column;padding:26px 22px}
.prices.three .pc ul{flex:1 1 auto}
.prices.three .pc .btn{margin-top:auto;padding:15px 12px;font-size:15px;white-space:nowrap;text-align:center}
.prices.three .pc .p{font-size:34px;line-height:1.15;white-space:normal}
.q.big .mini div{gap:14px}.q.big .mini div span+span{text-align:right}
.pass .trust a{color:inherit;text-decoration:none}
.pass .trust a:hover{color:var(--acc)}
.crumb-bar .crumb a{color:inherit}
.mh .btn,.mm .btn{display:inline-flex;align-items:center;gap:10px;padding:12px 20px;border-radius:12px;font-weight:600;font-size:15px;white-space:nowrap;border:0;cursor:pointer;font-family:inherit}
.mh .btn.m,.mm .btn.m{background:var(--acc);color:#fff}
"""


def main():
    src = io.open(SRC, encoding="utf-8").read()
    head = src[: src.index("</style>")]
    head = re.sub(r"<title>.*?</title>", "<title>Внедрение 1С под ключ - макет v3</title>", head)
    head += menu.CSS_C + "\n" + HERO_CSS + "\n" + EXTRA_CSS + "</style>\n</head>\n<body>\n"
    script = src[src.index("<script>"): src.index("</script>") + len("</script>")]
    demo = (
        '<div style="background:#F7F8FA;border-bottom:1px solid #D7DADD;font:13px Onest,sans-serif;color:#6b7075;padding:8px 0">'
        '<div class="in"><b style="color:#212121">Макет.</b> Общая страница «Внедрение 1С» '
        '(<a href="https://alsn.ru/development1c" style="color:#F55823">alsn.ru/development1c</a>) в стиле v3. '
        "На Тильду не переносить без письменного «да».</div></div>"
    )
    html = (
        head + demo + menu.header_a(menu.LOGO_WHITE_TEXT) + menu.mobile()
        + '\n<div class="v3">' + body() + "</div>\n"
        + script + f"\n<script>{menu.JS}</script>\n</body>\n</html>\n"
    )
    assert "\u2014" not in html and "\u2013" not in html
    assert "MPV" not in html
    assert "депортамент" not in html
    assert "Мазницына" in html
    assert "Мазницина" not in html
    io.open(OUT, "w", encoding="utf-8").write(html)
    print("ok", OUT)


if __name__ == "__main__":
    main()
