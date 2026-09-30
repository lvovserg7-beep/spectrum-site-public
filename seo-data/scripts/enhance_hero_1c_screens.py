# -*- coding: utf-8 -*-
"""Делает интерфейсы 1С в баннере чёткими.

Сотрудник и склад остаются пикселями исходного баннера.
На мониторы накладываются заново отрисованные формы 1С с логотипом Аллсан
в панели подсистем.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "brand-images" / "allsun-hero-mp-warehouse-1c-real.png"
LOGO = ROOT / "logo" / "Аллсан_9.png"
OUT = ROOT / "brand-images"
FONTS = Path(r"C:\Windows\Fonts")

INK = "#252525"
MUTED = "#686868"
LINE = "#d1d1c3"
TOP = "#f4e78c"
NAV = "#f6e88a"
HEAD = "#ebe7c7"
ROW = "#fffef4"
GROUP = "#eeeacb"
ORANGE = "#f55823"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / name), size)


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, size: int) -> str:
    value = text
    face = font(size)
    while value and draw.textlength(value, font=face) > max_width:
        value = value[:-1]
    return value if value == text else value.rstrip() + "…"


def paste_brand_mark(window: Image.Image, x: int, y: int, size: int) -> None:
    mark = Image.open(LOGO).convert("RGBA")
    mark.thumbnail((size, size), Image.Resampling.LANCZOS)
    window.alpha_composite(mark, (x + (size - mark.width) // 2, y))


def draw_shell(window: Image.Image, title: str) -> tuple[ImageDraw.ImageDraw, int, int]:
    draw = ImageDraw.Draw(window)
    w, _ = window.size
    draw.rectangle((0, 0, w, 24), fill=TOP)
    draw.text((8, 5), "1С:Предприятие", font=font(11, True), fill=INK)
    draw.text((w - 54, 5), "−  □  ×", font=font(11), fill=MUTED)

    draw.rectangle((0, 24, w, 50), fill="#faf8e8")
    draw.text((12, 31), "Главное", font=font(11), fill=MUTED)
    draw.text((78, 31), title, font=font(11, True), fill=INK)

    nav_w = max(72, round(w * 0.16))
    draw.rectangle((0, 50, nav_w, window.height), fill=NAV)
    paste_brand_mark(window, 10, 62, 25)
    draw.text((39, 67), "Аллсан МП", font=font(10, True), fill=INK)

    items = ("Главное", "Продажи", "Закупки", "Ozon", "Wildberries", "Отзывы")
    y = 103
    for index, item in enumerate(items):
        if item in ("Ozon", "Wildberries"):
            draw.rounded_rectangle((8, y - 2, nav_w - 6, y + 19), radius=4, fill="#fde7de")
        draw.ellipse((10, y + 3, 16, y + 9), fill=ORANGE if index >= 3 else "#7e7e72")
        draw.text((21, y), item, font=font(9, index >= 3), fill=INK)
        y += 27

    content_x = nav_w + 10
    draw.text((content_x, 60), title, font=font(18, True), fill=INK)
    draw.rectangle((content_x, 88, content_x + 82, 116), fill="#f4d724", outline="#c2a900")
    draw.text((content_x + 9, 95), "Сформировать", font=font(9, True), fill=INK)
    draw.rectangle((content_x + 92, 88, w - 10, 116), fill="#ffffff", outline=LINE)
    draw.text((content_x + 101, 95), "Период: 01.09.2026 - 15.09.2026", font=font(9), fill=MUTED)
    return draw, content_x, 126


def draw_table(
    window: Image.Image,
    title: str,
    headers: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
    widths: tuple[float, ...],
    emphasize_last: bool = True,
) -> Image.Image:
    draw, x, y = draw_shell(window, title)
    available = window.width - x - 10
    column_widths = [round(available * share) for share in widths]
    column_widths[-1] += available - sum(column_widths)
    row_h = max(24, round((window.height - y - 10) / (len(rows) + 1)))

    cx = x
    for header, width in zip(headers, column_widths):
        draw.rectangle((cx, y, cx + width, y + row_h), fill=HEAD, outline=LINE)
        draw.text(
            (cx + 5, y + 7),
            fit_text(draw, header, width - 10, 9),
            font=font(9, True),
            fill=INK,
        )
        cx += width

    y += row_h
    for index, row in enumerate(rows):
        fill = GROUP if index == len(rows) - 1 and emphasize_last else ROW
        cx = x
        for cell, width in zip(row, column_widths):
            draw.rectangle((cx, y, cx + width, y + row_h), fill=fill, outline=LINE)
            color = ORANGE if index == len(rows) - 1 and cx > x else INK
            draw.text(
                (cx + 5, y + 7),
                fit_text(draw, cell, width - 10, 9),
                font=font(9, index == len(rows) - 1),
                fill=color,
            )
            cx += width
        y += row_h
    return window


def cost_window(size: tuple[int, int]) -> Image.Image:
    window = Image.new("RGBA", size, "#fffef4")
    return draw_table(
        window,
        "Расчёт себестоимости",
        ("Категория", "Кол.", "Выручка", "Себест.", "Комиссия", "Логистика", "Прибыль"),
        (
            ("Бытовая химия", "248", "614 820", "327 540", "92 220", "41 860", "153 200"),
            ("Канцелярия", "179", "438 610", "231 870", "65 790", "30 210", "110 740"),
            ("Товары для дома", "316", "792 450", "428 630", "118 870", "48 970", "195 980"),
            ("Мисты", "142", "356 920", "184 110", "53 540", "24 880", "94 390"),
            ("Итого", "885", "2 202 800", "1 172 150", "330 420", "145 920", "554 310"),
        ),
        (0.25, 0.08, 0.15, 0.14, 0.13, 0.13, 0.12),
    )


def drr_window(size: tuple[int, int]) -> Image.Image:
    window = Image.new("RGBA", size, "#fffef4")
    return draw_table(
        window,
        "Расчёт доли рекламных расходов",
        ("Товарная группа", "Выручка", "Реклама", "ДРР"),
        (
            ("Бытовая химия", "684 920 ₽", "54 380 ₽", "7,9 %"),
            ("Канцелярия", "536 410 ₽", "42 760 ₽", "8,0 %"),
            ("Товары для дома", "721 330 ₽", "56 940 ₽", "7,9 %"),
            ("Мисты", "412 870 ₽", "34 610 ₽", "8,4 %"),
            ("Итого", "2 355 530 ₽", "188 690 ₽", "8,0 %"),
        ),
        (0.38, 0.24, 0.22, 0.16),
    )


def reviews_window(size: tuple[int, int]) -> Image.Image:
    window = Image.new("RGBA", size, "#fffef4")
    return draw_table(
        window,
        "Работа с отзывами",
        ("Товар", "Оценка", "Ответ ИИ", "Статус"),
        (
            ("Товар A", "5", "Подготовлен", "Готов"),
            ("Товар B", "4", "Подготовлен", "Проверка"),
            ("Товар C", "5", "Подготовлен", "Готов"),
            ("Товар D", "3", "Подготовлен", "Проверка"),
            ("Итого", "17", "4 ответа", "2 готовы"),
        ),
        (0.36, 0.14, 0.30, 0.20),
        False,
    )


def preserve_employee(result: Image.Image, source: Image.Image) -> None:
    """Возвращает исходные пиксели сотрудника поверх правого монитора."""
    mask = Image.new("L", source.size, 0)
    draw = ImageDraw.Draw(mask)
    polygon = (
        (1410, 92),
        (1495, 90),
        (1542, 125),
        (1555, 205),
        (1525, 265),
        (1555, 315),
        (1590, 390),
        (1595, 525),
        (1645, 605),
        (1630, 790),
        (1555, 866),
        (1410, 865),
        (1350, 785),
        (1370, 650),
        (1360, 540),
        (1380, 445),
        (1368, 345),
        (1398, 270),
        (1392, 180),
    )
    draw.polygon(polygon, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    result.paste(source, (0, 0), mask)


def main() -> None:
    base = Image.open(SOURCE).convert("RGBA")
    if base.size != (1920, 900):
        raise ValueError(f"Ожидался баннер 1920x900, получен {base.size}")
    result = base.copy()

    placements = (
        (cost_window((553, 433)), (64, 94)),
        (drr_window((470, 433)), (647, 92)),
        (reviews_window((362, 416)), (1153, 109)),
    )
    for window, position in placements:
        result.alpha_composite(window, position)

    preserve_employee(result, base)

    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / "allsun-hero-mp-warehouse-1c-sharp.png"
    jpg = OUT / "allsun-hero-mp-warehouse-1c-sharp.jpg"
    result.convert("RGB").save(png, "PNG", optimize=True)
    result.convert("RGB").save(jpg, "JPEG", quality=94)
    print(png)
    print(jpg)


if __name__ == "__main__":
    main()
