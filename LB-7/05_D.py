#
#  Fix violation of Dependency Inversion Principle (DIP)
# High-level modules should not depend on low-level modules. Both should depend on abstractions.
#


class MySQLDatabase:
    def connect(self):
        print("Connecting to MySQL")

    def save(self, data):
        print(f"Saving to MySQL: {data}")


class UserService:
    def __init__(self):
        self.database = MySQLDatabase()

    def register_user(self, name):
        self.database.connect()
        self.database.save(name)


service = UserService()
service.register_user("Alice")
