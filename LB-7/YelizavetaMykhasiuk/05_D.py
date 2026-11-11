from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

class MySQLDatabase(Database):
    def connector(self):
        print("Connecting to MySQL")

    def save(self, data):
        self.connector()
        print(f"Saving {data} to MySQL")

class UserService:
    def __init__(self, database: Database):
        self.database = database

    def register_user(self, name):
        self.database.save(name)

service = UserService(MySQLDatabase())
service.register_user("Alice")