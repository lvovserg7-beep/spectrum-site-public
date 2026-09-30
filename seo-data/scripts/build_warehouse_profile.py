# -*- coding: utf-8 -*-
"""Портрет сотрудника в кресле на фоне склада.

Лицо и профиль берутся из исходной фотографии без генерации.
AI используется только для пустой сцены склада с креслом.
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ASSETS = Path(
    r"C:\Users\ALSN_LSA\.cursor\projects"
    r"\c-Users-ALSN-LSA-Desktop-cursor\assets"
)
SOURCE = ASSETS / (
    "c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    "9f3c600fb9460aaba34cb8d3eca23f12_images_"
    "image-61ffb68c-bc7d-4daf-9c59-9d562c63bba9.png"
)
SCENE = ASSETS / "allsun-warehouse-empty-chair.png"
OUTPUT = ASSETS / "allsun-warehouse-seated-profile-real-face.png"


def extract_person() -> Image.Image:
    source = cv2.imread(str(SOURCE), cv2.IMREAD_COLOR)
    if source is None:
        raise FileNotFoundError(SOURCE)

    height, width = source.shape[:2]
    mask = np.full((height, width), cv2.GC_BGD, np.uint8)
    outline = np.array(
        [
            (150, 90),
            (255, 88),
            (315, 112),
            (345, 164),
            (351, 210),
            (379, 244),
            (378, 277),
            (350, 306),
            (375, 335),
            (398, 385),
            (414, 442),
            (445, 505),
            (474, 574),
            (523, 641),
            (540, 716),
            (516, 784),
            (470, 822),
            (248, 830),
            (184, 785),
            (153, 706),
            (121, 625),
            (90, 542),
            (67, 454),
            (70, 362),
            (98, 294),
            (136, 251),
            (132, 180),
        ],
        dtype=np.int32,
    )
    cv2.fillPoly(mask, [outline], cv2.GC_PR_FGD)

    # Надёжные внутренние области фигуры.
    cv2.ellipse(mask, (257, 193), (76, 91), 0, 0, 360, cv2.GC_FGD, -1)
    torso = np.array(
        [(139, 292), (318, 292), (374, 354), (420, 520), (470, 675), (215, 742), (96, 520)],
        dtype=np.int32,
    )
    cv2.fillPoly(mask, [torso], cv2.GC_FGD)

    background = np.zeros((1, 65), np.float64)
    foreground = np.zeros((1, 65), np.float64)
    cv2.grabCut(
        source,
        mask,
        None,
        background,
        foreground,
        10,
        cv2.GC_INIT_WITH_MASK,
    )
    alpha = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0
    ).astype("uint8")

    # Убираем соседнего человека и предметы перед столом.
    alpha[410:, :58] = 0

    # Серый фрагмент старой стены справа от плеча не относится к фигуре.
    hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
    yy, xx = np.indices(alpha.shape)
    gray_wall = (
        (xx > 305)
        & (yy > 285)
        & (hsv[:, :, 1] < 42)
        & (hsv[:, :, 2] > 72)
    )
    alpha[gray_wall] = 0

    # Нижняя часть исходника перекрыта столом. Оставляем чистый поясной портрет
    # и мягко сводим его к спинке кресла.
    fade_start, fade_end = 575, 650
    for row in range(fade_start, fade_end):
        alpha[row] = (
            alpha[row].astype(np.float32)
            * (fade_end - row)
            / (fade_end - fade_start)
        ).astype(np.uint8)
    alpha[fade_end:] = 0
    alpha = cv2.GaussianBlur(alpha, (0, 0), 1.0)

    rgba = cv2.cvtColor(source, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = alpha
    person = Image.fromarray(rgba)
    bbox = person.getchannel("A").getbbox()
    if not bbox:
        raise RuntimeError("Фигура не выделена")
    return person.crop(bbox)


def build() -> Image.Image:
    scene = Image.open(SCENE).convert("RGBA")
    person = extract_person()
    target_height = 650
    person = person.resize(
        (round(person.width * target_height / person.height), target_height),
        Image.Resampling.LANCZOS,
    )

    rgb = person.convert("RGB")
    rgb = ImageEnhance.Brightness(rgb).enhance(1.025)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.02)
    rgb = ImageEnhance.Color(rgb).enhance(0.96)
    corrected = rgb.convert("RGBA")
    corrected.putalpha(person.getchannel("A"))
    person = corrected

    x, y = 104, 116
    alpha = person.getchannel("A")
    shadow = Image.new("RGBA", person.size, (20, 24, 28, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(10)).point(lambda p: p // 4))
    scene.alpha_composite(shadow, (x + 9, y + 10))
    scene.alpha_composite(person, (x, y))
    return scene.convert("RGB")


def main() -> None:
    result = build()
    result.save(OUTPUT, "PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
