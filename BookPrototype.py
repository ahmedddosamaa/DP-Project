from abc import ABC, abstractmethod
import copy

# Step 1: Define the Prototype Interface
class BookPrototype(ABC):
    @abstractmethod
    def clone(self):
        """
        Abstract method to clone an object.
        """
        pass