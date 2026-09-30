# -*- coding: utf-8 -*-
"""Страница «Интеграция 1С с Ozon»: описание для поиска, соцсетей и разметки с четырьмя схемами. 28.09.2026."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_mp_ozon_blocks as b  # noqa: E402
import build_mp_ozon_v3_day as d  # noqa: E402

OUT = os.path.join(b.ROOT, "seo-data", "tilda-briefs", "tier4-1c-ozon-description-2026-09-28.html")

steps = re.search(r'<section class="task" id="s1">.*?id="s3">.*?</section>', d.doc, re.S).group(0)

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Интеграция 1С с Ozon - описание страницы с четырьмя схемами - 28.09.2026</title>
<style>{b.BRIEF_CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Интеграция 1С с Ozon - описание страницы: FBO, FBS, rFBS и DBS</h1>
<p class="muted">Страница: <a href="https://alsn.ru/1c-ozon">https://alsn.ru/1c-ozon</a> (в списке Тильды <code>1c-ozon</code>) · тексты сверены с живой страницей 28.09.2026, 15:18 · каждый шаг после письменного «да», «Опубликовать» один раз в конце</p>
<div class="callout ok"><strong>Не трогать:</strong> заголовок страницы, картинку превью, остальной код в HEAD страницы и HEAD сайта.</div>
{steps}
<p class="muted">Файл: <code>seo-data/tilda-briefs/tier4-1c-ozon-description-2026-09-28.html</code> · собирает <code>seo-data/scripts/build_mp_ozon_desc.py</code></p>
</div>
{b.COPY_JS}
</body>
</html>"""

open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT)
