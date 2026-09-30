import urllib.request, re, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
u = 'https://alsn.ru/products/tproduct/946953291-241626506282-1s-predpriyatie-8-proizvodstvennaya-bezo?x=%d' % time.time()
h = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30).read().decode('utf-8', 'replace')
sp = re.search(r'storepart[a-z_]*["\':= ]+["\']?(\d{5,})', h).group(1)
a = 'https://store.tildaapi.com/api/getproduct/?storepartuid=%s&productuid=241626506282&x=%d' % (sp, time.time())
j = urllib.request.urlopen(urllib.request.Request(a, headers={'User-Agent': UA, 'Referer': 'https://alsn.ru/'}), timeout=30).read().decode('utf-8')
i = j.find('Бесплатн')
print(repr(j[max(0, i - 80):i + 40]))
