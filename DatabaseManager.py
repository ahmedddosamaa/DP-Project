import sqlite3
from sqlite3 import Error

class DatabaseManager:
    _instance = None  # To hold the single instance of the class
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance of DatabaseManager"""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize_db()
        return cls._instance

    def _initialize_db(self):
        """Initialize the database and create tables if they do not exist"""
        try:
            self.conn = sqlite3.connect('bookstore.db')
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Error as e:
            print(f"Error initializing the database: {e}")
        
    def create_tables(self):
        """Create the tables if they do not exist"""
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'customer')),
            address TEXT,
            phone TEXT,  
            orders TEXT  
        );
        """

        create_book_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            ISBN TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL,
            popularity INTEGER,
            stock INTEGER NOT NULL,
            cover_image_path TEXT,
            edition TEXT,
            category TEXT DEFAULT 'Undefined',
            sold INTEGER DEFAULT 0
            
        );
        """

        create_orders_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_username TEXT NOT NULL,
            status TEXT NOT NULL,
            total REAL NOT NULL,
            shipping_method TEXT NOT NULL,
            gift_note TEXT,
            customization TEXT,
            FOREIGN KEY (customer_username) REFERENCES users(username)
        );
        """

        create_order_books_table_query = """
        CREATE TABLE IF NOT EXISTS order_books (
            order_id INTEGER NOT NULL,
            book_isbn TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            PRIMARY KEY (order_id, book_isbn),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (book_isbn) REFERENCES books(ISBN)
        );
        """

        create_book_reviews_table_query = """
        CREATE TABLE IF NOT EXISTS book_reviews (
            ISBN TEXT NOT NULL,
            review TEXT NOT NULL,
            PRIMARY KEY (ISBN, review),
            FOREIGN KEY (ISBN) REFERENCES books(ISBN)
        );
        """
        
        try:
            self.cursor.execute(create_users_table_query)
            self.cursor.execute(create_book_table_query)
            self.cursor.execute(create_orders_table_query)
            self.cursor.execute(create_order_books_table_query)
            self.cursor.execute(create_book_reviews_table_query)
            self.conn.commit()
        except Error as e:
            print(f"Error creating tables: {e}")

    def execute_query(self, query, params=None):
        """Executes a query"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_one_entry(self, query, params=None):
        """Fetch a single entry from the database."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error fetching one entry: {e}")
            return None

    def fetch_all_entries(self, query, params=None):
        """Fetch multiple or all entries from the database."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Error as e:
            print(f"Error fetching all entries: {e}")
            return None

    
    # Methods for managing users (both customers and admins)
    def insert_user(self, username, password, role, address=None, phone=None):
        """Insert a user (customer or admin) into the database"""
        try:
            query = "INSERT INTO users (username, password, role, address, phone) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(query, (username, password, role, address, phone))
            self.conn.commit()
            print(f"{role.capitalize()} {username} inserted successfully.")
        except Error as e:
            print(f"Error inserting user: {e}")

    # Methods for managing books
    def insert_book(self, book):
        """Insert a book into the database using a Book instance"""
        try:
            query = """
            INSERT INTO books (ISBN, title, author, price, popularity, stock, cover_image_path, edition, category) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                book.getisbn(),
                book.gettitle(),
                book.getauthor(),
                book.getprice(),
                book.getpopularity(),
                book.getstock(),
                book.getcover_image(), 
                book.getedition(),
                book.getcategory()
            ))
            self.conn.commit()
            print(f"Book {book.gettitle()} inserted successfully.")
        except Error as e:
            print(f"Error inserting book: {e}")
    

    # Methods for managing orders
    def insert_order(self, order):
        """Insert an order into the database using an Order object"""
        try:
            # Extracting attributes safely
            customer_username = order.customer
            status = order.status
            total = order.total
            shipping_method = order.shipping_method
            
            # Check for gift note and customization attributes
            gift_note = getattr(order, 'note', None)  # Default to None if not present
            customization = getattr(order, 'customization_name', None)  # Default to None if not present

            # Insert order record
            query = """
            INSERT INTO orders (customer_username, status, total, shipping_method, gift_note, customization)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                customer_username,
                status,
                total,
                shipping_method,
                gift_note,
                customization
            ))
            order_id = self.cursor.lastrowid

            # Create a dictionary to track book quantities
            book_quantities = {}
            for book in order.book_list:
                isbn = book['isbn']
                if isbn in book_quantities:
                    book_quantities[isbn] += 1
                else:
                    book_quantities[isbn] = 1

            # Insert the books in the order_books table with their quantities
            for isbn, quantity in book_quantities.items():
                query = "INSERT INTO order_books (order_id, book_isbn, quantity) VALUES (?, ?, ?)"
                self.cursor.execute(query, (order_id, isbn, quantity))
            
            self.conn.commit()
            return order_id
        except Error as e:
            print(f"Error placing order: {e}")
            self.conn.rollback()  # Rollback in case of error
            return None


    def get_order(self, order_id):
        """Retrieve an order by ID along with the books in it"""
        try:
            query = """
            SELECT orders.order_id, orders.customer_id, orders.order_date, orders.status, order_books.book_isbn, order_books.quantity 
            FROM orders
            INNER JOIN order_books ON orders.order_id = order_books.order_id
            WHERE orders.order_id = ?
            """
            self.cursor.execute(query, (order_id,))
            order_details = self.cursor.fetchall()
            return order_details
        except Error as e:
            print(f"Error retrieving order: {e}")
            return None
    
    def close(self):
        """Close the database connection"""
        self.conn.close()

    def top_categories(self):
        # Top catgeories 
        """Retrieve the top 3 sold categories from the database."""
        query = """
        SELECT category, SUM(sold) AS total_sold
        FROM books
        GROUP BY category
        ORDER BY total_sold DESC
        LIMIT 3;
        """
        db_manager=DatabaseManager()
        results = db_manager.fetch_all_entries(query)
        print("Top 3 Sold Categories:")
        print("Category              | Total Sold")
        print("-" * 40)
        for row in results:
            print(f"{row[0]:<22} | {row[1]}")
        return results

    def get_categories(self):
        """Fetch all unique categories from books table"""
        try:
            query = "SELECT DISTINCT category FROM books ORDER BY category"
            self.cursor.execute(query)
            categories = [row[0] for row in self.cursor.fetchall()]
            return categories
        except Error as e:
            print(f"Error fetching categories: {e}")
            return []

    def get_total_books_sold(self):
        """Get the total number of books sold across all books"""
        query = "SELECT SUM(sold) FROM books"
        result = self.fetch_one_entry(query)
        return result[0] if result[0] is not None else 0

    def insert_book_review(self, isbn, review):
        """Insert a review for a book into the book_reviews table"""
        try:
            query = "INSERT INTO book_reviews (ISBN, review) VALUES (?, ?)"
            self.cursor.execute(query, (isbn, review))
            self.conn.commit()
            print(f"Review added successfully for book with ISBN: {isbn}")
            return True
        except Error as e:
            print(f"Error inserting review: {e}")
            return False

    def save_categories_to_file(self, categories):
        """Save all unique categories from the database to a file"""
        try:
            with open('categories.txt', 'w') as f:
                for category in categories:
                    f.write(f"{category}\n")
        except Exception as e:
            print(f"Error saving categories to file: {e}")

    def load_categories_from_file(self):
        """Load categories from file, create default if file doesn't exist"""
        try:
            with open('categories.txt', 'r') as f:
                categories = [line.strip() for line in f.readlines()]
                return categories
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading categories from file: {e}")