# -*- coding: utf-8 -*-
"""OG 1200×630 для витрин лицензий 1С.

Весь текст — в центральном квадрате 630×630: Telegram кропает середину
превью. Слайд 16:9 allsun-tpl-licenses сюда не копировать.
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


def face(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    filename = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(FONTS / filename), size)


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, color: str, bold: bool = False) -> float:
    font = face(size, bold)
    width = draw.textlength(text, font=font)
    draw.text(((W - width) / 2, y), text, font=font, fill=color)
    return width


def chip(draw: ImageDraw.ImageDraw, x: int, y: int, label: str) -> int:
    font = face(22, True)
    tw = int(draw.textlength(label, font=font))
    pad_x, pad_y = 22, 12
    box = (x, y, x + tw + pad_x * 2, y + 22 + pad_y * 2)
    draw.rounded_rectangle(box, radius=14, fill=PAPER, outline=LINE, width=2)
    draw.text((x + pad_x, y + pad_y - 1), label, font=font, fill=GRAPHITE)
    return box[2]


def main() -> None:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((150, 64), Image.Resampling.LANCZOS)
    image.paste(logo, ((W - logo.width) // 2, 48), logo)

    centered(draw, 128, "ОФИЦИАЛЬНЫЙ ПАРТНЁР 1С", 16, ORANGE, True)
    centered(draw, 172, "Лицензии 1С", 64, GRAPHITE, True)
    centered(draw, 252, "и Битрикс24", 36, GRAPHITE, True)
    centered(draw, 318, "электронная поставка · PIN-код", 24, MUTED)

    rail_w = 280
    rail_x = (W - rail_w) // 2
    for offset, length, color in (
        (0, rail_w, LINE),
        (16, int(rail_w * 0.72), ORANGE),
        (32, int(rail_w * 0.88), LINE),
    ):
        draw.rounded_rectangle(
            (rail_x, 372 + offset, rail_x + length, 377 + offset),
            radius=3,
            fill=color,
        )

    left_chip = "1С"
    right_chip = "Битрикс24"
    gap = 52
    f_chip = face(22, True)
    w1 = int(draw.textlength(left_chip, font=f_chip)) + 44
    w2 = int(draw.textlength(right_chip, font=f_chip)) + 44
    total = w1 + gap + w2
    x0 = (W - total) // 2
    y_chip = 440
    chip(draw, x0, y_chip, left_chip)
    xf = face(28, True)
    x_mark = x0 + w1 + (gap - int(draw.textlength("×", font=xf))) / 2
    draw.text((x_mark, y_chip + 8), "×", font=xf, fill=ORANGE)
    chip(draw, x0 + w1 + gap, y_chip, right_chip)

    draw.line((48, 314, 250, 314), fill=LINE, width=2)
    draw.line((950, 314, 1152, 314), fill=LINE, width=2)

    OUT.mkdir(parents=True, exist_ok=True)
    png_og = OUT / "allsun-og-licenses.png"
    jpg_og = OUT / "allsun-og-licenses.jpg"
    png_tpl = OUT / "allsun-tpl-licenses.png"
    image.save(png_og, "PNG", optimize=True)
    image.save(jpg_og, "JPEG", quality=86, optimize=True)
    image.save(png_tpl, "PNG", optimize=True)

    left = (W - SAFE) // 2
    crop = image.crop((left, 0, left + SAFE, H))
    crop_path = OUT / "_og-licenses-telegram-crop.png"
    crop.save(crop_path, "PNG")
    print(png_og, png_og.stat().st_size)
    print(jpg_og, jpg_og.stat().st_size)
    print(png_tpl)
    print(crop_path)


if __name__ == "__main__":
    main()
