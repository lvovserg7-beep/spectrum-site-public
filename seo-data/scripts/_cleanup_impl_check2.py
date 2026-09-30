import re, os, html as H

D = os.path.join(os.path.dirname(__file__), "_cleanup_impl_pages")
src = {k: open(os.path.join(D, k + ".html"), encoding="utf-8").read() for k in ["dev", "ka", "erp", "sup"]}
out = open(os.path.join(os.path.dirname(__file__), "_cleanup_impl_out2.txt"), "w", encoding="utf-8")


def p(*a):
    print(*a, file=out)


def text(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s).replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s)


def around(k, w, n=250, maxhits=3, raw=False):
    t = src[k] if raw else text(src[k])
    hits = [m.start() for m in re.finditer(re.escape(w), t)][:maxhits]
    p("---", k, repr(w), "hits:", len(hits))
    for h in hits:
        p("   ", repr(t[max(0, h - n):h + n]))


around("dev", "ТОП")
around("dev", "Центр")
around("dev", "Обследование, настройка, обучение и запуск")
around("dev", "Внедрение 1С под ключ:")
around("dev", "Какие конфигурации 1С внедряем", raw=True, n=200, maxhits=8)
around("erp", "Предпроектное обследование", n=400)
around("erp", "Ввод в действие", n=300)
around("erp", "ТОП")
around("erp", "Реакция на задачи")
around("dev", "Реакция на задачи")
around("ka", "Реакция на задачи")
around("sup", "Особенности тарифа", raw=True, n=400)
around("sup", "Это не 1С:КП и не внедрение с нуля", raw=True, n=1500, maxhits=1)
around("sup", "Хлебные крошки", raw=True, n=300)
around("sup", "Сертификат", raw=True, n=300)
around("sup", "Зеленоград")
for k in ["dev", "ka", "erp"]:
    around(k, "Хлебные крошки", raw=True, n=300, maxhits=1)
    # find rec id containing crumbs and its bg
    m = re.search(r'<div id="(rec\d+)"[^>]*>(?:(?!<div id="rec).)*?Хлебные крошки', src[k], re.S)
    if m:
        p("crumb rec:", m.group(1))
        m2 = re.search(r'<div id="%s"[^>]*>' % m.group(1), src[k])
        p("   tag:", m2.group(0))
around("ka", "Полезные страницы по внедрению 1С", raw=True, n=600, maxhits=1)
around("dev", "Кейсы внедрения и автоматизации", raw=True, n=900, maxhits=1)
around("erp", "Кейсы внедрения и автоматизации", raw=True, n=900, maxhits=1)
p("ERP breve total:", text(src["erp"]).count("\u0306"))
t = text(src["erp"])
i = t.find("Шесть основных этапов")
j = t.find("Из чего складывается")
p("ERP stages section breves:", t[i:j].count("\u0306") if i >= 0 else "n/a", "i,j", i, j)
p(repr(t[i:i + 2000]))
