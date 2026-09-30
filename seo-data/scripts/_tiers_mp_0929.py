# -*- coding: utf-8 -*-
import re
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("utf-8", "replace")


def txt(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


for p in ["/1c-ozon", "/1c-wildberries", "/casemarketplace"]:
    h = get("https://alsn.ru" + p + "?mp=2909")
    t = txt(h)
    print("==", p)
    for k in ["НДС 5%", "Цены с НДС", "79 000", "БЕСПЛАТНО", "со скидкой", "FBO", "rFBS", "с 2015", "Остатки на вашем складе",
              "Принимаем любые предложения", "Корзина", "t706"]:
        print(f"  {k!r}: {(t.count(k) + (h.count(k) if k == 't706' else 0))}")
    print("  tproduct:", sorted(set(re.findall(r'https://alsn\.ru/[^"\s]*tproduct/[0-9\-]+[^"\s<]*', h)))[:6])
