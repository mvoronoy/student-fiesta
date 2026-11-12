#
#  Fix violation of Dependency Inversion Principle (DIP)
# High-level modules should not depend on low-level modules. Both should depend on abstractions.
#

from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def save(self, data): ...


class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL")

    def save(self, data):
        print(f"Saving to MySQL: {data}")


class UserService:
    def __init__(self, database: Database):  # залежність передається ззовні
        self.database = database

    def register_user(self, name):
        self.database.connect()
        self.database.save(name)


UserService(MySQLDatabase()).register_user("Alice")
