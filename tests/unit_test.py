import pytest

from inf5190.models import Product, Order

class TestProduct(object):
    def test_init(self):
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

