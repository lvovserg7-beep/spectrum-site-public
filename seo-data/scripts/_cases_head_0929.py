# -*- coding: utf-8 -*-
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
r = urllib.request.urlopen(urllib.request.Request(f"https://alsn.ru/cases?x={int(time.time())}", headers=UA), timeout=40)
print("Last-Modified:", r.headers.get("Last-Modified"))
h = r.read().decode("utf-8", "replace")
head = h[: h.find("</head>")]
for i, m in enumerate(re.finditer(r"<script[^>]*application/ld\+json[^>]*>.*?</script>", head, re.S | re.I), 1):
    s = m.group(0)
    print(f"\n--- LD #{i} (BreadcrumbList={'BreadcrumbList' in s}, caseecom={'caseecom' in s})")
    print(s)
