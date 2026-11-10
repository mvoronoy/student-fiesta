class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class UserRepository:
    def save(self, user):
        print(f"Saving {user.name} to database")


class EmailService:
    def send(self, user, message):
        print(f"Sending email to {user.email}: {message}")


class ReportService:
    def generate(self, user):
        print(f"Generating report for {user.name}")


if __name__ == "__main__":
    user = User("Alice", "alice@example.com")

    repository = UserRepository()
    email_service = EmailService()
    report_service = ReportService()

    repository.save(user)
    email_service.send(user, "Welcome!")
    report_service.generate(user)