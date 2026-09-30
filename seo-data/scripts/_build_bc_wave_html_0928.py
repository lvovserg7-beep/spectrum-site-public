import json, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'tilda-briefs' / 'tier2-breadcrumbs-wave-2026-09-28.html'
TPL = ROOT.parent / 'tilda-briefs' / 'tier2-breadcrumbs-tail-2026-09-28.html'

probe = json.load(open(ROOT / '_bc-wave-probe-2026-09-28.json', encoding='utf-8'))
allbc = {x['path']: x for x in json.load(open(ROOT / '_bc-all-2026-09-28.json', encoding='utf-8'))}
_raw758 = json.load(open(ROOT / '_bc-t758-2026-09-28.json', encoding='utf-8'))
t758 = {'double': [], 'only': []}
for _p, _v in _raw758.items():
    if not isinstance(_v, dict) or not _v.get('t758'):
        continue
    _b = _v['t758'][0]
    t758['double' if _v.get('t123') else 'only'].append({'path': _p, 'rec': _b['rec'], 'text': _b['text']})

tpl = TPL.read_text(encoding='utf-8')
STYLE = tpl[tpl.index('<style>'):tpl.index('</style>') + len('</style>')]
SCRIPT = tpl[tpl.rindex('<script>'):tpl.rindex('</script>') + len('</script>')]

LIGHT, DARK = '#8a8a8a', '#cfcfcf'
HOME_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.2 3 10.8V21h6.2v-6.5h5.6V21H21V10.8L12 3.2z"/></svg>'

_id = [0]


def nid(prefix):
    _id[0] += 1
    return f'{prefix}-{_id[0]}'


def esc(s):
    return html.escape(s, quote=False)


def nav(color, parent, name):
    lines = [
        f'<nav aria-label="Хлебные крошки" style="display:flex;align-items:center;flex-wrap:nowrap;font-size:14px;line-height:1.2;color:{color};padding:12px 20px 8px;">',
        '  <a href="https://alsn.ru/" aria-label="Главная" title="Главная" style="display:inline-flex;color:inherit;text-decoration:none;">',
        f'    {HOME_SVG}',
        '  </a>',
        '  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>',
    ]
    if parent:
        lines += [
            f'  <a href="https://alsn.ru/{parent[1]}" style="color:inherit;text-decoration:none;white-space:nowrap;">{parent[0]}</a>',
            '  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>',
        ]
    lines += [f'  <span style="opacity:.75;white-space:nowrap;">{name}</span>', '</nav>']
    return '\n'.join(lines)


def ld(slug, parent, name):
    items = ['    { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/" }']
    pos = 2
    if parent:
        items.append(f'    {{ "@type": "ListItem", "position": {pos}, "name": "{parent[0]}", "item": "https://alsn.ru/{parent[1]}" }}')
        pos += 1
    items.append(f'    {{ "@type": "ListItem", "position": {pos}, "name": "{name}", "item": "https://alsn.ru/{slug}" }}')
    return ('<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n'
            f'  "@id": "https://alsn.ru/{slug}#breadcrumb",\n  "itemListElement": [\n' + ',\n'.join(items) + '\n  ]\n}\n</script>')


def copybox(text, prefix='c'):
    i = nid(prefix)
    return f'<div class="copybox"><pre id="{i}">{esc(text)}</pre><button type="button" data-copy="{i}">Копировать</button></div>'


def h1(path):
    v = probe.get(path, {}).get('h1') or allbc.get(path, {}).get('h1') or ''
    return v


def swatch(c):
    return f'<span class="swatch" style="background:{c}"></span><code>{c}</code>'


def t758_text(path):
    for group in ('double', 'only'):
        for r in t758.get(group, []):
            if r.get('path') == path:
                return r.get('rec'), r.get('text', '')
    return None, ''


parts = []
A = parts.append

A('<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
  '  <title>Хлебные крошки: вторая волна - alsn.ru - 28.09.2026</title>\n  ' + STYLE + '\n</head>\n<body>\n  <div class="wrap">')
A('<h1>Хлебные крошки: вторая волна</h1>')
A('<p class="muted">Проверка живого alsn.ru: 28.09.2026 · только Тильда, не Битрикс · вид как в каталоге: иконка дома и <code>/</code></p>')
A('<div class="pills"><span class="pill warn">2 страницы с лишним кодом</span><span class="pill warn">2 страницы с чужими крошками</span>'
  '<span class="pill warn">1 витрина без служебного пути</span><span class="pill warn">12 страниц с двойными крошками</span>'
  '<span class="pill danger">15 страниц без новых крошек</span></div>')
A('<div class="callout danger">Каждый шаг - только после письменного «да». «Опубликовать» - отдельным шагом по каждой странице. robots.txt, Twitter и Bing не трогаем. HEAD сайта (Organization, WebSite) не трогаем.</div>')
A('<div class="callout ok"><strong>Уже готово, не трогать:</strong> «Лицензии 1С», «Команда», «Публикации в СМИ», «Блог» из прошлого хвоста; внедрение 1С, КА, ERP, модуль маркетплейсов, «Интеграция с поставщиками» и страницы партнёров с новыми крошками, поддержка, 1С:КП, ЦРА, отзывы и остальные страницы с видом «дом /».</div>')
A('<div class="callout info"><strong>Старый блок крошек.</strong> На многих страницах первым под меню стоит старый блок Тильды T758: строка со стрелкой, например «Интеграция 1C по API с B2B поставщиками и дистрибьютерами → Merlion». Его убираем и ставим новый T123 с домом и <code>/</code>. Кейсы, статьи блога и страницы Telegram-бота (ещё 61 страница со старым блоком) - третьей волной, в эту пачку не входят. Страница <code>/1c-ozon-old</code> отдаёт 404, её больше нет: пункт закрыт.</div>')

A('<div class="toc"><strong>Задачи</strong><ol>'
  '<li><a href="#v1">В-1. «Кейсы»: удалить чужой код из HEAD</a></li>'
  '<li><a href="#v2">В-2. Кейс СЦ на /vesii: удалить сломанный код из HEAD</a></li>'
  '<li><a href="#v3">В-3. Кейс «Софтвидео»: исправить крошки</a></li>'
  '<li><a href="#v4">В-4. Интервью Сергея Львова: исправить крошки</a></li>'
  '<li><a href="#v5">В-5. Витрина «Фастфуд и Общепит»: служебный путь для карточек</a></li>'
  '<li><a href="#v6">В-6. Удалить старый блок там, где новые крошки уже есть (12 страниц)</a></li>'
  '<li><a href="#v7">В-7. Поставщики B2B: заменить старые крошки (7 страниц)</a></li>'
  '<li><a href="#v8">В-8. Переходы и синхронизации: заменить старые крошки (8 страниц)</a></li>'
  '<li><a href="#pub">Опубликовать</a></li><li><a href="#skip">Что не делать</a></li></ol></div>')

HEAD_PATH = 'Список страниц → страница → <strong>Настройки</strong> (шестерёнка) → <strong>Дополнительно</strong> → поле «HTML-код для вставки внутрь head»'

# V1
A('<section class="task" id="v1"><h2><span class="num">В-1</span> «Кейсы»: удалить чужой код из HEAD</h2>')
A('<p class="muted">Страница «Кейсы» · <a href="https://alsn.ru/cases">https://alsn.ru/cases</a> · адрес в Тильде <code>cases</code></p>')
A('<span class="lbl">Что сделать</span><p>В HEAD страницы удалить блок кода про кейс СЦ со старым адресом <code>/caseecom</code>. Свой путь «Главная / Кейсы» оставить.</p>')
A('<span class="lbl">Зачем</span><p>Поисковик видит на «Кейсах» два пути, и один ведёт на старый адрес кейса. Шаг был в хвосте (К-1), на 28.09 код всё ещё на месте.</p>')
A(f'<span class="lbl">Как в Тильде</span><ol class="steps"><li>{HEAD_PATH} (<code>cases</code>).</li><li>Найти (Ctrl+F) строку:</li></ol>')
A('<p class="cap find">Найти</p>' + copybox('https://alsn.ru/caseecom#breadcrumb', 'v1'))
A('<ol class="steps" start="3"><li>Выделить весь блок, в котором стоит эта строка: от ближайшего сверху <code>&lt;script type="application/ld+json"&gt;</code> (под ним <code>"@graph": [</code>) до ближайшего снизу <code>&lt;/script&gt;</code>. Перед <code>&lt;/script&gt;</code> идёт кусок <code>"about"</code> с текстом «Интеграция 1С с поставщиками телеком- и IT-оборудования».</li>'
  '<li><strong>Удалить</strong> выделенное.</li><li>Блок со строкой <code>https://alsn.ru/cases#breadcrumb</code> оставить. <strong>Сохранить</strong>.</li></ol></section>')

# V2
A('<section class="task" id="v2"><h2><span class="num">В-2</span> Кейс РЭК: удалить из HEAD сломанный код кейса СЦ</h2>')
A('<div class="callout ok"><strong>Заменено задачей Д-1б</strong> из инструкции <code>tier2-dubli-title-description-2026-09-29.html</code> (29.09.2026): там этот блок не просто удаляется, а сразу заменяется правильным кодом кейса РЭК. Делать по Д-1б, шаги ниже оставлены для справки.</div>')
A('<p class="muted">Страница «Автоматизация производственного учета и интеграция весового оборудования с 1С:УНФ для ООО «РЭК»» · <a href="https://alsn.ru/vesii">https://alsn.ru/vesii</a> · адрес в Тильде <code>vesii</code></p>')
A('<span class="lbl">Что сделать</span><p>Удалить из HEAD страницы блок кода, скопированный с кейса СЦ (<code>/caseecomsc</code>). В нём пропущена запятая, поисковик не может его прочитать.</p>')
A('<span class="lbl">Зачем</span><p>Страница про весы и 1С:УНФ для ООО «РЭК», а код описывает кейс СЦ и при этом сломан. Пользы от него нет, а в Вебмастере и Google он всплывает ошибкой разметки. Описание страницы и старый блок со стрелкой, где тоже написано про СЦ, - в инструкции <code>tier2-dubli-title-description-2026-09-29.html</code>, задача Д-1. Крошки для этой страницы поставим с кейсами в третьей волне.</p>')
A(f'<span class="lbl">Как в Тильде</span><ol class="steps"><li>{HEAD_PATH} (<code>vesii</code>).</li><li>Найти (Ctrl+F) строку:</li></ol>')
A('<p class="cap find">Найти</p>' + copybox('"url": "https://alsn.ru/caseecomsc"', 'v2'))
A('<ol class="steps" start="3"><li>Прямо над ней строка <code>"description": "Обмен 1С с ЛК и API поставщиков: остатки, цены, резерв и заказы. Результаты проекта для ООО «СЦ»."</code> без запятой в конце - это и есть поломка.</li>'
  '<li>Выделить весь блок: от ближайшего сверху <code>&lt;script type="application/ld+json"&gt;</code> до ближайшего снизу <code>&lt;/script&gt;</code> (около 2 КБ). <strong>Удалить</strong>.</li>'
  '<li>Если в поле больше ничего не осталось - так и должно быть. <strong>Сохранить</strong>.</li></ol></section>')


def fix_task(tid, path, title, find_nav_text, parent, name, bg_note, old_ld_id, slug):
    rec = probe[path]['nav_rec']
    A(f'<section class="task" id="{tid.lower().replace("-", "")}"><h2><span class="num">{tid}</span> {title}</h2>')
    A(f'<p class="muted">Страница «{esc(h1(path))}» · <a href="https://alsn.ru{path}">https://alsn.ru{path}</a> · адрес в Тильде <code>{path.lstrip("/")}</code></p>')
    return rec


# V3
p = '/cracasesoftvideo'
rec = fix_task('В-3', p, 'Кейс «Софтвидео»: исправить крошки', '', None, None, None, None, None)
A('<span class="lbl">Что сделать</span><p>Крошки на странице кейса показывают «дом / ЦРА», как будто это сама страница ЦРА. Сделать «дом / ЦРА / Кейс «Софтвидео»», где «ЦРА» - ссылка. Служебный путь в HEAD заменить на такой же. Старый блок со стрелкой «Все кейсы → …» удалить.</p>')
A('<span class="lbl">Зачем</span><p>Сейчас поисковик думает, что этот адрес и есть страница ЦРА: путь в коде ведёт на <code>/cra</code>. Две страницы спорят за одно место в выдаче.</p>')
A(f'<span class="lbl">Где</span><p>Самый верх, под меню. Первым идёт новый HTML-блок T123 (фон {swatch("#000000")}, номер <code>rec{rec}</code>) со строкой «/ ЦРА». Ниже старый блок T758 «Все кейсы → Кейс "Внедрение CRM системы в ООО "Софтвидео"». Дальше первый экран T205 на фото с тёмной вуалью, заголовок «Кейс «Внедрение CRM системы в ООО "Софтвидео"»».</p>')
A('<span class="lbl">Как в Тильде: на экране</span><ol class="steps"><li>Список страниц → <code>cracasesoftvideo</code> → <strong>Редактировать</strong>.</li><li>Первый блок под меню (T123, строка «/ ЦРА») → <strong>Контент</strong> → найти:</li></ol>')
A('<p class="cap find">Найти</p>' + copybox('<span style="opacity:.75;white-space:nowrap;">ЦРА</span>', 'v3'))
A('<p class="cap put">Заменить на</p>' + copybox('<a href="https://alsn.ru/cra" style="color:inherit;text-decoration:none;white-space:nowrap;">ЦРА</a>\n  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>\n  <span style="opacity:.75;white-space:nowrap;">Кейс «Софтвидео»</span>', 'v3'))
A('<ol class="steps" start="3"><li>Фон T123 не менять: <code>#000000</code> совпадает с тёмным фото ниже. <strong>Сохранить</strong>.</li>'
  '<li>Следующий блок со стрелкой «Все кейсы → …» (T758): навести → в правом верхнем углу блока иконка корзины / «Удалить» → подтвердить.</li></ol>')
A(f'<span class="lbl">Как в Тильде: в HEAD</span><ol class="steps"><li>{HEAD_PATH} (<code>cracasesoftvideo</code>).</li><li>Найти (Ctrl+F):</li></ol>')
A('<p class="cap find">Найти</p>' + copybox('https://alsn.ru/cra#breadcrumb', 'v3'))
A('<ol class="steps" start="3"><li>Выделить весь этот блок от <code>&lt;script type="application/ld+json"&gt;</code> до <code>&lt;/script&gt;</code> (путь «Главная / ЦРА») и заменить на:</li></ol>')
A('<p class="cap put">Заменить на</p>' + copybox(ld('cracasesoftvideo', ('ЦРА', 'cra'), 'Кейс «Софтвидео»'), 'v3'))
A('<ol class="steps" start="4"><li><strong>Сохранить</strong>.</li></ol></section>')

# V4
p = '/persons/interw_lvov'
rec = fix_task('В-4', p, 'Интервью Сергея Львова: исправить крошки', '', None, None, None, None, None)
A('<span class="lbl">Что сделать</span><p>Сейчас на экране «дом / Команда», будто это страница команды. Сделать «дом / Команда / Интервью Сергея Львова», где «Команда» - ссылка на <code>/persons</code>. Служебный путь заменить. Старый блок «Блог → Интервью с основателем ALLSUN» удалить.</p>')
A('<span class="lbl">Зачем</span><p>Путь в коде сейчас ведёт на <code>/persons</code>, и поисковик считает интервью копией страницы команды.</p>')
A(f'<span class="lbl">Где</span><p>Самый верх, под меню. Первым идёт T123 (фон {swatch("#000000")}, <code>rec{rec}</code>) со строкой «/ Команда». Ниже старый T758 «Блог → Интервью с основателем ALLSUN». Дальше первый экран T18 на тёмном фото, заголовок «Интеграция 1С. Как услуга стала отдельным бизнесом?».</p>')
A('<span class="lbl">Как в Тильде: на экране</span><ol class="steps"><li>Список страниц → <code>persons/interw_lvov</code> (или поиск по «interw») → <strong>Редактировать</strong>.</li><li>Первый блок под меню (T123, «/ Команда») → <strong>Контент</strong> → найти:</li></ol>')
A('<p class="cap find">Найти</p>' + copybox('<span style="opacity:.75;white-space:nowrap;">Команда</span>', 'v4'))
A('<p class="cap put">Заменить на</p>' + copybox('<a href="https://alsn.ru/persons" style="color:inherit;text-decoration:none;white-space:nowrap;">Команда</a>\n  <span style="margin:0 6px;opacity:.45;" aria-hidden="true">/</span>\n  <span style="opacity:.75;white-space:nowrap;">Интервью Сергея Львова</span>', 'v4'))
A('<ol class="steps" start="3"><li>Фон T123 оставить <code>#000000</code>. <strong>Сохранить</strong>.</li><li>Блок со стрелкой «Блог → Интервью с основателем ALLSUN» (T758) удалить: навести → корзина / «Удалить».</li></ol>')
A(f'<span class="lbl">Как в Тильде: в HEAD</span><ol class="steps"><li>{HEAD_PATH} (<code>persons/interw_lvov</code>).</li><li>Найти (Ctrl+F):</li></ol>')
A('<p class="cap find">Найти</p>' + copybox('https://alsn.ru/persons#breadcrumb', 'v4'))
A('<ol class="steps" start="3"><li>Выделить весь этот блок от <code>&lt;script type="application/ld+json"&gt;</code> до <code>&lt;/script&gt;</code> и заменить на:</li></ol>')
A('<p class="cap put">Заменить на</p>' + copybox(ld('persons/interw_lvov', ('Команда', 'persons'), 'Интервью Сергея Львова'), 'v4'))
A('<ol class="steps" start="4"><li><strong>Сохранить</strong>.</li></ol></section>')

# V5
SKUS = [
    ('2900002156812', '1С Предприятие 8 Общепит Электронная поставка'),
    ('4601546118998', '1С:Предприятие 8. Общепит'),
    ('2900002156829', '1С Предприятие 8 Общепит Комплект для 5 пользователей Электронная поставка'),
    ('4601546119001', '1С:Предприятие 8. Общепит. Комплект для 5 пользователей'),
    ('2900001901932', '1С Предприятие 8 Фастфуд Фронт-офис Электронная поставка'),
    ('2900002156850', '1С Общепит Клиентские лицензии на рабочие места Электронная поставка'),
    ('4601546119032', '1С:Общепит. Клиентские лицензии на рабочие места'),
    ('2900001901963', '1С Фастфуд и Ресторан Клиентские лицензии на рабочие места Электронная поставка'),
    ('4601546136718', '1С:Фастфуд и Ресторан. Клиентские лицензии на рабочие места'),
]
A('<section class="task" id="v5"><h2><span class="num">В-5</span> Витрина «Фастфуд и Общепит»: служебный путь для карточек</h2>')
A('<p class="muted">Страница «1C:Предприятие 8. Фастфуд и Общепит» · <a href="https://alsn.ru/1_obschepit_fastfood">https://alsn.ru/1_obschepit_fastfood</a> · адрес в Тильде <code>1_obschepit_fastfood</code></p>')
A('<span class="lbl">Что сделать</span><p>Вставить в HEAD витрины тот же универсальный скрипт, что уже работает на «Лицензиях 1С». Он сам собирает путь для каждой карточки товара этой витрины.</p>')
A('<span class="lbl">Зачем</span><p>На карточках товаров этой витрины поисковик сейчас не видит путь «Главная / раздел / товар». На других витринах он уже есть. Скрипт один на витрину, новые товары подхватываются сами.</p>')
A(f'<span class="lbl">Как в Тильде</span><ol class="steps"><li>{HEAD_PATH} (<code>1_obschepit_fastfood</code>). Это настройки <strong>страницы витрины</strong>, не HEAD сайта.</li><li>Встать <strong>в конец</strong> поля, ничего не стирая, вставить:</li></ol>')
A(copybox(probe['_showcase_script']['code'], 'v5'))
A('<ol class="steps" start="3"><li><strong>Сохранить</strong>.</li>'
  '<li>Видимые крошки на карточках дают блоки каталога ST340: в блоке каталога на витрине → Контент → вкладка «Хлебные крошки» → «Над заголовком». Если уже включено, не трогать.</li></ol>')
A('<p class="cap">Карточки, которые покроет скрипт (для сверки: Товары → поиск → вставить артикул)</p>')
rows = ''.join(f'<tr><td>{esc(n)}</td><td><code>{s}</code></td><td>{copybox(s, "sku")}</td></tr>' for s, n in SKUS)
A(f'<table><tr><th>Товар</th><th>Артикул</th><th>Копировать</th></tr>{rows}</table>')
A('<p class="muted">В карточки ничего вставлять не нужно. Код в поле «Текст» или во вкладку SEO товара не класть.</p></section>')

# V6 doubles
doubles = t758.get('double', [])
A('<section class="task" id="v6"><h2><span class="num">В-6</span> Удалить старый блок там, где новые крошки уже есть</h2>')
A('<span class="lbl">Что сделать</span><p>На этих страницах крошки стоят дважды: сверху новый блок «дом / …», под ним старый со стрелкой. Старый блок T758 удалить. Новый T123 и HEAD не трогать.</p>')
A('<span class="lbl">Зачем</span><p>Гость видит две строки пути подряд, одна со старыми названиями. Выглядит как ошибка вёрстки.</p>')
A('<span class="lbl">Как в Тильде (на каждой странице)</span><ol class="steps"><li>Список страниц → адрес из таблицы → <strong>Редактировать</strong>.</li>'
  '<li>Сразу под меню: сначала новый блок крошек (T123, иконка дома), под ним блок с текстом из колонки «Старый блок» со стрелкой <code>→</code>.</li>'
  '<li>Навести на старый блок → корзина / «Удалить» → подтвердить. Новый блок над ним оставить.</li><li><strong>Сохранить</strong>.</li></ol>')
rows = ''
for r in doubles:
    path = r['path']
    note = ''
    if path in ('/cracasesoftvideo', '/persons/interw_lvov'):
        note = ' <span class="tag warn">входит в В-3 / В-4</span>'
    rows += (f'<tr><td>{esc(h1(path))}{note}<br><a href="https://alsn.ru{path}">https://alsn.ru{path}</a></td>'
             f'<td><code>{path.lstrip("/")}</code></td><td>{esc(r["text"])}<br><span class="muted">rec{r["rec"]}</span></td></tr>')
A(f'<table><tr><th>Страница</th><th>Адрес в Тильде</th><th>Старый блок (удалить)</th></tr>{rows}</table></section>')


def wave_table(tid, title, what, why, where, pages):
    A(f'<section class="task" id="{tid.lower().replace("-", "")}"><h2><span class="num">{tid}</span> {title}</h2>')
    A(f'<span class="lbl">Что сделать</span><p>{what}</p><span class="lbl">Зачем</span><p>{why}</p><span class="lbl">Где</span><p>{where}</p>')
    A('<span class="lbl">Как в Тильде (на каждой странице)</span><ol class="steps">'
      '<li>Список страниц → адрес страницы → <strong>Редактировать</strong>.</li>'
      '<li>Если под меню есть блок со стрелкой <code>→</code> (T758) - навести → корзина / «Удалить».</li>'
      '<li>Навести на первый экран с заголовком → «+» <strong>сверху</strong> → Библиотека блоков → <strong>Другое</strong> → <strong>T123 «HTML-код»</strong>.</li>'
      '<li>Контент T123 → вставить код «На экран» этой страницы.</li>'
      '<li>Настройки T123 → цвет фона из карточки страницы, отступы сверху и снизу 0. <strong>Сохранить</strong>.</li>'
      f'<li>{HEAD_PATH} → в конец, ничего не стирая, вставить код «В HEAD». <strong>Сохранить</strong>.</li></ol>')
    for path, parent, name, dark, first in pages:
        slug = path.lstrip('/')
        rec, txt = t758_text(path)
        color, bg = (DARK, '#000000') if dark else (LIGHT, '#ffffff')
        A(f'<h3>{esc(h1(path))}</h3>')
        A(f'<p class="muted"><a href="https://alsn.ru{path}">https://alsn.ru{path}</a> · адрес в Тильде <code>{slug}</code> · на экране: дом / {esc(parent[0])} / {esc(name)}</p>')
        old = f'Старый блок удалить: «{esc(txt)}» (rec{rec}).' if rec else 'Старого блока со стрелкой нет.'
        A(f'<p>{old} Первый экран: {first}. Фон T123: {swatch(bg)}.</p>')
        A('<p class="cap put">На экран (T123)</p>' + copybox(nav(color, parent, name), 'w'))
        A('<p class="cap put">В HEAD страницы</p>' + copybox(ld(slug, parent, name), 'w'))
    A('</section>')


ECOM = ('Интеграция с поставщиками', 'ecom')
LIGHT_B2B = 'баннер T180 «Однократная оплата без ежегодного продления!» на светлом фоне'
wave_table('В-7', 'Поставщики B2B: заменить старые крошки',
           'Убрать старую строку «Интеграция 1C по API с B2B поставщиками и дистрибьютерами → …» и поставить крошки «дом / Интеграция с поставщиками / Имя поставщика», как уже сделано на странице Мерлион. Добавить служебный путь в HEAD.',
           'Это страницы продукта «Интеграция с B2B-поставщиками телеком-оборудования». Новые крошки ведут гостя на общую страницу продукта, а поисковик видит, что все партнёры - часть одного раздела. Эталон на сайте: <a href="https://alsn.ru/merlion">https://alsn.ru/merlion</a>.',
           'Сразу под меню стоит старый блок со стрелкой, под ним баннер T180 «Однократная оплата без ежегодного продления! Интеграция 1C с …». Верх баннера светлый, поэтому крошки серые на белом.',
           [('/vtt', ECOM, 'ВТТ', False, LIGHT_B2B),
            ('/dssl', ECOM, 'DSSL', False, LIGHT_B2B),
            ('/elko', ECOM, 'Элко Рус', False, LIGHT_B2B),
            ('/digis', ECOM, 'DIGIS', False, LIGHT_B2B),
            ('/auvix', ECOM, 'AUVIX', False, LIGHT_B2B),
            ('/resurs-media', ECOM, 'Ресурс-Медиа', False, LIGHT_B2B),
            ('/russkiy-svet', ECOM, 'Русский Свет', False, LIGHT_B2B)])

DEV = ('Внедрение 1С', 'development1c')
SUP = ('Техподдержка 1С', 'support1c')
MP = ('Модуль 1С для маркетплейсов', 'casemarketplace')
LIGHT_T = 'баннер T180 «Быстро и легко» на белом фоне, картинка справа'
wave_table('В-8', 'Переходы и синхронизации: заменить старые крошки',
           'Убрать старую строку «Сопровождение 1С → …» и поставить крошки «дом / раздел / короткое имя». Переходы на новую конфигурацию - в разделе «Внедрение 1С», как уже сделано на странице перехода с УПП. Синхронизации баз - в разделе «Техподдержка 1С». Перевыставление последней мили - в разделе «Модуль 1С для маркетплейсов». Добавить служебный путь в HEAD.',
           'Старая строка ведёт на «Внедрение 1С» с подписью «Сопровождение 1С», это путает гостя. Новый путь честно показывает раздел, а поисковик связывает страницу с нужной услугой. Эталон: <a href="https://alsn.ru/perehod-s-upp-na-ka-unf-ut">https://alsn.ru/perehod-s-upp-na-ka-unf-ut</a>.',
           'На шести страницах под меню старый блок со стрелкой, под ним баннер T180 на белом фоне: крошки серые, фон белый. На «Переход с МойСклад» и «Последняя миля Ozon» старого блока нет, первый экран - фото с тёмной вуалью: крошки светло-серые, фон T123 чёрный. Если раздел для синхронизаций хотите другой (например «Внедрение 1С»), скажите до вставки.',
           [('/perehod-s-ut-na-unf', DEV, 'Переход с УТ на УНФ', False, LIGHT_T),
            ('/perehod-s-dokumentooborota-2-1-na-3-0', DEV, 'Переход на Документооборот 3.0', False, LIGHT_T),
            ('/perehod-s-ut-10-3', DEV, 'Переход с УТ 10.3 на 11.5', False, LIGHT_T),
            ('/moy-sklad-perenos-v-1s', DEV, 'Переход с МойСклад на 1С', True, 'обложка T179 на фото с тёмной вуалью 70%'),
            ('/sinhronizaciya-bp-i-bp', SUP, 'Синхронизация БП и БП', False, LIGHT_T),
            ('/sinhronizaciya-mezhdu-zup-i-zup', SUP, 'Синхронизация ЗУП и ЗУП', False, LIGHT_T),
            ('/sinhronizaciya-mezhdu-ut-i-ut', SUP, 'Синхронизация УТ и УТ', False, LIGHT_T),
            ('/perevystavlenie-uslug-posledney-mili-ozon-v-1s', MP, 'Последняя миля Ozon', True, 'обложка T1065 на фото с тёмной вуалью')])

pages_pub = ['cases', 'vesii', 'cracasesoftvideo', 'persons/interw_lvov', '1_obschepit_fastfood'] + \
            [r['path'].lstrip('/') for r in doubles if r['path'] not in ('/cracasesoftvideo', '/persons/interw_lvov')] + \
            ['vtt', 'dssl', 'elko', 'digis', 'auvix', 'resurs-media', 'russkiy-svet',
             'perehod-s-ut-na-unf', 'perehod-s-dokumentooborota-2-1-na-3-0', 'perehod-s-ut-10-3', 'moy-sklad-perenos-v-1s',
             'sinhronizaciya-bp-i-bp', 'sinhronizaciya-mezhdu-zup-i-zup', 'sinhronizaciya-mezhdu-ut-i-ut',
             'perevystavlenie-uslug-posledney-mili-ozon-v-1s']
A('<section class="task" id="pub"><h2><span class="num">P</span> Опубликовать</h2><ol class="steps">'
  '<li>После «да» по задаче нажать <strong>«Опубликовать»</strong> на каждой затронутой странице: '
  + ', '.join(f'<code>{x}</code>' for x in pages_pub) + '.</li>'
  '<li>«Опубликовать все страницы» не нужно: HEAD сайта не меняли.</li></ol></section>')

A('<section class="task" id="skip"><h2>Что не делать</h2><ul class="tight">'
  '<li>Не трогать страницы из зелёного блока вверху.</li>'
  '<li>Не удалять новый блок крошек (с иконкой дома) на страницах из В-6: удаляем только блок со стрелкой.</li>'
  '<li>Не трогать кейсы, статьи блога и страницы Telegram-бота со старым блоком: они в третьей волне. Telegram-бот на сайте не снимаем.</li>'
  '<li>Не ставить второй служебный путь, если свой уже есть. Не класть его в HEAD сайта.</li>'
  '<li>Не вставлять скрипт витрины в карточки товаров, во вкладку SEO товара и в HEAD сайта.</li>'
  '<li>Не писать на экране «Главная →». Только иконка дома и <code>/</code>.</li>'
  '<li>Не править robots.txt, Twitter, Bing. Не смешивать с Битрикс.</li></ul></section>')

A('<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-breadcrumbs-wave-2026-09-28.html</code> · прошлый хвост: <code>tier2-breadcrumbs-tail-2026-09-28.html</code> · проверка: <code>seo-data/scripts/_bc-all-2026-09-28.json</code>, <code>_bc-t758-2026-09-28.json</code></p>')
A('  </div>\n  ' + SCRIPT + '\n</body>\n</html>\n')

text = '\n'.join(parts)
text = text.replace('\u2014', '-').replace('\u2013', '-')
OUT.write_text(text, encoding='utf-8')
print(OUT, len(text))

