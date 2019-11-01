from inf5190.models import Product, Order

class Services(object):
    @classmethod
    def create_new_order_from_post_data(cls, post_data):
        order = Order.create(
            total_price=0,
            email="",
            credit_card="",
            shipping_information="",
            paid=False,
            transaction="",
            product=0,
            shipping_price=0,
        )

        return order
