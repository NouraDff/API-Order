import pytest
import inf5190

from inf5190.models import Product, Order

class TestProduct(object):
    def test_init_product(self):
        p = Product(id=123, 
        name ='CatCool',
        in_stock = True,
        description = "Very cool product",
        price = 1234,
        weight= 700,
        image = "http://placekitten.com/200/300")

        assert p.id == 123
        assert p.name =='CatCool'
        assert p.in_stock == True
        assert p.description == "Very cool product"
        assert p.price == 1234
        assert p.weight == 700
        assert p.image == "http://placekitten.com/200/300"

class TestOrder(object):
     def test_init_order(self):
        o = Order(id=123, 
        total_price = 598,
        email = "toto@gmail.com",
        credit_card = {},
        shipping_information = {},
        paid = False,
        transaction = {},
        product = {},
        shipping_price = 0)

        assert o.id == 123
        assert o.total_price == 598
        assert o.email == "toto@gmail.com"
        assert o.credit_card == {}
        assert o.shipping_information == {}
        assert o.paid == False
        assert o.transaction == {}
        assert o.product == {}
        assert o.shipping_price == 0

 
