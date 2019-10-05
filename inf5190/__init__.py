from flask import Flask, jsonify
import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
import logging
from inf5190.models import init_app, Product



def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)


    @app.route('/',  methods=['GET', 'POST'])
    def index():
        url = "https://caissy.dev/shops/products"
        try:
            response = urlopen(url).read()
        except HTTPError as e:
            print("Error code : ", e.code)
        except URLError as e:
            print("Error code : ", e.reason) #load a jSON file with the error
        jsonObject = json.loads(response)
        saveJsonToDB(jsonObject)
        return jsonObject

    def saveJsonToDB(jsonObject):
        
        return None

    @app.route('/order/<int:order_id>', methods=['POST'])
    def order_product(order_id):
        return "Order"
    
    
    return app

