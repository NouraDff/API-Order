from urllib.request import urlopen
import json


jsonObject = { "product": { "id": 123, "quantity": 2 } }
print(jsonObject['product'])
print(jsonObject['product']['quantity'])
