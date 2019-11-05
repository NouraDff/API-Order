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
from peewee import DoesNotExist


def create_app(initial_config=None):
    app = Flask("inf5190")
    init_app(app)


    @app.route('/',  methods=['GET'])
    def index():
        """Returns a list of product in a json format

        Data are retrieve from the external api "https://caissy.dev/shops/products" and saved in the database.
        If data are already saved in the database we then retrieve the data from there. 

        Return : json of the products
        """
        if(Product.select().count() <= 0):
            #get products
            url = "https://caissy.dev/shops/products"
            response = urlopen(url).read()
            
            #Save data to database           
            jsonObject = json.loads(response)
            for d in jsonObject['products']:
                Product.create(**d)
            return Response(json.dumps(jsonObject, ensure_ascii=False), mimetype='application/json')   

        #if data are already saved in the db we retrieved them     
        else:
            list_products = []
            for product in Product.select():
                list_products.append(model_to_dict(product))
            dict_products = {}
            dict_products['products'] = list_products 
            return Response(json.dumps(dict_products, ensure_ascii=False), mimetype='application/json')    


    @app.route('/order', methods=['POST'])
    def post_product():
        """Return a redirection to the newly created order

        This function will first check if the data send by the POST request are complete 
        and then will create a new order in the database if the product is not out of stock.

        Return : redirect to order/<order_id> 
                 else error message in json format
        """
        if request.headers['Content-Type'] == 'application/json':
            try:
                # it retrieves the id of the product in the db and check if the key quantity is not missing
                product_db = Product.select().where(Product.id == request.json['product']['id']).get()
                qty = request.json['product']['quantity']
            except (DoesNotExist, KeyError) as error:
                #failed to find the id or the fiel quantity
                return Response(json.dumps({'errors': {
                    'product' : {
                        'code' : 'missing-fields',
                        'name' : "La création d'une commande nécessite un produit"
                        }}},  ensure_ascii=False), status=422)
                
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
                        }}}, ensure_ascii=False), status=422)
            
            location = "/order/{}".format(new_order.id)

            return redirect(location, 302)
    
    
    @app.route('/order/<int:order_id>', methods=['GET'])
    def get_order(order_id):
        """Returns the order as dict     
        The function will calculate shipping_price if not already saved in the db. 

        Paramater: 
            order_id(int): id of the order

        Return: order(json): the order retrieved from the database
        """    
        try:
            order_bd = Order.select().where(Order.id == order_id).get()
        except DoesNotExist:
            return Response(json.dumps({'errors': {
                'order' : {
                'code' : '404',
                'name' : "Not Found - La commande n'existe pas"
                }}}, ensure_ascii=False), status=404)

        order = model_to_dict(order_bd)        
        #check if shipping_price is not already set
        if order['shipping_price'] == 0 :
            shipping_price = calculate_shipping_price(order)
            order_bd.shipping_price = shipping_price 
            order_bd.save()
      
       
        return add_key_order_to_json(order)


    def calculate_shipping_price(order):
        """Returns the calculated shipping price based en the weigth and the quantity. 
        
        Parameter:
            order(dict): the order retrieved from the database in which we calculate shipping_price.
        
        Return: shipping_price(int): the value of the shipping price.  
        """
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
        return order['shipping_price']
            

    @app.route('/order/<int:order_id>', methods=['PUT'])
    def edit_order(order_id):
        """Return a dict of the order with the updates applied. 
        The function first check if the id exist and there's no missing fields 
        Manage:
        - the update of the email and the shipping address
        - the payment with credit card by a post request to an external api. 
        Parameter: 
            order_id(int) : id of the order. 
        Return: the order with the updated field
                else message error
        """ 
        try:
            order_db = Order.select().where(Order.id == order_id).get()                
        except DoesNotExist:
            return Response(json.dumps({'errors': {
                'order' : {
                'code' : '404',
                'name' : "Not Found - La commande n'existe pas"
                }}}, ensure_ascii=False), status=404)
    
        
        if 'order' in request.json:  
            try: 
                 verify_missing_field(request.json)
            except (Exception, KeyError):
                return Response(json.dumps({'errors': {
                    'order' : {
                    'code' : 'missing-fields',
                    'name' : "Il manque un ou plusieurs champs qui sont obligatoire"
                    }}}, ensure_ascii=False), status=422)

            order_db.email = request.json['order']['email']
            order_db.shipping_information = request.json['order']['shipping_information']
            order_db.save()
            order = model_to_dict(order_db)  
            return add_key_order_to_json(order)

        elif 'credit_card' in request.json:
            try:
                dict_order = {}
                dict_order['order'] = model_to_dict(order_db)
                verify_missing_field(dict_order)
            except (Exception, KeyError):
                return Response(json.dumps({"errors" : {
                    "order": {
                    "code": "missing-fields",
                    "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"
                    }}}, ensure_ascii=False), status=422)

            order = model_to_dict(order_db)      
            request.json["amount_charged"] = order['shipping_price'] + order['total_price']
            try:
               confirmation = post_payment_api()
            except HTTPError as error:
                data = json.load(error)
                return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json', status=422)
                 
            if confirmation['transaction']['success'] == True :
                order_db.credit_card = confirmation['credit_card']
                order_db.transaction = confirmation['transaction']
                order_db.paid = True
                order_db.save()
                        
            return add_key_order_to_json(model_to_dict(order_db))       
        

    def post_payment_api():
        """Return the response of the call to the external api. 
        Return: confirmatio(json): transaction information else message error
        """
        req = Request("https://caissy.dev/shops/pay", headers={'Host' : 'caissy.dev', 'Content-Type':'application/json'} , method='POST')
        data = json.dumps(request.json).encode("utf8")
        res = urlopen(req, data).read()
        confirmation = res.decode('utf8')
        confirmation = json.loads(confirmation)
        return confirmation



    def add_key_order_to_json(order):
        """Retrun the order with the key order. 
        Parameter: order(dict): order from the database
        Return: JSON of the order with its key 'order'
        """
        dict_order = {}
        dict_order['order'] = order
        return Response(json.dumps(dict_order, ensure_ascii=False), mimetype='application/json')
        

    def verify_missing_field(data):
        """
        Verify if all required information are there as the email and the shipping information
        Parameter: data(dict): data where we check for missing field
        Raise Exception and KeyError if the key is not find or if the email field is empty or null. 
        """
        if data['order']['email'] == None or data['order']['email'] == "":
            raise Exception
        data['order']['email']
        shipping_info = data['order']['shipping_information']
        shipping_info['country']
        shipping_info['address']
        shipping_info['postal_code']
        shipping_info['city']
        shipping_info['province']


    return app

