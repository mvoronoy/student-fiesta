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
    def __init__(self, database: Database):
        self.database = database

    def register_user(self, name):
        self.database.connect()
        self.database.save(name)


if __name__ == "__main__":
    mysql_service = UserService(MySQLDatabase())
    mysql_service.register_user("Alice")

    postgres_service = UserService(PostgreSQLDatabase())
    postgres_service.register_user("Bob")