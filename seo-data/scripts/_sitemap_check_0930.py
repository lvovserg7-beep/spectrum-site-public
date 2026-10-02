import re, json, time, random, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
      "Accept-Language": "ru"}


def get(url, tries=4):
    s = 0
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            s = e.code
            if e.code == 404:
                return 404, ""
        except Exception:
            s = 0
        time.sleep(3 + random.random() * 3)
    return s, ""


s, xml = get("https://alsn.ru/sitemap.xml")
urls = sorted(set(re.findall(r"<loc>(.*?)</loc>", xml)))
print("sitemap.xml status", s, "urls", len(urls))

extra = ["https://alsn.ru" + p for p in ("/whatsapp", "/uslugi", "/produkty", "/licenzii", "/dorabotka-1c",
                                         "/max1c", "/b2b-postavshiki", "/licenzii-1c-ut", "/test-menu")]
res = []
for u in urls + extra:
    st, html = get(u)
    ni = bool(re.search(r'<meta[^>]+name="robots"[^>]+noindex', html))
    res.append({"url": u, "status": st, "noindex": ni})
    time.sleep(0.8)

bad = [r for r in res[: len(urls)] if r["status"] != 200 or r["noindex"]]
print("Плохие в sitemap:", json.dumps(bad, ensure_ascii=False, indent=1))
for r in res[len(urls):]:
    print(" ", r["url"], r["status"], "noindex" if r["noindex"] else "")
json.dump({"urls": urls, "res": res}, open("_sitemap_0930.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
