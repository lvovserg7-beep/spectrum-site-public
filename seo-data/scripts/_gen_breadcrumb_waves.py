# -*- coding: utf-8 -*-
from pathlib import Path

HOME_SVG = """  <a href="https://alsn.ru/" aria-label="Главная" title="Главная" style="display:inline-flex;color:inherit;text-decoration:none;">
    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.2 3 10.8V21h6.2v-6.5h5.6V21H21V10.8L12 3.2z"/></svg>
  </a>"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def uid(slug: str) -> str:
    return slug.replace("/", "-").replace("_", "-")


def nav2(name: str, dark: bool = False) -> str:
    color = "#cfcfcf" if dark else "#8a8a8a"
    op_slash = ".55" if dark else ".45"
    op_name = ".85" if dark else ".75"
    return f"""<nav aria-label="Хлебные крошки" style="display:flex;align-items:center;flex-wrap:nowrap;font-size:14px;line-height:1.2;color:{color};padding:12px 20px 8px;">
{HOME_SVG}
  <span style="margin:0 6px;opacity:{op_slash};" aria-hidden="true">/</span>
  <span style="opacity:{op_name};white-space:nowrap;">{name}</span>
</nav>"""


def nav3(mid_url: str, mid_name: str, name: str, dark: bool = False) -> str:
    color = "#cfcfcf" if dark else "#8a8a8a"
    op_slash = ".55" if dark else ".45"
    op_name = ".85" if dark else ".75"
    return f"""<nav aria-label="Хлебные крошки" style="display:flex;align-items:center;flex-wrap:nowrap;font-size:14px;line-height:1.2;color:{color};padding:12px 20px 8px;">
{HOME_SVG}
  <span style="margin:0 6px;opacity:{op_slash};" aria-hidden="true">/</span>
  <a href="{mid_url}" style="color:inherit;text-decoration:none;white-space:nowrap;">{mid_name}</a>
  <span style="margin:0 6px;opacity:{op_slash};" aria-hidden="true">/</span>
  <span style="opacity:{op_name};white-space:nowrap;">{name}</span>
</nav>"""


def bc2(slug: str, name: str) -> str:
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": "https://alsn.ru/{slug}#breadcrumb",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{name}", "item": "https://alsn.ru/{slug}" }}
  ]
}}
</script>"""


def bc3(slug: str, mid_name: str, mid_url: str, name: str) -> str:
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": "https://alsn.ru/{slug}#breadcrumb",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://alsn.ru/" }},
    {{ "@type": "ListItem", "position": 2, "name": "{mid_name}", "item": "{mid_url}" }},
    {{ "@type": "ListItem", "position": 3, "name": "{name}", "item": "https://alsn.ru/{slug}" }}
  ]
}}
</script>"""


def box(box_id: str, raw_html: str) -> str:
    return (
        f'      <div class="copybox"><pre id="{box_id}">{esc(raw_html)}</pre>'
        f'<button type="button" data-copy="{box_id}">Копировать</button></div>'
    )


def page_block(slug: str, title: str, html: str, bc: str | None, note: str | None = None) -> str:
    parts = [f'      <h3><a href="https://alsn.ru/{slug}">/{slug}</a> - {title}</h3>']
    if note:
        parts.append(f'      <div class="callout warn">{note}</div>')
    parts.append('      <p class="muted"><strong>На экран (T123)</strong></p>')
    parts.append(box(f"c-html-{uid(slug)}", html))
    if bc:
        parts.append('      <p class="muted"><strong>В HEAD (BreadcrumbList)</strong></p>')
        parts.append(box(f"c-bc-{uid(slug)}", bc))
    else:
        parts.append('      <p class="muted">BreadcrumbList уже есть - не дублировать.</p>')
    return "\n".join(parts)


wave_a = [
    ("about_us", "О компании", "О компании"),
    ("contacts", "Контакты", "Контакты"),
    ("vacancy", "Вакансии", "Вакансии"),
    ("cra", "ЦРА", "ЦРА"),
    ("clients", "Клиенты", "Клиенты"),
    ("bitrix24", "Битрикс24", "Битрикс24"),
    ("telegram1c", "Telegram-бот 1С", "Telegram-бот 1С"),
    ("cases", "Кейсы", "Кейсы"),
]

wave_b = [
    ("etm-ipro", "ЭТМ iPRO"),
    ("merlion", "Мерлион"),
    ("ocs", "OCS"),
    ("marvel", "Марвел"),
    ("treolan", "Treolan"),
    ("3logic", "3logic"),
]

wave_c = [
    ("products", "Продукты", 2, None),
    ("1cbitrix", "Интеграция Битрикс24 и 1С", 2, None),
    ("buhv8", "1С:Бухгалтерия", 2, None),
    ("zup8", "1С:ЗУП", 2, None),
    ("upt8", "1С:УТ", 2, None),
    ("upravlenie_nashei_firmoi", "1С:УНФ", 2, None),
    ("dokumentooborot8", "1С:Документооборот", 2, None),
    ("perehod-s-upp-na-ka-unf-ut", "Переход с УПП", 3, "dev"),
    ("integrationsite", "Интеграция с сайтом", 2, None),
    ("integrationeco", "Интеграция с экосистемой", 2, None),
    ("blog", "Блог", 2, None),
    ("internship", "Стажировка", 2, None),
    ("persons", "Команда", 2, None),
    ("review", "Отзывы", 2, None),
    ("amo_crm", "amoCRM", 2, None),
    ("whatsapp", "WhatsApp-бот 1С", 2, None),
    ("crmfurniture", "CRM для мебели", 2, None),
    ("outsorce_vs_inhouse", "Аутсорс или штат", 2, None),
    ("case_telegram_bot", "Кейсы Telegram-ботов", 3, "cases"),
    ("moy-sklad-perenos-v-1s", "Переход с МойСклад", 2, None),
    ("perevystavlenie-uslug-posledney-mili-ozon-v-1s", "Перевыставление Озон", 2, None),
]

chunks: list[str] = []

chunks.append("<!-- WAVE_A_START -->")
for slug, title, name in wave_a:
    note = None
    if slug == "cases":
        note = (
            "В HEAD сейчас чужой BreadcrumbList про кейс ООО «СЦ». "
            "Старый блок <code>BreadcrumbList</code> удалить и вставить код ниже. "
            "Не оставлять два."
        )
    chunks.append(page_block(slug, title, nav2(name), bc2(slug, name), note))
chunks.append("<!-- WAVE_A_END -->")

chunks.append("<!-- WAVE_B_START -->")
for slug, name in wave_b:
    html = nav3("https://alsn.ru/ecom", "Интеграция с поставщиками", name)
    bc = bc3(slug, "Интеграция с поставщиками", "https://alsn.ru/ecom", name)
    chunks.append(page_block(slug, name, html, bc))
chunks.append("<!-- WAVE_B_END -->")

case_name = "Интеграция 1С с поставщиками — ООО «СЦ»"
chunks.append("<!-- CASEECOMSC_START -->")
chunks.append(
    page_block(
        "caseecomsc",
        "кейс СЦ",
        nav3("https://alsn.ru/cases", "Кейсы", case_name),
        None,
        "Имя последнего звена совпадает с уже стоящим BreadcrumbList. Новый код в HEAD не добавлять.",
    )
)
chunks.append("<!-- CASEECOMSC_END -->")

chunks.append("<!-- WAVE_C_START -->")
for slug, name, levels, mid in wave_c:
    if levels == 3 and mid == "dev":
        html = nav3("https://alsn.ru/development1c", "Внедрение 1С", name)
        bc = bc3(slug, "Внедрение 1С", "https://alsn.ru/development1c", name)
    elif levels == 3 and mid == "cases":
        html = nav3("https://alsn.ru/cases", "Кейсы", name)
        bc = bc3(slug, "Кейсы", "https://alsn.ru/cases", name)
    else:
        html = nav2(name)
        bc = bc2(slug, name)
    chunks.append(page_block(slug, name, html, bc))
chunks.append("<!-- WAVE_C_END -->")

out_path = Path(__file__).resolve().parents[1] / "tilda-briefs" / "_wave_blocks.html"
out_path.write_text("\n".join(chunks), encoding="utf-8")
print(f"wrote {out_path} ({len(chunks)} chunks)")
