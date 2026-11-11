class User_Logger:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def save_to_database(self):
        print(f"Saving {self.name} to database")

class Email_Sender:
    def send_email(self, message):
        print(f"Sending email to {self.email}: {message}")

class Report_Generator:
    def generate_report(self):
        print(f"Generating report for {self.name}")
