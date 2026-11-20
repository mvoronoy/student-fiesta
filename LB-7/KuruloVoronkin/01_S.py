class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class UserRepository:
    def save(self, user: User) -> None:
        print(f"Saving {user.name} to database")


class EmailService:
    def send_email(self, user: User, message: str) -> None:
        print(f"Sending email to {user.email}: {message}")


class UserReportGenerator:
    def generate(self, user: User) -> None:
        print(f"Generating report for {user.name}")


if __name__ == "__main__":
    user = User("Kyrylo", "kyrylo@example.com")
    repo = UserRepository()
    mailer = EmailService()
    reporter = UserReportGenerator()

    repo.save(user)
    mailer.send_email(user, "Welcome!")
    reporter.generate(user)