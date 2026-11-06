
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save_to_database(self, user):
        print(f"Saving {user.name} to database")

class EmailService:
    def send_email(self, user, message):
        print(f"Sending email to {user.email}: {message}")

class ReportGenerator:
    def generate_report(self, user):
        print(f"Generating report for {user.name}")