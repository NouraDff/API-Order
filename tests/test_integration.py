import pytest
import json


from inf5190.models import Product, Order

class TestRoutesAPIExterne(object):
    def test_credit_card_API(self, app, client):
        with app.app_context():
            #get products
            client.get("/")
            #post order
            client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
            #put shipping information
            client.put("/order/1", json = {"order" : {"email" : "nouradjaffri@gmail.com",
                                                    "shipping_information" : {
                                                    "country" : "Canada",
                                                    "address" : "7645 15e avenue",
                                                    "postal_code" : "H2A 2V4",
                                                    "city" : "Montréal",
                                                    "province" : "QC"}} })
            #valid transaction                                        
            response = client.put("/order/1", json = {"credit_card" : {
                                                    "name" : "John Doe",
                                                    "number" : "4242 4242 4242 4242",
                                                    "expiration_year" : 2024,
                                                    "cvv" : "123",
                                                    "expiration_month" : 9
                                                    }
                                                    })
            assert response.status_code == 200
            #4 number in cvv
            response = client.put("/order/1", json = {"credit_card" : {
                                                            "name" : "John Doe",
                                                            "number" : "4242 4242 4242 4242",
                                                            "expiration_year" : 2024,
                                                            "cvv" : "1234",
                                                            "expiration_month" : 9
                                                            }
                                                            })
            assert response.status_code == 422
            assert json.loads(response.data) == dict({"errors": {"credit_card":
            {"code": "invalid-card","name": "Le champ cvv doit être composé de 3 chiffres" }}})
            #expired credit card
            response = client.put("/order/1", json = {"credit_card" : {
                                                            "name" : "John Doe",
                                                            "number" : "4242 4242 4242 4242",
                                                            "expiration_year" : 2018,
                                                            "cvv" : "123",
                                                            "expiration_month" : 9
                                                            }
                                                            })
            assert response.status_code == 422
            #invalid credit card
            response = client.put("/order/1", json = {"credit_card" : {
                                                            "name" : "John Doe",
                                                            "number" : "4000 0000 0000 0002",
                                                            "expiration_year" : 2024,
                                                            "cvv" : "123",
                                                            "expiration_month" : 9
                                                            }
                                                            })
            assert response.status_code == 422
            assert json.loads(response.data) == dict({ "errors": 
            {"credit_card": {"code": "card-declined","name": "La carte de crédit a été déclinée."}}})
           