from abc import ABC, abstractmethod


# Определение абстрактного класса-интерфейса
class DB_Interface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add(self, object_class):
        pass

    @abstractmethod
    def exists(self, tg_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get(self, tg_id):
        pass
