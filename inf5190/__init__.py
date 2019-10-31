from flask import Flask, jsonify, request
import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
import logging
from inf5190.models import init_app, Product
from functools import lru_cache
from  playhouse.shortcuts import model_to_dict



def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)


    @app.route('/',  methods=['GET'])
    def index():
        if(Product.select().count() <= 0):
            url = "https://caissy.dev/shops/products"
            try:
                response = urlopen(url).read()
            except HTTPError as e:
                print("Error code : ", e.code)
            except URLError as e:
                print("Error message : ", e.reason) #load a jSON file with the error
            jsonObject = json.loads(response)
            saveJsonToDB(jsonObject)
            
            return jsonObject
        else:
            list_products = []
            for product in Product.select():
                list_products.append(model_to_dict(product))
            dict_products = {}
            dict_products['products'] = list_products 
            return dict_products
            


    def saveJsonToDB(jsonObject):
        for d in jsonObject['products']:
            Product.create(**d)
    
        #return None

    @app.route('/order')
    def post_product():
        if request.headers['Content-Type'] == 'application/json':

            return request.data
    


    @app.route('/order/<int:order_id>', methods=['POST', 'GET'])
    def get_product(order_id):


        return "Order"
    
    
    return app

