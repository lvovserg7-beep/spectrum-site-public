import re, sys, html, pathlib
D = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\tilda-briefs")
f = sys.argv[1]
maxpre = int(sys.argv[2]) if len(sys.argv) > 2 else 200
t = (D / f).read_text(encoding="utf-8")
t = re.sub(r"<style.*?</style>|<script.*?</script>", "", t, flags=re.S)
def pre(m):
    s = html.unescape(m.group(1))
    return "\n[PRE " + str(len(s)) + "]: " + s[:maxpre].replace("\n", " / ") + "\n"
t = re.sub(r"<pre[^>]*>(.*?)</pre>", pre, t, flags=re.S)
t = re.sub(r"<(h1|h2|h3|li|p|tr|div)[^>]*>", "\n", t)
t = re.sub(r"<[^>]+>", "", t)
t = html.unescape(t)
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
print(t)
