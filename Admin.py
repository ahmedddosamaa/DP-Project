from User import User
from Order import Order
from Book import Book
from DatabaseManager import DatabaseManager
class Admin (User):

    # Attributes for the Admin class
    def __init__(self, username, password):
        super().__init__(username, password)

    def add_book(self):
        # Method to add a new book
        db_manager= DatabaseManager()
        db_manager.insert_book()

    def edit_book(self, ISBN, title, author, price, stock, edition, category):
        """Edit a book's details in the database."""
        db_manager = DatabaseManager()
        query = """
        UPDATE books 
        SET title=?, author=?, price=?, stock=?, edition=?, category=?
        WHERE ISBN=?
        """
        db_manager.execute_query(query, (title, author, price, stock, edition, category, ISBN))

    def delete_book(self, ISBN):
        """Delete a book from the database by its ISBN."""
        db_manager=DatabaseManager()

        query = "DELETE FROM books WHERE ISBN = ?"
            # Execute the query
        db_manager.execute_query(query, (ISBN,))
        
        # Check if the book was deleted
        
        print(f"Book with ISBN {ISBN} has been deleted successfully.")



    def manage_categories(self):
        # Method to manage book categories
        pass

    def view_orders(self):
        
        # Method to view customer orders
        """Retrieve and display all orders from the database."""
        query = "SELECT * FROM orders"
        self.cursor.execute(query)
        orders = self.cursor.fetchall()

        # Print orders in a readable format
        print("Order ID | Customer ID | Order Date              | Status")
        print("-" * 50)
        for order in orders:
            print(f"{order[0]:<8} | {order[1]:<11} | {order[2]} | {order[3]}")
        
        return orders

    def confirm_order(self, order_id):
        """
        Confirm an order and update the sold count for each book in the order.
        Args:
            order_id: The ID of the order to confirm
        Raises:
            Exception: If order isn't in pending status
        """
        db_manager = DatabaseManager()
        
        # Check order status first
        query = "SELECT status FROM orders WHERE order_id = ?"
        order_status = db_manager.fetch_one_entry(query, (order_id,))
        
        if not order_status:
            raise Exception("Order not found")
        
        if order_status[0].lower() != 'pending':
            raise Exception("Only pending orders can be confirmed")
        
        # Update order status to confirmed
        self.update_status("confirmed", order_id)
        
        # Get all books in this order with their quantities
        query = """
        SELECT book_isbn, quantity 
        FROM order_books 
        WHERE order_id = ?
        """
        order_books = db_manager.fetch_all_entries(query, (order_id,))
        
        # Update sold count and stock for each book
        for book_isbn, quantity in order_books:
            # Get current sold count and stock
            get_book_query = "SELECT sold, stock FROM books WHERE ISBN = ?"
            book_data = db_manager.fetch_one_entry(get_book_query, (book_isbn,))
            
            if book_data:
                current_sold = book_data[0] or 0  # Use 0 if sold is NULL
                current_stock = book_data[1]
                
                new_sold = current_sold + quantity
                new_stock = current_stock - quantity
                
                # Update both sold count and stock
                update_query = "UPDATE books SET sold = ?, stock = ? WHERE ISBN = ?"
                db_manager.execute_query(update_query, (new_sold, new_stock, book_isbn))

    def cancel_order(self, order_id):
        """
        Cancel an order if it's in pending status
        Args:
            order_id: The ID of the order to cancel
        Raises:
            Exception: If order isn't in pending status
        """
        db_manager = DatabaseManager()
        
        # Check order status
        query = "SELECT status FROM orders WHERE order_id = ?"
        order_status = db_manager.fetch_one_entry(query, (order_id,))
        
        if not order_status:
            raise Exception("Order not found")
        
        if order_status[0].lower() != 'pending':
            raise Exception("Only pending orders can be cancelled")
        
        # Update order status to cancelled
        self.update_status("cancelled", order_id)


    def top_selling_books(self):
        """Generate sales statistics for top-selling books from confirmed orders."""
        query = """
        SELECT ISBN, title, author, sold
        FROM books
        ORDER BY sold DESC
        LIMIT 3;
        """
        
        db_manager = DatabaseManager()
        top_books = db_manager.fetch_all_entries(query)
        return top_books
    
    def top_categories(self):
        """Retrieve the top 3 sold categories from confirmed orders."""
        query = """
        SELECT category, SUM(sold) AS total_sold
        FROM books
        GROUP BY category
        ORDER BY total_sold DESC
        LIMIT 3;
        """
        db_manager = DatabaseManager()
        results = db_manager.fetch_all_entries(query)
        return results
        
    def stock_level(self):
        """Retrieve and display each book with its available stock quantity."""
        query = """
        SELECT ISBN, title, stock
        FROM books
        ORDER BY stock DESC;
        """
        db_manager = DatabaseManager()
        books = db_manager.fetch_all_entries(query)
        return books


    def generate_statistics(self):
        # Method to generate sales statistics
        self.top_selling_books()
        self.top_categories()
        self.stock_level()

    def update_status(self, status, order_id):
        #method to update statud of an order
        db_manager = DatabaseManager()
        query = "UPDATE orders SET status = ? WHERE order_id= ?"
        db_manager.execute_query(query, (status, order_id))
        self.status = status        
    
    def clone_book(self, isbn):
        """Clone a book from an existing one in the database."""
        db_manager = DatabaseManager()
        query = """
        SELECT title, author, price, category, stock, edition, cover_image_path, sold, reviews
        FROM books WHERE ISBN = ?
        """
        book_data = db_manager.fetch_one_entry(query, (isbn,))
        
        if not book_data:
            raise ValueError("Book not found")
        
        # Create a Book instance with the fetched data
        original_book = Book(
            title=book_data[0],
            author=book_data[1],
            price=book_data[2],
            category=book_data[3],
            stock=book_data[4],
            edition=book_data[5],
            cover_image=book_data[6],
            sold=book_data[7],
            reviews=book_data[8]
        )
        
        # Return the cloned book
        return original_book.clone()
    
    def ship_order(self, order_id):
        """
        Ship a confirmed order
        Args:
            order_id: The ID of the order to ship
        Raises:
            Exception: If order isn't in confirmed status
        """
        db_manager = DatabaseManager()
        
        # Check order status
        query = "SELECT status FROM orders WHERE order_id = ?"
        order_status = db_manager.fetch_one_entry(query, (order_id,))
        
        if not order_status:
            raise Exception("Order not found")
        
        if order_status[0].lower() != 'confirmed':
            raise Exception("Only confirmed orders can be shipped")
        
        # Update order status to shipped
        self.update_status("shipped", order_id)
    
