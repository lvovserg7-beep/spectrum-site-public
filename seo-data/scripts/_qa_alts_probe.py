# -*- coding: utf-8 -*-
"""Probe how Tilda stores gallery alt on one leftover card."""
import json
import re
import urllib.request

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
URL = (
    "https://alsn.ru/buhv8/tproduct/379482785-889199487282-"
    "1s-buhgalteriya-snt-elektronnaya-postavk"
)


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "text/html"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


html = fetch(URL)
print("len", len(html))
print("gallery count", len(re.findall(r'"gallery"', html)))
print("uid present", "889199487282" in html)

out = []
for i, m in enumerate(re.finditer(r'"gallery"\s*:\s*(\[.{0,500})', html)):
    out.append(f"---g {i}\n{m.group(1)[:400]}")
    if i >= 5:
        break
print("\n".join(out))

# product json near uid
idx = html.find("889199487282")
print("first uid idx", idx)
if idx != -1:
    print(html[max(0, idx - 200) : idx + 400])
