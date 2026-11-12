# В оригінальному варіанті високорівневий клас UserService був прив'язаний до низькорівневого класу MySQLDatabase (створював його екземпляр всередині свого конструктора).
# Через це неможливо легко замінити базу даних без переписування коду UserService.
# Нам потрібно, щоб модулі верхнього рівня не залежали від модулів нижнього рівня. Обидва типи модулів повинні залежати від абстракцій.
# Для цього був створений абстрактний інтерфейс Database.

from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def save(self, data: str):
        pass

class MySQLDatabase(Database):
    def connect(self):
        print("Connecting to MySQL")

    def save(self, data: str):
        print(f"Saving to MySQL: {data}")

class PostgreSQLDatabase(Database):
    def connect(self):
        print("Connecting to PostgreSQL")

    def save(self, data: str):
        print(f"Saving to PostgreSQL: {data}")

class UserService:
    def __init__(self, database: Database):
        self.database = database

    def register_user(self, name: str):
        self.database.connect()
        self.database.save(name)
