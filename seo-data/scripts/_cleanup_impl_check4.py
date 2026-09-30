import re, os, urllib.request

D = os.path.join(os.path.dirname(__file__), "_cleanup_impl_pages")
out = open(os.path.join(os.path.dirname(__file__), "_cleanup_impl_out4.txt"), "w", encoding="utf-8")
src = {k: open(os.path.join(D, k + ".html"), encoding="utf-8").read() for k in ["dev", "ka", "erp", "sup"]}
for k, s in src.items():
    for m in re.finditer(r'<link[^>]*rel="canonical"[^>]*>', s):
        print(k, "canonical at", m.start(), repr(s[max(0, m.start() - 300):m.end() + 50]), file=out)
    print(k, "offers:", s.count('"offers"'), "price:", s.count('"price"'), file=out)
    print(k, "ld blocks:", len(re.findall(r'application/ld\+json', s)), "#organization:", s.count("alsn.ru/#organization"), file=out)

req = urllib.request.Request("https://alsn.ru/?chk=2909b", headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
    "Accept": "text/html", "Accept-Language": "ru-RU"})
home = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
print("home LocalBusiness:", home.count("LocalBusiness"), "#organization:", home.count("alsn.ru/#organization"), file=out)
