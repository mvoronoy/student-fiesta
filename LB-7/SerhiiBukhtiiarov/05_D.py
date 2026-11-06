#Ввів інтерфейс бази даних і передав конкретну реалізацію через конструктор

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

class PostgreSQLDatabase(Database):
    def connect(self):
        print("Connecting to PostgreSQL")

    def save(self, data):
        print(f"Saving to PostgreSQL: {data}")

class UserService:
    # Залежимо від абстракції (Database), а не від конкретної реалізації
    def __init__(self, database: Database):
        self.database = database

    def register_user(self, name):
        self.database.connect()
        self.database.save(name)

# Тепер ми легко можемо підставити будь-яку базу даних
mysql_db = MySQLDatabase()
service = UserService(mysql_db)
service.register_user("Alice")