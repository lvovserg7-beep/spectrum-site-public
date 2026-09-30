# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _audit_breadcrumbs_all_0928 as bc  # noqa: E402
from _audit_alts_tail import IMG_RE, attrs, basename  # noqa: E402

names = {"Tatneft-Logosvg.png", "Logo_LANIT.png", "logo.png", "thumb_6478_participa.png", "logo-ss-ru.jpg",
         "c8561e493ab77c8933fc.png", "logo11_350.jpg", "5e82004a227a092f3923.png", "image.png"}
out = []
for p in ["/caseecomsc", "/xitsadmarketplace"]:
    h = bc.get("https://alsn.ru" + p + "?pk2=2909")
    for m in IMG_RE.finditer(h):
        a = attrs(m.group(1))
        fn = basename(a.get("src") or a.get("data-original") or "")
        if fn in names:
            out.append("%s | %s | %r" % (p, fn, a.get("alt")))
Path(__file__).with_name("_cleanup_bc_peek2.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
