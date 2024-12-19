from User import User
from DatabaseManager import DatabaseManager
import hashlib
from StandardOrder import StandardOrder
from ExpressOrder import ExpressOrder
from Customization import Customization
from GiftNote import GiftNote

class Customer (User):
    # Attributes for the Customer class
    def __init__(self, username, password, address, phone):
        super().__init__(username, password)
        self.address = address
        self.phone = phone
        self.cart = {}

    def update_username(self, username):
        db_manager = DatabaseManager()
        query = "UPDATE users SET username = ? WHERE username = ?"
        db_manager.execute_query(query, (username, self.username))
        self.username = username

    def update_password(self, password):
        db_manager = DatabaseManager()
        query = "UPDATE users SET password = ? WHERE username = ?"
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        db_manager.execute_query(query, (hashed_password, self.username))
        self.password = password

    def update_address(self, address):
        db_manager = DatabaseManager()
        query = "UPDATE users SET address = ? WHERE username = ?"
        db_manager.execute_query(query, (address, self.username))
        self.address = address

    def update_phone(self, phone):
        db_manager = DatabaseManager()
        query = "UPDATE users SET phone = ? WHERE username = ?"
        db_manager.execute_query(query, (phone, self.username))
        self.phone = phone

    def add_to_cart(self, book_isbn):
        if book_isbn in self.cart:
            self.cart[book_isbn] += 1
        else:
            self.cart[book_isbn] = 1

    def remove_from_cart(self, book):
        if self.cart[book] == 1:
            del self.cart[book]
        else:
            self.cart[book] -= 1

    def place_order(self, shipping_type, gift_note=None, customization=None):
        """
        Place an order with optional decorators
        shipping_type: 'standard' or 'express'
        gift_note: optional message for gift note
        customization: optional name for customization
        gift_receipt: boolean to include gift receipt
        """
        if not self.cart:
            raise ValueError("Cart is empty")

        try:
            # Create base order based on shipping type
            if shipping_type.lower() == 'express':
                order = ExpressOrder()
            else:
                order = StandardOrder()

            # Set order details
            order.customer = self.username
            order.book_list = []
            order.shipping_method = shipping_type
            
            # Add books from cart to order
            db_manager = DatabaseManager()
            total = 0
            
            for book_isbn, quantity in self.cart.items():
                query = "SELECT title, price FROM books WHERE ISBN = ?"
                book_data = db_manager.fetch_one_entry(query, (book_isbn,))
                if book_data:
                    for _ in range(quantity):
                        book_info = {
                            'isbn': book_isbn,
                            'title': book_data[0],
                            'price': book_data[1]
                        }
                        order.book_list.append(book_info)
                        total += book_data[1]

            # Apply decorators if specified
            if gift_note:
                order = GiftNote(order, gift_note)
            if customization:
                order = Customization(order, customization)

            # Calculate final total with decorators
            order.total = order.calculate_total()

            # Insert order into database
            order_id = db_manager.insert_order(order)
            if not order_id:
                raise Exception("Failed to insert order into database")

            # Clear the cart after successful order
            self.cart.clear()
            
            return {
                'order_id': order_id,
                'description': order.get_description(),
                'total': order.total
            }

        except Exception as e:
            raise Exception(f"Order placement failed: {str(e)}")

    def view_order_status(self):
        # Method to view order status
        pass

    def cancel_order(self, order_id):
        """
        Cancel an order if it's in pending status
        Args:
            order_id: The ID of the order to cancel
        Raises:
            Exception: If order doesn't exist, isn't owned by this customer, or isn't in pending status
        """
        try:
            db_manager = DatabaseManager()
            
            # Check if order exists and belongs to this customer
            query = """
            SELECT status 
            FROM orders 
            WHERE order_id = ? AND customer_username = ?
            """
            order_status = db_manager.fetch_one_entry(query, (order_id, self.username))
            
            if not order_status:
                raise Exception("Order not found or doesn't belong to you")
            
            if order_status[0].lower() != 'pending':
                raise Exception("Only pending orders can be cancelled")
            
            # Update order status to cancelled
            update_query = "UPDATE orders SET status = 'Cancelled' WHERE order_id = ?"
            db_manager.execute_query(update_query, (order_id,))
            
        except Exception as e:
            raise Exception(f"Failed to cancel order: {str(e)}")

    def leave_review(self, ISBN, review):
        pass

    def adjust_quantity(self, book_isbn, amount):
        """
        Adjust the quantity of a book in the cart
        Args:
            book_isbn: The ISBN of the book to adjust
            amount: The amount to adjust by (+1 or -1)
        """
        if book_isbn in self.cart:
            new_quantity = self.cart[book_isbn] + amount
            if new_quantity <= 0:
                del self.cart[book_isbn]
            else:
                self.cart[book_isbn] = new_quantity






