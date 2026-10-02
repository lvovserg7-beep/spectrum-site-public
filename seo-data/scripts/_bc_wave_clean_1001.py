# -*- coding: utf-8 -*-
"""01.10.2026: убрать из В-6 страницы, где старый блок T758 ушёл вместе с переходом на новый дизайн поставщиков."""
import re
from pathlib import Path

P = Path(__file__).parents[1] / "tilda-briefs/tier2-breadcrumbs-wave-2026-09-28.html"
DONE = ["marvel", "treolan", "3logic", "etm-ipro"]
s = P.read_text(encoding="utf-8")

for slug in DONE:
    s, n = re.subn(rf'<tr><td>[^<]*<br><a href="https://alsn\.ru/{re.escape(slug)}">.*?</tr>', "", s, count=1, flags=re.S)
    assert n == 1, slug
    s = s.replace(f"<code>{slug}</code>, ", "", 1)

s = s.replace("12 страниц с двойными крошками", "8 страниц с двойными крошками")
s = s.replace("(12 страниц)</a>", "(8 страниц)</a>")
s = s.replace("сверка с живым alsn.ru 30.09.2026 (В-3...В-8 на сайте ещё не сделаны), обновлено 30.09.2026",
              "сверка с живым alsn.ru 01.10.2026 (В-3...В-8 на сайте ещё не сделаны, кроме 4 страниц из В-6), обновлено 01.10.2026")
line = ("<li>В-6, «Марвел», «Треолан», «3Logic», «ЭТМ iPRO»: старый блок со стрелкой ушёл вместе с переходом страниц "
        "на новый дизайн поставщиков - проверено на сайте 01.10.2026.</li>")
s = s.replace("</li></ul></div>\n<div class=\"callout info\"><strong>Старый блок крошек.", "</li>" + line + "</ul></div>\n<div class=\"callout info\"><strong>Старый блок крошек.", 1)
assert line in s
P.write_text(s, encoding="utf-8")
print("ok", s.count("\u2014") + s.count("\u2013"))
