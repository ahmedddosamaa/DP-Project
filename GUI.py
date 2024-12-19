import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog 
from Book import Book
from Main import login, register
from Customer import Customer
from Admin import Admin
from DatabaseManager import DatabaseManager
from PIL import Image, ImageTk

class BookstoreGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bookstore Management System")
        self.root.geometry("800x600")
        
        # Initialize the database manager
        self.db_manager = DatabaseManager()
        
        # Initialize the login frame and current user
        self.current_frame = None
        self.current_user = None
        
        # Load categories when starting
        self.categories = self.db_manager.load_categories_from_file()
        
        # Bind the closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_login_frame()

    def on_closing(self):
        """Handle cleanup when the window is closing"""
        try:
            # Save categories to file
            self.db_manager.save_categories_to_file(self.categories)
        finally:
            # Close the window
            self.root.destroy()

    def show_login_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        # Create main container with gradient background
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill='both', expand=True)
        
        # Create left panel for image/logo (40% width)
        left_panel = tk.Frame(self.current_frame, bg='#2C3E50')
        left_panel.pack(side='left', fill='both', expand=True, padx=0)
        left_panel.pack_propagate(False)  # Prevent the frame from shrinking
        left_panel.configure(width=self.root.winfo_width() * 0.4)  # Set width this way
        
        # Add welcome text to left panel
        tk.Label(left_panel, text="Welcome Back!", 
                 font=('Helvetica', 32, 'bold'), 
                 fg='white', bg='#2C3E50').pack(pady=(100,10))
        tk.Label(left_panel, text="Please login to continue", 
                 font=('Helvetica', 12), 
                 fg='#BDC3C7', bg='#2C3E50').pack()

        # Create right panel for login form (60% width)
        right_panel = tk.Frame(self.current_frame, bg='white')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Create form container with padding
        form_frame = tk.Frame(right_panel, bg='white')
        form_frame.pack(pady=(80,0), padx=50)
        
        # Login header
        tk.Label(form_frame, text="Login", 
                 font=('Helvetica', 24, 'bold'), 
                 fg='#2C3E50', bg='white').pack(pady=(0,30))
        
        # Username field with custom styling
        username_frame = tk.Frame(form_frame, bg='white')
        username_frame.pack(fill='x', pady=10)
        tk.Label(username_frame, text="Username", 
                 font=('Helvetica', 10), 
                 fg='#7F8C8D', bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(username_frame, 
                                     font=('Helvetica', 12),
                                     bg='#ECF0F1',
                                     relief='flat',
                                     bd=0)
        self.username_entry.pack(fill='x', pady=(5,0), ipady=8)
        
        # Password field with custom styling
        password_frame = tk.Frame(form_frame, bg='white')
        password_frame.pack(fill='x', pady=10)
        tk.Label(password_frame, text="Password", 
                 font=('Helvetica', 10), 
                 fg='#7F8C8D', bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(password_frame, 
                                     show="•",
                                     font=('Helvetica', 12),
                                     bg='#ECF0F1',
                                     relief='flat',
                                     bd=0)
        self.password_entry.pack(fill='x', pady=(5,0), ipady=8)
        
        # Buttons with hover effect
        def on_enter(e):
            e.widget['background'] = '#2980B9'
        def on_leave(e):
            e.widget['background'] = '#3498DB'
        
        login_btn = tk.Button(form_frame, text="Login",
                             font=('Helvetica', 12, 'bold'),
                             fg='white', bg='#3498DB',
                             activebackground='#2980B9',
                             activeforeground='white',
                             relief='flat',
                             command=self.handle_login)
        login_btn.pack(fill='x', pady=(30,10), ipady=10)
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        
        # Register link
        register_frame = tk.Frame(form_frame, bg='white')
        register_frame.pack(pady=10)
        tk.Label(register_frame, text="Don't have an account? ", 
                 font=('Helvetica', 10), 
                 fg='#7F8C8D', bg='white').pack(side='left')
        register_link = tk.Label(register_frame, text="Register",
                                font=('Helvetica', 10, 'bold'),
                                fg='#3498DB', bg='white',
                                cursor='hand2')
        register_link.pack(side='left')
        register_link.bind("<Button-1>", lambda e: self.show_register_frame())

    def show_register_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        # Create main container
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill='both', expand=True)
        
        # Create left panel
        left_panel = tk.Frame(self.current_frame, bg='#2C3E50')
        left_panel.pack(side='left', fill='both', expand=True, padx=0)
        left_panel.pack_propagate(False)  # Prevent the frame from shrinking
        left_panel.configure(width=self.root.winfo_width() * 0.4)  # Set width this way
        
        # Add welcome text to left panel
        tk.Label(left_panel, text="Join Us!", 
                 font=('Helvetica', 32, 'bold'), 
                 fg='white', bg='#2C3E50').pack(pady=(100,10))
        tk.Label(left_panel, text="Create your account today", 
                 font=('Helvetica', 12), 
                 fg='#BDC3C7', bg='#2C3E50').pack()

        # Create right panel with scrollbar for registration form
        right_panel = tk.Frame(self.current_frame, bg='white')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(right_panel, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_panel, orient='vertical', command=canvas.yview)
        
        # Create form container
        form_frame = tk.Frame(canvas, bg='white')
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True, padx=(50,0))
        scrollbar.pack(side='right', fill='y')
        
        # Add form frame to canvas
        canvas.create_window((0,0), window=form_frame, anchor='nw', width=canvas.winfo_reqwidth())
        
        # Register header
        tk.Label(form_frame, text="Create Account", 
                 font=('Helvetica', 24, 'bold'), 
                 fg='#2C3E50', bg='white').pack(pady=(30,20))

        # Function to create styled entry fields
        def create_entry_field(parent, label_text, show=None):
            frame = tk.Frame(parent, bg='white')
            frame.pack(fill='x', pady=10)
            tk.Label(frame, text=label_text, 
                    font=('Helvetica', 10), 
                    fg='#7F8C8D', bg='white').pack(anchor='w')
            entry = tk.Entry(frame, 
                            show=show,
                            font=('Helvetica', 12),
                            bg='#ECF0F1',
                            relief='flat',
                            bd=0)
            entry.pack(fill='x', pady=(5,0), ipady=8)
            return entry

        # Create registration fields
        self.reg_username_entry = create_entry_field(form_frame, "Username")
        self.reg_password_entry = create_entry_field(form_frame, "Password", show="•")
        
        # Role selection with custom styling
        role_frame = tk.Frame(form_frame, bg='white')
        role_frame.pack(fill='x', pady=10)
        tk.Label(role_frame, text="Role", 
                 font=('Helvetica', 10), 
                 fg='#7F8C8D', bg='white').pack(anchor='w')
        
        self.role_var = tk.StringVar(value="customer")
        roles_frame = tk.Frame(role_frame, bg='white')
        roles_frame.pack(fill='x', pady=(5,0))
        
        # Styled radio buttons
        style = ttk.Style()
        style.configure("Custom.TRadiobutton",
                       background="white",
                       font=('Helvetica', 10))
        
        ttk.Radiobutton(roles_frame, text="Customer", 
                        variable=self.role_var,
                        value="customer",
                        style="Custom.TRadiobutton",
                        command=lambda: self.customer_fields_frame.pack(after=role_frame) if self.role_var.get() == "customer" else self.customer_fields_frame.pack_forget()).pack(side='left', padx=(0,20))
        ttk.Radiobutton(roles_frame, text="Admin", 
                        variable=self.role_var,
                        value="admin",
                        style="Custom.TRadiobutton",
                        command=lambda: self.customer_fields_frame.pack(after=role_frame) if self.role_var.get() == "customer" else self.customer_fields_frame.pack_forget()).pack(side='left')

        # Customer specific fields
        self.customer_fields_frame = tk.Frame(form_frame, bg='white')
        self.address_entry = create_entry_field(self.customer_fields_frame, "Address")
        self.phone_entry = create_entry_field(self.customer_fields_frame, "Phone")
        self.customer_fields_frame.pack(after=role_frame)

        # Buttons with hover effect
        def on_enter(e):
            e.widget['background'] = '#2980B9'
        def on_leave(e):
            e.widget['background'] = '#3498DB'

        # Register button
        register_btn = tk.Button(form_frame, text="Register",
                                font=('Helvetica', 12, 'bold'),
                                fg='white', bg='#3498DB',
                                activebackground='#2980B9',
                                activeforeground='white',
                                relief='flat',
                                command=self.handle_register)
        register_btn.pack(fill='x', pady=(20,10), ipady=10)
        register_btn.bind("<Enter>", on_enter)
        register_btn.bind("<Leave>", on_leave)

        # Back to login link
        login_frame = tk.Frame(form_frame, bg='white')
        login_frame.pack(pady=(0,30))
        tk.Label(login_frame, text="Already have an account? ", 
                 font=('Helvetica', 10), 
                 fg='#7F8C8D', bg='white').pack(side='left')
        login_link = tk.Label(login_frame, text="Login",
                             font=('Helvetica', 10, 'bold'),
                             fg='#3498DB', bg='white',
                             cursor='hand2')
        login_link.pack(side='left')
        login_link.bind("<Button-1>", lambda e: self.show_login_frame())

        # Configure canvas scrolling
        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            user_data = login(username, password)
            if user_data[2] == 'admin':
                self.current_user = Admin(username, password)
                self.show_admin_interface(user_data)
            else:
                self.current_user = Customer(username, password, user_data[3], user_data[4])
                self.show_customer_interface(user_data)
        except Exception as e:
            messagebox.showerror("Error", "Invalid username or password")

    def handle_register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.role_var.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        
        if register(username, password, role, address, phone):
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login_frame()
        else:
            messagebox.showerror("Error", "Registration failed!")

    def show_admin_interface(self, user_data):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(pady=20)

        tk.Label(self.current_frame, text=f"Welcome Admin: {user_data[0]}", font=('Arial', 24)).pack(pady=20)
        
        tk.Button(self.current_frame, text="Manage Books", command=self.manage_books).pack(pady=5)
        tk.Button(self.current_frame, text="Manage Categories", command=self.manage_book_categories).pack(pady=5)
        tk.Button(self.current_frame, text="View Orders", command=self.view_orders).pack(pady=5)
        tk.Button(self.current_frame, text="Statistics", command=self.manage_categories).pack(pady=5)
        tk.Button(self.current_frame, text="Logout", command=self.show_login_frame).pack(pady=20)

    def show_customer_interface(self, user_data):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(pady=20)

        tk.Label(self.current_frame, text=f"Welcome {user_data[0]}", font=('Arial', 24)).pack(pady=20)
        
        tk.Button(self.current_frame, text="Browse Books", command=self.browse_books).pack(pady=5)
        tk.Button(self.current_frame, text="View Cart", command=self.view_cart).pack(pady=5)
        tk.Button(self.current_frame, text="View Orders", command=self.view_customer_orders).pack(pady=5)
        tk.Button(self.current_frame, text="Update Profile", command=self.update_profile).pack(pady=5)
        tk.Button(self.current_frame, text="My Purchased Books", command=self.view_purchased_books).pack(pady=5)
        tk.Button(self.current_frame, text="Logout", command=self.show_login_frame).pack(pady=20)

    def show_add_book_form(self):
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add New Book")
        add_book_window.geometry("900x600")

        # Create main container frames
        left_frame = tk.Frame(add_book_window)
        left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill='both', expand=True)
        
        right_frame = tk.Frame(add_book_window)
        right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill='both', expand=True)

        # Add clone selection at the top
        clone_frame = tk.Frame(left_frame)
        clone_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(clone_frame, text="Clone existing book:").pack(side=tk.LEFT, padx=5)
        
        # Get books from database
        db_manager = DatabaseManager()
        query = "SELECT ISBN, title FROM books"
        books = db_manager.fetch_all_entries(query)
        book_list = [''] + [f"{book[0]} - {book[1]}" for book in books]  # Add empty option
        
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(clone_frame, textvariable=book_var, values=book_list, width=40)
        book_combo.pack(side=tk.LEFT, padx=5)

        # Create entries dictionary to store all entry fields
        entries = {}

        # Add regular fields
        fields = ['ISBN', 'Title', 'Author', 'Price', 'Stock', 'Edition']
        for field in fields:
            tk.Label(left_frame, text=f"{field}:").pack(pady=5)
            entry = tk.Entry(left_frame, width=40)
            entry.pack(pady=5, fill='x')
            entries[field.lower()] = entry

        # Category dropdown
        tk.Label(left_frame, text="Category:").pack(pady=5)
        category_var = tk.StringVar(value=self.categories[0])
        category_dropdown = ttk.Combobox(left_frame, 
                                    textvariable=category_var, 
                                    values=self.categories,
                                    state='readonly',
                                    width=37)
        category_dropdown.pack(pady=5, fill='x')

        # Image selection
        tk.Label(left_frame, text="Cover Image:").pack(pady=5)
        image_path_var = tk.StringVar()
        image_path_entry = tk.Entry(left_frame, textvariable=image_path_var, width=40)
        image_path_entry.pack(pady=5, fill='x')

        # Right side - Image preview
        preview_label = tk.Label(right_frame, text="No image selected")
        preview_label.pack(fill='both', expand=True)

        def load_image(filepath):
            try:
                image = Image.open(filepath)
                image = image.resize((200, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                preview_label.config(image=photo)
                preview_label.image = photo
            except Exception as e:
                preview_label.config(text="Failed to load image")

        def select_image():
            filepath = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if filepath:
                image_path_var.set(filepath)
                load_image(filepath)

        tk.Button(left_frame, text="Browse...", command=select_image).pack(pady=5)

        def add_book():
            try:
                # Get values from entries
                isbn = entries['isbn'].get()
                title = entries['title'].get()
                author = entries['author'].get()
                price = float(entries['price'].get())
                stock = int(entries['stock'].get())
                edition = entries['edition'].get()
                category = category_var.get()
                cover_image = image_path_var.get()

                # Validate required fields
                if not all([isbn, title, author, price, stock, category]):
                    messagebox.showerror("Error", "Please fill all required fields")
                    return

                # If a book was cloned, check if any field (except ISBN) was modified
                db_manager = DatabaseManager()
                if book_var.get():
                    original_isbn = book_var.get().split(' - ')[0]
                    query = """
                    SELECT *
                    FROM books WHERE ISBN = ?
                    """
                    original_book_data = db_manager.fetch_one_entry(query, (original_isbn,))
                    
                    if original_book_data:
                        # Fetch reviews for the original book
                        review_query = "SELECT review FROM book_reviews WHERE ISBN = ?"
                        reviews = db_manager.fetch_all_entries(review_query, (original_isbn,))
                        reviews_list = [review[0] for review in reviews]  # Extract reviews from tuples




                        # Create a Book instance from the original data, including reviews
                        original_book = Book(*original_book_data, reviews=reviews_list)
                        cloned_book_instance = original_book.clone()  # Clone the book

                        # Check if any field (except ISBN) was modified
                        if  all([
                            title == cloned_book_instance.gettitle(),
                            author == cloned_book_instance.getauthor(),
                            price == cloned_book_instance.getprice(),
                            stock == cloned_book_instance.getstock(),
                            edition == cloned_book_instance.getedition(),
                            category == cloned_book_instance.getcategory(),
                            cover_image == cloned_book_instance.getcover_image()
                        ]):
                            messagebox.showerror("Error", "Book already exists, please modify at least one field other than ISBN")
                            return
                    cloned_book_instance.setisbn(isbn)
                    cloned_book_instance.settitle(title)
                    cloned_book_instance.setauthor(author)
                    cloned_book_instance.setprice(price)
                    cloned_book_instance.setstock(stock)
                    cloned_book_instance.setcover_image(cover_image)
                    cloned_book_instance.setedition(edition)
                    cloned_book_instance.setcategory(category)
                    db_manager.insert_book(cloned_book_instance)
                else:
                    book = Book(isbn, title, author, price, 0, stock, cover_image, edition, category)
                    db_manager.insert_book(book)
                

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for price and stock")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {str(e)}")

        # Add Book button at the bottom
        tk.Button(left_frame, text="Add Book", command=add_book, width=30).pack(pady=20)

        def on_clone_select(event):
            if not book_var.get():
                return
            
            try:
                isbn = book_var.get().split(' - ')[0]
                query = """
                SELECT ISBN, title, author, price, stock, edition, category, cover_image_path
                FROM books WHERE ISBN = ?
                """
                db_manager = DatabaseManager()
                book_data = db_manager.fetch_one_entry(query, (isbn,))
                
                if book_data:
                    # Clear ISBN field (must be unique)
                    entries['isbn'].delete(0, tk.END)
                    
                    # Fill other fields with book data
                    entries['title'].delete(0, tk.END)
                    entries['title'].insert(0, book_data[1])
                    
                    entries['author'].delete(0, tk.END)
                    entries['author'].insert(0, book_data[2])
                    
                    entries['price'].delete(0, tk.END)
                    entries['price'].insert(0, str(book_data[3]))
                    
                    entries['stock'].delete(0, tk.END)
                    entries['stock'].insert(0, str(book_data[4]))
                    
                    entries['edition'].delete(0, tk.END)
                    entries['edition'].insert(0, book_data[5])
                    
                    category_var.set(book_data[6])
                    image_path_var.set(book_data[7])
                    
                    # Update image preview
                    if book_data[7]:
                        load_image(book_data[7])
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load book data: {str(e)}")

        # Bind the clone selection event
        book_combo.bind('<<ComboboxSelected>>', on_clone_select)
    

    def view_orders(self):
        # Create a new window for viewing orders
        orders_window = tk.Toplevel(self.root)
        orders_window.title("View Orders")
        orders_window.geometry("800x600")

        # Create a treeview to display orders
        tree = ttk.Treeview(orders_window, 
                           columns=('Order ID', 'Customer Username', 'Status', 'Shipping Method', 'Total'),
                           show='headings')
        
        # Set column headings
        for col in ('Order ID', 'Customer Username', 'Status', 'Shipping Method', 'Total'):
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(orders_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_orders():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
                
            # Get orders from database
            db_manager = DatabaseManager()
            query = """
            SELECT order_id, customer_username, status, shipping_method, total, customization, gift_note
            FROM orders
            ORDER BY order_id DESC
            """
            orders = db_manager.fetch_all_entries(query)
            
            # Insert orders into treeview
            if orders:
                for order in orders:
                    tree.insert('', tk.END, values=order)
        # Create frame for buttons
        button_frame = tk.Frame(orders_window)
        button_frame.pack(pady=10)

        # Add buttons
        tk.Button(button_frame, text="Refresh", command=refresh_orders).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="View Details", 
                 command=lambda: self.show_order_details(tree, orders_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Confirm Order", 
                 command=lambda: self.confirm_selected_order(tree, refresh_orders)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Ship Order", 
                 command=lambda: self.ship_selected_order(tree, refresh_orders)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel Order", 
                 command=lambda: self.cancel_selected_order(tree, refresh_orders)).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_orders()

    def manage_categories(self):
        # Create a new window for statistics
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Sales Statistics")
        stats_window.geometry("800x600")

        # Create notebook for different statistics views
        notebook = ttk.Notebook(stats_window)
        
        # Create frames for different views
        top_selling_frame = ttk.Frame(notebook)
        popular_categories_frame = ttk.Frame(notebook)
        stock_levels_frame = ttk.Frame(notebook)
        
        notebook.add(top_selling_frame, text='Top Selling')
        notebook.add(popular_categories_frame, text='Popular Categories')
        notebook.add(stock_levels_frame, text='Stock Levels')
        notebook.pack(expand=True, fill='both')

        # Top Selling Books
        def show_top_selling():
            # Clear previous content
            for widget in top_selling_frame.winfo_children():
                widget.destroy()
            
            # Create treeview for top selling books
            tree = ttk.Treeview(top_selling_frame, 
                               columns=('ISBN', 'Title', 'Author', 'Total Sold'),
                               show='headings')
            
            # Set column headings
            for col in ('ISBN', 'Title', 'Author', 'Total Sold'):
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # Get top selling books from admin
            top_books = self.current_user.top_selling_books()
            
            # Insert data into treeview
            for book in top_books:
                tree.insert('', tk.END, values=book)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(top_selling_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack the treeview and scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add refresh button
            tk.Button(top_selling_frame, text="Refresh", 
                     command=show_top_selling).pack(pady=10)

        # Initial load of top selling books
        show_top_selling()

        def show_popular_categories():
            # Clear previous content
            for widget in popular_categories_frame.winfo_children():
                widget.destroy()
            
            # Create treeview for popular categories
            tree = ttk.Treeview(popular_categories_frame, 
                               columns=('Category', 'Total Sold'),
                               show='headings')
            
            # Set column headings
            for col in ('Category', 'Total Sold'):
                tree.heading(col, text=col)
                tree.column(col, width=200)

            # Get popular categories from admin
            popular_categories = self.current_user.top_categories()
            
            if not popular_categories:
                # Show message if no data
                tk.Label(popular_categories_frame, 
                        text="No category data available", 
                        font=('Arial', 12)).pack(pady=20)
            else:
                # Insert data into treeview
                for category in popular_categories:
                    tree.insert('', tk.END, values=category)
                    
                # Add scrollbar
                scrollbar = ttk.Scrollbar(popular_categories_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                # Pack the treeview and scrollbar
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add refresh button
            tk.Button(popular_categories_frame, text="Refresh", 
                     command=show_popular_categories).pack(pady=10)

        # Initial load of popular categories
        show_popular_categories()

        def show_stock_levels():
            # Clear previous content
            for widget in stock_levels_frame.winfo_children():
                widget.destroy()
            
            # Create treeview for stock levels
            tree = ttk.Treeview(stock_levels_frame, 
                               columns=('ISBN', 'Title', 'Stock'),
                               show='headings')
            
            # Set column headings
            for col in ('ISBN', 'Title', 'Stock'):
                tree.heading(col, text=col)
                tree.column(col, width=200)

            # Get stock levels from admin
            stock_levels = self.current_user.stock_level()
            
            if not stock_levels:
                # Show message if no data
                tk.Label(stock_levels_frame, 
                        text="No books in inventory", 
                        font=('Arial', 12)).pack(pady=20)
            else:
                # Insert data into treeview
                for book in stock_levels:
                    tree.insert('', tk.END, values=book)
                    
                # Add scrollbar
                scrollbar = ttk.Scrollbar(stock_levels_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                # Pack the treeview and scrollbar
                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add refresh button
            tk.Button(stock_levels_frame, text="Refresh", 
                     command=show_stock_levels).pack(pady=10)

        # Initial load of stock levels
        show_stock_levels()

    def browse_books(self):
        books_window = tk.Toplevel(self.root)
        books_window.title("Browse Books")
        books_window.geometry("1200x800")  # Adjusted for better layout

        # Add search frame at the top
        search_frame = tk.Frame(books_window)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Create category filter
        category_var = tk.StringVar(value="All Categories")
        db_manager = DatabaseManager()
        categories = ["All Categories"] + db_manager.get_categories()
        category_filter = ttk.Combobox(search_frame, 
                                     textvariable=category_var, 
                                     values=categories, 
                                     state='readonly',
                                     width=20)
        category_filter.pack(side=tk.LEFT, padx=5)

        # Create scrollable frame
        main_frame = tk.Frame(books_window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        grid_frame = tk.Frame(canvas)

        grid_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def show_book_details(book_data):
            details_window = tk.Toplevel(books_window)
            details_window.title(f"Book Details - {book_data[1]}")
            details_window.geometry("600x800")

            # Create main container
            main_container = tk.Frame(details_window)
            main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Create frames for organization
            image_frame = tk.Frame(main_container)
            image_frame.pack(pady=10)

            details_frame = tk.Frame(main_container)
            details_frame.pack(pady=10, fill='x')

            reviews_frame = tk.LabelFrame(main_container, text="Reviews", font=('Arial', 10, 'bold'))
            reviews_frame.pack(pady=10, fill='both', expand=True)

            # Display image
            if book_data[7]:  # cover_image_path
                try:
                    image = Image.open(book_data[7])
                    image = image.resize((200, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    img_label = tk.Label(image_frame, image=photo)
                    img_label.image = photo
                    img_label.pack()
                except Exception:
                    tk.Label(image_frame, text="No Image Available").pack()

            # Book details with better formatting
            details = [
                ("Title", book_data[1]),
                ("Author", book_data[2]),
                ("ISBN", book_data[0]),
                ("Price", f"${book_data[3]:.2f}"),
                ("Stock", book_data[4]),
                ("Edition", book_data[5]),
                ("Category", book_data[6])
            ]

            for label, value in details:
                detail_frame = tk.Frame(details_frame)
                detail_frame.pack(fill='x', pady=2)
                tk.Label(detail_frame, text=f"{label}:", font=('Arial', 10, 'bold'), 
                        width=15, anchor='e').pack(side=tk.LEFT, padx=10)
                tk.Label(detail_frame, text=str(value), 
                        font=('Arial', 10)).pack(side=tk.LEFT, padx=10)

            # Create scrollable reviews area
            reviews_canvas = tk.Canvas(reviews_frame)
            reviews_scrollbar = ttk.Scrollbar(reviews_frame, orient="vertical", 
                                            command=reviews_canvas.yview)
            reviews_container = tk.Frame(reviews_canvas)

            reviews_canvas.configure(yscrollcommand=reviews_scrollbar.set)

            # Bind mouse wheel to scroll
            def _on_mousewheel(event):
                reviews_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            reviews_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            # Get reviews from database
            db_manager = DatabaseManager()
            query = "SELECT review FROM book_reviews WHERE ISBN = ?"
            reviews = db_manager.fetch_all_entries(query, (book_data[0],))

            if not reviews:
                # Show "No reviews" message
                no_reviews_label = tk.Label(reviews_container, text="No reviews yet", 
                                          font=('Arial', 10, 'italic'), fg='gray')
                no_reviews_label.pack(pady=20)
            else:
                # Display each review in a nice format
                for i, review_data in enumerate(reviews, 1):
                    review_frame = tk.Frame(reviews_container, relief=tk.GROOVE, bd=1)
                    review_frame.pack(fill='x', pady=5, padx=5)
                    
                    # Review number
                    tk.Label(review_frame, text=f"Review #{i}", 
                            font=('Arial', 9, 'bold')).pack(anchor='w', padx=5, pady=2)
                    
                    # Review text with word wrap
                    review_text = tk.Label(review_frame, text=review_data[0], 
                                         wraplength=450, justify='left',
                                         font=('Arial', 9))
                    review_text.pack(fill='x', padx=10, pady=5)

            # Configure the canvas and scrolling
            reviews_canvas.create_window((0, 0), window=reviews_container, anchor='nw')
            
            def configure_scroll_region(event):
                reviews_canvas.configure(scrollregion=reviews_canvas.bbox("all"))
            reviews_container.bind('<Configure>', configure_scroll_region)

            # Pack the canvas and scrollbar
            reviews_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            reviews_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Add to cart button at bottom
            button_frame = tk.Frame(main_container)
            button_frame.pack(pady=10)
            
            if book_data[4] > 0:  # if stock available
                tk.Button(button_frame, text="Add to Cart", 
                         command=lambda: self.add_to_cart(book_data[0], details_window)).pack()
            else:
                tk.Label(button_frame, text="Out of Stock", fg="red").pack()

            # Clean up scrolling when window is closed 
            def on_closing():
                reviews_canvas.unbind_all("<MouseWheel>")
                details_window.destroy()
            
            details_window.protocol("WM_DELETE_WINDOW", on_closing)

        def search_books():
            # Clear existing books
            for widget in grid_frame.winfo_children():
                widget.destroy()

            search_term = search_var.get().lower()
            selected_category = category_var.get()

            query = """
            SELECT ISBN, title, author, price, stock, edition, category, cover_image_path, sold
            FROM books
            WHERE (LOWER(title) LIKE ? OR LOWER(author) LIKE ?)
            """
            params = [f"%{search_term}%", f"%{search_term}%"]

            if selected_category != "All Categories":
                query += " AND category = ?"
                params.append(selected_category)

            books = db_manager.fetch_all_entries(query, tuple(params))
            display_books(books)

        def display_books(books):
            # Clear existing books first
            for widget in grid_frame.winfo_children():
                widget.destroy()

            for i, book in enumerate(books):
                row = i // 4
                col = i % 4
                
                # Create frame for each book
                book_frame = tk.Frame(grid_frame, relief=tk.RAISED, borderwidth=1)
                book_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Image display
                image_frame = tk.Frame(book_frame, height=200)
                image_frame.pack(fill=tk.X, pady=5)
                
                if book[7]:  # If there's an image path
                    try:
                        image = Image.open(book[7])
                        image = image.resize((150, 200), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        img_label = tk.Label(image_frame, image=photo)
                        img_label.image = photo
                        img_label.pack()
                    except Exception:
                        tk.Label(image_frame, text="No Image Available").pack()

                # Title only
                tk.Label(book_frame, text=book[1], wraplength=150, 
                        font=('Arial', 10, 'bold')).pack(pady=5)

                # Buttons frame
                buttons_frame = tk.Frame(book_frame)
                buttons_frame.pack(pady=5)

                # Details button
                tk.Button(buttons_frame, text="Details", 
                         command=lambda b=book: show_book_details(b)).pack(side=tk.LEFT, padx=2)

                # Add to Cart button
                if book[4] > 0:  # If stock available
                    tk.Button(buttons_frame, text="Add to Cart", 
                             command=lambda isbn=book[0]: self.add_to_cart(isbn, books_window)).pack(side=tk.LEFT, padx=2)
                else:
                    tk.Label(buttons_frame, text="Out of Stock", fg="red").pack(side=tk.LEFT, padx=2)

        # Configure grid columns to be equal width
        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add search button and bind Enter key
        tk.Button(search_frame, text="Search", command=search_books).pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: search_books())
        category_filter.bind('<<ComboboxSelected>>', lambda e: search_books())

        # Get initial books list
        query = "SELECT ISBN, title, author, price, stock, edition, category, cover_image_path, sold FROM books"
        books = db_manager.fetch_all_entries(query)
        
        # Initial display of all books
        display_books(books)

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Shopping Cart")
        cart_window.geometry("800x500")  # Made wider to accommodate buttons

        # Create frame for cart items
        cart_frame = tk.Frame(cart_window)
        cart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        def refresh_cart():
            # Clear previous content
            for widget in cart_frame.winfo_children():
                widget.destroy()

            if not self.current_user.cart:
                tk.Label(cart_frame, text="Cart is empty").pack()
                return

            total = 0
            db_manager = DatabaseManager()
            
            for isbn, quantity in self.current_user.cart.items():
                query = "SELECT title, price FROM books WHERE ISBN = ?"
                book_data = db_manager.fetch_one_entry(query, (isbn,))
                
                if book_data:
                    item_frame = tk.Frame(cart_frame)
                    item_frame.pack(fill=tk.X, pady=5, padx=10)
                    
                    # Book details
                    details_frame = tk.Frame(item_frame)
                    details_frame.pack(side=tk.LEFT)
                    tk.Label(details_frame, text=f"{book_data[0]} - ${book_data[1]}").pack(side=tk.LEFT)
                    
                    # Quantity control frame
                    qty_frame = tk.Frame(item_frame)
                    qty_frame.pack(side=tk.LEFT, padx=20)
                    
                    # Decrease button
                    tk.Button(qty_frame, text="-", 
                             command=lambda i=isbn: adjust_quantity(i, -1)).pack(side=tk.LEFT, padx=5)
                    
                    # Quantity label
                    tk.Label(qty_frame, text=str(quantity)).pack(side=tk.LEFT, padx=5)
                    
                    # Increase button
                    tk.Button(qty_frame, text="+", 
                             command=lambda i=isbn: adjust_quantity(i, 1)).pack(side=tk.LEFT, padx=5)
                    
                    # Remove button
                    tk.Button(item_frame, text="Remove", 
                             command=lambda i=isbn: remove_from_cart(i)).pack(side=tk.RIGHT)
                    
                    total += book_data[1] * quantity

            tk.Label(cart_frame, text=f"Total: ${total:.2f}", 
                    font=('Arial', 12, 'bold')).pack(pady=10)

        def adjust_quantity(isbn, amount):
            self.current_user.adjust_quantity(isbn, amount)
            refresh_cart()

        def place_order():
            if not self.current_user.cart:
                messagebox.showwarning("Warning", "Cart is empty")
                return

            # Create order window
            order_window = tk.Toplevel(cart_window)
            order_window.title("Place Order")
            order_window.geometry("400x300")

            # Shipping options
            shipping_var = tk.StringVar(value="standard")
            tk.Radiobutton(order_window, text="Standard Shipping", 
                          variable=shipping_var, value="standard").pack(pady=5)
            tk.Radiobutton(order_window, text="Express Shipping", 
                          variable=shipping_var, value="express").pack(pady=5)

            # Gift options
            gift_note_var = tk.StringVar()
            tk.Label(order_window, text="Gift Note (optional):").pack(pady=5)
            tk.Entry(order_window, textvariable=gift_note_var).pack()

            customization_var = tk.StringVar()
            tk.Label(order_window, text="Customization Name (optional):").pack(pady=5)
            tk.Entry(order_window, textvariable=customization_var).pack()

      
            def confirm_order():
                try:
                    order_details = self.current_user.place_order(
                        shipping_var.get(),
                        gift_note_var.get() if gift_note_var.get() else None,
                        customization_var.get() if customization_var.get() else None,
                    )
                    
                    if order_details:
                        messagebox.showinfo("Success", 
                            f"Order placed successfully!\n"
                            f"Order ID: {order_details['order_id']}\n"
                            f"Description: {order_details['description']}\n"
                            f"Total: ${order_details['total']:.2f}")
                        order_window.destroy()
                        refresh_cart()
                    else:
                        messagebox.showerror("Error", "Failed to place order: No order details returned")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to place order: {str(e)}")
        # Add confirm button
            tk.Button(order_window, text="Confirm Order", command=confirm_order).pack(pady=20)


        def remove_from_cart(isbn):
            if isbn in self.current_user.cart:
                del self.current_user.cart[isbn]
                refresh_cart()

        # Add buttons
        button_frame = tk.Frame(cart_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Refresh", command=refresh_cart).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Place Order", 
                 command=place_order).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_cart()

    def add_to_cart(self, isbn, window):
        try:
            self.current_user.add_to_cart(isbn)
            messagebox.showinfo("Success", "Book added to cart!")
            window.destroy()  # Close the browse window
            self.browse_books()  # Refresh the browse window
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book to cart: {str(e)}")

    def view_customer_orders(self):
        # Create a new window for viewing orders
        orders_window = tk.Toplevel(self.root)
        orders_window.title("My Orders")
        orders_window.geometry("800x600")

        # Create a treeview to display orders
        tree = ttk.Treeview(orders_window, 
                           columns=('Order ID', 'Status', 'Shipping Method', 'Total'),
                           show='headings')
        
        # Set column headings
        for col in ('Order ID', 'Status', 'Shipping Method', 'Total'):
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(orders_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_orders():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
                
            # Get orders from database
            db_manager = DatabaseManager()
            query = """
            SELECT order_id, status, shipping_method, total 
            FROM orders 
            WHERE customer_username = ?
            ORDER BY order_id DESC
            """
            orders = db_manager.fetch_all_entries(query, (self.current_user.username,))
            
            # Insert orders into treeview
            for order in orders:
                tree.insert('', tk.END, values=order)
        

        def view_order_details():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an order to view details")
                return
            
            order_data = tree.item(selected_item[0])['values']
            order_id = order_data[0]
            
            # Create details window
            details_window = tk.Toplevel(orders_window)
            details_window.title(f"Order #{order_id} Details")
            details_window.geometry("400x400")
            
            # Create text widget for details
            text_widget = tk.Text(details_window, height=20, width=45)
            text_widget.pack(pady=10, padx=10)
            
            # Get order books
            db_manager = DatabaseManager()
            query = """
            SELECT b.title, b.price, ob.quantity
            FROM books b
            JOIN order_books ob ON b.ISBN = ob.book_isbn
            JOIN orders o ON ob.order_id = o.order_id
            WHERE ob.order_id = ?
            """
            books = db_manager.fetch_all_entries(query, (order_id,))
            
            # Display order details
            text_widget.insert(tk.END, f"Order #{order_id}\n")
            text_widget.insert(tk.END, f"Status: {order_data[1]}\n")
            text_widget.insert(tk.END, f"Shipping Method: {order_data[2]}\n")
            text_widget.insert(tk.END, "\nOrdered Items:\n")
            text_widget.insert(tk.END, "-" * 40 + "\n")
            
            for book in books:
                text_widget.insert(tk.END, f"Title: {book[0]}\n")
                text_widget.insert(tk.END, f"Price: ${book[1]:.2f}\n")
                text_widget.insert(tk.END, f"Quantity: {book[2]}\n")
                text_widget.insert(tk.END, "-" * 40 + "\n")
            
            text_widget.insert(tk.END, f"\nTotal: ${float(order_data[3]):.2f}")
            text_widget.config(state='disabled')

        # Create frame for buttons
        button_frame = tk.Frame(orders_window)
        button_frame.pack(pady=10)

        # Add buttons
        tk.Button(button_frame, text="Refresh", command=refresh_orders).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="View Details", 
                 command=view_order_details).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel Order", 
                 command=lambda: self.cancel_selected_order(tree, refresh_orders)).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_orders()

    def update_profile(self):
        if not isinstance(self.current_user, Customer):
            messagebox.showerror("Error", "Only customers can update their profile")
            return

        # Create a new window for profile update
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Update Profile")
        profile_window.geometry("400x500")

        # Create frames for different update options
        fields_frame = tk.Frame(profile_window)
        fields_frame.pack(pady=20)

        # Username update
        tk.Label(fields_frame, text="New Username:").pack()
        username_entry = tk.Entry(fields_frame)
        username_entry.insert(0, self.current_user.username)
        username_entry.pack(pady=5)

        # Password update
        tk.Label(fields_frame, text="New Password:").pack()
        password_entry = tk.Entry(fields_frame, show="*")
        password_entry.pack(pady=5)

        # Address update
        tk.Label(fields_frame, text="New Address:").pack()
        address_entry = tk.Entry(fields_frame)
        address_entry.insert(0, self.current_user.address)
        address_entry.pack(pady=5)

        # Phone update
        tk.Label(fields_frame, text="New Phone:").pack()
        phone_entry = tk.Entry(fields_frame)
        phone_entry.insert(0, self.current_user.phone)
        phone_entry.pack(pady=5)

        def update_all():
            try:
                # Get all new values
                new_username = username_entry.get()
                new_password = password_entry.get()
                new_address = address_entry.get()
                new_phone = phone_entry.get()

                # Track if any updates were made
                updates_made = False

                # Update username if changed
                if new_username and new_username != self.current_user.username:
                    self.current_user.update_username(new_username)
                    updates_made = True

                # Update password if provided
                if new_password:
                    self.current_user.update_password(new_password)
                    updates_made = True

                # Update address if changed
                if new_address and new_address != self.current_user.address:
                    self.current_user.update_address(new_address)
                    updates_made = True

                # Update phone if changed
                if new_phone and new_phone != self.current_user.phone:
                    self.current_user.update_phone(new_phone)
                    updates_made = True

                if updates_made:
                    messagebox.showinfo("Success", "Profile updated successfully!")
                    profile_window.destroy()
                else:
                    messagebox.showinfo("Info", "No changes were made")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

        # Individual update functions remain the same
        def update_username():
            new_username = username_entry.get()
            if new_username and new_username != self.current_user.username:
                try:
                    self.current_user.update_username(new_username)
                    messagebox.showinfo("Success", "Username updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update username: {str(e)}")

        def update_password():
            new_password = password_entry.get()
            if new_password:
                try:
                    self.current_user.update_password(new_password)
                    messagebox.showinfo("Success", "Password updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update password: {str(e)}")

        def update_address():
            new_address = address_entry.get()
            if new_address and new_address != self.current_user.address:
                try:
                    self.current_user.update_address(new_address)
                    messagebox.showinfo("Success", "Address updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update address: {str(e)}")

        def update_phone():
            new_phone = phone_entry.get()
            if new_phone and new_phone != self.current_user.phone:
                try:
                    self.current_user.update_phone(new_phone)
                    messagebox.showinfo("Success", "Phone updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update phone: {str(e)}")

        # Buttons frame
        buttons_frame = tk.Frame(profile_window)
        buttons_frame.pack(pady=10)

        # Add Update All button at the top
        tk.Button(buttons_frame, text="Update All", command=update_all, 
                  bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Individual update buttons
        tk.Button(buttons_frame, text="Update Username", command=update_username).pack(pady=5)
        tk.Button(buttons_frame, text="Update Password", command=update_password).pack(pady=5)
        tk.Button(buttons_frame, text="Update Address", command=update_address).pack(pady=5)
        tk.Button(buttons_frame, text="Update Phone", command=update_phone).pack(pady=5)

    def confirm_selected_order(self, tree, refresh_callback):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to confirm")
            return
        
        try:
            order_data = tree.item(selected_item[0])['values']
            order_id = order_data[0]  # First column is Order ID
            status = order_data[2]    # Third column is Status
            
            # Check if order is pending
            if status.lower() != 'pending':
                messagebox.showerror("Error", "Only pending orders can be confirmed")
                return
            
            self.current_user.confirm_order(order_id)
            messagebox.showinfo("Success", f"Order #{order_id} has been confirmed")
            
                        
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to confirm order: {str(e)}")

    def cancel_selected_order(self, tree, refresh_callback):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to cancel")
            return
        
        try:
            order_data = tree.item(selected_item[0])['values']
            order_id = order_data[0]  # First column is Order ID
            status = order_data[1]    # Third column is Status
            
            # Check if order is already confirmed
            if status.lower() != 'pending':
                messagebox.showerror("Error", "Only pending orders can be cancelled")
                return
            
            self.current_user.cancel_order(order_id)
            messagebox.showinfo("Success", f"Order #{order_id} has been cancelled")
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to cancel order: {str(e)}")

    def manage_books(self):
        books_window = tk.Toplevel(self.root)
        books_window.title("Manage Books")
        books_window.geometry("1000x600")

        # Create a treeview to display books
        tree = ttk.Treeview(books_window, 
                           columns=('ISBN', 'Title', 'Author', 'Price', 'Stock', 'Edition', 'Category'),
                           show='headings')
        
        # Set column headings
        for col in ('ISBN', 'Title', 'Author', 'Price', 'Stock', 'Edition', 'Category'):
            tree.heading(col, text=col)
            tree.column(col, width=140)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(books_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_books():
            for item in tree.get_children():
                tree.delete(item)
                
            db_manager = DatabaseManager()
            query = "SELECT ISBN, title, author, price, stock, edition, category FROM books"
            books = db_manager.fetch_all_entries(query)
            
            for book in books:
                tree.insert('', tk.END, values=book)

        def edit_book():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a book to edit")
                return
            
            book_data = tree.item(selected_item[0])['values']
            
            # Get the current image path from database
            db_manager = DatabaseManager()
            query = "SELECT cover_image_path FROM books WHERE ISBN = ?"
            result = db_manager.fetch_one_entry(query, (book_data[0],))
            current_image_path = result[0] if result else None

            edit_window = tk.Toplevel(books_window)
            edit_window.title("Edit Book")
            edit_window.geometry("900x600")

            # Create main container frames
            left_frame = tk.Frame(edit_window)
            left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill='both', expand=True)
            
            right_frame = tk.Frame(edit_window)
            right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill='both', expand=True)

            # Show ISBN but make it readonly
            tk.Label(left_frame, text="ISBN:").pack(pady=5)
            isbn_entry = tk.Entry(left_frame, state='readonly')
            isbn_entry.pack(pady=5, fill='x')
            isbn_entry.configure(state='normal')
            isbn_entry.insert(0, book_data[0])
            isbn_entry.configure(state='readonly')

            # Add regular fields
            fields = ['Title', 'Author', 'Price', 'Stock', 'Edition']
            entries = {}
            
            for i, field in enumerate(fields, 1):
                tk.Label(left_frame, text=f"{field}:").pack(pady=5)
                entry = tk.Entry(left_frame, width=40)
                entry.insert(0, book_data[i])
                entry.pack(pady=5, fill='x')
                entries[field.lower()] = entry

            # Add category dropdown
            tk.Label(left_frame, text="Category:").pack(pady=5)
            category_var = tk.StringVar(value=book_data[6])

            category_dropdown = ttk.Combobox(left_frame,
                                textvariable=category_var, 
                                values=self.categories,
                                state='readonly',
                                width=37)
            category_dropdown.pack(pady=5, fill='x')

            # Image selection
            tk.Label(left_frame, text="Cover Image:").pack(pady=5)
            image_path_var = tk.StringVar(value=current_image_path)  # Set current path
            image_path_entry = tk.Entry(left_frame, textvariable=image_path_var, width=40)
            image_path_entry.pack(pady=5, fill='x')
            
            # Right side - Image preview
            preview_label = tk.Label(right_frame, text="No image selected")
            preview_label.pack(fill='both', expand=True)

            # Function to load and display image
            def load_image(filepath):
                if filepath:
                    try:
                        image = Image.open(filepath)
                        preview_width = right_frame.winfo_width()
                        preview_height = right_frame.winfo_height()
                        aspect_ratio = image.width / image.height
                        
                        if aspect_ratio > preview_width/preview_height:
                            new_width = preview_width
                            new_height = int(preview_width / aspect_ratio)
                        else:
                            new_height = preview_height
                            new_width = int(preview_height * aspect_ratio)
                        
                        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        preview_label.config(image=photo)
                        preview_label.image = photo
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load image: {str(e)}")

            # Load current image if exists
            edit_window.update()  # Update window to get correct dimensions
            if current_image_path:
                load_image(current_image_path)

            def select_image():
                filepath = filedialog.askopenfilename(
                    filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
                )
                if filepath:
                    image_path_var.set(filepath)
                    load_image(filepath)

            tk.Button(left_frame, text="Browse...", command=select_image).pack(pady=5)

            def save_changes():
                try:
                    # Get values from entries
                    isbn = book_data[0]
                    title = entries['title'].get()
                    author = entries['author'].get()
                    price = float(entries['price'].get())
                    stock = int(entries['stock'].get())
                    edition = entries['edition'].get()
                    category = category_var.get()
                    cover_image = image_path_var.get()

                    # Update book in database
                    query = """
                    UPDATE books 
                    SET title=?, author=?, price=?, stock=?, edition=?, category=?, cover_image_path=?
                    WHERE ISBN=?
                    """
                    db_manager = DatabaseManager()
                    db_manager.execute_query(query, (title, author, price, stock, edition, category, cover_image, isbn))
                    
                    messagebox.showinfo("Success", "Book updated successfully!")
                    edit_window.destroy()
                    refresh_books()
                except ValueError as e:
                    messagebox.showerror("Error", "Please enter valid numeric values for price and stock.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update book: {str(e)}")

            tk.Button(left_frame, text="Save Changes", command=save_changes, width=30).pack(pady=20)

        def delete_book():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a book to delete")
                return
            
            book_data = tree.item(selected_item[0])['values']
            isbn = book_data[0]
            title = book_data[1]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{title}'?"):
                try:
                    self.current_user.delete_book(isbn)
                    messagebox.showinfo("Success", "Book deleted successfully!")
                    refresh_books()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

        # Add buttons
        button_frame = tk.Frame(books_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Refresh", command=refresh_books).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Book", command=edit_book).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Book", command=delete_book).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add New Book", command=self.show_add_book_form).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_books()

    def manage_book_categories(self):
        categories_window = tk.Toplevel(self.root)
        categories_window.title("Manage Categories")
        categories_window.geometry("400x500")

        # Create listbox for categories
        categories_frame = tk.Frame(categories_window)
        categories_frame.pack(pady=10, padx=20, fill='both', expand=True)

        tk.Label(categories_frame, text="Current Categories", font=('Arial', 12, 'bold')).pack(pady=5)
        
        categories_listbox = tk.Listbox(categories_frame)
        categories_listbox.pack(fill='both', expand=True)

        def refresh_categories():
            categories_listbox.delete(0, tk.END)
            for category in self.categories:
                if category:  # Only add non-empty categories
                    categories_listbox.insert(tk.END, category)

        def edit_category():
            selected = categories_listbox.curselection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a category to edit")
                return

            old_name = categories_listbox.get(selected)
            edit_window = tk.Toplevel(categories_window)
            edit_window.title("Edit Category")
            edit_window.geometry("300x150")

            tk.Label(edit_window, text="New Category Name:").pack(pady=5)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, old_name)
            name_entry.pack(pady=5)

            def save_edit():
                new_name = name_entry.get()
                if not new_name:
                    messagebox.showerror("Error", "Category name cannot be empty")
                    return
                try:
                    # Update category in self.categories
                    if old_name in self.categories:
                        index = self.categories.index(old_name)
                        self.categories[index] = new_name
                    
                    # Update category name in books table
                    db_manager = DatabaseManager()
                    query = "UPDATE books SET category = ? WHERE category = ?"
                    db_manager.execute_query(query, (new_name, old_name))
                    
                    messagebox.showinfo("Success", "Category updated successfully!")
                    edit_window.destroy()
                    refresh_categories()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        def delete_category():
            selected = categories_listbox.curselection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a category to delete")
                return

            category_name = categories_listbox.get(selected)
            if messagebox.askyesno("Confirm Delete", 
                                  f"Are you sure you want to delete '{category_name}'?\n"
                                  "Books with this category will have no category assigned."):
                try:
                    # Remove category from self.categories
                    if category_name in self.categories:
                        self.categories.remove(category_name)
                    
                    # Set category to NULL for all books with this category
                    db_manager = DatabaseManager()
                    query = "UPDATE books SET category = NULL WHERE category = ?"
                    db_manager.execute_query(query, (category_name,))
                    
                    messagebox.showinfo("Success", "Category deleted successfully!")
                    refresh_categories()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        def add_category():
            add_window = tk.Toplevel(categories_window)
            add_window.title("Add Category")
            add_window.geometry("300x150")

            tk.Label(add_window, text="Category Name:").pack(pady=5)
            name_entry = tk.Entry(add_window)
            name_entry.pack(pady=5)

            def save_category():
                new_name = name_entry.get()
                if not new_name:
                    messagebox.showerror("Error", "Category name cannot be empty")
                    return
                
                if new_name in self.categories:
                    messagebox.showerror("Error", "Category already exists")
                    return
                    
                try:
                    # Add category to self.categories
                    self.categories.append(new_name)
                    
                    messagebox.showinfo("Success", "Category added successfully!")
                    add_window.destroy()
                    refresh_categories()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(add_window, text="Save", command=save_category).pack(pady=10)

        # Add buttons
        button_frame = tk.Frame(categories_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Category", command=add_category).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Category", command=edit_category).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Category", command=delete_category).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=refresh_categories).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_categories()

    def ship_selected_order(self, tree, refresh_callback):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to ship")
            return
        
        try:
            order_data = tree.item(selected_item[0])['values']
            order_id = order_data[0]  # First column is Order ID
            status = order_data[2]    # Third column is Status
            
            # Check if order is confirmed
            if status.lower() != 'confirmed':
                messagebox.showerror("Error", "Only confirmed orders can be shipped")
                return
            
            self.current_user.ship_order(order_id)
            messagebox.showinfo("Success", f"Order #{order_id} has been shipped")
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to ship order: {str(e)}")

    def view_purchased_books(self):
        purchased_window = tk.Toplevel(self.root)
        purchased_window.title("My Purchased Books")
        purchased_window.geometry("800x600")

        # Create main frame
        main_frame = tk.Frame(purchased_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create treeview for purchased books
        tree = ttk.Treeview(main_frame, 
                            columns=('ISBN', 'Title', 'Author', 'Price'),
                            show='headings')
        
        # Set column headings
        for col in ('ISBN', 'Title', 'Author', 'Price'):
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_books():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
                
            # Get purchased books from database
            db_manager = DatabaseManager()
            query = """
            SELECT DISTINCT b.ISBN, b.title, b.author, b.price
            FROM books b
            JOIN order_books ob ON b.ISBN = ob.book_isbn
            JOIN orders o ON ob.order_id = o.order_id
            WHERE o.customer_username = ? 
            AND o.status = 'shipped'
            """
            books = db_manager.fetch_all_entries(query, (self.current_user.username,))
            
            # Insert books into treeview
            for book in books:
                tree.insert('', tk.END, values=book)

        def add_review():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a book to review")
                return
            
            book_data = tree.item(selected_item[0])['values']
            isbn = book_data[0]
            title = book_data[1]
            
            # Create review window
            review_window = tk.Toplevel(purchased_window)
            review_window.title(f"Review - {title}")
            review_window.geometry("400x300")
            
            tk.Label(review_window, text="Write your review:", font=('Arial', 12)).pack(pady=10)
            
            # Add text area for review
            review_text = tk.Text(review_window, height=8, width=40)
            review_text.pack(pady=10)
            
            def submit_review():
                review = review_text.get("1.0", tk.END).strip()
                if not review:
                    messagebox.showwarning("Warning", "Please write a review")
                    return
                
                db_manager = DatabaseManager()
                if db_manager.insert_book_review(isbn, review):
                    messagebox.showinfo("Success", "Review submitted successfully!")
                    review_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to submit review")
            
            tk.Button(review_window, text="Submit Review", command=submit_review).pack(pady=10)

        # Add buttons
        button_frame = tk.Frame(purchased_window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Refresh", command=refresh_books).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Add Review", command=add_review).pack(side=tk.LEFT, padx=5)

        # Initial load
        refresh_books()

    def show_order_details(self, tree, orders_window):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an order to view details")
            return
        
        order_data = tree.item(selected_item[0])['values']
        order_id = order_data[0]
        
        # Create details window
        details_window = tk.Toplevel(orders_window)
        details_window.title(f"Order #{order_id} Details")
        details_window.geometry("600x500")
        
        # Create main container
        main_frame = tk.Frame(details_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Order information section
        info_frame = tk.LabelFrame(main_frame, text="Order Information", font=('Arial', 10, 'bold'))
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Get order details from database
        db_manager = DatabaseManager()
        query = """
        SELECT o.order_id, o.customer_username, o.status, o.shipping_method, 
               o.total, o.customization, o.gift_note
        FROM orders o
        WHERE o.order_id = ?
        """
        order_details = db_manager.fetch_one_entry(query, (order_id,))
        
        if order_details:
            # Display order information
            labels = ['Order ID:', 'Customer:', 'Status:', 'Shipping Method:', 
                     'Total:', 'Customization:', 'Gift Note:']
            for i, (label, value) in enumerate(zip(labels, order_details)):
                frame = tk.Frame(info_frame)
                frame.pack(fill='x', pady=2)
                tk.Label(frame, text=label, width=15, anchor='e', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
                tk.Label(frame, text=str(value) if value else "None", anchor='w').pack(side=tk.LEFT, padx=5)
        
        # Books section
        books_frame = tk.LabelFrame(main_frame, text="Ordered Books", font=('Arial', 10, 'bold'))
        books_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create treeview for books
        books_tree = ttk.Treeview(books_frame, 
                                 columns=('ISBN', 'Title', 'Author', 'Price', 'Quantity'),
                                 show='headings')
        
        # Set column headings
        for col in ('ISBN', 'Title', 'Author', 'Price', 'Quantity'):
            books_tree.heading(col, text=col)
            books_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(books_frame, orient=tk.VERTICAL, command=books_tree.yview)
        books_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Get books in order
        query = """
        SELECT b.ISBN, b.title, b.author, b.price, ob.quantity
        FROM books b
        JOIN order_books ob ON b.ISBN = ob.book_isbn
        JOIN orders o ON ob.order_id = o.order_id
        WHERE ob.order_id = ?
        """
        books = db_manager.fetch_all_entries(query, (order_id,))
        
        # Insert books into treeview
        for book in books:
            books_tree.insert('', tk.END, values=book)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BookstoreGUI()
    app.run()