import re, sys, html, pathlib
D = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\tilda-briefs")
FILES = sys.argv[1:]
for f in FILES:
    t = (D / f).read_text(encoding="utf-8")
    print("=" * 30, f)
    t2 = re.sub(r"<style.*?</style>|<script.*?</script>", "", t, flags=re.S)
    for m in re.finditer(r"<(h1|h2|h3|h4)[^>]*>(.*?)</\1>", t2, flags=re.S):
        s = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        s = re.sub(r"\s+", " ", s)
        print(f"  {m.group(1)} @{m.start()}: {s[:150]}")
