from flask import Flask, jsonify, request, redirect, Response
import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
import logging
from inf5190.models import init_app, Product, Order
from functools import lru_cache
from  playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import SqliteExtDatabase
from inf5190.services import Services




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

    @app.route('/order', methods=['POST'])
    def post_product():
        if request.headers['Content-Type'] == 'application/json':

            id =  request.json['product']['id']
            qty =  request.json['product']['quantity']
            order = Product.select().where(Product.id == id).get()
            product = model_to_dict(order)
            if(product['in_stock'] == True):
                price = product['price']*2
                new_order = Order.create(
                    total_price=price,
                    email="",
                    paid=False,
                    credit_card={},
                    shipping_information={},
                    transaction={},
                    product=request.json['product'],
                    shipping_price=0,
                )
            else:
                return Response(json.dumps({'errors': {
                    'product' : {
                        'code' : 'out-of-inventory,',
                        'name' : "Le produit demandé n'est pas en inventaire"
                        }}}), status=422)
            
            location = "/order/{}".format(new_order.id)

            return redirect(location, 302)
    


    @app.route('/order/<int:order_id>', methods=['POST', 'GET'])
    def get_product(order_id):
        if request.method == 'GET':
            order = Order.select().where(Order.id == order_id).get()
            the_order = model_to_dict(order)
          



        dict_order = {}
        dict_order['order'] = the_order

        return dict_order
    
    
    return app

