---
name: allsun-brand-images
description: ALLSUN / Аллсан brand system «Контур управления» for site visuals, banners, OG, cases, icons and 16:9 slides. Use before every GenerateImage call and whenever producing branded visual assets.
---

# Изображения в стиле Аллсан

Источник: ТЗ дизайна главной
(`Предложеная структура/TZ-dizajn-glavnoj-ALLSUN-2026-09-02.txt`, §3–5),
опросники сотрудников, визуальная проверка конкурентов 11.09.2026, PNG в
`seo-data/logo/`.

На живой alsn.ru и в Битрикс не публиковать без отдельной задачи.

## Концепция «Контур управления»

Аллсан связывает данные, учёт и действия бизнеса в один управляемый маршрут.
Каждый сюжет строится по формуле:

**входные данные → модуль / команда Аллсан → измеримый результат**.

Визуальные признаки:

- светлое поле `#F7F8FA`, крупная типографика, много воздуха;
- прямоугольные карточки маршрута вместо круглых универсальных иконок;
- три горизонтальные линии как рифма со знаком, но не второй логотип;
- тонкие серые связи и оранжевые стрелки;
- графитовая карточка только в точке результата / контраста;
- один экран — одна задача — один результат;
- реальные интерфейсы, отзывы, документы и люди как доказательства.

Эталон: `seo-data/brand-images/allsun-brand-board-2026.png`.

## Палитра (с логотипа, 11.09.2026)

| Роль | HEX |
|---|---|
| Фон слайда | `#F7F8FA` |
| Акцент | `#F55823` |
| Графит / текст | `#212121` |
| Линии схемы | `#D7DADD` |
| Мягкий оранжевый фон | `#FDE7DE` |
| Белый | `#FFFFFF` |

Оранжевый — стрелки, маркеры, CTA. Не основной фон.

## Как делать кадр

| Задача | Как |
|---|---|
| Hero сайта | Логотип остаётся в шапке; в hero — оффер слева, маршрут решения справа, строка доказательств снизу. |
| Баннер / презентация 16:9 | Полный логотип допустим в верхней полосе; один маршрут и короткий оффер. |
| OG / превью Telegram | Холст 1200×630; логотип и текст только в центральном квадрате 630×630. Не слайд 16:9. |
| Иконка 1:1 без текста | `GenerateImage`: плоская метафора, графит + оранжевый штрих, без логотипа. |
| Кейс | Три шага: задача → решение → результат; ниже реальный скрин / отзыв / фотография. |

Люди: не генерировать. Реальные фото — с alsn.ru (`/vacancy`, «о компании»).

## Референсы

- Светлый логотип в макет: `seo-data/logo/Аллсан_6.png`.
- Только знак (якорь цвета / геометрии для GenerateImage): `seo-data/logo/Аллсан_9.png`.
- Светлый якорь с белым словом (на тёмный фон, не на слайд): `seo-data/logo/Аллсан_1.png`.
- Эталон системы: `seo-data/brand-images/allsun-brand-board-2026.png`.
- Первый понравившийся слайд: `seo-data/brand-images/allsun-tpl-reference-mp.png`.

Знак и словомарк нейросетью **не** генерировать.

## GenerateImage (только фон или иконка)

Промпт на английском:

```
corporate B2B process architecture, off-white #F7F8FA, generous negative space,
flat orthogonal data routes, rectangular process cards, three horizontal rails,
graphite #212121 structure, orange #F55823 used only as signal arrows,
one business problem and one measurable outcome, no logos, no text
```

Negative:

```
photorealistic office people, handshake, call center, neon cyberpunk,
purple/blue sci-fi glow, colorful 3D objects, glossy logos, blue 1C competitor
palette, readable text, Cyrillic lettering, ALLSUN wordmark, distorted logo,
watermark, busy catalog, carousel, ecommerce badges, dark full-bleed background
```

`reference_image_paths`: `seo-data/logo/Аллсан_9.png`. Не просить модель собрать готовый баннер с логотипом и Ozon/WB.

## Готовые шаблоны концепции

Скрипт: `python seo-data/scripts/build_brand_concept.py`

- бренд-доска: `seo-data/brand-images/allsun-brand-board-2026.png`
- МП: `seo-data/brand-images/allsun-concept-hero-mp.png`
- B2B-телеком: `seo-data/brand-images/allsun-concept-hero-b2b.png`
- услуги: `seo-data/brand-images/allsun-concept-hero-services.png`
- кейс: `seo-data/brand-images/allsun-concept-case.png`

## Ранние слайд-шаблоны

Скрипт: `python seo-data/scripts/build_brand_templates.py`

- МП: `seo-data/brand-images/allsun-tpl-mp.png`
- B2B телеком: `seo-data/brand-images/allsun-tpl-b2b.png`
- Услуги: `seo-data/brand-images/allsun-tpl-services.png`
- Лицензии (слайд 16:9): `seo-data/brand-images/allsun-tpl-licenses-16x9.png`
- Лицензии OG / Telegram: `seo-data/brand-images/allsun-og-licenses.png` (`python seo-data/scripts/build_og_licenses.py`)

HTML-макеты тех же четырёх слайдов: `seo-data/brand-images/templates.html`.

Иконка (не слайд): `seo-data/brand-images/allsun-icon-exchange.png`.

Тёмные абстрактные hero/кейс из первой пробы — не эталон баннера.

## Что взято у референсов — без копирования

- Рарус: структура продуктов, крупные карточки и воздух; не синяя палитра и не карусель.
- Гэндальф: вход по задачам и статусам; не тёмный перегруженный hero.
- WiseAdvice: кейс как проблема → решение → цифра; не декоративная 3D-абстракция.
- КОРУС: уверенная типографика и ощущение сильного партнёра.
- 1С-АБ: FAQ и конкретные пакеты; не длинные полотна текста.
- Айтекс: логика витрины; не пёстрый магазин и бейджи «Хит».
- Кодерлайн: цифры и проекты; не типовой дизайн франчайзи.

## Чеклист брака

Переделать, если:

- логотип кривой или нарисован моделью;
- на слайде кириллица «рассыпалась»;
- оранжевый залил фон;
- лица / стоковый офис / неон;
- синий стал главным фирменным цветом;
- продукт спрятан в карусель или растворился в каталоге;
- чипы обрезаны краем кадра;
- OG для Telegram собран как слайд 16:9 (логотип слева, текст справа).

Один переген фона; готовый слайд чинить в скрипте, не новой нейрокартинкой.
