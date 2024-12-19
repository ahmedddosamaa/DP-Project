from Order import Order
# Concrete Component 1
class StandardOrder(Order):
    def get_description(self):
        return "Standard Order"

    def calculate_total(self):
        self.total = sum(book['price'] for book in self.book_list)
        return self.total
