class User:
    """Відповідає лише за дані користувача."""

    def __init__(self, name, email):
        self.name = name
        self.email = email


class UserRepository:
    """Відповідає лише за збереження користувача в базу даних."""

    def save(self, user):
        print(f"Saving {user.name} to database")


class EmailService:
    """Відповідає лише за надсилання email."""

    def send(self, user, message):
        print(f"Sending email to {user.email}: {message}")


class ReportGenerator:
    """Відповідає лише за генерацію звітів."""

    def generate(self, user):
        print(f"Generating report for {user.name}")


if __name__ == "__main__":
    user = User("Alice", "alice@example.com")

    UserRepository().save(user)
    EmailService().send(user, "Welcome!")
    ReportGenerator().generate(user)