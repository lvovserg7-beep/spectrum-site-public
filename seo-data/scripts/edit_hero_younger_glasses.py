# -*- coding: utf-8 -*-
"""Локальная правка баннера: лёгкое освежение лица и очки.

Склад, стол, отчёты, руки и поза остаются исходными пикселями.
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "brand-images"
SOURCE = Path(
    r"C:\Users\ALSN_LSA\.cursor\projects"
    r"\c-Users-ALSN-LSA-Desktop-cursor\assets"
    r"\c__Users_ALSN_LSA_AppData_Roaming_Cursor_User_workspaceStorage_"
    r"9f3c600fb9460aaba34cb8d3eca23f12_images_"
    r"image-ee2ab04f-6bea-4d20-b587-75f0b0769b9a.png"
)


def soften_skin(image: np.ndarray) -> np.ndarray:
    """Незаметно смягчает кожу, не меняя черты лица."""
    result = image.copy()
    x1, y1, x2, y2 = 620, 78, 805, 282
    roi = image[y1:y2, x1:x2]
    ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
    skin = cv2.inRange(
        ycrcb,
        np.array((45, 132, 76), dtype=np.uint8),
        np.array((255, 178, 132), dtype=np.uint8),
    )

    ellipse = np.zeros_like(skin)
    cv2.ellipse(ellipse, (91, 105), (79, 94), 0, 0, 360, 255, -1)
    skin = cv2.bitwise_and(skin, ellipse)
    skin = cv2.GaussianBlur(skin, (0, 0), 3.0)

    smooth = cv2.bilateralFilter(roi, 9, 24, 24)
    alpha = (skin.astype(np.float32) / 255.0 * 0.22)[:, :, None]
    mixed = roi.astype(np.float32) * (1 - alpha) + smooth.astype(np.float32) * alpha

    # Очень лёгкое осветление только кожи.
    mixed = np.clip(mixed + alpha * 2.5, 0, 255).astype(np.uint8)
    result[y1:y2, x1:x2] = mixed
    return result


def add_glasses(image: Image.Image) -> Image.Image:
    """Добавляет тонкую оправу в перспективе профиля."""
    scale = 4
    overlay = Image.new("RGBA", (image.width * scale, image.height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    def points(values: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return [(x * scale, y * scale) for x, y in values]

    frame = (43, 47, 50, 215)
    lens = (212, 224, 228, 10)
    width = 6

    # В профиль почти полностью видна одна линза.
    near = points([(658, 148), (704, 149), (706, 168), (662, 170)])
    draw.polygon(near, fill=lens)
    draw.line(near + [near[0]], fill=frame, width=width, joint="curve")

    # Переносица, дужка и посадка за ухом.
    draw.line(points([(658, 152), (650, 155)]), fill=frame, width=width)
    draw.line(points([(704, 151), (738, 153), (752, 158)]), fill=frame, width=width)

    overlay = overlay.resize(image.size, Image.Resampling.LANCZOS)
    return Image.alpha_composite(image.convert("RGBA"), overlay)


def main() -> None:
    source = cv2.imread(str(SOURCE), cv2.IMREAD_COLOR)
    if source is None:
        raise FileNotFoundError(SOURCE)
    edited = soften_skin(source)
    rgb = cv2.cvtColor(edited, cv2.COLOR_BGR2RGB)
    result = add_glasses(Image.fromarray(rgb)).convert("RGB")

    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / "allsun-hero-mp-younger-glasses-preserved.png"
    jpg = OUT / "allsun-hero-mp-younger-glasses-preserved.jpg"
    result.save(png, "PNG", optimize=True)
    result.save(jpg, "JPEG", quality=94)
    print(png)
    print(jpg)


if __name__ == "__main__":
    main()
