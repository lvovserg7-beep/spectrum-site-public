import re, pathlib
C = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_cleanup_mp_cache")
t = (C / "hub.html").read_text(encoding="utf-8", errors="replace")
for m in re.finditer(r'<img[^>]*alt=""[^>]*>', t):
    print(t[max(0, m.start() - 120): m.end()].replace("\n", " "))
    print("---")
