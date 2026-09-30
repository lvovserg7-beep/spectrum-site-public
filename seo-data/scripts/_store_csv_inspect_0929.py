import csv, io, json, re
P = r'C:\Users\ALSN_LSA\Desktop\Спектр\store-163322-202609291141.csv'
raw = open(P, 'rb').read()
print('crlf', raw.count(b'\r\n'), 'lf', raw.count(b'\n'), 'qmark-bullet', raw.count(b'? '), 'fffd', raw.count('\ufffd'.encode()))
t = raw.decode('utf-8')
rows = list(csv.reader(io.StringIO(t, newline=''), delimiter=';'))
h = rows[0]
print(len(rows) - 1, 'rows')
ix = {k: i for i, k in enumerate(h)}
SKUS = ['2900002159738','2900002159820','2900002159639','2900002159325','2900002159394',
        '4601546116697','4601546080875','2900002153033','4601546142894']
ns = {'__file__': 'x'}
src = open(r'c:\Users\ALSN_LSA\Desktop\Спектр\cursor\Сайт\seo-data\scripts\_build_dups_html_0929.py', encoding='utf-8').read()
m = re.search(r'^PRODUCTS\s*=.*?^\]', src, re.S | re.M)
print(m.group(0)[:3000])
for r in rows[1:]:
    if r[ix['SKU']] in SKUS or any(s in r[ix['Title']] for s in ['ПРОФ Клиентская лицензия на 50', 'на 100', 'на 300', 'на 500']):
        print(json.dumps({k: r[ix[k]] for k in ['Tilda UID','SKU','Parent UID','Title','SEO title','SEO descr']}, ensure_ascii=False))
