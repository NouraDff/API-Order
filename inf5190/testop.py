from urllib.request import urlopen
import json

url = "https://caissy.dev/shops/products"
response = urlopen(url).read()
jsonObject = json.loads(response)
for d in jsonObject['products']:
    for key, value in d.items() : 
        print(d, d['name'])