import re, sys, html, pathlib
C = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_cleanup_mp_cache")
page = sys.argv[1]
w = 160
t = (C / f"{page}.html").read_text(encoding="utf-8", errors="replace")
for kw in sys.argv[2:]:
    idx = [m.start() for m in re.finditer(re.escape(kw), t)]
    print(f"### {kw}: {len(idx)}")
    for i in idx[:6]:
        s = t[max(0, i - w): i + w].replace("\n", " ")
        print("   ...", s, "...")
