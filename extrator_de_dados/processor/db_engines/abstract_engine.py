from abc import ABC, abstractmethod

class AbstractEngine(ABC):
    
    @abstractmethod
    def connect(self, *args, **kargs):
        ...

    @abstractmethod
    def _create_connection_url(self, *args, **kargs):
        ...

    @abstractmethod
    def execute_query(self, *args, **kargs):
        ...

    @abstractmethod
    def insert_data(self, *args, **kargs):
        ...