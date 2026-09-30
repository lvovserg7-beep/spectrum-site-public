import re
GEN = r'c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_build_dups_html_0929.py'
OUT = r'c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\yandex\recrawl-2026-09-29.txt'
body = re.search(r'^PRODUCTS\s*=.*?^\]', open(GEN, encoding='utf-8').read(), re.S | re.M).group(0)
PRODUCTS = eval(body.split('=', 1)[1], {'PB': 0, 'LIC': 0, 'KA': 0})
urls = [
    'https://alsn.ru/development1c',
    'https://alsn.ru/erp-time-price',
    'https://alsn.ru/kompleksnaya_avtomatizaciya',
    'https://alsn.ru/vesii',
    'https://alsn.ru/event-2025-06',
    'https://alsn.ru/event-2025-06-----old1',
    'https://alsn.ru/event-marketplaces',
    'https://alsn.ru/products',
    'https://alsn.ru/dopolnitelnie_licenzii',
]
for _, _, items in PRODUCTS:
    urls += ['https://alsn.ru' + u for u, _ in items]
assert len(urls) == len(set(urls)) == 26
import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write('\n'.join(urls) + '\n')
print(len(urls))
