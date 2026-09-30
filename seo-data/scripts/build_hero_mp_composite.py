# -*- coding: utf-8 -*-
"""Баннер МП: реальный склад, реальный сотрудник, четкие окна 1С."""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS = Path(r"C:\Users\ALSN_LSA\.cursor\projects\c-Users-ALSN-LSA-Desktop-cursor\assets")
OUT = Path(__file__).resolve().parents[1] / "brand-images"

WAREHOUSE = ASSETS / "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_image-1d462ddd-c538-488a-8b29-b813264f58f3.jpg"
EMPLOYEE = ASSETS / "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_9f3c600fb9460aaba34cb8d3eca23f12_images_image-72d019a0-bb39-4ee6-82e3-394afd86d534.jpg"
ONEC = ASSETS / "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_9f3c600fb9460aaba34cb8d3eca23f12_images_image-df940f6e-fb65-4ed6-9148-c2afdb138c5c.png"
COST = ASSETS / "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_9f3c600fb9460aaba34cb8d3eca23f12_images_image-da892699-a2cc-43f6-affb-42c340ebf024.png"
DRR = ASSETS / "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_9f3c600fb9460aaba34cb8d3eca23f12_images_image-c867e758-976a-44d7-8d18-0b236e73480e.png"
REVIEWS = ASSETS / "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_9f3c600fb9460aaba34cb8d3eca23f12_images_image-afc0b8c5-985a-4d8e-b8e7-ffb460d1c393.png"

W, H = 1920, 900
BG = (247, 248, 250)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    ratio = max(tw / image.width, th / image.height)
    resized = image.resize(
        (round(image.width * ratio), round(image.height * ratio)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def warehouse_bg() -> Image.Image:
    image = cover(Image.open(WAREHOUSE).convert("RGB"), (W, H))
    overlay = Image.new("RGBA", (W, H), (*BG, 36))
    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    gradient = Image.new("L", (W, 1))
    values = []
    for x in range(W):
        if x <= 420:
            alpha = 150
        elif x >= 980:
            alpha = 8
        else:
            alpha = round(150 - (x - 420) * 142 / 560)
        values.append(alpha)
    gradient.putdata(values)
    gradient = gradient.resize((W, H))
    white = Image.new("RGBA", (W, H), (*BG, 255))
    image.paste(white, (0, 0), gradient)
    return image


def make_1c_window(report: Image.Image, use_full_chrome: bool = False) -> Image.Image:
    """Собирает окно 1С: живая жёлтая подсистема с логотипом + чёткий отчёт."""
    chrome = Image.open(ONEC).convert("RGB")
    cw, ch = chrome.size
    left_w = 100
    top_h = 110
    win_w, win_h = 1280, 780
    window = Image.new("RGB", (win_w, win_h), (248, 248, 248))

    left = chrome.crop((0, 0, left_w, ch)).resize((int(win_w * 0.11), win_h), Image.Resampling.LANCZOS)
    window.paste(left, (0, 0))

    top = chrome.crop((0, 0, cw, top_h)).resize((win_w, int(win_h * 0.15)), Image.Resampling.LANCZOS)
    window.paste(top, (0, 0))

    content_x = left.width
    content_y = top.height
    content_w = win_w - content_x - 6
    content_h = win_h - content_y - 6

    if use_full_chrome:
        body = chrome.crop((left_w, top_h, cw, ch))
    else:
        body = report.convert("RGB")
    body = body.resize((content_w, content_h), Image.Resampling.LANCZOS)
    window.paste(body, (content_x, content_y))
    return window


def draw_monitor(scene: Image.Image, screen: Image.Image, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    bezel = 14
    draw = ImageDraw.Draw(scene)
    draw.rounded_rectangle((x1 - 10, y1 - 10, x2 + 10, y2 + 18), 10, fill=(18, 18, 18))
    inner = screen.resize((x2 - x1, y2 - y1), Image.Resampling.LANCZOS)
    scene.paste(inner, (x1, y1))
    # подставка
    mx = (x1 + x2) // 2
    draw.rectangle((mx - 18, y2 + 18, mx + 18, y2 + 78), fill=(22, 22, 22))
    draw.rectangle((mx - 70, y2 + 78, mx + 70, y2 + 90), fill=(22, 22, 22))


def extract_employee() -> Image.Image:
    source_bgr = cv2.imread(str(EMPLOYEE), cv2.IMREAD_COLOR)
    if source_bgr is None:
        raise FileNotFoundError(EMPLOYEE)
    h, w = source_bgr.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    body = np.array(
        [
            (422, 292),
            (455, 276),
            (498, 290),
            (520, 332),
            (512, 392),
            (528, 435),
            (548, 505),
            (538, 575),
            (505, 640),
            (478, 710),
            (445, 790),
            (410, 870),
            (358, 935),
            (322, 955),
            (330, 900),
            (352, 810),
            (358, 730),
            (338, 650),
            (318, 585),
            (340, 545),
            (358, 500),
            (368, 430),
            (388, 355),
        ],
        dtype=np.int32,
    )
    chair = np.array(
        [
            (552, 512),
            (605, 545),
            (640, 590),
            (648, 650),
            (638, 710),
            (600, 742),
            (555, 770),
            (538, 830),
            (555, 900),
            (610, 955),
            (555, 1005),
            (490, 1008),
            (450, 970),
            (475, 920),
            (500, 860),
            (518, 800),
            (535, 740),
            (548, 680),
            (558, 600),
        ],
        dtype=np.int32,
    )
    bridge = np.array(
        [
            (520, 480),
            (555, 505),
            (545, 600),
            (510, 620),
            (500, 540),
        ],
        dtype=np.int32,
    )
    cv2.fillPoly(mask, [body, chair, bridge], 255)
    alpha = cv2.GaussianBlur(mask, (0, 0), 1.05)
    rgba = cv2.cvtColor(source_bgr, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = alpha
    person = Image.fromarray(rgba)
    bbox = person.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError("Не удалось вырезать сотрудника")
    return person.crop(bbox)


def build() -> Image.Image:
    scene = warehouse_bg()
    # стол
    draw = ImageDraw.Draw(scene)
    draw.rounded_rectangle((20, 545, 1540, 780), 6, fill=(210, 210, 206))
    draw.rectangle((20, 545, 1540, 562), fill=(228, 228, 224))

    cost = make_1c_window(Image.open(COST))
    drr = make_1c_window(Image.open(DRR))
    reviews = Image.open(ONEC).convert("RGB")

    draw_monitor(scene, reviews, (36, 88, 620, 530))
    draw_monitor(scene, cost, (635, 78, 1125, 515))
    draw_monitor(scene, drr, (1140, 92, 1525, 500))

    person = extract_employee()
    target_h = 820
    person = person.resize(
        (round(person.width * target_h / person.height), target_h),
        Image.Resampling.LANCZOS,
    )
    px, py = 1310, 80
    alpha = person.getchannel("A")
    shadow = Image.new("RGBA", person.size, (20, 22, 24, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(12)).point(lambda v: v // 4))
    scene.alpha_composite(shadow, (px + 10, py + 14))
    scene.alpha_composite(person, (px, py))
    return scene.convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    person = extract_employee()
    preview = Image.new("RGB", person.size, (240, 80, 40))
    preview.paste(person, (0, 0), person)
    preview.save(OUT / "_hero-mp-employee-cutout.png")
    result = build()
    png = OUT / "allsun-hero-mp-warehouse-1c-real.png"
    jpg = OUT / "allsun-hero-mp-warehouse-1c-real.jpg"
    result.save(png, "PNG", optimize=True)
    result.save(jpg, "JPEG", quality=95)
    result.save(ASSETS / "allsun-hero-mp-warehouse-1c-real.png", "PNG", optimize=True)
    print(png)
    print(jpg)


if __name__ == "__main__":
    main()
