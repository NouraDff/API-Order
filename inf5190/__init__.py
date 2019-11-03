from flask import Flask, jsonify, request, redirect, Response
import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
from urllib import parse
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
            order = Product.select().where(Product.id == request.json['product']['id']).get()
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
    


    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        if request.method == 'GET':
            order_bd = Order.select().where(Order.id == order_id).get()
            order = model_to_dict(order_bd)
            
            product_id = order['product']['id']
            product = Product.select().where(Product.id == product_id).get() 
            product = model_to_dict(product)

            weight = product['weight'] * order['product']['quantity']
            if(weight <= 500):
                order['shipping_price'] = 500
            elif(weight <= 2000):
                order['shipping_price'] = 1000
            else:
                order['shipping_price'] = 2500

            order_bd.shipping_price =  order['shipping_price']
            order_bd.save()

            
        dict_order = {}
        dict_order['order'] = order

        return dict_order


    @app.route('/order/<int:order_id>', methods=['PUT'])
    def edit_order(order_id):
        
        if 'order' in request.json:
            query = Order.update(request.json['order']).where(Order.id == order_id)
            query.execute()
            order = Order.select().where(Order.id == order_id).get()
            order = model_to_dict(order)   

            dict_order = {}
            dict_order['order'] = order
            return dict_order

        elif 'credit_card' in request.json:
            order_db = Order.select().where(Order.id == order_id).get()
            order = model_to_dict(order_db) 
            total_amount = order['shipping_price'] + order['total_price']

            request.json["amount_charged"] = total_amount
    
            req = Request("https://caissy.dev/shops/pay", headers={'Host' : 'caissy.dev', 'Content-Type':'application/json'} , method='POST')
            data = json.dumps(request.json).encode("utf8")
            res = urlopen(req, data).read()
            confirmation = res.decode('utf8')
            confirmation = json.loads(confirmation)
            if confirmation['transaction']['success'] == True :
                order_db.credit_card = confirmation['credit_card']
                order_db.transaction = confirmation['transaction']
                order_db.paid = True
                order_db.save()
            
            order = model_to_dict(order_db)   
            dict_order = {}
            dict_order['order'] = order
            return dict_order
            

            #TODO check if all required info are there
            

        

    
    return app

