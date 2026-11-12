# В оригінальному варіанті клас User поєднував одразу чотири різні відповідальності, що недопустимо, бо кожен клас повинен мати лише одну зону відповідальності
# Тому в виправленому варіанті відповідальності були розділені між окремими спеціалізованими класами
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserRepository:
    def save_to_database(self, user: User):
        print(f"Saving {user.name} to database")

class EmailService:
    def send_email(self, user: User, message: str):
        print(f"Sending email to {user.email}: {message}")

class UserReportGenerator:
    def generate_report(self, user: User):
        print(f"Generating report for {user.name}")
