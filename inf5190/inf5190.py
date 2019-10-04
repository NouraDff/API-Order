from flask import Flask, jsonify
import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

app = Flask(__name__)

@app.route('/',  methods=['GET'])
def index():
    url = "https://caissy.dev/shops/products"
    try:
        response = urlopen(url).read()
    except HTTPError as e:
        print("Error code : ", e.code)
    except URLError as e:
        print("Error code : ", e.reason) #load a jSON file with the error

    return json.loads(str(response, encoding='utf-8'))

@app.route('/order/<int:order_id>', methods=['POST'])
def order_product(order_id):
    return "Order" #return code 302 + link vers la commande nouvellement crée


if __name__ == '__main__':
    app.run(debug=True)
