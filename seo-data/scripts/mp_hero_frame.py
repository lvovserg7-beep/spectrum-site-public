# -*- coding: utf-8 -*-
"""Первый экран «в рамке» для страниц v3 (канон 30.09.2026, правило tilda-hero-frame.mdc).

Слева текст на белом, справа фото на всю высоту рамки, край фото уходит в белый до первого монитора.
CSS кладётся в конец единственного <style> в HEAD страницы, разметка заменяет <section class="hero"> в блоке B1.
"""

PHOTO = ("https://optim.tildacdn.com/tild3632-3333-4139-b730-663861323430/-/format/webp/"
         "allsun-hero-mp-emplo.jpg.webp")

HERO_CSS = """/* первый экран в рамке (.hf) */
.v3 .hf{padding:8px 0 0;--h:clamp(400px,36vw,460px)}
.v3 .hf .frame{position:relative;height:var(--h);border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff}
.v3 .hf .txt{position:relative;z-index:2;width:calc(100% - var(--h)*16/9*.95);height:100%;padding:36px 8px 36px 40px;display:flex;flex-direction:column;box-sizing:border-box}
.v3 .hf .eyebrow{margin-bottom:16px}
.v3 .hf h1{font-size:clamp(38px,3.3vw,48px);line-height:1.05;margin:0 0 16px}
.v3 .hf .lead{font-size:16px;line-height:1.5;margin:0 0 20px;max-width:none}
.v3 .hf .btns{margin:auto 0 0;gap:10px;flex-wrap:wrap}
.v3 .hf .btns .btn{padding:14px 18px;font-size:15px;white-space:nowrap}
.v3 .hf .ph{position:absolute;top:0;right:0;bottom:0;aspect-ratio:16/9}
.v3 .hf .ph img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover;object-position:50% 50%}
.v3 .hf .veil{position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,#fff 0%,#fff 5%,rgba(255,255,255,.7) 6.5%,rgba(255,255,255,.3) 8%,rgba(255,255,255,0) 9.5%)}
.v3 .hf .who{position:absolute;z-index:3;right:16px;bottom:16px;font-size:12.5px;line-height:1.3;padding:7px 12px;border-radius:10px;background:rgba(255,255,255,.92);color:var(--ink);border:1px solid var(--line)}
.v3 .hf .who b{font-weight:600}
@media(min-width:1001px) and (max-width:1240px){.v3 .hf .txt{padding:26px 8px 26px 32px}.v3 .hf h1{font-size:36px;margin-bottom:12px}.v3 .hf .eyebrow{margin-bottom:12px}.v3 .hf .lead{font-size:15px;line-height:1.45;margin-bottom:14px}.v3 .hf .btns{gap:8px}.v3 .hf .btns .btn{padding:12px 16px}}
@media(min-width:1001px) and (max-width:1140px){.v3 .hf .txt{width:340px}.v3 .hf .ph{aspect-ratio:auto;width:calc(100% - 318px)}.v3 .hf .ph img{object-position:100% 50%}.v3 .hf .veil{background:linear-gradient(90deg,#fff 0%,#fff 3%,rgba(255,255,255,.5) 4.5%,rgba(255,255,255,0) 6%)}.v3 .hf .eyebrow{font-size:12px}}
@media(max-width:1000px){
.v3 .hf .frame{display:flex;flex-direction:column;height:auto}
.v3 .hf .txt{width:auto;height:auto;padding:0 20px 24px;margin-top:-6px}
.v3 .hf .ph{position:relative;order:-1;aspect-ratio:auto;padding-top:62.5%}
.v3 .hf .ph img{bottom:auto;height:auto;aspect-ratio:16/10;object-position:40% 25%}
.v3 .hf .veil{bottom:auto;aspect-ratio:16/10;background:linear-gradient(180deg,rgba(255,255,255,0) 60%,#fff 100%)}
.v3 .hf h1{font-size:44px}
.v3 .hf .lead{font-size:17px}
.v3 .hf .who{position:static;margin:8px 20px 18px;padding:0;background:none;border:0;border-radius:0;font-size:13px;line-height:1.4;color:var(--mut)}
.v3 .hf .who b{color:var(--ink)}
.v3 .hf .btns .btn{width:100%;justify-content:center}
}"""


def hero_html(eyebrow, h1, lead, btns, alt, who, photo=PHOTO):
    """eyebrow/h1/lead/btns - готовые куски разметки как на странице, alt - текст, who - HTML подписи."""
    return (f'<section class="hf"><div class="in"><div class="frame">'
            f'<div class="txt">{eyebrow}{h1}{lead}{btns}</div>'
            f'<div class="ph"><img src="{photo}" alt="{alt}" fetchpriority="high"><div class="veil"></div>'
            f'<div class="who">{who}</div></div></div></div></section>')
