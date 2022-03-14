import requests

option = {'Referer': 'http://finance.sina.com.cn'}
result = requests.get('http://w.sinajs.cn/?list=nf_SA2205', headers=option).text
print(result)

