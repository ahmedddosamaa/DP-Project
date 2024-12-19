from Order import Order
# Concrete Component 2
class ExpressOrder(Order):
    def __init__(self):
        super().__init__()
        self.shipping_method = "Express"

    def get_description(self):
        return "Express Order with faster delivery"

    def calculate_total(self):
        self.total = (
            sum(book['price'] for book in self.book_list) + 10  # Additional express fee
        )
        return self.total
