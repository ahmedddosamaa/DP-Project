from OrderDecorator import OrderDecorator

class GiftNote(OrderDecorator):
    def __init__(self, order, note):
        super().__init__(order)
        self.note = note

    def get_description(self):
        return self.order.get_description() + f" with Gift Note: {self.note}"

    def calculate_total(self):
        return self.order.calculate_total() + 30
