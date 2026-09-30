# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _audit_breadcrumbs_all_0928 as bc  # noqa: E402

out = []
for path, fn in [("/kompleksnaya_avtomatizaciya", "kak-sformirovat-plat.jpg"), ("/ecom", "integraciya-1c-po-ap.jpg"),
                 ("/bitrix24", "Group_1_1.png"), ("/development1c", "0001_1.jpg")]:
    h = bc.get("https://alsn.ru" + path + "?pk=2909")
    for m in re.finditer(re.escape(fn), h):
        s = h.rfind("<", 0, m.start())
        out.append("%s | %s" % (path, h[s:m.end() + 250].replace("\n", " ")))
Path(__file__).with_name("_cleanup_bc_peek.txt").write_text("\n".join(out), encoding="utf-8")
print(len(out))
