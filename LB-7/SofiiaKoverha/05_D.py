
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL")

    def save(self, data):
        print(f"Saving to MySQL: {data}")

class UserService:
    # Залежимо від абстракції, а не від конкретного MySQLDatabase
    def __init__(self, database: Database):
        self.database = database

    def register_user(self, name):
        self.database.connect()
        self.database.save(name)

db = MySQLDatabase()
service = UserService(db)
service.register_user("Alice")