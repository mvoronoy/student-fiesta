class EmojiDatabase:
    _data = {
        "happy": "😀",
        "rocket": "🚀",
        "heart": "❤️",
        "cat": "🐱",
        "fire": "🔥",
    }

    @classmethod
    def load(cls, symbol_id):
        print(f"[DB] Пошук '{symbol_id}' у сховищі")
        return cls._data.get(symbol_id)


class Emoji:
    def __init__(self, symbol_id, unicode_char):
        self.symbol_id = symbol_id
        self.unicode_char = unicode_char
        print(f"[NEW] Створено новий об'єкт Emoji для '{symbol_id}'")

    def draw(self):
        print(f"{self.symbol_id} -> {self.unicode_char}")


class EmojiFactory:
    def __init__(self):
        self._cache = {}

    def get_emoji(self, symbol_id):
        if symbol_id in self._cache:
            print(f"[CACHE] Повторне використання об'єкта '{symbol_id}'")
            return self._cache[symbol_id]

        unicode_char = EmojiDatabase.load(symbol_id)

        if unicode_char is None:
            print(f"[ERROR] Емодзі '{symbol_id}' не знайдено")
            return None

        emoji = Emoji(symbol_id, unicode_char)
        self._cache[symbol_id] = emoji
        return emoji

    def show_cache(self):
        print("\nСтворені Flyweight-об'єкти:")
        for symbol_id in self._cache:
            print("-", symbol_id)

        print("Кількість об'єктів:", len(self._cache))


def main():
    factory = EmojiFactory()

    print("=== Emoji Flyweight ===")
    print("Команда: draw <id>")
    print("Наприклад: draw happy")
    print("Доступні: happy, rocket, heart, cat, fire")
    print("Для завершення введіть: exit\n")

    while True:
        command = input("> ").strip()

        if command == "exit":
            break

        if not command.startswith("draw "):
            print("Невірна команда. Приклад: draw happy")
            continue

        parts = command.split(maxsplit=1)

        if len(parts) != 2:
            print("Не вказано ідентифікатор")
            continue

        symbol_id = parts[1]

        emoji = factory.get_emoji(symbol_id)

        if emoji:
            emoji.draw()

        print()

    factory.show_cache()


if __name__ == "__main__":
    main()