"""Сверка кода живой /ecom с инструкцией + скриншоты."""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).parent
h = (D / "_ecom_live_chk.html").read_text(encoding="utf-8")
brief = (D.parent / "tilda-briefs" / "tier4-ecom-v3-2026-09-30.html").read_text(encoding="utf-8")
import html as H

pre = {m.group(1): H.unescape(m.group(2)) for m in re.finditer(r'<pre id="(\w+)"[^>]*>(.*?)</pre>', brief, re.S)}
norm = lambda s: re.sub(r"\s+", "", s)
hn = norm(h)
for k, name in (("e2a", "первый экран"), ("e3a", "основная часть"), ("e4a", "последний экран")):
    frag = pre[k]
    parts = [p for p in re.split(r"<script>.*?</script>", frag, flags=re.S) if p.strip()]
    probe = [norm(x)[:400] for x in parts] + [norm(x)[-400:] for x in parts]
    print("OK " if all(p in hn for p in probe) else "!! ", name, "совпадает с инструкцией")
head_live = h[:h.index("</head>")]
ld = [json.loads(m.group(1)) for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', head_live, re.S)]
faq_live = [x for x in ld if x.get("@type") == "FAQPage"][0]
faq_ours = [json.loads(m.group(1)) for m in re.finditer(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', pre["e1a"], re.S) if '"FAQPage"' in m.group(1)][0]
print("OK " if faq_live["mainEntity"] == faq_ours["mainEntity"] else "!! ", "FAQPage совпадает с инструкцией")
css_ours = re.search(r"<style>(.*?)</style>", pre["e1a"], re.S).group(1)
print("OK " if norm(css_ours) in norm(head_live) else "!! ", "стили HEAD совпадают целиком")
print("style-тегов в HEAD страницы:", head_live.count("<style>"))

CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
S = D.parent / "competitors" / "screens"
url = "https://alsn.ru/ecom?c=shot1346"
subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=12000",
                "--window-size=1440,5200", f"--screenshot={S / '_live-ecom-desk.png'}", url], capture_output=True, timeout=150)
subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=12000",
                "--window-size=390,2600", "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
                f"--screenshot={S / '_live-ecom-mob.png'}", url], capture_output=True, timeout=150)
print("shots", (S / "_live-ecom-desk.png").exists(), (S / "_live-ecom-mob.png").exists())
