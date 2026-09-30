import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'tilda-briefs' / 'tier2-dubli-title-description-2026-09-29.html'
TPL = ROOT.parent / 'tilda-briefs' / 'tier2-breadcrumbs-tail-2026-09-28.html'
live = json.load(open(ROOT / '_wm-dups-live-2026-09-29.json', encoding='utf-8'))

tpl = TPL.read_text(encoding='utf-8')
STYLE = tpl[tpl.index('<style>'):tpl.index('</style>') + len('</style>')]
SCRIPT = tpl[tpl.rindex('<script>'):tpl.rindex('</script>') + len('</script>')]

_n = [0]


def esc(s):
    return html.escape(s, quote=False)


def cb(text):
    _n[0] += 1
    i = f'c{_n[0]}'
    return f'<div class="copybox"><pre id="{i}">{esc(text)}</pre><button type="button" data-copy="{i}">Копировать</button></div>'


PB = 'https://alsn.ru/products'
LIC = 'https://alsn.ru/dopolnitelnie_licenzii'
KA = 'https://alsn.ru/kompleksnaya_avtomatizaciya'

# (url, new title)
PRODUCTS = [
    ('Витрина «Продукты 1С»', PB, [
        ('/products/tproduct/946953291-241626506282-1s-predpriyatie-8-proizvodstvennaya-bezo', 'Купить 1С Промышленная безопасность, электронная поставка | Аллсан'),
        ('/products/tproduct/946953291-725353126612-1s-predpriyatie-8-proizvodstvennaya-bezo', 'Купить 1С Пожарная безопасность, электронная поставка | Аллсан'),
        ('/products/tproduct/946953291-573152840912-1s-predpriyatie-8-proizvodstvennaya-bezo', 'Купить 1С Производственная безопасность Комплексная | Аллсан'),
        ('/products/tproduct/946953291-614846453552-1s-predpriyatie-8-proizvodstvennaya-bezo', 'Купить 1С Охрана окружающей среды, электронная поставка | Аллсан'),
        ('/products/tproduct/946953291-157999786462-1s-predpriyatie-8-proizvodstvennaya-bezo', 'Купить 1С Охрана труда, электронная поставка | Аллсан'),
    ]),
    ('Витрина «Купить лицензии 1С ПРОФ»', LIC, [
        ('/dopolnitelnie_licenzii/tproduct/1231123726-697998222332-1s-predpriyatie-8-prof-klientskaya-litse', 'Купить лицензию 1С ПРОФ на 1 место, электронная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-350780030942-1spredpriyatie-8-prof-klientskaya-litsen', 'Купить лицензию 1С ПРОФ на 1 место, коробочная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-159637201592-1s-predpriyatie-8-prof-klientskaya-litse', 'Купить лицензию 1С ПРОФ на 50 мест, электронная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-295893253862-1spredpriyatie-8-prof-klientskaya-litsen', 'Купить лицензию 1С ПРОФ на 50 мест, коробочная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-658261749802-1s-predpriyatie-8-prof-klientskaya-litse', 'Купить лицензию 1С ПРОФ на 100 мест, электронная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-583281700322-1spredpriyatie-8-prof-klientskaya-litsen', 'Купить лицензию 1С ПРОФ на 100 мест, коробочная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-293950783102-1s-predpriyatie-8-prof-klientskaya-litse', 'Купить лицензию 1С ПРОФ на 300 мест, электронная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-792021947492-1spredpriyatie-8-prof-klientskaya-litsen', 'Купить лицензию 1С ПРОФ на 300 мест, коробочная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-556990081002-1s-predpriyatie-8-prof-klientskaya-litse', 'Купить лицензию 1С ПРОФ на 500 мест, электронная поставка | Аллсан'),
        ('/dopolnitelnie_licenzii/tproduct/1231123726-308293969592-1spredpriyatie-8-prof-klientskaya-litsen', 'Купить лицензию 1С ПРОФ на 500 мест, коробочная поставка | Аллсан'),
    ]),
    ('Витрина «1С:Комплексная автоматизация»', KA, [
        ('/kompleksnaya_avtomatizaciya/tproduct/382573839-680601662821-1s-kompleksnaya-avtomatizatsiya-dlya-10', 'Купить 1С КА на 10 пользователей, клиент-сервер, электронная поставка | Аллсан'),
        ('/kompleksnaya_avtomatizaciya/tproduct/382573839-282548349311-1s-kompleksnaya-avtomatizatsiya-dlya-10', 'Купить 1С КА на 10 пользователей, клиент-сервер, коробочная поставка | Аллсан'),
    ]),
]

VESII_DESC = 'Кейс ООО «РЭК»: подключили весы к 1С:УНФ. Взвешивание катушек, печать этикеток и выпуск продукции в 1С без ручного ввода. Обработка быстрее в 3 раза.'

P = []
A = P.append
A('<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
  '  <title>Одинаковые title и description - alsn.ru - 29.09.2026</title>\n  ' + STYLE + '\n</head>\n<body>\n  <div class="wrap">')
A('<h1>Одинаковые title и description</h1>')
A('<p class="muted">Сигнал Яндекс.Вебмастера от 29.09.2026: «20 страниц содержат одинаковые title», «4 страницы содержат одинаковые description». Все адреса проверены на живом alsn.ru 29.09.2026. Только Тильда, не Битрикс.</p>')
A('<div class="pills"><span class="pill warn">17 карточек товаров</span><span class="pill warn">3 страницы вебинара</span><span class="pill danger">1 кейс с чужим описанием</span><span class="pill info">/caseecom уже 404</span></div>')
A('<div class="callout danger">Каждый шаг - только после письменного «да». «Опубликовать» - отдельным шагом. robots.txt, Twitter и Bing не трогаем. HEAD сайта не трогаем.</div>')
A('<div class="callout info"><strong>Откуда дубли.</strong> У карточек товаров в поле «Заголовок» во вкладке SEO имя обрезано примерно до 55 знаков. Всё, что отличает товары (электронная или коробочная поставка, «Охрана труда» или «Охрана окружающей среды»), отрезалось, и заголовки совпали. Описания у этих карточек уже разные, их не трогаем. У вебинаров три страницы одного и того же мероприятия, все три больше не нужны. У кейса РЭК описание скопировано с кейса СЦ. Адрес <code>/caseecom</code> из отчёта уже отдаёт 404, делать с ним ничего не нужно, Вебмастер сам уберёт его после обхода.</div>')
A('<div class="toc"><strong>Задачи</strong><ol>'
  '<li><a href="#d1">Д-1. Кейс РЭК: своё описание вместо описания кейса СЦ</a></li>'
  '<li><a href="#d1b">Д-1б. Кейс РЭК: свой код в HEAD вместо сломанного кода кейса СЦ</a></li>'
  '<li><a href="#d1c">Д-1в. Кейс РЭК: своя картинка превью</a></li>'
  '<li><a href="#d1d">Д-1г. Кейс РЭК: крошки вместо блока со стрелкой</a></li>'
  '<li><a href="#d2">Д-2. Вебинары: закрыть от поиска все три страницы</a></li>'
  '<li><a href="#d3">Д-3. Карточки товаров: вернуть в заголовок то, что их отличает (17 шт.)</a></li>'
  '<li><a href="#pub">Опубликовать</a></li><li><a href="#skip">Что не делать</a></li></ol></div>')

# D1
A('<section class="task" id="d1"><h2><span class="num">Д-1</span> Кейс РЭК: своё описание вместо описания кейса СЦ</h2>')
A('<p class="muted">Страница «Автоматизация производственного учета и интеграция весового оборудования с 1С:УНФ для ООО «РЭК»» · <a href="https://alsn.ru/vesii">https://alsn.ru/vesii</a> · адрес в Тильде <code>vesii</code></p>')
A('<span class="lbl">Что сделать</span><p>Заменить описание страницы на текст про весы и 1С:УНФ. Там же поправить описание для превью в мессенджерах.</p>')
A('<span class="lbl">Зачем</span><p>Страница про подключение весов на производстве пластика, а в поиске под ней сейчас текст про интеграцию с B2B-поставщиками. Человек, который ищет автоматизацию взвешивания, не узнает свою задачу и не кликнет. Вебмастер считает это дублем с кейсом СЦ.</p>')
A('<span class="lbl">Как в Тильде</span><ol class="steps">'
  '<li>Список страниц → <code>vesii</code> → <strong>Настройки</strong> (шестерёнка) → <strong>Главное</strong> → поле «Описание».</li>'
  '<li>Стереть старый текст и вставить новый:</li></ol>')
A('<p class="cap find">Найти (сейчас в поле)</p>' + cb(live['/vesii']['desc']))
A('<p class="cap put">Заменить на</p>' + cb(VESII_DESC))
A('<ol class="steps" start="3"><li>Вкладка <strong>«Соцсети»</strong> (или «Facebook и соцсети») → поле «Описание»: там тот же старый текст. Заменить на тот же новый. Если поле пустое, не заполнять: Тильда возьмёт описание из «Главного».</li>'
  '<li><strong>Сохранить</strong>.</li></ol>')
A('<div class="callout warn"><strong>Заодно видно гостю.</strong> Сразу под первым экраном страницы, под кнопкой «ЗАКАЗАТЬ КОНСУЛЬТАЦИЮ», стоит старый блок крошек со стрелкой: «Все кейсы → Кейс «Автоматизация B2B-интеграции с поставщиками в ООО «СЦ»». Гость на кейсе РЭК видит название чужого кейса. Предлагаю удалить этот блок (навести → корзина / «Удалить») отдельным шагом. Новые крошки для кейсов - в третьей волне.</div>')
A('<p class="muted">Состояние 29.09, 11:20: описание и описание для превью уже заменены, на сайте новый текст. Осталось удалить блок со стрелкой и заменить HEAD (Д-1б).</p>')
A('</section>')

# D1b
HEAD_VESII = (ROOT.parent / 'tilda-briefs' / '_head-vesii-2026-09-29.txt').read_text(encoding='utf-8').strip()
A('<section class="task" id="d1b"><h2><span class="num">Д-1б</span> Кейс РЭК: свой код в HEAD вместо сломанного кода кейса СЦ</h2>')
A('<p class="muted">Страница «Автоматизация производственного учета и интеграция весового оборудования с 1С:УНФ для ООО «РЭК»» · <a href="https://alsn.ru/vesii">https://alsn.ru/vesii</a> · адрес в Тильде <code>vesii</code></p>')
A('<span class="lbl">Что сделать</span><p>Всё содержимое поля HEAD страницы заменить одним готовым блоком: путь «Главная / Кейсы / Кейс «РЭК»» и описание кейса для поисковика. Эта задача заменяет В-2 из инструкции по крошкам: там код предлагалось просто удалить, здесь сразу ставим правильный.</p>')
A('<span class="lbl">Зачем</span><p>Сейчас в HEAD лежит код, скопированный с кейса СЦ: другой адрес, другое название, и в нём пропущена запятая, поэтому поисковик не читает его вовсе. Новый код говорит поиску, что это кейс в разделе «Кейсы» про весы и 1С:УНФ. Страница может получить в выдаче путь «alsn.ru › Кейсы» и попадать в ответы на запросы про интеграцию весов с 1С.</p>')
A('<span class="lbl">Где</span><p>В поле «HTML-код для вставки внутрь head» <strong>этой страницы</strong> сейчас только один блок, около 2 КБ. Начинается с <code>&lt;script type="application/ld+json"&gt;</code>, внутри адрес <code>https://alsn.ru/caseecomsc</code>. Блок «Организация / Сайт» (Organization, WebSite) лежит в HEAD <strong>сайта</strong>, не здесь, и его не трогаем.</p>')
A(f'<span class="lbl">Как в Тильде</span><ol class="steps"><li>Список страниц → <code>vesii</code> → <strong>Настройки</strong> (шестерёнка) → <strong>Дополнительно</strong> → поле «HTML-код для вставки внутрь head».</li>'
  '<li>Найти (Ctrl+F) в поле строку ниже и убедиться, что это тот самый блок кейса СЦ:</li></ol>')
A('<p class="cap find">Найти</p>' + cb('https://alsn.ru/caseecomsc#breadcrumb'))
A('<ol class="steps" start="3"><li>Если в поле нет ничего, кроме этого блока: выделить всё (Ctrl+A) и удалить. Если есть другой код (например, счётчик), удалить только блок от <code>&lt;script type="application/ld+json"&gt;</code> до <code>&lt;/script&gt;</code> вокруг найденной строки.</li>'
  '<li>Вставить на его место:</li></ol>')
A('<p class="cap put">Заменить на</p>' + cb(HEAD_VESII))
A('<ol class="steps" start="5"><li><strong>Сохранить</strong> → <strong>«Опубликовать»</strong>.</li></ol>')
A('<div class="callout info"><strong>На будущее.</strong> Когда в третьей волне на этой странице появятся видимые крошки, имя последнего звена на экране должно быть тем же: «Кейс «РЭК»».</div>')
A('<p class="muted">Состояние 29.09, 11:25: код в HEAD стоит и совпадает с образцом, старого кода кейса СЦ нет.</p>')
A('</section>')

# D1c
A('<section class="task" id="d1c"><h2><span class="num">Д-1в</span> Кейс РЭК: своя картинка превью</h2>')
A('<p class="muted">Страница «Автоматизация производственного учета и интеграция весового оборудования с 1С:УНФ для ООО «РЭК»» · <a href="https://alsn.ru/vesii">https://alsn.ru/vesii</a> · адрес в Тильде <code>vesii</code></p>')
A('<span class="lbl">Что сделать</span><p>Загрузить во вкладку «Соцсети» новую картинку превью кейса РЭК вместо картинки кейса СЦ.</p>')
A('<span class="lbl">Зачем</span><p>Когда ссылку на кейс кидают в Telegram или WhatsApp, сейчас показывается картинка чужого кейса. Новая говорит сразу: весы в 1С:УНФ, без бумажных журналов, обработка в 3 раза быстрее. Весь текст стоит в центре, поэтому Telegram его не обрежет.</p>')
A('<span class="lbl">Файл</span><p><code>seo-data/brand-images/allsun-og-case-rek.jpg</code> (1200×630, 39 КБ). Запасной вариант без сжатия: <code>allsun-og-case-rek.png</code>.</p>')
A('<p><img src="../brand-images/allsun-og-case-rek.jpg" alt="Превью кейса РЭК" style="max-width:100%;border:1px solid #e2e2de;border-radius:8px"></p>')
A('<span class="lbl">Как в Тильде</span><ol class="steps">'
  '<li>Список страниц → <code>vesii</code> → <strong>Настройки</strong> → вкладка <strong>«Соцсети»</strong> (или «Facebook и соцсети»).</li>'
  '<li>Поле «Картинка» / «Изображение для соцсетей» → удалить старую → загрузить <code>allsun-og-case-rek.jpg</code>.</li>'
  '<li>Если Тильда предложит обрезать картинку до квадрата, отказаться: нужна вся картинка 1200×630.</li>'
  '<li><strong>Сохранить</strong> → <strong>«Опубликовать»</strong>.</li>'
  '<li>Старые сообщения в Telegram сами не обновятся. Для проверки отправить ссылку заново или прогнать её через <code>@WebpageBot</code>.</li></ol>')
A('</section>')

# D1d
NAV_REK = '''<nav aria-label="Хлебные крошки" style="display:flex;align-items:center;flex-wrap:nowrap;font-size:14px;line-height:1.2;color:#cfcfcf;padding:12px 20px 8px;">
  <a href="https://alsn.ru/" aria-label="Главная" title="Главная" style="display:inline-flex;color:inherit;text-decoration:none;">
    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.2 3 10.8V21h6.2v-6.5h5.6V21H21V10.8L12 3.2z"/></svg>
  </a>
  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>
  <a href="https://alsn.ru/cases" style="color:inherit;text-decoration:none;white-space:nowrap;">Кейсы</a>
  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>
  <span style="opacity:.75;white-space:nowrap;">Кейс «РЭК»</span>
</nav>'''
A('<section class="task" id="d1d"><h2><span class="num">Д-1г</span> Кейс РЭК: крошки «дом / Кейсы / Кейс «РЭК»» вместо блока со стрелкой</h2>')
A('<p class="muted">Страница «Автоматизация производственного учета и интеграция весового оборудования с 1С:УНФ для ООО «РЭК»» · <a href="https://alsn.ru/vesii">https://alsn.ru/vesii</a> · адрес в Тильде <code>vesii</code></p>')
A('<span class="lbl">Что сделать</span><p>Удалить старый блок «Все кейсы → Кейс «Автоматизация B2B-интеграции с поставщиками в ООО «СЦ»» и поставить сверху, над первым экраном, крошки как в каталоге: иконка дома / Кейсы / Кейс «РЭК». Служебный путь в HEAD уже стоит (Д-1б), его не трогать.</p>')
A('<span class="lbl">Зачем</span><p>Сейчас гость на кейсе РЭК читает название чужого кейса. Новые крошки показывают, где он, и одним кликом ведут ко всем кейсам. Имя «Кейс «РЭК»» на экране совпадает с именем в коде HEAD, поисковик видит один и тот же путь.</p>')
A('<span class="lbl">Где</span><p>Первый экран под меню - обложка T205 на фото с тёмной вуалью 50% и заголовком «Автоматизация производственного учета и интеграция весового оборудования с 1С:УНФ для ООО «РЭК»», кнопка «ЗАКАЗАТЬ КОНСУЛЬТАЦИЮ». Старый блок со стрелкой стоит <strong>под</strong> этой обложкой. Верх обложки тёмный, поэтому крошки светло-серые, фон T123 чёрный.</p>')
A('<span class="lbl">Как в Тильде</span><ol class="steps">'
  '<li>Список страниц → <code>vesii</code> → <strong>Редактировать</strong>.</li>'
  '<li>Под обложкой найти блок с текстом «Все кейсы → Кейс «Автоматизация B2B-интеграции с поставщиками в ООО «СЦ»» (T758). Навести → корзина / «Удалить» → подтвердить.</li>'
  '<li>Навести на обложку с заголовком «Автоматизация производственного учета…» → «+» <strong>сверху</strong> → Библиотека блоков → <strong>Другое</strong> → <strong>T123 «HTML-код»</strong>.</li>'
  '<li>Контент T123 → вставить:</li></ol>')
A('<p class="cap put">На экран (T123)</p>' + cb(NAV_REK))
A('<ol class="steps" start="5"><li>Настройки T123: цвет фона <span class="swatch" style="background:#000000"></span><code>#000000</code>, отступы сверху и снизу 0. Не оставлять фон пустым: Тильда нарисует белую полосу над тёмным фото.</li>'
  '<li><strong>Сохранить</strong> → <strong>«Опубликовать»</strong>.</li></ol>')
A('<p class="muted">В HEAD ничего добавлять не нужно: путь «Главная / Кейсы / Кейс «РЭК»» уже есть в коде из Д-1б. Второй такой код не ставить.</p>')
A('</section>')

# D2
A('<section class="task" id="d2"><h2><span class="num">Д-2</span> Вебинары: закрыть от поиска все три страницы</h2>')
A('<span class="lbl">Что сделать</span><p>Три страницы одного вебинара «Секретные способы увеличения продаж на маркетплейсах ОЗОН и Wildberries» с одинаковыми заголовком и описанием. Все три больше не нужны (решение 29.09.2026): закрыть от индексации.</p>')
A('<table><tr><th>Страница</th><th>Дата на экране</th><th>Состояние на 29.09, 11:04</th><th>Что делаем</th></tr>'
  '<tr><td><a href="https://alsn.ru/event-2025-06-----old1">https://alsn.ru/event-2025-06-----old1</a><br><code>event-2025-06-----old1</code></td><td>26 июня</td>'
  '<td><span class="tag ok">готово</span> Опубликована 29.09 в 11:04, запрет индексации стоит, в карте сайта нет.</td>'
  '<td>Не трогать.</td></tr>'
  '<tr><td><a href="https://alsn.ru/event-2025-06">https://alsn.ru/event-2025-06</a><br><code>event-2025-06</code></td><td>18 июля</td>'
  '<td><span class="tag danger">не та галочка</span> Стоит «не переходить по ссылкам» (<code>nofollow</code>), страница осталась в карте сайта.</td>'
  '<td>Снять галочку про ссылки, поставить запрет индексации, «Опубликовать».</td></tr>'
  '<tr><td><a href="https://alsn.ru/event-marketplaces">https://alsn.ru/event-marketplaces</a><br><code>event-marketplaces</code></td><td>16 октября</td>'
  '<td><span class="tag ok">готово</span> Запрет индексации стоит, из карты сайта убрана.</td>'
  '<td>Не трогать.</td></tr></table>')
A('<span class="lbl">Зачем</span><p>Вебинары прошли. Поиск видит три одинаковые страницы с приглашением на прошедшие даты, и человек из поиска попадает на мероприятие, которого уже не будет. Ссылок на эти страницы с главной, модуля маркетплейсов и кейсов нет, посещаемость сайт не теряет.</p>')
A('<span class="lbl">Как в Тильде</span><ol class="steps">'
  '<li>Список страниц → <code>event-2025-06</code> → <strong>Настройки</strong> → <strong>Facebook и SEO</strong> (или «SEO»).</li>'
  '<li>Снять галочку про ссылки (формулировка вроде «Запретить поисковикам переходить по ссылкам на этой странице»).</li>'
  '<li>Поставить галочку <strong>«Запретить поисковикам индексировать эту страницу»</strong>. <strong>Сохранить</strong> → <strong>«Опубликовать»</strong>.</li>'
  '<li>Страницы не удалять и с публикации не снимать: ссылки из старых рассылок продолжат открываться.</li></ol>')
A('<p class="muted">Файл robots.txt для этого не нужен: галочка ставит запрет прямо в код страницы и убирает её из карты сайта. Из поиска страницы уйдут после следующего обхода, обычно за 1-3 недели.</p>')
A('</section>')

# D3
A('<section class="task" id="d3"><h2><span class="num">Д-3</span> Карточки товаров: вернуть в заголовок то, что их отличает</h2>')
A('<span class="lbl">Что сделать</span><p>У 17 карточек заменить поле «Заголовок» во вкладке SEO товара. Новый заголовок говорит, чем товар отличается от соседа: вид поставки, число мест, модуль.</p>')
A('<span class="lbl">Зачем</span><p>Сейчас в поиске две карточки «лицензия на 100 мест» выглядят одинаково, и человек не видит, где электронная поставка, а где коробка. Поисковик тоже склеивает их и показывает одну. С разными заголовками каждая карточка сможет ловить свой запрос: «1С ПРОФ 100 мест электронная поставка», «1С охрана труда купить».</p>')
A('<span class="lbl">Как в Тильде (для каждой строки таблицы)</span><ol class="steps">'
  '<li>Магазин → <strong>Товары</strong> → поле поиска → вставить <strong>артикул</strong> из таблицы.</li>'
  '<li>Открыть найденную карточку (саму карточку, не родителя с вариантами) → вкладка <strong>SEO</strong> → поле «Заголовок» (title).</li>'
  '<li>Стереть старый заголовок, вставить новый из колонки «Заменить на». Поле «Описание» не трогать, оно уже своё у каждой карточки.</li>'
  '<li><strong>Сохранить</strong> карточку.</li></ol>')
A('<div class="callout danger"><strong>Не путать с названием товара.</strong> Основное поле «Название» вверху карточки не менять: это имя, которое гость видит на плитке витрины, в заголовке карточки и в корзине. Новый текст идёт только во вкладку <strong>SEO</strong> → «Заголовок». '
  'Проверка 29.09 в 11:28 (витрины опубликованы в 11:25): у <strong>9 карточек</strong> новый текст оказался в «Названии» и уже виден гостю как заголовок карточки и имя на плитке: все 5 карточек «Продуктов 1С», ПРОФ на 1 место (обе) и КА на 10 пользователей (обе). '
  'При этом SEO-заголовок у всех 17 карточек старый, дубли не ушли. '
  'Для этих 9: вернуть в «Название» текст из колонки «Название товара», а текст из «Заменить на» вписать во вкладку SEO → «Заголовок». Вкладка может называться «SEO» или открываться ссылкой «Настройки SEO» внизу карточки; в ней три поля: заголовок, описание, ключевые слова.</div>')
for vitr, vurl, items in PRODUCTS:
    A(f'<h3>{vitr} · <a href="{vurl}">{vurl}</a></h3>')
    rows = ''
    for u, new in items:
        r = live[u]
        rows += (f'<tr><td>{cb(r["h1"])}<a href="https://alsn.ru{u}">открыть карточку</a></td>'
                 f'<td>{cb(r["sku"])}</td>'
                 f'<td><span class="muted">{esc(r["title"])}</span></td>'
                 f'<td>{cb(new)}</td></tr>')
    A(f'<table><tr><th>Название товара (поле «Название», оставить так)</th><th>Артикул</th><th>Сейчас во вкладке SEO → «Заголовок»</th><th>Заменить на (вкладка SEO → «Заголовок»)</th></tr>{rows}</table>')
A('<p class="muted">Заголовки держим до 80 знаков, в конце « | Аллсан», как у остальных карточек. Модули производственной безопасности продаются только в электронной поставке, поэтому у «Комплексной» вид поставки не указан, чтобы не раздувать длину.</p>')
A('</section>')

A('<section class="task" id="pub"><h2><span class="num">P</span> Опубликовать</h2><ol class="steps">'
  '<li>Д-1 и Д-2: «Опубликовать» на страницах <code>vesii</code>, <code>event-2025-06</code>. <code>event-2025-06-----old1</code> и <code>event-marketplaces</code> уже опубликованы с запретом.</li>'
  '<li>Д-3: карточки товаров публикуются вместе с витриной. После правок нажать «Опубликовать» на <code>products</code>, <code>dopolnitelnie_licenzii</code>, <code>kompleksnaya_avtomatizaciya</code>.</li>'
  '<li>«Опубликовать все страницы» не нужно.</li>'
  '<li>Вебмастер пересчитает дубли после нового обхода, обычно за 1-3 недели. Ускорить можно через «Переобход страниц» для этих адресов, это отдельный шаг.</li></ol></section>')

A('<section class="task" id="skip"><h2>Что не делать</h2><ul class="tight">'
  '<li>Не трогать описания карточек товаров: они уже разные.</li>'
  '<li>Не удалять страницы вебинаров и не снимать их с публикации, только галочка запрета индексации.</li>'
  '<li>Не менять адреса карточек и не объединять электронную и коробочную поставку в одну карточку без отдельного решения.</li>'
  '<li>Не класть заголовки и код в поле «Текст» карточки.</li>'
  '<li>Не править robots.txt, Twitter, Bing. Не смешивать с Битрикс.</li></ul></section>')

A('<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-dubli-title-description-2026-09-29.html</code> · выгрузки Вебмастера: <code>alsn.ru_f25bf58936f374e6ee9acef7.xlsx</code> (title), <code>alsn.ru_5393361f057d96302826a6ea.xlsx</code> (description) · проверка: <code>seo-data/scripts/_wm-dups-live-2026-09-29.json</code></p>')
A('  </div>\n  ' + SCRIPT + '\n</body>\n</html>\n')

text = '\n'.join(P).replace('\u2014', '-').replace('\u2013', '-')
OUT.write_text(text, encoding='utf-8')
print(OUT, len(text))
for _, _, items in PRODUCTS:
    for u, new in items:
        print(len(new), new)
print(len(VESII_DESC))
