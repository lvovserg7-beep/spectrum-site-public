# -*- coding: utf-8 -*-
"""T3 бренд: проверка шагов T3-1..T3-4 на живом сайте."""
import re
from _tiers_mp_0929 import get, txt


def meta(h, attr, name):
    m = re.search(rf'<meta[^>]+{attr}="{name}"[^>]+content="([^"]*)"', h) or re.search(
        rf'<meta[^>]+content="([^"]*)"[^>]+{attr}="{name}"', h)
    return m.group(1) if m else None


h = get("https://alsn.ru/?c=1611")
t = txt(h)
print("== T3-1 главная")
print("title:", re.search(r"<title>(.*?)</title>", h, re.S).group(1))
print("description:", meta(h, "name", "description"))
print("og:title:", meta(h, "property", "og:title"))
print("og:description:", meta(h, "property", "og:description"))
for k in ("Аллсан Интеграция - внедрение 1С и интеграции", "Аллсан Интеграция — внедрение 1С и интеграции",
          "Аллсан Интеграция - официальный франчайзи 1С", "Аллсан Интеграция — официальный франчайзи 1С",
          "Наши специалисты - это", "Наши специалисты — это"):
    print(f"  [{k}]:", k in t)
h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
print("  H1:", [re.sub(r"<[^>]+>", "", x).strip() for x in h1])

h = get("https://alsn.ru/about_us?c=1611")
t = txt(h)
print("== T3-2 / T3-3 about_us")
h2 = [re.sub(r"<[^>]+>|\s+", " ", x).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", h, re.S)]
print("  H2 list:", h2)
print("  'Частые вопросы' in text:", "Частые вопросы" in t)
print("  'Контакты Аллсан Интеграции' in text:", "Контакты Аллсан Интеграции" in t)
print("  'Аллсан Интеграция - главная' in text:", "Аллсан Интеграция - главная" in t)
for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', h, re.S):
    label = re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
    if "Контакты Аллсан" in label or "главная" in label.lower():
        print("  link:", label, "->", m.group(1))

h = get("https://alsn.ru/vacancy?c=1611")
print("== T3-4 vacancy")
print("  description:", meta(h, "name", "description"))
print("  robots meta:", re.findall(r'<meta[^>]+name="robots"[^>]*>', h))
