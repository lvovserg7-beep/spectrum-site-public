import json, re, urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def get(p):
    return urllib.request.urlopen(urllib.request.Request('https://alsn.ru' + p, headers={'User-Agent': UA})).read().decode('utf-8')


for p, r in [('/vtt', '1131768636'), ('/perehod-s-ut-na-unf', '1266450781'), ('/merlion', '4022017101')]:
    h = get(p)
    i = h.find('id="rec' + r + '"')
    s = h[i - 50:i + 3000]
    print('==', p)
    print(re.findall(r'(?:background-color:[^;"]+|background-image:[^;"]+|data-original="[^"]+"|data-bg-color="[^"]+"|t-bgimg|t-cover__filter[^>]{0,200})', s)[:15])

d = json.load(open('_bc-all-2026-09-28.json', encoding='utf-8'))
want = ['/outsorce_vs_inhouse', '/review', '/merlion', '/ocs', '/marvel', '/treolan', '/3logic', '/constr', '/etm-ipro',
        '/perehod-s-upp-na-ka-unf-ut', '/cracasesoftvideo', '/persons/interw_lvov']
for x in d:
    if x['path'] in want:
        print(x['path'], x['style'], x['crumb'][:90], '| ld', x['last_ld'], x['name_match'], x['n_lists'], x['last_url_ok'])
