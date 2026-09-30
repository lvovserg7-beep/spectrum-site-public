# -*- coding: utf-8 -*-
"""Чистка tier2-breadcrumbs-wave-2026-09-28.html: убрать В-1 и В-2."""
import re
from pathlib import Path

F = Path(__file__).parent.parent / "tilda-briefs" / "tier2-breadcrumbs-wave-2026-09-28.html"
raw = F.read_text(encoding="utf-8")
s = raw


def sub1(pat, rep, flags=re.S):
    global s
    new, n = re.subn(pat, rep, s, count=1, flags=flags)
    assert n == 1, pat
    s = new


sub1(r'<section class="task" id="v1">.*?</section>\n', "")
sub1(r'<section class="task" id="v2">.*?</section>\n', "")
sub1(r'<li><a href="#v1">.*?</li><li><a href="#v2">.*?</li>', "")
sub1(r'<p class="muted">Проверка живого alsn.ru: 28.09.2026 ·',
     '<p class="muted">Первая версия 28.09.2026, сверка с живым alsn.ru 29.09.2026 ·')
sub1(r'<span class="pill warn">2 страницы с лишним кодом</span>', "")
sub1(r'(<div class="callout ok"><strong>Уже готово, не трогать:</strong>.*?</div>)',
     r'\1\n<div class="callout ok"><strong>Уже сделано - не трогать</strong><ul style="margin:6px 0 0;padding-left:18px;">'
     r'<li>В-1: из HEAD страницы «Кейсы» (<code>/cases</code>) удалён чужой код кейса СЦ со старым адресом <code>/caseecom</code>, остался один путь «Главная / Кейсы» - проверено на сайте 29.09.2026.</li>'
     r'<li>В-2: из HEAD кейса РЭК (<code>/vesii</code>) убран сломанный код кейса СЦ, служебный путь теперь «Кейс «РЭК»» - проверено на сайте 29.09.2026 (делали по Д-1б из <code>tier2-dubli-title-description-2026-09-29.html</code>).</li>'
     r'</ul></div>')
sub1(r'<code>cases</code>, <code>vesii</code>, ', "")
F.write_text(s, encoding="utf-8")
print(len(raw), "->", len(s), "dash", s.count("\u2014") + s.count("\u2013"))
