import json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'tilda-briefs' / 'tier2-dubli-title-description-2026-09-29.html'
TPL = ROOT.parent / 'tilda-briefs' / 'tier2-breadcrumbs-tail-2026-09-28.html'
before = json.load(open(ROOT / '_wm-dups-live-2026-09-29.json', encoding='utf-8'))

src = (ROOT / '_build_dups_html_0929.py').read_text(encoding='utf-8')
ns = {'__file__': str(ROOT / '_build_dups_html_0929.py')}
exec(src.split('P = []')[0].replace("live = json.load(open(ROOT / '_wm-dups-live-2026-09-29.json', encoding='utf-8'))", ''), ns)
PRODUCTS = ns['PRODUCTS']

tpl = TPL.read_text(encoding='utf-8')
STYLE = tpl[tpl.index('<style>'):tpl.index('</style>') + len('</style>')]
SCRIPT = tpl[tpl.rindex('<script>'):tpl.rindex('</script>') + len('</script>')]

# карточки, где 29.09 новый текст попал в поле «Название»
WRONG_NAME = {
    '241626506282', '725353126612', '573152840912', '157999786462',
    '697998222332', '350780030942', '680601662821', '282548349311',
}
# после правки 11:37 у электронной ПРОФ на 1 место стоит название коробочной
SWAPPED = {'697998222332': '1С:Предприятие 8 ПРОФ. Клиентская лицензия на 1 рабочее место. Коробочная поставка (арт. 4601546080875)'}

_n = [0]


def esc(s):
    return html.escape(s, quote=False)


def cb(text):
    _n[0] += 1
    i = f'c{_n[0]}'
    return f'<div class="copybox"><pre id="{i}">{esc(text)}</pre><button type="button" data-copy="{i}">Копировать</button></div>'


def uid(u):
    return u.split('/tproduct/')[1].split('-')[1]


P = []
A = P.append
A('<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
  '  <title>Одинаковые title: остаток - alsn.ru - 29.09.2026</title>\n  ' + STYLE + '\n</head>\n<body>\n  <div class="wrap">')
A('<h1>Одинаковые title: остаток</h1>')
A('<p class="muted">Сигнал Яндекс.Вебмастера от 29.09.2026 («20 страниц с одинаковыми title», «4 страницы с одинаковыми description»). Проверка живого alsn.ru: 29.09.2026, 11:37 (витрины опубликованы в 11:37). Только Тильда, не Битрикс. В файле только то, что осталось сделать.</p>')
A('<div class="pills"><span class="pill danger">8 карточек: вернуть название</span><span class="pill warn">17 карточек: SEO-заголовок</span></div>')
A('<div class="callout danger">Каждый шаг - только после письменного «да». «Опубликовать» - отдельным шагом. robots.txt, Twitter и Bing не трогаем. HEAD сайта не трогаем.</div>')
A('<div class="callout ok"><strong>Уже сделано, не трогать:</strong> кейс РЭК (<a href="https://alsn.ru/vesii">/vesii</a>) полностью: описание, превью, код в HEAD, крошки на чёрном фоне, старый блок со стрелкой удалён. Три страницы вебинара закрыты от поиска. Описания всех 17 карточек разные. У «Охраны окружающей среды» (арт. <code>2900002159639</code>) название уже возвращено. Адрес <code>/caseecom</code> отдаёт 404, Вебмастер уберёт его сам.</div>')
A('<div class="toc"><strong>Задачи</strong><ol>'
  '<li><a href="#r2">Д-3а. 8 карточек: вернуть название товара</a></li>'
  '<li><a href="#r3">Д-3б. 17 карточек: новый заголовок во вкладке SEO</a></li>'
  '<li><a href="#pub">Опубликовать</a></li><li><a href="#skip">Что не делать</a></li></ol></div>')

# R2
A('<section class="task" id="r2"><h2><span class="num">Д-3а</span> 8 карточек: вернуть название товара</h2>')
A('<span class="lbl">Что сделать</span><p>У 7 карточек в основном поле «Название» стоит «Купить … | Аллсан», у одной - название соседнего товара. Вернуть каждой её прежнее название.</p>')
A('<div class="callout warn"><strong>Внимание, ПРОФ на 1 место.</strong> У электронной поставки (арт. <code>4601546116697</code>) сейчас название коробочной: «1С:Предприятие 8 ПРОФ. Клиентская лицензия на 1 рабочее место. Коробочная поставка (арт. 4601546080875)». Покупатель, открыв электронную лицензию, прочтёт «Коробочная поставка». Вернуть ей название из таблицы («… Электронная поставка»). Коробочной (арт. <code>4601546080875</code>) нужно своё название, у неё сейчас «Купить … | Аллсан».</div>')
A('<span class="lbl">Зачем</span><p>После публикации витрин гость видит «Купить 1С Охрана труда, электронная поставка | Аллсан» как заголовок карточки, имя на плитке витрины и в корзине. Для покупателя это выглядит как ошибка. А SEO-заголовок при этом не поменялся, дубль в поиске остался.</p>')
A('<span class="lbl">Как в Тильде (для каждой строки)</span><ol class="steps">'
  '<li>Магазин → <strong>Товары</strong> → поле поиска → вставить <strong>артикул</strong>.</li>'
  '<li>Открыть карточку. Верхнее поле <strong>«Название»</strong>: стереть «Купить … | Аллсан», вставить название из таблицы.</li>'
  '<li>Не закрывая карточку, сразу сделать для неё Д-3б (вкладка SEO). <strong>Сохранить</strong>.</li></ol>')
rows = ''
for vitr, vurl, items in PRODUCTS:
    for u, new in items:
        if uid(u) not in WRONG_NAME:
            continue
        b = before[u]
        now = SWAPPED.get(uid(u), new)
        rows += (f'<tr><td>{esc(vitr)}<br><a href="https://alsn.ru{u}">открыть карточку</a></td><td>{cb(b["sku"])}</td>'
                 f'<td><span class="muted">{esc(now)}</span></td><td>{cb(b["h1"])}</td></tr>')
A(f'<table><tr><th>Витрина</th><th>Артикул</th><th>Сейчас в «Названии»</th><th>Вернуть в поле «Название»</th></tr>{rows}</table>')
A('</section>')

# R3
A('<section class="task" id="r3"><h2><span class="num">Д-3б</span> 17 карточек: новый заголовок во вкладке SEO</h2>')
A('<span class="lbl">Что сделать</span><p>У всех 17 карточек заменить заголовок для поиска. Он лежит не в «Названии», а во вкладке <strong>SEO</strong> карточки.</p>')
A('<span class="lbl">Зачем</span><p>Сейчас в поиске пары карточек выглядят одинаково: «лицензия на 100 мест» электронная и коробочная, «Охрана труда» и «Охрана окружающей среды». Человек не видит разницы, поисковик склеивает их в одну. Новый заголовок говорит, чем товар отличается.</p>')
A('<span class="lbl">Как в Тильде (для каждой строки)</span><ol class="steps">'
  '<li>Магазин → <strong>Товары</strong> → поиск по <strong>артикулу</strong> → открыть карточку.</li>'
  '<li>Вкладка <strong>SEO</strong>. В некоторых версиях кабинета это ссылка «Настройки SEO» внизу карточки. Внутри три поля: заголовок (title), описание (description), ключевые слова.</li>'
  '<li>Поле <strong>«Заголовок»</strong>: сейчас там текст из колонки «Сейчас». Стереть, вставить текст из колонки «Вставить».</li>'
  '<li>Поле «Описание» не трогать. Верхнее поле «Название» не трогать (кроме 8 карточек из Д-3а). <strong>Сохранить</strong>.</li></ol>')
A('<p class="muted">Проверка 11:37: ни у одной из 17 карточек SEO-заголовок ещё не поменялся.</p>')
for vitr, vurl, items in PRODUCTS:
    A(f'<h3>{vitr} · <a href="{vurl}">{vurl}</a></h3>')
    rows = ''
    for u, new in items:
        b = before[u]
        flag = ' <span class="tag danger">и Д-3а</span>' if uid(u) in WRONG_NAME else ''
        rows += (f'<tr><td>{esc(b["h1"])}{flag}<br><a href="https://alsn.ru{u}">открыть карточку</a></td>'
                 f'<td>{cb(b["sku"])}</td><td><span class="muted">{esc(b["title"])}</span></td><td>{cb(new)}</td></tr>')
    A(f'<table><tr><th>Товар</th><th>Артикул</th><th>Сейчас в SEO → «Заголовок»</th><th>Вставить в SEO → «Заголовок»</th></tr>{rows}</table>')
A('</section>')

A('<section class="task" id="pub"><h2><span class="num">P</span> Опубликовать</h2><ol class="steps">'
  '<li>Д-3: карточки выходят на сайт вместе с витриной. После всех правок нажать «Опубликовать» на <code>products</code>, <code>dopolnitelnie_licenzii</code>, <code>kompleksnaya_avtomatizaciya</code>.</li>'
  '<li>«Опубликовать все страницы» не нужно.</li>'
  '<li>Вебмастер пересчитает дубли после нового обхода, обычно за 1-3 недели.</li></ol></section>')
A('<section class="task" id="skip"><h2>Что не делать</h2><ul class="tight">'
  '<li>Не писать «Купить … | Аллсан» в поле «Название»: это имя товара для гостя.</li>'
  '<li>Не трогать описания карточек: они уже разные.</li>'
  '<li>Не менять адреса карточек и не объединять электронную и коробочную поставку.</li>'
  '<li>Не трогать кейс РЭК и страницы вебинаров: там всё готово.</li>'
  '<li>Не копировать название из соседней строки таблицы: у электронной и коробочной поставки названия разные.</li>'
  '<li>Не править robots.txt, Twitter, Bing. Не смешивать с Битрикс.</li></ul></section>')
A('<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-dubli-title-description-2026-09-29.html</code> · проверка: <code>seo-data/scripts/_cards_full_check_0929.py</code>, <code>_vesii_verify_0929.py</code>, <code>_events_check_0929.py</code></p>')
A('  </div>\n  ' + SCRIPT + '\n</body>\n</html>\n')

text = '\n'.join(P).replace('\u2014', '-').replace('\u2013', '-')
OUT.write_text(text, encoding='utf-8')
print(OUT, len(text), 'rows wrong name:', sum(1 for _, _, it in PRODUCTS for u, _ in it if uid(u) in WRONG_NAME))
