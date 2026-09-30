import os

B = os.path.join(os.path.dirname(__file__), "..", "tilda-briefs")
p = os.path.join(B, "tier3-vnedrenie-1c-ostatok-2026-09-28.html")
s = open(p, encoding="utf-8").read()
s = s.replace("{{BREVE}}", "\u0438\u0306")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("placeholders left:", s.count("{{"), "breves:", s.count("\u0306"))
print("long dashes:", s.count("\u2014"), s.count("\u2013"))
