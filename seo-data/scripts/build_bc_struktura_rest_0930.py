# -*- coding: utf-8 -*-
"""Остаток инструкции tier2-breadcrumbs-struktura-2026-09-30.html после сверки 30.09.2026 (_bc_struct_verify_0930.py).

Видимые крошки на 13 страницах уже на сайте. На 8 витринах HEAD страницы и T123 крошек отдаются целиком:
поля берутся с живого сайта (_sc_head_probe_0930.py → _sc_fields_0930.py), JSON-LD из HEAD переезжает в T123.
Полную инструкцию больше не собирать build_bc_struktura_0930.py: она вернёт сделанные задачи.
"""
import json
import re
from pathlib import Path

import build_bc_struktura_0930 as B

esc, copybox, A_ld = B.esc, B.copybox, B.ld
LOST = {"/upt8": ([B.DEV], "1С:УТ"), "/buhv8": ([B.DEV], "1С:Бухгалтерия"), "/zup8": ([B.DEV], "1С:ЗУП"),
        "/upravlenie_nashei_firmoi": ([B.DEV], "1С:УНФ"), "/products": ([], "Программы 1С"),
        "/its": ([B.PROG], "1С:КП"), "/1cfresh": ([B.PROG], "1С:Фреш"), "/dokumentooborot8": ([B.PROG], "1С:Документооборот")}
F = json.load(open(Path(__file__).parent / "_sc_pages_0930/_fields.json", encoding="utf-8"))


def split_head(raw):
    """Поле HEAD витрины без JSON-LD и WebPage отдельно: всё это Тильда копирует на карточки товаров."""
    webpage = ""
    for m in re.finditer(r'<script type="application/ld\+json">.*?</script>', raw, re.S):
        if '"WebPage"' in m.group(0):
            webpage = re.sub(r"\n{2,}", "\n", m.group(0))
    rest = re.sub(r'<script type="application/ld\+json">.*?</script>', "", raw, flags=re.S)
    return re.sub(r"\s+", " ", rest).strip(), webpage


HEAD8 = ["/its"]

parts = []
A = parts.append
A('<!DOCTYPE html>\n<html lang="ru">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
  '  <title>Хлебные крошки под новую структуру - alsn.ru - остаток</title>\n  ' + B.STYLE + '\n</head>\n<body>\n  <div class="wrap">')
A('<h1>Хлебные крошки под новую структуру сайта: что осталось</h1>')
A('<p class="muted">Сверка с живым alsn.ru 30.09.2026, 17:10 · только Тильда, не Битрикс · '
  'структура: <code>struktura-karta-2026-09-30.html</code></p>')
A('<div class="pills"><span class="pill warn">1С:КП: два поля целиком</span><span class="pill info">1 проверка в каталоге</span></div>')
A('<div class="callout danger">Каждый шаг - только после письменного «да». «Опубликовать» - отдельным шагом. '
  'robots.txt, Twitter и Bing не трогаем. HEAD сайта (Organization, WebSite) не трогаем. Адреса страниц не меняем.</div>')
A('<div class="callout warn"><strong>Что сейчас не так.</strong> Осталась одна витрина «1С:КП». Крошки на экране правильные, '
  'но поисковик видит старый путь «Главная / 1С:КП» из HEAD страницы, а гость «Программы 1С / 1С:КП». '
  'Старый путь и описание страницы из HEAD Тильда копирует на все карточки товаров этой витрины (проверено 30.09.2026 17:10).</div>')

A('<section class="task" id="done"><h2>Уже сделано - не трогать</h2><ul class="tight">'
  '<li>30.09.2026: видимые крошки по новой структуре на всех 13 страницах (С-1 - С-4), фон блоков верный.</li>'
  '<li>30.09.2026: «Лицензии 1С» - один верный путь, старый из блока крошек убран (бывшая задача С-6).</li>'
  '<li>30.09.2026 17:10: С-5 на 7 витринах (1С:УТ, 1С:Бухгалтерия, 1С:ЗУП, 1С:УНФ, Программы 1С, 1С:Фреш, 1С:Документооборот) - '
  'HEAD страницы без путей, новый путь в блоке крошек, карточки товаров чистые.</li>'
  '<li>30.09.2026: «Фастфуд и Общепит», «Интеграция с сайтом», «Для продавцов компьютерной техники», «Последняя миля Ozon» - полностью готовы.</li>'
  '</ul></section>')

A('<div class="toc"><strong>Задачи</strong><ol><li><a href="#s1">С-5. 1С:КП: заменить HEAD страницы и блок крошек целиком</a></li>'
  '<li><a href="#s3">С-7. Проверить имя в крошках карточек «Программы 1С»</a></li>'
  '<li><a href="#pub">Опубликовать</a></li></ol></div>')

A('<section class="task" id="s1"><h2><span class="num">С-5</span> 1С:КП: заменить HEAD страницы и блок крошек целиком</h2>')
A('<span class="lbl">Что сделать</span><p>На каждой витрине два поля. Ничего в них не искать: скопировать готовый код и вставить поверх старого целиком. '
  'В HEAD страницы остаётся только то, что можно показывать и карточкам товаров. Путь для поисковика и описание страницы живут в блоке крошек.</p>')
A('<span class="lbl">Зачем</span><p>Сейчас поисковик видит старый путь, а гость новый. Старый путь из HEAD витрины Тильда ещё и копирует на все карточки товаров. '
  'После замены у витрины один верный путь, как на экране, а карточки перестанут выдавать себя за витрину.</p>')
A('<div class="callout warn"><strong>Как вставлять.</strong> В поле: Ctrl+A → Delete → вставить скопированное → «Сохранить». '
  'Перед этим скопируйте старое содержимое поля в блокнот, чтобы можно было откатить. HEAD сайта (Настройки сайта → Вставка кода) не трогать.</div>')
A('<span class="lbl">Как в Тильде</span>')
for path in HEAD8:
    slug = path.lstrip("/")
    f = F[slug]
    parents, name = LOST[path]
    head_new, webpage = split_head(f["page_head"])
    t123_new = f["t123"].strip() + "\n" + (webpage + "\n" if webpage else "") + A_ld(slug, parents, name)
    A(f'<h3>{esc(B.LIVE[path].get("h1", "") or name)}</h3>')
    A(f'<p class="muted"><a href="https://alsn.ru{path}">https://alsn.ru{path}</a> · адрес в Тильде <code>{slug}</code> · '
      f'путь для поисковика станет «Главная / {" / ".join(n for n, _ in parents + [(name, "")])}»</p>')
    A(f'<p><strong>Поле 1. HEAD страницы.</strong></p><ol class="steps"><li>{B.HEAD_PATH} (<code>{slug}</code>).</li>')
    if head_new:
        A('<li>Ctrl+A → Delete → вставить код ниже → <strong>Сохранить изменения</strong>.</li></ol>')
        A('<p class="cap put">HEAD страницы целиком</p>' + copybox(head_new, "p"))
    else:
        A('<li>Ctrl+A → Delete. Поле остаётся <strong>пустым</strong>, вставлять ничего не нужно: всё, что там было, переезжает в блок крошек. '
          '<strong>Сохранить изменения</strong>.</li></ol>')
    A(f'<p><strong>Поле 2. Блок крошек</strong> (самый верх холста, сразу под меню, T123 <code>rec{f["rec"]}</code>).</p>'
      f'<ol class="steps"><li>Список страниц → <code>{slug}</code> → <strong>Редактировать</strong> → блок крошек → <strong>Контент</strong>.</li>'
      '<li>Ctrl+A → Delete → вставить код ниже → <strong>Сохранить и закрыть</strong>.</li></ol>')
    A('<p class="cap put">Блок крошек целиком</p>' + copybox(t123_new, "p"))
A('</section>')

A('<section class="task" id="s3"><h2><span class="num">С-7</span> Проверить имя в крошках карточек «Программы 1С»</h2>')
A('<span class="lbl">Что сделать</span><p>Посмотреть, какое имя витрины стоит в крошках карточек товаров на <code>/products</code>. Нужно «Программы 1С», как на самой витрине.</p>')
A('<span class="lbl">Зачем</span><p>На витрине уже «Программы 1С». Если на карточке осталось «Продукты», гость увидит два разных имени одной страницы.</p>')
A('<span class="lbl">Как в Тильде</span><ol class="steps"><li>Список страниц → <code>products</code> → <strong>Редактировать</strong>.</li>'
  '<li>Клик по блоку каталога → <strong>Контент</strong> → вкладка «Хлебные крошки».</li>'
  '<li>Если там вручную написано «Продукты» - заменить на «Программы 1С» и <strong>Сохранить</strong>. Если имя берётся само и поля нет - ничего не делать, пункт закрыт.</li></ol>')
A('</section>')

pub = ", ".join(f"<code>{p.lstrip('/')}</code>" for p in HEAD8)
A('<section class="task" id="pub"><h2><span class="num">P</span> Опубликовать</h2><ol class="steps">'
  f'<li>После «да» по задаче нажать <strong>«Опубликовать»</strong> на каждой затронутой странице: {pub}.</li>'
  '<li>«Опубликовать все страницы» не нужно: HEAD сайта не меняли.</li></ol></section>')

A('<section class="task" id="wait"><h2>Ждут новых страниц - сейчас не трогать</h2><p>Звенья «Услуги», «Продукты», «Лицензии», «Разработка и доработка 1С» '
  'добавим отдельной волной после выхода <code>/uslugi</code>, <code>/produkty</code>, <code>/licenzii</code>, <code>/dorabotka-1c</code>. '
  'Пока их нет, в крошки не вставлять: ссылка вела бы на 404.</p></section>')

A('<p class="muted">Файл: <code>seo-data/tilda-briefs/tier2-breadcrumbs-struktura-2026-09-30.html</code> · сборщик: <code>seo-data/scripts/build_bc_struktura_rest_0930.py</code> · '
  'сверка: <code>seo-data/scripts/_bc_struct_verify_0930.py</code></p>')
A('  </div>\n  ' + B.SCRIPT + '\n</body>\n</html>\n')

text = "\n".join(parts).replace("\u2014", "-").replace("\u2013", "-")
B.OUT.write_text(text, encoding="utf-8")
print(B.OUT, len(text))
