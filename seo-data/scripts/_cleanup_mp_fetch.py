import urllib.request, pathlib
OUT = pathlib.Path(r"c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_cleanup_mp_cache")
OUT.mkdir(exist_ok=True)
URLS = {
    "ozon": "https://alsn.ru/1c-ozon",
    "wb": "https://alsn.ru/1c-wildberries",
    "hub": "https://alsn.ru/casemarketplace",
    "xitsad": "https://alsn.ru/xitsadmarketplace",
    "card_both": "https://alsn.ru/casemarketplace/tproduct/913805053-413216341712-modul-integratsii-1s-s-marketpleisami-oz",
    "card_ozon": "https://alsn.ru/casemarketplace/tproduct/913805053-713209120582-modul-integratsii-1s-s-ozon",
    "card_wb": "https://alsn.ru/casemarketplace/tproduct/913805053-553126495292-modul-integratsii-1s-s-wildberries",
}
import sys, time
only = sys.argv[1:]
for k, u in URLS.items():
    if only and k not in only:
        continue
    time.sleep(3)
    req = urllib.request.Request(u + "?chk=2909mp2", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", "Accept": "text/html", "Accept-Language": "ru"})
    try:
        b = urllib.request.urlopen(req, timeout=40).read()
        (OUT / f"{k}.html").write_bytes(b)
        print(k, len(b))
    except Exception as e:
        print(k, "ERR", e)
