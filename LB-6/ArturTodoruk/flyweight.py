import os
from abc import ABC, abstractmethod


class EmojiDatabase:
    DB_FILE = "emoji.db"

    @classmethod
    def initialize_db(cls):
        default_data = {
            "symbol-A": "😀",
            "symbol-B": "🚀",
            "symbol-C": "❤️",
            "symbol-D": "🐱",
            "symbol-E": "🔥",
            "symbol-F": "🌟",
            "symbol-G": "🍕",
        }
        with open(cls.DB_FILE, "w", encoding="utf-8") as f:
            for key, value in default_data.items():
                f.write(f"{key}={value}\n")

    @classmethod
    def load(cls, symbol_id: str):
        print(f"  [DB] Читання '{ cls.DB_FILE }': пошук запису для '{symbol_id}'...")
        if not os.path.exists(cls.DB_FILE):
            return None

        with open(cls.DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", maxsplit=1)
                if key == symbol_id:
                    return value
        return None


class EmojiDraw(ABC):

    @abstractmethod
    def draw(self):
        pass


class Emoji(EmojiDraw):

    def __init__(self, symbol_id: str, unicode_char: str):
        self._symbol_id = symbol_id
        self._unicode_char = unicode_char
        print(f"  [NEW] Створено новий об'єкт Emoji для '{symbol_id}' (id в пам'яті: {id(self)})")

    @property
    def symbol_id(self) -> str:
        return self._symbol_id

    @property
    def unicode_char(self) -> str:
        return self._unicode_char

    def draw(self):
        print(f"draw {self._symbol_id} -> {self._unicode_char}")


class EmojiFactory:

    def __init__(self):
        self._cache: dict[str, Emoji] = {}

    def get_emoji(self, symbol_id: str) -> Emoji | None:
        if symbol_id in self._cache:
            emoji = self._cache[symbol_id]
            print(f"  [CACHE] Повторне використання наявного об'єкта '{symbol_id}' (id в пам'яті: {id(emoji)})")
            return emoji

        unicode_char = EmojiDatabase.load(symbol_id)
        if unicode_char is None:
            print(f"  [ERROR] Ідентифікатор '{symbol_id}' відсутній у сховищі '{EmojiDatabase.DB_FILE}'!")
            return None

        emoji = Emoji(symbol_id, unicode_char)
        self._cache[symbol_id] = emoji
        return emoji

    def show_cache_stats(self):
        print("\n=== Статистика фабрики Flyweight ===")
        print(f"Усього створено унікальних об'єктів у пам'яті: {len(self._cache)}")
        for sym_id, obj in self._cache.items():
            print(f" - {sym_id}: {obj.unicode_char} (id об'єкта: {id(obj)})")
        print("====================================")


def process_command(command: str, factory: EmojiFactory):
    parts = command.strip().split(maxsplit=1)
    if len(parts) != 2 or parts[0] != "draw":
        print(f"  [ Помилка ] Невірний формат команди: '{command}'. Використовуйте: draw <id>")
        return

    symbol_id = parts[1]
    emoji = factory.get_emoji(symbol_id)
    if emoji is not None:
        emoji.draw()


def main():
    EmojiDatabase.initialize_db()
    factory = EmojiFactory()

    demo_commands = [
        "draw symbol-A",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-C",
        "draw symbol-B",
        "draw symbol-A",
        "draw symbol-X",
    ]

    print("=== Демонстрація роботи програми ===")
    for cmd in demo_commands:
        print(f"\nЗапит: {cmd}")
        process_command(cmd, factory)

    factory.show_cache_stats()

    print("\n=== Інтерактивний режим ===")
    print("Доступні символи у файлі emoji.db: symbol-A ... symbol-G")
    print("Введіть команду (наприклад: draw symbol-B) або 'exit' для виходу.\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        process_command(user_input, factory)

    factory.show_cache_stats()


if __name__ == "__main__":
    main()