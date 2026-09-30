import html
import pathlib
import re

base = pathlib.Path(__file__).parent
src = (base / "_cleanup_brand_pages" / "hub.html").read_text(encoding="utf-8")
blocks = re.findall(r"<script[^>]*>.*?</script>", src, re.S)
hit = [b for b in blocks if "alsn-bc-jsonld" in b and "tproduct" in b]
print("found:", len(hit))
code = hit[0]
print(code)
(base / "_cleanup_brand_scriptd.txt").write_text(html.escape(code, quote=False), encoding="utf-8")
