# -*- coding: utf-8 -*-
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"}
h = urllib.request.urlopen(urllib.request.Request(f"https://alsn.ru/cases?x={int(time.time())}", headers=UA), timeout=40).read().decode("utf-8", "replace")
head = h[: h.find("</head>")]
i = head.find("#organization")
start = head.rfind("<script", 0, i)
tail = head[start:]
tail = re.sub(r'(<script type="application/ld\+json">).*?(</script>)', r"\1 [LD] \2", tail, flags=re.S)
print(tail)
print("\n--- meta robots:", re.findall(r'<meta[^>]+name="robots"[^>]*>', head))
print("--- title:", re.findall(r"<title>(.*?)</title>", head))
print("--- description:", re.findall(r'<meta name="description"[^>]*>', head))
print("--- og:", re.findall(r'<meta property="og:[^>]*>', head))
print("--- canonical:", re.findall(r'<link rel="canonical"[^>]*>', head))
