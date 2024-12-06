from abc import ABC, abstractmethod

class AbstractEngine(ABC):
    
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def engine(self):
        ...

    @abstractmethod
    def execute_query(self):
        ...

    @abstractmethod
    def insert_data(self):
        ...