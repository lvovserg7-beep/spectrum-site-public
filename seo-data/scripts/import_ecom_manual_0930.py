"""Забирает инструкцию по модулю поставщиков из Google Docs в seo-data/ecom-manual/.

manual.md - текст со ссылками на скриншоты, images/ - скриншоты с понятными именами,
source.html - исходный экспорт. Копии для сайта кладёт в seo-data/brand-images/ecom-screens/.
"""
import html
import io
import re
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageFilter

DOC_ID = "1cud4TAcxw8qylqZCw65x53OIS5t2WQ7oMFHy9NAODiE"
DOC_URL = f"https://docs.google.com/document/d/{DOC_ID}/edit"
URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=zip"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ecom-manual"
WEB = ROOT / "brand-images" / "ecom-screens"

NAMES = {
    "image1.png": "ecom-1c-reglament-zadaniya.png",
    "image2.png": "ecom-1c-otchet-rezervirovanie.png",
    "image3.png": "ecom-1c-podbor-nalichie-postavshchik.png",
    "image4.png": "ecom-1c-ochistka-sootvetstviy.png",
    "image5.png": "ecom-1c-rezerv-u-postavshchika.png",
    "image6.png": "ecom-1c-tranzitnaya-baza.png",
    "image7.png": "ecom-1c-nastroyka-postavshchika.png",
    "image8.png": "ecom-1c-otchet-rezervirovanie-2.png",
    "image9.png": "ecom-1c-monitor-zagruzki.png",
    "image10.png": "ecom-1c-monitoring-avtorezerva.png",
    "image11.png": "ecom-1c-sopostavlenie-nomenklatury.png",
    "image12.png": "ecom-1c-ostatki-po-praysam.png",
}
# на сайт идут только экраны работы, без служебных настроек
WEB_USE = [
    "ecom-1c-podbor-nalichie-postavshchik.png", "ecom-1c-rezerv-u-postavshchika.png",
    "ecom-1c-sopostavlenie-nomenklatury.png", "ecom-1c-ostatki-po-praysam.png",
    "ecom-1c-monitor-zagruzki.png", "ecom-1c-monitoring-avtorezerva.png", "ecom-1c-otchet-rezervirovanie.png",
]
# имя склада клиента в шапке колонки - размываем в копии для сайта
BLUR = {"ecom-1c-podbor-nalichie-postavshchik.png": [(735, 190, 932, 228)]}


def main():
    raw = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})).read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "images").mkdir(parents=True)
    src = ""
    for n in z.namelist():
        if n.endswith(".html"):
            src = z.read(n).decode("utf-8")
        elif n.startswith("images/"):
            (OUT / "images" / NAMES.get(n[7:], n[7:])).write_bytes(z.read(n))
    for old, new in NAMES.items():
        src = src.replace(f"images/{old}", f"images/{new}")
    (OUT / "source.html").write_text(src, encoding="utf-8")

    h = re.sub(r"<style.*?</style>", "", src, flags=re.S)
    h = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', r"\n![](\1)\n", h)
    h = re.sub(r"</(p|h\d|li|tr)>", "\n", h)
    h = re.sub(r"<li[^>]*>", "- ", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h))
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    for head in ("Настройка работы системы", "Загрузка прайсов поставщиков", "Резервирование"):
        t = re.sub(rf"^{head}\s*$", f"\n## {head}\n", t, count=1, flags=re.M)
    top = (f"# Модуль интеграции 1С с поставщиками по API - инструкция\n\n"
           f"Источник: [Google Docs]({DOC_URL}). Забрано скриптом `seo-data/scripts/import_ecom_manual_0930.py`.\n")
    (OUT / "manual.md").write_text(top + "\n" + re.sub(r"\n{3,}", "\n\n", t).strip() + "\n", encoding="utf-8")

    WEB.mkdir(parents=True, exist_ok=True)
    for name in WEB_USE:
        im = Image.open(OUT / "images" / name).convert("RGB")
        for box in BLUR.get(name, []):
            im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(7)), box[:2])
        im.save(WEB / name, optimize=True)
    sys.stdout.reconfigure(encoding="utf-8")
    print("ok", OUT, len(NAMES), "картинок;", WEB, len(WEB_USE))


if __name__ == "__main__":
    main()
