from Order import Order
from Book import Book
from Customer import Customer
from User import User
from Admin import Admin
import hashlib
from DatabaseManager import DatabaseManager
from OrderDecorator import OrderDecorator
from StandardOrder import StandardOrder
from ExpressOrder import ExpressOrder
from Customization import Customization
from GiftNote import GiftNote

def hash_password(password):
    """Helper method to hash passwords"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register(username, password, role, address=None, phone=None):
    """Register a new user"""
    hashed_password = hash_password(password)
    
    db_manager = DatabaseManager()

    # Check if user already exists
    query = "SELECT * FROM users WHERE username = ?"
    db_manager.cursor.execute(query, (username,))
    user_exists = db_manager.cursor.fetchone()
    if user_exists:
        print("User already registered.")
        return False
    db_manager.insert_user(username, hashed_password, role, address, phone)

    return True

def login(username, password):
    """Login an existing user"""
    hashed_password = hash_password(password)
    db_manager = DatabaseManager()

    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    db_manager.cursor.execute(query, (username, hashed_password))
    user = db_manager.cursor.fetchone()
    
    return user[0], user[1], user[2], user[3], user[4]

if __name__ == "__main__":
# # Create an original book instance
#     original_book = Book(
#         title="The Great Gatsby",
#         author="F. Scott Fitzgerald",
#         price=10.99,
#         category="Fiction",
#         stock=20,
#         edition="1st",
#         cover_image="gatsby_cover.jpg"
#     )

    order = StandardOrder()
    order.book_list = [{'title': 'Book 1', 'price': 15}, {'title': 'Book 2', 'price': 20}]
    order.discount = 5

    # Add decorators
    order = GiftNote(order, "HBD")
    order = Customization(order, "Maryam")

    print(order.get_description())  # Standard Order with a Gift Card with Customization with a Gift Receipt
    print(order.calculate_total())  # Calculates the total considering all decorators

    print("----------")

    order = StandardOrder()
    order.book_list = [{'title': 'Book 1', 'price': 15}, {'title': 'Book 2', 'price': 20}]
    order.discount = 5

    # Add decorators
    order = GiftNote(order, "HBD")
    order = Customization(order, "thankyou")

    print(order.get_description())  # Standard Order with a Gift Card with Customization with a Gift Receipt
    print(order.calculate_total())  # Calculates the total considering all decorators
