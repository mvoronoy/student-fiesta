#
#   Fix violation of Single Responsibility Principle (SRP)
#
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_database(self):
        print(f"Saving {self.name} to database")

    def send_email(self, message):
        print(f"Sending email to {self.email}: {message}")

    def generate_report(self):
        print(f"Generating report for {self.name}")
