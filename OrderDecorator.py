from abc import ABC, abstractmethod
from Order import Order

class OrderDecorator(Order):
    def __init__(self, order):
        super().__init__()
        self.order = order

        self.customer = order.customer
        self.book_list = order.book_list
        self.status = order.status
        self.shipping_method = order.shipping_method
        self.total = order.total

    def __getattr__(self, name):
        # Delegate attribute access to the wrapped order
        return getattr(self.order, name)

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def calculate_total(self):
        pass
