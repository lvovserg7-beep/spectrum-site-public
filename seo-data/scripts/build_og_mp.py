# -*- coding: utf-8 -*-
"""OG 1200×630 для https://alsn.ru/1c-ozon и https://alsn.ru/1c-wildberries.

Весь текст — в центральном квадрате 630×630: Telegram кропает середину
превью и иначе режет заголовок пополам. Марки площадок только текстом.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "brand-images"
LOGO = ROOT / "logo" / "Аллсан_6.png"
FONTS = Path(r"C:\Windows\Fonts")

W, H = 1200, 630
SAFE = 630
BG = "#F7F8FA"
PAPER = "#FFFFFF"
GRAPHITE = "#212121"
MUTED = "#64686C"
LINE = "#D7DADD"
ORANGE = "#F55823"

VARIANTS = (
    {
        "slug": "ozon",
        "kicker": "МОДУЛЬ ДЛЯ СЕЛЛЕРОВ",
        "title": "Ozon в вашей 1С",
        "subtitle": "остатки и заказы",
        "facts": "цены · FBS · юнит-экономика",
        "chip": "1С  →  Ozon  →  1С",
    },
    {
        "slug": "wildberries",
        "kicker": "МОДУЛЬ ДЛЯ СЕЛЛЕРОВ",
        "title": "Wildberries в 1С",
        "subtitle": "остатки и заказы",
        "facts": "цены · поставки · маржа",
        "chip": "1С  →  Wildberries  →  1С",
    },
)


def face(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / filename), size)


def centered(draw, y, text, size, color, bold=False) -> float:
    font = face(size, bold)
    width = draw.textlength(text, font=font)
    draw.text(((W - width) / 2, y), text, font=font, fill=color)
    return width


def build(variant: dict) -> None:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((150, 64), Image.Resampling.LANCZOS)
    image.paste(logo, ((W - logo.width) // 2, 56), logo)

    centered(draw, 148, variant["kicker"], 18, ORANGE, True)

    title_size = 68
    while draw.textlength(variant["title"], font=face(title_size, True)) > 540:
        title_size -= 2
    centered(draw, 196, variant["title"], title_size, GRAPHITE, True)
    centered(draw, 286, variant["subtitle"], 36, GRAPHITE, True)
    centered(draw, 348, variant["facts"], 26, MUTED)

    rail_w = 280
    rail_x = (W - rail_w) // 2
    for offset, length, color in (
        (0, rail_w, LINE),
        (16, int(rail_w * 0.72), ORANGE),
        (32, int(rail_w * 0.88), LINE),
    ):
        draw.rounded_rectangle(
            (rail_x, 412 + offset, rail_x + length, 417 + offset),
            radius=3,
            fill=color,
        )

    chip_font = face(22, True)
    chip_w = int(draw.textlength(variant["chip"], font=chip_font))
    pad_x, pad_y = 28, 16
    box = (
        (W - chip_w) // 2 - pad_x,
        492,
        (W + chip_w) // 2 + pad_x,
        492 + 22 + pad_y * 2,
    )
    draw.rounded_rectangle(box, radius=16, fill=GRAPHITE)
    draw.text(
        (box[0] + pad_x, box[1] + pad_y - 2),
        variant["chip"],
        font=chip_font,
        fill=PAPER,
    )

    # Боковые поля — воздух, не текст: их Telegram обрежет.
    draw.line((48, 314, 250, 314), fill=LINE, width=2)
    draw.line((950, 314, 1152, 314), fill=LINE, width=2)

    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"allsun-og-mp-{variant['slug']}.png"
    jpg = OUT / f"allsun-og-mp-{variant['slug']}.jpg"
    image.save(png, "PNG", optimize=True)
    image.save(jpg, "JPEG", quality=86, optimize=True)

    left = (W - SAFE) // 2
    crop_path = OUT / f"_og-mp-{variant['slug']}-telegram-crop.png"
    image.crop((left, 0, left + SAFE, H)).save(crop_path, "PNG")
    print(jpg, jpg.stat().st_size)
    print(crop_path)


def main() -> None:
    for variant in VARIANTS:
        build(variant)


if __name__ == "__main__":
    main()
