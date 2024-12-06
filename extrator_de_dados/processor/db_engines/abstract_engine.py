from abc import ABC, abstractmethod

class AbstractEngine(ABC):
    
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def _create_connection_url(self):
        ...

    @abstractmethod
    def execute_query(self):
        ...

    @abstractmethod
    def insert_data(self):
        ...