from dataclasses import dataclass


@dataclass(frozen=True)
class Emoji:
    emoji_id: str
    name: str
    unicode: str

    def display(self):
        print(f"{self.name}: {self.unicode}")


class EmojiDatabase:
    def __init__(self):
        self.storage = {
            "happy": ("Happy face", "😀"),
            "sad": ("Sad face", "😢"),
            "rocket": ("Rocket", "🚀"),
            "love": ("Heart", "❤️"),
            "monkey": ("Monkey", "🐵"),
            "fire": ("Fire", "🔥"),
            "music": ("Music", "🎵"),
            "earth": ("Earth", "🌍"),
            "game": ("Game", "🎮"),
            "pizza": ("Pizza", "🍕"),
            "dog": ("Dog", "🐶"),
            "cat": ("Cat", "🐱"),
            "sun": ("Sun", "☀️"),
            "moon": ("Moon", "🌙"),
            "star": ("Star", "⭐"),
            "car": ("Car", "🚗"),
            "football": ("Football", "⚽"),
            "basketball": ("Basketball", "🏀"),
            "gift": ("Gift", "🎁"),
            "flower": ("Flower", "🌸"),
            "apple": ("Apple", "🍎"),
            "coffee": ("Coffee", "☕"),
            "rainbow": ("Rainbow", "🌈"),
            "panda": ("Panda", "🐼"),
            "airplane": ("Airplane", "✈️")
        }

        self.requests = 0

    def get_description(self, emoji_id):
        self.requests += 1
        print(f"[DATABASE] Завантаження: {emoji_id}")

        data = self.storage.get(emoji_id)

        if data is None:
            return None

        name, unicode = data

        return Emoji(emoji_id, name, unicode)


class EmojiFactory:
    def __init__(self, database):
        self.database = database
        self.objects = {}

    def get_emoji(self, emoji_id):
        if emoji_id in self.objects:
            print(f"[CACHE] Повторне використання: {emoji_id}")
            return self.objects[emoji_id]

        emoji = self.database.get_description(emoji_id)

        if emoji is None:
            print(f"[ERROR] Емодзі '{emoji_id}' не знайдено!")
            return None

        self.objects[emoji_id] = emoji

        print(f"[FACTORY] Створено новий об'єкт: {emoji_id}")

        return emoji

    def show_statistics(self):
        print("\n========== СТАТИСТИКА ==========")
        print("Емодзі в базі:", len(self.database.storage))
        print("Звернень до бази:", self.database.requests)
        print("Створено об'єктів:", len(self.objects))

        print("\nОб'єкти в кеші:")
        for emoji_id in self.objects:
            print("-", emoji_id)


class Client:
    def __init__(self, factory, database):
        self.factory = factory
        self.database = database

    def run(self):
        print("===== EMOJI DISPLAY SYSTEM =====")
        print("Доступні емодзі:")

        for emoji_id in self.database.storage:
            print("-", emoji_id)

        print("\nФормат команди: draw happy")
        print("Для виходу введіть: exit")

        while True:
            command = input("\nКоманда: ").strip()

            if command.lower() == "exit":
                break

            parts = command.split()

            if len(parts) != 2 or parts[0].lower() != "draw":
                print("Неправильна команда! Приклад: draw happy")
                continue

            emoji = self.factory.get_emoji(parts[1].lower())

            if emoji is not None:
                emoji.display()

        self.factory.show_statistics()
        print("\nПрограму завершено.")

database = EmojiDatabase()
factory = EmojiFactory(database)
client = Client(factory, database)

client.run()