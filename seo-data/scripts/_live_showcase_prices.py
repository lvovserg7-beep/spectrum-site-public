# -*- coding: utf-8 -*-
"""Live Tilda showcase prices vs 1C recommended. Read-only."""
from __future__ import annotations

import json
import re
import urllib.request
from html import unescape
from pathlib import Path

import xlrd

XLS = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\prices\price_1c.xls")
OUT = Path(r"C:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\prices\_live-showcase-prices.txt")

PAGES = [
    "https://alsn.ru/dopolnitelnie_licenzii",
    "https://alsn.ru/its",
    "https://alsn.ru/1cfresh",
]


def load_rec() -> dict[str, float]:
    wb = xlrd.open_workbook(str(XLS))
    sh = wb.sheet_by_index(0)
    rec: dict[str, float] = {}
    for r in range(2, sh.nrows):
        v = sh.cell_value(r, 0)
        if v in ("", None):
            continue
        if isinstance(v, float) and v == int(v):
            sku = str(int(v))
        else:
            sku = str(v).strip()
        if not sku:
            continue
        cur = str(sh.cell_value(r, 3)).strip().lower()
        if cur and cur not in ("руб.", "руб", "rub", "rur"):
            continue
        try:
            pf = float(sh.cell_value(r, 4))
        except (TypeError, ValueError):
            continue
        if pf > 0:
            rec[sku] = pf
    return rec


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def products_from_html(html: str) -> list[dict]:
    out = []
    # Tilda store JSON blobs
    for m in re.finditer(r"window\.products\s*=\s*(\[.*?\]);", html, re.S):
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            for p in data:
                if isinstance(p, dict):
                    out.append(p)
    for m in re.finditer(
        r'<div[^>]+class="[^"]*js-product[^"]*"[^>]*>', html, re.I
    ):
        pass
    # data-product-sku / price attributes
    for m in re.finditer(
        r'data-product-sku="([^"]*)"[^>]*data-product-price="([^"]*)"',
        html,
        re.I,
    ):
        out.append({"sku": unescape(m.group(1)), "price": m.group(2), "src": "attr"})
    for m in re.finditer(
        r'data-product-price="([^"]*)"[^>]*data-product-sku="([^"]*)"',
        html,
        re.I,
    ):
        out.append({"sku": unescape(m.group(2)), "price": m.group(1), "src": "attr2"})
    return out


def norm_sku(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (int, float)):
        return str(int(v))
    return str(v).strip()


def money(v) -> float | None:
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace(" ", "").replace("\xa0", "").replace(",", ".")
    s = re.sub(r"[^\d.]", "", s)
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def main() -> None:
    rec = load_rec()
    lines = ["проверка живых витрин alsn.ru vs прайс 1С 16.09.2026"]
    all_items = []
    for url in PAGES:
        html = fetch(url)
        title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
        items = []
        # tilda catalog: tilda-catalog-*.js inline json
        for pat in (
            r'"sku"\s*:\s*"([^"]+)"[^}]{0,400}?"price"\s*:\s*"?([\d.]+)"?',
            r'"price"\s*:\s*"?([\d.]+)"?[^}]{0,400}?"sku"\s*:\s*"([^"]+)"',
        ):
            pass
        # product cards in store JSON
        blobs = re.findall(r"var\s+tstore_products\s*=\s*(\{.*?\});", html, re.S)
        blobs += re.findall(r"window\.tstore_products\s*=\s*(\{.*?\});", html, re.S)
        for raw in products_from_html(html):
            sku = norm_sku(raw.get("sku") or raw.get("SKU") or raw.get("uid"))
            price = money(raw.get("price") or raw.get("Price"))
            name = raw.get("title") or raw.get("name") or ""
            if sku:
                items.append((sku, price, str(name)[:80]))

        # fallback: itemprop
        blocks = re.findall(
            r'itemtype="https://schema.org/Product".*?</div>\s*</div>',
            html,
            re.S | re.I,
        )
        sku_price_pairs = re.findall(
            r'itemprop="sku"[^>]*>([^<]+)</[^>]+>.*?itemprop="price"[^>]*content="([^"]+)"',
            html,
            re.S | re.I,
        )
        sku_price_pairs += re.findall(
            r'itemprop="price"[^>]*content="([^"]+)".*?itemprop="sku"[^>]*>([^<]+)<',
            html,
            re.S | re.I,
        )
        for a, b in sku_price_pairs:
            if a.replace(".", "").isdigit() or not b.replace(".", "").isdigit():
                sku, price = a.strip(), money(b)
            else:
                sku, price = b.strip(), money(a)
            items.append((sku, price, ""))

        # js-store-prod-price + nearby sku
        for m in re.finditer(
            r'data-product-gen-uid="(\d+)"[^>]*>.*?js-product-sku[^>]*>([^<]+)<.*?js-product-price[^>]*>([^<]+)<',
            html,
            re.S | re.I,
        ):
            items.append((m.group(2).strip(), money(m.group(3)), m.group(1)))

        # simpler: all sku + following price in 800 chars
        for m in re.finditer(
            r'(?:артикул|арт\.|sku)[^0-9A-Za-zА-Яа-я]{0,20}([A-Za-zА-Яа-я]*\d[\dA-Za-z._-]*)',
            html,
            re.I,
        ):
            pass

        lines.append("")
        lines.append(f"=== {url}")
        lines.append(f"title: {title}")
        lines.append(f"html_len {len(html)}")
        # dump distinctive markers
        for marker in ("tstore", "js-store", "data-product-price", "itemprop=\"price\"", "js-product-price"):
            lines.append(f"  marker {marker}: {html.lower().count(marker.lower())}")
        uniq = {}
        for sku, price, name in items:
            if sku:
                uniq[sku] = (price, name)
        lines.append(f"parsed products {len(uniq)}")
        all_items.append((url, html, uniq))

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUT)
    for url, html, uniq in all_items:
        print(url, "parsed", len(uniq), "len", len(html))


if __name__ == "__main__":
    main()
