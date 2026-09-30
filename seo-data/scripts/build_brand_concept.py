# -*- coding: utf-8 -*-
"""Фирменная концепция Аллсан «Контур управления».

Собирает бренд-доску и четыре демонстрационных макета 16:9.
Логотип берётся из проекта и не перерисовывается.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "brand-images"
LOGO = ROOT / "logo" / "Аллсан_6.png"
FONTS = Path(r"C:\Windows\Fonts")

W, H = 1920, 1080
BG = "#F7F8FA"
PAPER = "#FFFFFF"
GRAPHITE = "#212121"
MUTED = "#64686C"
LINE = "#D7DADD"
SOFT = "#ECEEF0"
ORANGE = "#F55823"
ORANGE_SOFT = "#FDE7DE"


def face(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / filename), size)


def canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), BG)
    return image, ImageDraw.Draw(image)


def paste_logo(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    logo = Image.open(LOGO).convert("RGBA")
    max_w, max_h = box[2] - box[0], box[3] - box[1]
    logo.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    x = box[0] + (max_w - logo.width) // 2
    y = box[1] + (max_h - logo.height) // 2
    image.paste(logo, (x, y), logo)


def line_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    size: int,
    color: str = GRAPHITE,
    bold: bool = False,
) -> None:
    draw.text(xy, text, font=face(size, bold), fill=color)


def wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    lines: Iterable[str],
    size: int,
    color: str = GRAPHITE,
    bold: bool = False,
    leading: int | None = None,
) -> None:
    step = leading or int(size * 1.18)
    x, y = xy
    for index, line in enumerate(lines):
        line_text(draw, (x, y + step * index), line, size, color, bold)


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str,
    radius: int = 24,
    outline: str | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str = ORANGE,
    width: int = 5,
) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2 - 18, y2), fill=color, width=width)
    draw.polygon(
        [(x2, y2), (x2 - 22, y2 - 12), (x2 - 22, y2 + 12)], fill=color
    )


def signal_rail(
    draw: ImageDraw.ImageDraw, x: int, y: int, width: int = 330
) -> None:
    """Три линии — рифма с фирменным знаком, но не второй логотип."""
    for offset, length in ((0, width), (28, int(width * 0.76)), (56, int(width * 0.9))):
        draw.rounded_rectangle(
            (x, y + offset, x + length, y + offset + 8),
            radius=4,
            fill=ORANGE if offset == 28 else LINE,
        )


def label(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    orange: bool = False,
) -> int:
    font = face(24, orange)
    text_w = int(draw.textlength(text, font=font))
    rounded(
        draw,
        (x, y, x + text_w + 42, y + 54),
        ORANGE_SOFT if orange else PAPER,
        14,
        None if orange else LINE,
        2,
    )
    draw.text((x + 21, y + 11), text, font=font, fill=ORANGE if orange else GRAPHITE)
    return x + text_w + 42


def top_brand(image: Image.Image, draw: ImageDraw.ImageDraw, section: str) -> None:
    paste_logo(image, (72, 52, 250, 200))
    line_text(draw, (284, 76), section.upper(), 20, ORANGE, True)
    line_text(draw, (284, 112), "АРХИТЕКТУРА ПОТОКОВ", 18, MUTED)
    draw.line((72, 218, 1848, 218), fill=LINE, width=2)


def proof_row(draw: ImageDraw.ImageDraw, y: int) -> None:
    items = (("600+", "клиентов"), ("с 2015", "автоматизируем"), ("15 мин", "реакция"), ("ТОП 10", "ЦРА"))
    x = 72
    for value, caption in items:
        line_text(draw, (x, y), value, 30, GRAPHITE, True)
        line_text(draw, (x, y + 42), caption, 18, MUTED)
        x += 238


def process_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    kicker: str,
    title: str,
    detail: str,
    accent: bool = False,
) -> None:
    fill = GRAPHITE if accent else PAPER
    title_color = PAPER if accent else GRAPHITE
    muted_color = "#C9CDD0" if accent else MUTED
    rounded(draw, box, fill, 26, None if accent else LINE, 2)
    x1, y1, _, _ = box
    line_text(draw, (x1 + 28, y1 + 24), kicker.upper(), 16, ORANGE, True)
    line_text(draw, (x1 + 28, y1 + 58), title, 27, title_color, True)
    line_text(draw, (x1 + 28, y1 + 102), detail, 18, muted_color)


def save(image: Image.Image, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    image.save(path, "PNG", optimize=True)
    print(path)
    return path


def brand_board() -> Image.Image:
    image, draw = canvas()
    top_brand(image, draw, "Фирменная система 2026")

    line_text(draw, (72, 264), "Контур управления", 64, GRAPHITE, True)
    wrapped(
        draw,
        (72, 348),
        (
            "Аллсан связывает данные, учёт и действия бизнеса",
            "в один понятный управляемый маршрут.",
        ),
        28,
        MUTED,
        False,
        40,
    )
    signal_rail(draw, 72, 458, 430)

    # Palette
    line_text(draw, (72, 580), "ПАЛИТРА", 18, MUTED, True)
    swatches = (
        (GRAPHITE, "Структура", "#212121"),
        (ORANGE, "Сигнал", "#F55823"),
        (PAPER, "Ясность", "#FFFFFF"),
        (SOFT, "Контур", "#ECEEF0"),
    )
    x = 72
    for color, name, code in swatches:
        rounded(draw, (x, 624, x + 150, 714), color, 18, LINE if color == PAPER else None, 2)
        line_text(draw, (x, 734), name, 18, GRAPHITE, True)
        line_text(draw, (x, 762), code, 16, MUTED)
        x += 180

    # Visual language and product map
    rounded(draw, (790, 264, 1848, 826), PAPER, 32, LINE, 2)
    line_text(draw, (838, 306), "Язык бренда: маршрут данных", 34, GRAPHITE, True)
    line_text(
        draw,
        (838, 354),
        "Один экран — одна бизнес-задача — один измеримый результат",
        22,
        MUTED,
    )

    process_card(draw, (838, 430, 1100, 574), "Вход", "Данные", "ЛК · API · 1С")
    process_card(
        draw, (1184, 430, 1476, 574), "Обработка", "Аллсан", "модули · аналитика", True
    )
    process_card(draw, (1560, 430, 1800, 574), "Выход", "Результат", "контроль · прибыль")
    arrow(draw, (1104, 502), (1170, 502))
    arrow(draw, (1480, 502), (1546, 502))

    line_text(draw, (838, 638), "ШЕСТЬ НАПРАВЛЕНИЙ", 18, MUTED, True)
    x, y = 838, 682
    for index, item in enumerate(
        ("Внедрение", "Доработка", "Поддержка", "Маркетплейсы", "B2B-телеком", "Лицензии")
    ):
        x = label(draw, x, y, item, index in (3, 4))
        if x > 1680 and index < 5:
            x, y = 838, y + 72
        else:
            x += 12

    draw.line((72, 888, 1848, 888), fill=LINE, width=2)
    line_text(draw, (72, 924), "НЕ КОПИРУЕМ", 17, MUTED, True)
    line_text(draw, (72, 960), "чужую палитру · каталожный шум · стоковый офис", 23, GRAPHITE)
    line_text(draw, (1000, 924), "СОХРАНЯЕМ", 17, ORANGE, True)
    line_text(draw, (1000, 960), "живой логотип · реальные интерфейсы · реальные люди", 23, GRAPHITE)
    return image


def hero(
    section: str,
    kicker: str,
    title: tuple[str, ...],
    subtitle: tuple[str, ...],
    nodes: tuple[tuple[str, str, str], ...],
    proof: str,
) -> Image.Image:
    image, draw = canvas()
    top_brand(image, draw, section)

    line_text(draw, (72, 286), kicker.upper(), 18, ORANGE, True)
    wrapped(draw, (72, 328), title, 58, GRAPHITE, True, 70)
    wrapped(draw, (72, 500), subtitle, 25, MUTED, False, 36)
    x = label(draw, 72, 614, "Смотреть решение", True)
    label(draw, x + 14, 614, proof)
    proof_row(draw, 866)

    # Process architecture
    right_x = 1030
    line_text(draw, (right_x, 286), "КОНТУР РЕШЕНИЯ", 17, MUTED, True)
    signal_rail(draw, right_x, 326, 520)
    y = 438
    for index, (node_kicker, node_title, node_detail) in enumerate(nodes):
        box = (right_x, y, 1780, y + 128)
        process_card(
            draw,
            box,
            node_kicker,
            node_title,
            node_detail,
            accent=index == len(nodes) - 1,
        )
        if index < len(nodes) - 1:
            arrow(draw, (1405, y + 132), (1405, y + 160), ORANGE, 4)
        y += 160
    return image


def case_template() -> Image.Image:
    image, draw = canvas()
    top_brand(image, draw, "Кейс")
    line_text(draw, (72, 274), "Задача → решение → результат", 54, GRAPHITE, True)
    line_text(
        draw,
        (72, 350),
        "Кейс читается как управленческая история, а не как галерея логотипов.",
        25,
        MUTED,
    )
    cards = (
        ("01 · ЗАДАЧА", "Ручной обмен", "Ошибки в остатках и заказах"),
        ("02 · РЕШЕНИЕ", "Единый контур 1С", "Автоматический обмен и контроль"),
        ("03 · РЕЗУЛЬТАТ", "Меньше потерь", "Цифра результата — крупно"),
    )
    x = 72
    for index, (kicker, title, detail) in enumerate(cards):
        process_card(draw, (x, 460, x + 520, 670), kicker, title, detail, index == 2)
        if index < 2:
            arrow(draw, (x + 526, 566), (x + 574, 566))
        x += 620
    rounded(draw, (72, 760, 1848, 974), PAPER, 28, LINE, 2)
    line_text(draw, (110, 802), "РЕАЛЬНОЕ ДОКАЗАТЕЛЬСТВО", 17, ORANGE, True)
    line_text(
        draw,
        (110, 844),
        "Скрин интерфейса · отзыв с исходящим номером · фото команды · факт 600+",
        29,
        GRAPHITE,
        True,
    )
    line_text(
        draw,
        (110, 900),
        "Никаких сгенерированных людей и декоративных «серверов».",
        22,
        MUTED,
    )
    return image


def main() -> None:
    save(brand_board(), "allsun-brand-board-2026.png")
    save(
        hero(
            "Готовая интеграция",
            "1С × Ozon × Wildberries",
            ("Прозрачная", "юнит-экономика"),
            ("Остатки, заказы и финансовые документы", "маркетплейсов — в вашей 1С."),
            (
                ("Вход", "Заказы и остатки", "Ozon · Wildberries"),
                ("Контроль", "Модуль Аллсан", "синхронизация · аналитика"),
                ("Результат", "Прибыль видна", "меньше ошибок и штрафов"),
            ),
            "свои модули",
        ),
        "allsun-concept-hero-mp.png",
    )
    save(
        hero(
            "Готовая интеграция",
            "B2B · ТЕЛЕКОМ И IT",
            ("Поставщики —", "в вашей 1С"),
            ("Цены, остатки, резерв и заказы", "из личных кабинетов и API."),
            (
                ("Поставщики", "ЛК и API", "телеком · IT-железо"),
                ("Обмен", "Модуль Аллсан", "сопоставление · резерв"),
                ("Результат", "Закупки быстрее", "актуальные цены и остатки"),
            ),
            "телеком и IT",
        ),
        "allsun-concept-hero-b2b.png",
    )
    save(
        hero(
            "Услуги",
            "ВНЕДРЕНИЕ · ДОРАБОТКА · SLA",
            ("1С под ваши", "процессы"),
            ("Проектируем, запускаем и сопровождаем", "единый контур учёта."),
            (
                ("Старт", "Обследование", "процессы · цели · система"),
                ("Проект", "Настройка и запуск", "УТ · КА · ERP"),
                ("Поддержка", "Команда рядом", "реакция от 15 минут"),
            ),
            "торговля и производство",
        ),
        "allsun-concept-hero-services.png",
    )
    save(case_template(), "allsun-concept-case.png")


if __name__ == "__main__":
    main()
