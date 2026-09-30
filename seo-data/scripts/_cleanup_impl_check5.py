import re, os

D = os.path.join(os.path.dirname(__file__), "_cleanup_impl_pages")
s = open(os.path.join(D, "dev.html"), encoding="utf-8").read()
out = open(os.path.join(os.path.dirname(__file__), "_cleanup_impl_out5.txt"), "w", encoding="utf-8")
i = s.find("Настроим УТ")
st = s.rfind('<div id="rec', 0, i)
print(s[st:st + 200], file=out)
print("....", file=out)
print(s[i - 2500:i + 1200], file=out)
