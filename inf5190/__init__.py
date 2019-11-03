from flask import Flask, jsonify, request, redirect, Response, abort
import json
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
from urllib import parse, error
import logging
from inf5190.models import init_app, Product, Order
from functools import lru_cache
from  playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import SqliteExtDatabase
from inf5190.services import Services




def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)


    ###
    # TODO
    #
    #
    #
    ###
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
            
            #Save data to database           
            jsonObject = json.loads(response)
            for d in jsonObject['products']:
                Product.create(**d)
            return jsonObject

        #if data are already saved in the db    
        else:
            list_products = []
            for product in Product.select():
                list_products.append(model_to_dict(product))
            dict_products = {}
            dict_products['products'] = list_products 
            return dict_products
            

        
    
    
    ###
    # TODO
    #
    #
    #
    ###
    @app.route('/order', methods=['POST'])
    def post_product():
        if request.headers['Content-Type'] == 'application/json':
            try:
                product_db = Product.select().where(Product.id == request.json['product']['id']).get()
                qty = request.json['product']['quantity']
            except:
                return Response(json.dumps({'errors': {
                    'product' : {
                        'code' : 'missing-fields',
                        'name' : "La création d'une commande nécessite un produit"
                        }}}), status=422)
                
            product = model_to_dict(product_db)
            if(product['in_stock'] == True):
                price = product['price']*2
                new_order = Order.create(
                    total_price=price,
                    email=None,
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
                        'code' : 'out-of-inventory',
                        'name' : "Le produit demandé n'est pas en inventaire"
                        }}}), status=422)
            
            location = "/order/{}".format(new_order.id)

            return redirect(location, 302)
    

    ###
    # TODO
    #
    #
    #
    ###
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        if request.method == 'GET':
            try:
                order_bd = Order.select().where(Order.id == order_id).get()
            except:
                return abort(404)
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

    ###
    # TODO
    #
    #
    #
    ###
    @app.route('/order/<int:order_id>', methods=['PUT'])
    def edit_order(order_id):
        
        if 'order' in request.json:
            try:
                order_db = Order.select().where(Order.id == order_id).get() 
            except:
                return abort(404)
            try:
                if request.json['order']['email'] == None or request.json['order']['email'] == "":
                    return Response(json.dumps({'errors': {
                        'order' : {
                        'code' : 'missing-fields',
                        'name' : "Il manque un ou  plusieurs champs qui sont obligatoire"
                        }}}), status=422)
                
                shipping_info = request.json['order']['shipping_information']
                shipping_info['country']
                shipping_info['address']
                shipping_info['postal_code']
                shipping_info['city']
                shipping_info['province']
                    
            except:
                return Response(json.dumps({'errors': {
                        'order' : {
                        'code' : 'missing-fields',
                        'name' : "Il manque un ou plusieurs champs qui sont obligatoire"
                        }}}), status=422)
            

            order_db.email = request.json['order']['email']
            order_db.shipping_information = request.json['order']['shipping_information']
            order_db.save()
            order = Order.select().where(Order.id == order_id).get()
            order = model_to_dict(order)  

            dict_order = {}
            dict_order['order'] = order
            return dict_order

        elif 'credit_card' in request.json:
            order_db = Order.select().where(Order.id == order_id).get()
            order = model_to_dict(order_db) 
            if order['email'] == None or order['shipping_information'] == {}:
                return Response(json.dumps({'errors': {
                        'order' : {
                        'code' : 'missing-fields',
                        'name' : "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                        }}}), status=422)


            total_amount = order['shipping_price'] + order['total_price']

            request.json["amount_charged"] = total_amount
            
            try:
                req = Request("https://caissy.dev/shops/pay", headers={'Host' : 'caissy.dev', 'Content-Type':'application/json'} , method='POST')
                data = json.dumps(request.json).encode("utf8")
                res = urlopen(req, data).read()
                confirmation = res.decode('utf8')
                confirmation = json.loads(confirmation)
            except HTTPError as error:
                data = json.load(error)
                return data
                 
  
            if confirmation['transaction']['success'] == True :
                order_db.credit_card = confirmation['credit_card']
                order_db.transaction = confirmation['transaction']
                order_db.paid = True
                order_db.save()
            
            order = model_to_dict(order_db)   
            dict_order = {}
            dict_order['order'] = order
            return dict_order
            


        
    return app

