from abc import ABC, abstractmethod
from DatabaseManager import DatabaseManager

class Order(ABC):
    def __init__(self):
        self.customer = None
        self.book_list = []
        self.status = "Pending"
        self.shipping_method = "Standard"
        self.total = 0


    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def calculate_total(self):
        pass
    
    def update_status(self,status):
        # Method to update the order status
        self.status=status


    