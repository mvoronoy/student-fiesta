
# Розділено відповідальність на окремі спеціалізовані класи.
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save_to_database(self, user: User):
        print(f"Saving {user.name} to database")

class EmailService:
    def send_email(self, user: User, message: str):
        print(f"Sending email to {user.email}: {message}")

class ReportGenerator:
    def generate_report(self, user: User):
        print(f"Generating report for {user.name}")