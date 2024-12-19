from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    

