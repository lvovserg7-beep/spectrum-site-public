# -*- coding: utf-8 -*-
"""Баннер 1: маркетплейсы и прозрачная юнит-экономика.

Использует только реальные материалы пользователя:
- склад как фон;
- фотографию сотрудника без изменения лица;
- три интерфейса 1С как основу компактных карточек.

Числа исходных отчётов не переносятся: в карточках стоят демо-значения.
Текст заголовка и CTA не запекаются в изображение, потому что их выводит
баннер Аспро. Слева оставляется безопасное светлое поле.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "brand-images"
ASSETS = Path(
    r"C:\Users\ALSN_LSA\.cursor\projects"
    r"\c-Users-ALSN-LSA-Desktop-cursor\assets"
)

PRESENTER = ASSETS / (
    "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    "9f3c600fb9460aaba34cb8d3eca23f12_images_"
    "image-dc644b38-d9da-458c-9d9a-25ed8aef3989.png"
)
WAREHOUSE = ASSETS / (
    "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    "9f3c600fb9460aaba34cb8d3eca23f12_images_"
    "image-34a1e199-3aa9-4c52-94b5-9e425097c0c5.jpg"
)
REPORT = ASSETS / (
    "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    "9f3c600fb9460aaba34cb8d3eca23f12_images_"
    "image-da892699-a2cc-43f6-affb-42c340ebf024.png"
)
DRR_REPORT = ASSETS / (
    "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    "9f3c600fb9460aaba34cb8d3eca23f12_images_"
    "image-c867e758-976a-44d7-8d18-0b236e73480e.png"
)
REVIEWS_FORM = ASSETS / (
    "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    "9f3c600fb9460aaba34cb8d3eca23f12_images_"
    "image-afc0b8c5-985a-4d8e-b8e7-ffb460d1c393.png"
)
FONTS = Path(r"C:\Windows\Fonts")

W, H = 1920, 900
BG = (247, 248, 250)
GRAPHITE = (33, 33, 33)
MUTED = (91, 95, 99)
LINE = (215, 218, 221)
ORANGE = (245, 88, 35)
ORANGE_SOFT = (253, 231, 222)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / name), size)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Масштабирует с заполнением и центральным кропом."""
    target_w, target_h = size
    ratio = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * ratio), round(image.height * ratio)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def extract_presenter() -> Image.Image:
    """Отделяет фигуру от фона без генерации и ретуши лица."""
    source = cv2.imread(str(PRESENTER), cv2.IMREAD_COLOR)
    if source is None:
        raise FileNotFoundError(PRESENTER)

    h, w = source.shape[:2]
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)
    polygon = np.array(
        [
            (283, 102),
            (376, 101),
            (414, 126),
            (427, 184),
            (413, 250),
            (443, 331),
            (493, 396),
            (538, 500),
            (557, 617),
            (548, 735),
            (519, 850),
            (505, 1023),
            (176, 1023),
            (166, 865),
            (143, 735),
            (137, 611),
            (154, 507),
            (194, 405),
            (242, 336),
            (265, 254),
            (247, 186),
            (253, 130),
        ],
        dtype=np.int32,
    )
    cv2.fillPoly(mask, [polygon], cv2.GC_PR_FGD)

    # Опорные области фигуры. Лицо остаётся пикселями исходного снимка.
    cv2.ellipse(mask, (334, 195), (67, 88), 0, 0, 360, cv2.GC_FGD, -1)
    cv2.rectangle(mask, (223, 360), (472, 780), cv2.GC_FGD, -1)
    cv2.line(mask, (195, 520), (494, 650), cv2.GC_FGD, 48)
    cv2.rectangle(mask, (205, 740), (478, 1010), cv2.GC_FGD, -1)

    background = np.zeros((1, 65), np.float64)
    foreground = np.zeros((1, 65), np.float64)
    cv2.grabCut(
        source,
        mask,
        None,
        background,
        foreground,
        8,
        cv2.GC_INIT_WITH_MASK,
    )
    alpha = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0
    ).astype("uint8")

    count, labels, stats, _ = cv2.connectedComponentsWithStats(alpha, 8)
    if count > 1:
        largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        alpha = np.where(labels == largest, 255, 0).astype("uint8")
    alpha = cv2.GaussianBlur(alpha, (0, 0), 1.0)

    rgba = cv2.cvtColor(source, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = alpha
    person = Image.fromarray(rgba)
    bbox = person.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError("Не удалось выделить человека")
    return person.crop(bbox)


def warehouse_background() -> Image.Image:
    image = Image.open(WAREHOUSE).convert("RGB")
    image = cover(image, (W, H))
    image = ImageEnhance.Color(image).enhance(0.68)
    image = ImageEnhance.Contrast(image).enhance(0.88)
    image = image.filter(ImageFilter.GaussianBlur(0.55))

    # Светлая фирменная обработка и безопасное поле под текст Аспро.
    overlay = Image.new("RGBA", (W, H), (247, 248, 250, 38))
    image = Image.alpha_composite(image.convert("RGBA"), overlay)

    gradient = Image.new("L", (W, 1))
    values = []
    for x in range(W):
        if x <= 650:
            alpha = 178
        elif x >= 1220:
            alpha = 12
        else:
            alpha = round(178 - (x - 650) * 166 / 570)
        values.append(alpha)
    gradient.putdata(values)
    gradient = gradient.resize((W, H))
    white = Image.new("RGBA", (W, H), (*BG, 255))
    image.paste(white, (0, 0), gradient)
    return image


def make_table_card(
    title: str,
    subtitle: str,
    headers: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
    widths: tuple[int, ...],
    highlight_last: bool = False,
) -> Image.Image:
    """Компактная форма 1С с читаемыми подписями и демо-данными."""
    card_w, card_h = 700, 232
    card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 244))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle(
        (0, 0, card_w - 1, card_h - 1),
        radius=22,
        fill=(255, 255, 255, 244),
        outline=LINE,
        width=2,
    )

    draw.text((22, 16), title, font=font(23, True), fill=GRAPHITE)
    draw.text(
        (22, 47),
        subtitle,
        font=font(14),
        fill=MUTED,
    )
    draw.rounded_rectangle(
        (590, 18, 678, 46), radius=14, fill=ORANGE_SOFT
    )
    draw.text((609, 24), "ДЕМО", font=font(12, True), fill=ORANGE)

    columns: list[int] = []
    x = 22
    for width in widths:
        columns.append(x)
        x += width
    header_y = 76
    for x, width, label in zip(columns, widths, headers):
        draw.rectangle(
            (x, header_y, x + width, header_y + 34),
            fill=(239, 237, 207),
        )
        draw.text((x + 9, header_y + 9), label, font=font(13, True), fill=GRAPHITE)

    y = header_y + 34
    row_h = 34
    for index, row in enumerate(rows):
        row_fill = (250, 250, 247) if index % 2 == 0 else (255, 255, 255)
        if highlight_last and index == len(rows) - 1:
            row_fill = ORANGE_SOFT
        for x, width, value in zip(columns, widths, row):
            draw.rectangle(
                (x, y, x + width, y + row_h),
                fill=row_fill,
                outline=LINE,
                width=1,
            )
            color = (
                ORANGE
                if highlight_last and index == len(rows) - 1 and x > columns[0]
                else GRAPHITE
            )
            draw.text(
                (x + 9, y + 9),
                value,
                font=font(13, highlight_last and index == len(rows) - 1),
                fill=color,
            )
        y += row_h
    return card


def make_cost_card() -> Image.Image:
    return make_table_card(
        "Расчёт себестоимости",
        "Юнит-экономика Ozon и Wildberries в 1С",
        ("Показатель", "Ozon", "Wildberries", "Итого"),
        (
            ("Выручка", "2 481 730 ₽", "1 904 260 ₽", "4 385 990 ₽"),
            ("Расходы", "1 692 180 ₽", "1 363 450 ₽", "3 055 630 ₽"),
            ("Прибыль", "789 550 ₽", "540 810 ₽", "1 330 360 ₽"),
        ),
        (218, 150, 158, 130),
        True,
    )


def make_drr_card() -> Image.Image:
    return make_table_card(
        "Расчёт доли рекламных расходов",
        "Ozon · реклама и выручка по товарным группам",
        ("Товарная группа", "Выручка", "Реклама", "ДРР"),
        (
            ("Бытовая химия", "184 920 ₽", "14 380 ₽", "7,8 %"),
            ("Канцелярия", "236 410 ₽", "18 760 ₽", "7,9 %"),
            ("Итого", "421 330 ₽", "33 140 ₽", "7,9 %"),
        ),
        (260, 152, 142, 102),
        True,
    )


def make_reviews_card() -> Image.Image:
    return make_table_card(
        "Автоответы на отзывы от ИИ",
        "Подготовка ответа с учётом товара, оценки и текста отзыва",
        ("Товар", "Оценка", "Ответ ИИ", "Статус"),
        (
            ("Товар A", "5", "Подготовлен", "Готов"),
            ("Товар B", "4", "Подготовлен", "Проверка"),
            ("Товар C", "5", "Подготовлен", "Готов"),
        ),
        (260, 92, 168, 136),
        False,
    )


def add_signal_lines(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)
    # Три линии фирменного маршрута, но не повтор логотипа.
    x, y = 790, 112
    for offset, length in ((0, 190), (22, 138), (44, 168)):
        draw.rounded_rectangle(
            (x, y + offset, x + length, y + offset + 5),
            radius=3,
            fill=ORANGE if offset == 22 else LINE,
        )
    draw.line((790, 174, 790, 246, 848, 246), fill=LINE, width=3)
    draw.polygon([(860, 246), (842, 236), (842, 256)], fill=ORANGE)


def build() -> Image.Image:
    image = warehouse_background()
    add_signal_lines(image)

    cards = (
        (make_cost_card(), (690, 66)),
        (make_drr_card(), (748, 334)),
        (make_reviews_card(), (680, 602)),
    )
    for card, (x, y) in cards:
        shadow = Image.new("RGBA", (card.width + 44, card.height + 44), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle(
            (22, 22, card.width + 21, card.height + 21),
            radius=24,
            fill=(15, 20, 25, 48),
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(15))
        image.alpha_composite(shadow, (x - 22, y - 14))
        image.alpha_composite(card, (x, y))

    # Только силуэт с нового исходного фото. Лицо не генерируется и не ретушируется.
    person = extract_presenter()
    target_h = 810
    person = person.resize(
        (round(person.width * target_h / person.height), target_h),
        Image.Resampling.LANCZOS,
    )
    alpha = person.getchannel("A")
    shadow = Image.new("RGBA", person.size, (18, 22, 26, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(13)).point(lambda p: p // 3))
    person_x = 1450
    person_y = 58
    image.alpha_composite(shadow, (person_x + 12, person_y + 12))
    image.alpha_composite(person, (person_x, person_y))

    return image


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source in (PRESENTER, WAREHOUSE, REPORT, DRR_REPORT, REVIEWS_FORM):
        if not source.exists():
            raise FileNotFoundError(source)
    result = build().convert("RGB")
    result.save(OUT / "allsun-hero-mp-unit-economics-1920x900.jpg", quality=92)
    result.save(OUT / "allsun-hero-mp-unit-economics-1920x900.png", optimize=True)
    print(OUT / "allsun-hero-mp-unit-economics-1920x900.jpg")
    print(OUT / "allsun-hero-mp-unit-economics-1920x900.png")


if __name__ == "__main__":
    main()
