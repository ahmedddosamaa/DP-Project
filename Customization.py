from OrderDecorator import OrderDecorator
# Concrete Decorator 2
class Customization(OrderDecorator):
    def __init__(self, order, name):
        super().__init__(order)
        self.customization_name = name

    def get_description(self):
        return self.order.get_description() + f" with Customization name: {self.customization_name}"

    def calculate_total(self):
        return self.order.calculate_total() + 50

