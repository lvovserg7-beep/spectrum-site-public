# -*- coding: utf-8 -*-
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def get(p):
    return urllib.request.urlopen(urllib.request.Request("https://alsn.ru" + p + "?n=2", headers=UA), timeout=40).read().decode("utf-8")


h = get("/dopolnitelnie_licenzii")
s = h.find('id="rec3907172601"')
e = h.find('<div id="rec', s + 10)
c = h[s:e]
i = c.find("<nav")
j = c.find("</nav>") + 6
print(c[i:j])
print("---- scripts in block:", c.count("application/ld+json"))

h2 = get("/cases")
k = h2.find("caseecom#breadcrumb")
a = h2.rfind("<script", 0, k)
b = h2.find("</script>", k) + 9
print("=== cases stale length", b - a)
print(h2[a:a + 250])
print("...")
print(h2[b - 250:b])
