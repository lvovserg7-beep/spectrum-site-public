# -*- coding: utf-8 -*-
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
r = urllib.request.urlopen(urllib.request.Request(f"https://alsn.ru/cases?x={int(time.time())}", headers=UA), timeout=40)
print("Last-Modified:", r.headers.get("Last-Modified"))
h = r.read().decode("utf-8", "replace")
head = h[: h.find("</head>")]
print("head end", len(head), "| cases#breadcrumb at", [m.start() for m in re.finditer(r"cases#breadcrumb", h)], "| t123 recs:", re.findall(r'id="(rec\d+)"[^>]*data-record-type="131"', h))
m2 = re.search(r"cases#breadcrumb", h)
if m2:
    print(h[max(0, m2.start() - 400): m2.start()].replace("\n", " ")[-400:])
for m in re.finditer(r'<!-- nominify (?:begin|end) -->|"@id": "[^"]+"|application/ld\+json|<style|<link[^>]+fonts|<meta name="robots"', head):
    print(m.start(), m.group(0)[:80])
