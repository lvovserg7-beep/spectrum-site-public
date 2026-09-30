# -*- coding: utf-8 -*-
"""Чистка tier2-breadcrumbs-sitewide-2026-09-18.html: остаётся только /case_telegram_bot."""
import re
from pathlib import Path

F = Path(__file__).parent.parent / "tilda-briefs" / "tier2-breadcrumbs-sitewide-2026-09-18.html"
raw = F.read_text(encoding="utf-8")

head = raw[: raw.index("<body>") + len("<body>")]
tail = raw[raw.index("  <script>\n    (function () {"):]

m = re.search(r'      <h3><a href="https://alsn.ru/case_telegram_bot">.*?data-copy="c-bc-case-telegram-bot">Копировать</button></div>\n', raw, re.S)
tg = m.group(0)
html_block = re.search(r'<div class="copybox"><pre id="c-html-case-telegram-bot">.*?</div>', tg, re.S).group(0)
ld_block = re.search(r'<div class="copybox"><pre id="c-bc-case-telegram-bot">.*?</div>', tg, re.S).group(0)

body = '''
  <div class="wrap">
    <h1>Хлебные крошки по сайту alsn.ru</h1>
    <p class="muted">Тильда · живой сайт · первая версия 18.09.2026, сверка с сайтом 29.09.2026 · только обычные страницы (не карточки Каталога)</p>
    <div class="pills">
      <span class="pill info">TIER 2</span>
      <span class="pill warn">дом + /</span>
      <span class="pill danger">осталась 1 страница</span>
    </div>

    <div class="callout info">
      <strong>Как работать.</strong> Каждый шаг - отдельно. Перед кликом, вставкой и «Опубликовать» - письменное «да» в чате.
      «Опубликовать» в конце - тоже отдельный шаг.
    </div>

    <div class="callout warn">
      <strong>Канон вида.</strong> Как на карточке Каталога: иконка дома (ссылка на главную), слэш <code>/</code>, имя страницы.
      На экране не писать «Главная» и не ставить стрелку. В служебном коде первое имя по-прежнему «Главная». Имя текущей страницы на экране = имя в коде буква в букву.
    </div>

    <div class="callout ok">
      <strong>Уже сделано - не трогать</strong>
      <ul style="margin:6px 0 0;padding-left:18px;">
        <li>T1: дом и <code>/</code> вместо «Главная →» на страницах «Техподдержка 1С», «Интеграция с поставщиками», «Модуль 1С для маркетплейсов», «Лицензии 1С», «1С:КП», «1С:Фреш» - проверено на сайте 29.09.2026.</li>
        <li>T2, волна A: «О компании», «Контакты», «Вакансии», «ЦРА», «Клиенты», «Битрикс24», «Telegram-бот 1С», «Кейсы» - крошки и служебный путь стоят, проверено на сайте 29.09.2026.</li>
        <li>T2, волна B: ЭТМ iPRO, Мерлион, OCS, Марвел, Treolan, 3logic - новые крошки стоят, проверено на сайте 29.09.2026. Старый блок со стрелкой на них убирается по задаче В-6 - перенесено в <code>tier2-breadcrumbs-wave-2026-09-28.html</code>.</li>
        <li>T2, кейс СЦ (<code>/caseecomsc</code>) - проверено на сайте 29.09.2026.</li>
        <li>T2, волна C: «Продукты», «Интеграция Битрикс24 и 1С», 1С:Бухгалтерия, 1С:ЗУП, 1С:УТ, 1С:УНФ, 1С:Документооборот, «Переход с УПП», «Интеграция с сайтом», «Интеграция с экосистемой», «Блог», «Стажировка», «Команда», «Отзывы», amoCRM, WhatsApp-бот 1С, «CRM для мебели», «Аутсорс или штат» - проверено на сайте 29.09.2026.</li>
        <li>T2, «Переход с МойСклад» и «Перевыставление Озон» - перенесено в <code>tier2-breadcrumbs-wave-2026-09-28.html</code> (задача В-8).</li>
        <li>T0, T3, T4 (как подобрать фон, запасные шаблоны) - справка к закрытым страницам, убрана. Канон вида и фона: правило <code>tilda-breadcrumbs.mdc</code>.</li>
      </ul>
    </div>

    <div class="callout danger">
      <strong>Не трогать.</strong> Главную <code>/</code> (крошки не нужны). Карточки Каталога <code>/…/tproduct/…</code> (там ST340).
      <code>robots.txt</code>, Twitter/X, Bing. Блоки Telegram-бота на сайте не снимать.
      HEAD <strong>сайта</strong> не открывать - только HEAD конкретной страницы.
    </div>

    <section class="task" id="t2">
      <h2><span class="num">T2</span> «Кейсы Telegram-ботов»: добавить крошки</h2>
      <p class="muted">Страница «Кейсы Telegram-ботов» · <a href="https://alsn.ru/case_telegram_bot">https://alsn.ru/case_telegram_bot</a> · адрес в Тильде <code>case_telegram_bot</code></p>
      <span class="lbl">Что сделать</span>
      <p>Поставить над первым экраном блок крошек «дом / Кейсы / Кейсы Telegram-ботов» и добавить служебный путь в HEAD страницы. На 29.09.2026 новых крошек нет, под меню стоит старый блок со стрелкой.</p>
      <span class="lbl">Зачем</span>
      <p>Гость видит, что страница лежит в разделе «Кейсы», и может одним кликом туда вернуться. Поиск понимает место страницы в структуре сайта.</p>
      <span class="lbl">Как в Тильде</span>
      <ol class="steps">
        <li>Список страниц → <code>case_telegram_bot</code> → <strong>Редактировать</strong>.</li>
        <li>Если сразу под меню стоит блок со стрелкой <code>→</code> (старый T758) - навести → корзина / «Удалить».</li>
        <li>Навести на первый экран с заголовком → <strong>«+»</strong> сверху → Библиотека блоков → <strong>Другое</strong> → <strong>T123 «HTML-код»</strong>.</li>
        <li>Контент T123 → вставить блок «На экран».</li>
        <li>Настройки T123 → «Цвет фона»: то, что видно у верхнего края первого экрана ниже (заливка или картинка). Светлый экран - <code>#ffffff</code> и код ниже как есть. Тёмный экран или тёмное фото - <code>#000000</code> и в коде заменить <code>color:#8a8a8a</code> на <code>color:#cfcfcf</code>. Отступы сверху и снизу 0. <strong>Сохранить</strong>.</li>
        <li>Список страниц → страница → <strong>Настройки</strong> (шестерёнка) → <strong>Дополнительно</strong> → «HTML-код для вставки внутрь head» → в конец, ничего не стирая, вставить блок «В HEAD». <strong>Сохранить</strong>.</li>
        <li><strong>Опубликовать</strong> страницу (отдельное «да»).</li>
      </ol>
      <p class="muted"><strong>На экран (T123)</strong></p>
      ''' + html_block + '''
      <p class="muted"><strong>В HEAD (BreadcrumbList)</strong></p>
      ''' + ld_block + '''
    </section>

    <section class="task" id="skip">
      <h2>Не трогать / отложить</h2>
      <table>
        <tr><th>Что</th><th>Почему</th></tr>
        <tr><td>Главная <code>/</code></td><td>Крошки на корне не ставим</td></tr>
        <tr><td>Карточки <code>/…/tproduct/…</code></td><td>ST340, в этой инструкции не разбираем</td></tr>
        <tr><td><code>/policy</code>, <code>/privacy</code>, <code>/soglashenie</code>, <code>/uslovia-vozvrata</code>, <code>/sitemap</code></td><td>Служебные, по желанию позже</td></tr>
        <tr><td><code>/event-2025-*</code></td><td>Разовые лендинги</td></tr>
        <tr><td>robots.txt</td><td>Тильда не даёт править</td></tr>
        <tr><td>Twitter / Bing</td><td>Вне контура</td></tr>
      </table>
    </section>

    <footer class="note">
      Файл: <code>seo-data/tilda-briefs/tier2-breadcrumbs-sitewide-2026-09-18.html</code> ·
      на alsn.ru не заливать · правки только в кабинете Тильды по шагам с «да».
    </footer>
  </div>

'''
F.write_text(head + body + tail, encoding="utf-8")
out = F.read_text(encoding="utf-8")
print(len(raw), "->", len(out), "dash", out.count("\u2014") + out.count("\u2013"))
