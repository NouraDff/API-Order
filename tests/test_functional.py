import pytest
import json


from inf5190.models import Product, Order

class TestRoutes(object):
    def test_index(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert Product.select().count() == 5


    def test_post_order_redirection(self, app, client):
        with app.app_context():
            #get product
            client.get("/")
            #post valid order
            response = client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
            assert response.status_code == 302
            #post valid order but out_of_stock
            response = client.post("/order", json={ "product": { "id": 1232, "quantity": 2 } })
            assert response.status_code == 422
            #post order where id_product to not exist in products
            response2 = client.post("/order", json={ "product": { "id": 12488, "quantity": 2 } })
            assert response2.status_code == 422
            #post order missing id field
            response2 = client.post("/order", json={ "product": { "quantity": 2 } })
            assert response2.status_code == 422

    def test_get_order_by_id(self, app, client):
        with app.app_context():
            #get products
            client.get("/")
            #post order
            client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
            #get existing order
            response3 = client.get("/order/1")
            assert response3.status_code == 200
            #get non-existant order
            response4 = client.get("/order/3")
            assert response4.status_code == 404


    def test_put_order_by_id(self, app, client):
        with app.app_context():
            #get product
            client.get("/")
            #post order
            client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
            #try payment without email and shipping info entered. 
            response = client.put("/order/1", json = {"credit_card" : {
                                                    "name" : "John Doe",
                                                    "number" : "4242 4242 4242 4242",
                                                    "expiration_year" : 2024,
                                                    "cvv" : "123",
                                                    "expiration_month" : 9
                                                    }
                                                    })
            assert response.status_code == 422
            assert json.loads(response.data) == dict({"errors": 
            {"order": {"code": "missing-fields", "name": "Les informations du client sont nécessaire avant d'appliquer une carte de crédit"}}})
            #put valid shipping info
            response = client.put("/order/1", json = {"order" : {
                                                    "email" : "nouradjaffri@gmail.com",
                                                    "shipping_information" : {
                                                    "country" : "Canada",
                                                    "address" : "7645 15e avenue",
                                                    "postal_code" : "H2A 2V4",
                                                    "city" : "Montréal",
                                                    "province" : "QC"
                                                    }
                                                    }
                                                    })
            assert response.status_code == 200
            #Put email empty string 
            response = client.put("/order/1", json = {"order" : {
                                                    "email" : "",
                                                    "shipping_information" : {
                                                    "country" : "Canada",
                                                    "address" : "7645 15e avenue",
                                                    "postal_code" : "H2A 2V4",
                                                    "city" : "Montréal",
                                                    "province" : "QC"
                                                    }
                                                    }
                                                    })
            assert response.status_code == 422
            assert json.loads(response.data) == dict({"errors": {"order": {"code": "missing-fields", "name": "Il manque un ou plusieurs champs qui sont obligatoire"}}})
            #put with missing fields
            response = client.put("/order/1", json = {"order" : {
                                                    "email" : "toto@gmail.com",
                                                    "shipping_information" : {
                                                    "postal_code" : "H2A 2V4",
                                                    "city" : "Montréal",
                                                    "province" : "QC"
                                                    }
                                                    }
                                                    })
            assert response.status_code == 422
            assert json.loads(response.data) == dict({"errors": {"order": {"code": "missing-fields", "name": "Il manque un ou plusieurs champs qui sont obligatoire"}}})
            #try to put in non_existant order
            response = client.put("/order/7", json = {"order" : {
                                                    "email" : "nouradjaffri@gmail.com",
                                                    "shipping_information" : {
                                                    "country" : "Canada",
                                                    "address" : "7645 15e avenue",
                                                    "postal_code" : "H2A 2V4",
                                                    "city" : "Montréal",
                                                    "province" : "QC"
                                                    }
                                                    }
                                                    })
            assert response.status_code == 404
