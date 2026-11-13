class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        print(f"Saving {user.name} to database")

class EmailService:
    def send_email(self, user, message):
        print(f"Sending email to {user.email}: {message}")

class ReportGenerator:
    def generate_report(self, user):
        print(f"Generating report for {user.name}")

if __name__ == "__main__":
    user = User("Max Voronoy", "max@example.com")

    repository = UserRepository()
    email_service = EmailService()
    report_generator = ReportGenerator()

    repository.save(user)
    email_service.send_email(user, "Welcome!")
    report_generator.generate_report(user)