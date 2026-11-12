#
#   Fix violation of Single Responsibility Principle (SRP)
#
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class UserRepository:
    def save(self, user: User):
        print(f"Saving {user.name} to database")


class EmailService:
    def send(self, user: User, message: str):
        print(f"Sending email to {user.email}: {message}")


class ReportGenerator:
    def generate(self, user: User):
        print(f"Generating report for {user.name}")