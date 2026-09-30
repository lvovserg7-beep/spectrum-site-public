import re, zipfile, html, json

FILES = {
    'description': r'C:\Users\ALSN_LSA\Downloads\alsn.ru_5393361f057d96302826a6ea.xlsx',
    'title': r'C:\Users\ALSN_LSA\Downloads\alsn.ru_f25bf58936f374e6ee9acef7.xlsx',
}
out = {}
for kind, f in FILES.items():
    x = zipfile.ZipFile(f).read('xl/worksheets/sheet1.xml').decode('utf-8')
    groups = []
    for row in re.findall(r'<row r="\d+">(.*?)</row>', x, re.S):
        cells = dict(re.findall(r'<c r="([A-D])\d+"[^>]*?(?:/>|>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)?</c>)', row) and
                     [(m[0], html.unescape(m[1] or m[2])) for m in re.findall(r'<c r="([A-D])\d+"[^>]*?(?:/>|>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)?</c>)', row)])
        if cells.get('A') and cells['A'] != 'Value':
            groups.append({'value': cells['A'], 'count': cells.get('B'), 'urls': []})
        elif cells.get('C') and groups:
            groups[-1]['urls'].append((cells['C'], cells.get('D')))
    out[kind] = groups
    print('=====', kind, len(groups))
    for g in groups:
        print(g['count'], '|', g['value'])
        for u in g['urls']:
            print('    ', u[0], u[1])
json.dump(out, open('_wm-dups-2026-09-29.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
