import re, os, html as H

D = os.path.join(os.path.dirname(__file__), "_cleanup_impl_pages")
src = {k: open(os.path.join(D, k + ".html"), encoding="utf-8").read() for k in ["dev", "erp"]}
out = open(os.path.join(os.path.dirname(__file__), "_cleanup_impl_out3.txt"), "w", encoding="utf-8")


def text(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s)


t = text(src["erp"])
i = t.find("Шесть основных этапов")
j = t.find("Из чего складывается")
for m in re.finditer("\u0306", t[i:j]):
    k = i + m.start()
    print("ERP stage breve:", repr(t[k - 40:k + 10]), file=out)
print("erp stage raw rec:", file=out)
m = re.search(r'<div id="(rec\d+)"[^>]*data-record-type="(\d+)"(?:(?!<div id="rec).)*?Шесть основных этапов', src["erp"], re.S)
print(m.group(1) if m else None, m.group(2) if m else None, file=out)

d = text(src["dev"])
for w in ["Опыт", "ТОП", "TOP", "Топ", "ЦРА", "реальной автоматизации", "по всей России"]:
    print("dev", w, [d[x.start() - 80:x.start() + 80] for x in re.finditer(w, d)][:3], file=out)
k = d.find("Без головной боли")
print("DEV FIRST SCREEN:", d[k - 100:k + 900], file=out)
