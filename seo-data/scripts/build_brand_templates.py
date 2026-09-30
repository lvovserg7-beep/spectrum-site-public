# -*- coding: utf-8 -*-
"""Светлые слайд-шаблоны Аллсан 16:9. Логотип — готовый PNG, текст — набор.

OG / Telegram для лицензий — не этот скрипт: seo-data/scripts/build_og_licenses.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "logo" / "Аллсан_6.png"
OUT = ROOT / "brand-images"
FONTS = Path(r"C:\Windows\Fonts")

ORANGE = (245, 88, 35, 255)
GRAPHITE = (33, 33, 33, 255)
LINE = (196, 196, 196, 255)
BG = (247, 248, 250, 255)
OZON_BLUE = (0, 91, 255, 255)
WB_PURPLE = (203, 17, 171, 255)
WHITE = (255, 255, 255, 255)

W, H = 1920, 1080


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def draw_bg(im: Image.Image, draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((0, 0, W, H), fill=BG)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse((-220, -260, 520, 480), fill=(255, 255, 255, 90))
    d.ellipse((1480, 720, 2140, 1380), fill=(232, 234, 238, 110))
    d.ellipse((1680, -180, 2140, 280), fill=(255, 255, 255, 80))
    im.alpha_composite(overlay)
    draw.line((70, 980, 620, 70), fill=(228, 229, 232, 255), width=2)
    draw.line((1680, 40, 1910, 420), fill=(228, 229, 232, 255), width=2)


def paste_logo(im: Image.Image) -> None:
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((620, 560), Image.Resampling.LANCZOS)
    im.paste(logo, (120, (H - logo.height) // 2 - 10), logo)


def arrow(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 28) -> None:
    draw.polygon(
        [(x, y - size // 2), (x + size, y), (x, y + size // 2)],
        fill=ORANGE,
    )


def rounded(draw: ImageDraw.ImageDraw, box, fill, radius=18) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def ozon_chip(im: Image.Image, draw: ImageDraw.ImageDraw, x: int, y: int) -> int:
    rounded(draw, (x, y, x + 72, y + 72), OZON_BLUE, 18)
    d = ImageDraw.Draw(im)
    d.arc((x + 14, y + 22, x + 58, y + 62), 20, 160, fill=WHITE, width=7)
    f = font("segoeui.ttf", 40)
    draw.text((x + 90, y + 12), "Ozon", font=f, fill=OZON_BLUE)
    return x + 90 + int(draw.textlength("Ozon", font=f))


def wb_chip(im: Image.Image, draw: ImageDraw.ImageDraw, x: int, y: int) -> int:
    rounded(draw, (x, y, x + 72, y + 72), WB_PURPLE, 18)
    f_wb = font("segoeuib.ttf", 26)
    tw = draw.textlength("WB", font=f_wb)
    draw.text((x + (72 - tw) / 2, y + 18), "WB", font=f_wb, fill=WHITE)
    f = font("segoeui.ttf", 40)
    draw.text((x + 90, y + 12), "Wildberries", font=f, fill=WB_PURPLE)
    return x + 90 + int(draw.textlength("Wildberries", font=f))


def text_chip(
    draw: ImageDraw.ImageDraw, x: int, y: int, label: str, accent=GRAPHITE
) -> int:
    f = font("segoeui.ttf", 32)
    tw = int(draw.textlength(label, font=f))
    rounded(draw, (x, y, x + tw + 48, y + 64), (255, 255, 255, 255), 16)
    draw.rounded_rectangle(
        (x, y, x + tw + 48, y + 64), radius=16, outline=(220, 221, 224, 255), width=2
    )
    draw.text((x + 24, y + 12), label, font=f, fill=accent)
    return x + tw + 48


def flow_line(draw: ImageDraw.ImageDraw, x1: int, y: int, x2: int) -> None:
    draw.line((x1, y, x2, y), fill=LINE, width=3)


def slide_mp() -> Image.Image:
    im = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw_bg(im, draw)
    paste_logo(im)
    f_title = font("segoeuib.ttf", 68)
    draw.text((800, 290), "1С × маркетплейсы", font=f_title, fill=GRAPHITE)
    y_line = 420
    flow_line(draw, 800, y_line, 1260)
    draw.line((1260, y_line, 1260, 548), fill=LINE, width=3)
    flow_line(draw, 1260, 548, 1680)
    arrow(draw, 1690, 548)
    flow_line(draw, 1068, 548, 1210)
    arrow(draw, 1218, 548)
    ozon_chip(im, draw, 800, 488)
    wb_chip(im, draw, 1280, 488)
    return im


def slide_b2b() -> Image.Image:
    im = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw_bg(im, draw)
    paste_logo(im)
    f_title = font("segoeuib.ttf", 58)
    draw.text((820, 280), "1С × поставщики телеком", font=f_title, fill=GRAPHITE)
    f_sub = font("segoeui.ttf", 28)
    draw.text(
        (820, 370),
        "Цены, остатки, резерв и заказы из ЛК в вашу 1С",
        font=f_sub,
        fill=(90, 90, 90, 255),
    )
    y = 500
    x = 820
    for i, label in enumerate(("цены", "остатки", "резерв", "заказы")):
        x = text_chip(draw, x, y, label)
        if i < 3:
            flow_line(draw, x + 8, y + 32, x + 40)
            arrow(draw, x + 44, y + 32, 20)
            x += 78
    return im


def slide_services() -> Image.Image:
    im = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw_bg(im, draw)
    paste_logo(im)
    f_title = font("segoeuib.ttf", 56)
    draw.text((820, 280), "Внедрение и поддержка 1С", font=f_title, fill=GRAPHITE)
    f_sub = font("segoeui.ttf", 28)
    draw.text(
        (820, 370),
        "Под ваши процессы · реакция от 15 минут",
        font=f_sub,
        fill=(90, 90, 90, 255),
    )
    y = 500
    x = 800
    labels = ("обследование", "настройка", "запуск")
    for i, label in enumerate(labels):
        x = text_chip(draw, x, y, label)
        if i < len(labels) - 1:
            flow_line(draw, x + 8, y + 32, x + 36)
            arrow(draw, x + 40, y + 32, 20)
            x += 74
    return im


def slide_licenses() -> Image.Image:
    im = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw_bg(im, draw)
    paste_logo(im)
    f_title = font("segoeuib.ttf", 58)
    draw.text((820, 280), "Лицензии 1С и Битрикс24", font=f_title, fill=GRAPHITE)
    f_sub = font("segoeui.ttf", 28)
    draw.text(
        (820, 370),
        "Официальная поставка у партнёра 1С",
        font=f_sub,
        fill=(90, 90, 90, 255),
    )
    y = 500
    x = 800
    x = text_chip(draw, x, y, "1С")
    f_x = font("segoeuib.ttf", 36)
    draw.text((x + 18, y + 10), "×", font=f_x, fill=ORANGE)
    x += 58
    text_chip(draw, x, y, "Битрикс24")
    return im


def save(im: Image.Image, name: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im.convert("RGB").save(path, "PNG", optimize=True)
    return path


def main() -> None:
    for name, fn in (
        ("allsun-tpl-mp.png", slide_mp),
        ("allsun-tpl-b2b.png", slide_b2b),
        ("allsun-tpl-services.png", slide_services),
        ("allsun-tpl-licenses-16x9.png", slide_licenses),
    ):
        path = save(fn(), name)
        print(path)


if __name__ == "__main__":
    main()
