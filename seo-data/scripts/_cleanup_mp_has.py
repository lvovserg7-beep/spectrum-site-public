import re, sys, html, pathlib
C = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_cleanup_mp_cache")
# usage: page "str1" "str2" ...
page = sys.argv[1]
raw = (C / f"{page}.html").read_text(encoding="utf-8", errors="replace")
norm = html.unescape(raw).replace("\u00a0", " ")
for s in sys.argv[2:]:
    print(f"{page} | {norm.count(s)} | {s}")
