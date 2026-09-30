import sys
from pathlib import Path

sys.path.insert(0, r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts")
import fix_store_seo as m

lines = []
t = "1С Фреш БизнесСтарт Нулевка на 12 месяцев"
lines.append("core " + repr(m.core_name(t)))
lines.append("abbr " + repr(m.abbreviate(m.core_name(t))))
lines.append("fit " + repr(m.fit_title("Купить ", m.abbreviate(m.core_name(t)))))
t2 = "1С:Фреш-1С:Предприятие 8 через Интернет 1С:Касса. Стандартный на 12 месяцев"
lines.append("core2 " + repr(m.core_name(t2)))
lines.append("abbr2 " + repr(m.abbreviate(m.core_name(t2))))
c = m.core_name(t2)
if "фреш" not in c.lower():
    c = "1С:Фреш " + c
c = m.abbreviate(c)
c = __import__("re").sub(r"1С:?\s*Фреш[\s\-]*1С:?\s*Фреш", "1С:Фреш", c, flags=__import__("re").I)
lines.append("fresh path c " + repr(c))
lines.append("fit2 " + repr(m.fit_title("Купить ", c)))
Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_spot3.txt").write_text(
    "\n".join(lines), encoding="utf-8"
)
