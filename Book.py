import copy
from BookPrototype import BookPrototype

class Book (BookPrototype):
    def __init__(self, ISBN, title, author, price, popularity, stock, cover_image, edition, category, sold=0, reviews=None):
        """
        Initialize book attributes with private variables.
        """
        self.__ISBN = ISBN
        self.__title = title
        self.__author = author
        self.__price = price
        self.__popularity = popularity
        self.__category = category
        self.__stock = stock
        self.__edition = edition
        self.__cover_image = cover_image
        self.__sold= sold
        self.__reviews= reviews

    # Getter and Setter for ISBN
    def getisbn(self):
        return self.__ISBN
    
    def setisbn(self, isbn):
        self.__ISBN = isbn

    # Getter and Setter for title
    def gettitle(self):
        return self.__title

    def settitle(self, value):
        self.__title = value

    # Getter and Setter for popularity
    def getpopularity(self):
        return self.__popularity
    
    def setpopularity(self, popularity):
        self.__popularity = popularity

    # Getter and Setter for author
    def getauthor(self):
        return self.__author

    def setauthor(self, value):
        self.__author = value

    # Getter and Setter for price
    def getprice(self):
        return self.__price

    def setprice(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = value

    # Getter and Setter for category
    def getcategory(self):
        return self.__category

    def setcategory(self, value):
        self.__category = value

    # Getter and Setter for stock
    def getstock(self):
        return self.__stock

    def setstock(self, value):
        if value < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = value

    # Getter and Setter for edition
    def getedition(self):
        return self.__edition

    def setedition(self, value):
        self.__edition = value

    # Getter and Setter for cover_image
    def getcover_image(self):
        return self.__cover_image

    def setcover_image(self, value):
        self.__cover_image = value

    # Getter and Setter for sold
    def getsold(self):
        return self.__sold

    def setsold(self, value):
        self.__sold = value

    # Getter and Setter for reviews
    def getreviews(self):
        return self.__reviews

    def setreviews(self, value):
        self.__reviews = value


    def get_details(self):
        """
        Get a string representation of the book's details.
        :return: A string containing book details
        """
        return (
            f"Title: {self.__title}\n"
            f"Author: {self.__author}\n"
            f"Price: ${self.__price:.2f}\n"
            f"Category: {self.__category}\n"
            f"Edition: {self.__edition}\n"
            f"Stock Available: {self.__stock}\n"
            f"Cover Image: {self.__cover_image}"
            f"reviews: {self.__reviews}"
        )
    
    def clone(self):
        """
        Implement the clone method to create a copy of the current book.
        Uses the copy module to perform a deep copy.
        :return: A new Book instance with copied data
        """
        new_book = Book(
            self.__ISBN,
            self.__title,
            self.__author,
            self.__price,
            self.__popularity,
            self.__stock,
            self.__cover_image,
            self.__edition,
            self.__category,
            self.__sold,
            self.__reviews
        )
        return new_book

