import pytest

from inf5190.models import Product, Order

class TestRoutes(object):
    def test_empty_index(self, app, client):
        with app.app_context():
            response = client.get("/")
            assert response.status_code == 200
            assert Product.select().count() == 5

    
