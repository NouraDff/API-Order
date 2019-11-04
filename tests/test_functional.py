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
            client.get("/")
            response1 = client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
            assert response1.status_code == 302
            response2 = client.post("/order", json={ "product": { "id": 12488, "quantity": 2 } })
            assert response2.status_code == 422

    def test_get_order_by_id(self, app, client):
        with app.app_context():
            client.get("/")
            client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
            response3 = client.get("/order/1")
            assert response3.status_code == 200
            response4 = client.get("/order/3")
            assert response4.status_code == 404


    def test_put_order_by_id(self, app, client):
        with app.app_context():
            client.get("/")
            client.post("/order", json={ "product": { "id": 1248, "quantity": 2 } })
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
            msg_error_missing_field = dict({"errors": {"order": {"code": "missing-fields", "name": "Il manque un ou plusieurs champs qui sont obligatoire"}}})
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
            assert json.loads(response.data) == msg_error_missing_field
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
            assert json.loads(response.data) == msg_error_missing_field
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
            response = client.put("/order/1", json = {"credit_card" : {
                                                    "name" : "John Doe",
                                                    "number" : "4242 4242 4242 4242",
                                                    "expiration_year" : 2024,
                                                    "cvv" : "1234",
                                                    "expiration_month" : 9
                                                    }
                                                    })
            assert response.status_code == 422
            response = client.put("/order/1", json = {"credit_card" : {
                                                    "name" : "John Doe",
                                                    "number" : "4242 4242 4242 4242",
                                                    "expiration_year" : 2018,
                                                    "cvv" : "123",
                                                    "expiration_month" : 9
                                                    }
                                                    })
            assert response.status_code == 422
            response1 = client.put("/order/1", json = {"credit_card" : {
                                                    "name" : "John Doe",
                                                    "number" : "4000 0000 0000 0002",
                                                    "expiration_year" : 2024,
                                                    "cvv" : "123",
                                                    "expiration_month" : 9
                                                    }
                                                    })
            assert response1.status_code == 422
            response = client.put("/order/1", json = {"credit_card" : {
                                                    "name" : "John Doe",
                                                    "number" : "4242 4242 4242 4242",
                                                    "expiration_year" : 2024,
                                                    "cvv" : "123",
                                                    "expiration_month" : 9
                                                    }
                                                    })
            assert response.status_code == 200
